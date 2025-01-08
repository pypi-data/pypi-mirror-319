import pandas as pd
import psycopg2
import sys
import boto3
import json
import os
import base64
import hashlib
from datetime import datetime,timedelta
from Crypto.Cipher import DES3
from Crypto.Util.Padding import unpad
from Crypto.Util.Padding import pad
from cryptography.fernet import Fernet
from botocore.client import Config
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, generate_blob_sas, BlobSasPermissions,PublicAccess
import requests

def decrypt_keys(de_key):
    if de_key.startswith('azure'):
        de_key=de_key[6:]
        
    keys={}
    key = "xLrwTFMdJroA8zG_5wnkQADuJvD5TTmfCKfe8RRz_xU="
    key1 = hashlib.md5(key.encode("utf-8")).digest()
    cipher_bytes = base64.b64decode(de_key)
    cipher = DES3.new(key1, DES3.MODE_ECB)
    decrypted_bytes = cipher.decrypt(cipher_bytes)
    decrypted_text = unpad(decrypted_bytes, DES3.block_size).decode("utf-8")
    data=decrypted_text.split('|')
    
    for i in data:
        a=i.split(':')
        if len(a)==3:
            keys[a[0]]=a[1]+':'+a[2]          
        else:
            keys[a[0]]=a[1]

    Cloud=keys['Cloud']
    if Cloud == 'MinIO':
        endpoint_url=keys['endpoint_url']
        s3=boto3.client('s3',endpoint_url=f"http://{endpoint_url}",
                      aws_access_key_id=keys['Access'],
                      aws_secret_access_key=keys['Secret'],
                      config=Config(signature_version='s3v4'),region_name=keys['region_name']
                      )   
        
    elif Cloud == 'AWS':
        s3 = boto3.client('s3', aws_access_key_id=keys['Access'], aws_secret_access_key=keys['Secret'])
    elif Cloud == 'AZURE':
        connect_str = "DefaultEndpointsProtocol=https;AccountName={0};AccountKey={1};EndpointSuffix=core.windows.net".format(keys['Access'],keys['Secret'])            
        s3 = BlobServiceClient.from_connection_string(connect_str)
        
    if Cloud == 'MinIO'or Cloud =='AWS':       
        ContainerName = keys['Bucket']
        file_key = 'Connections/Dopplr_Connection.ini'
        db = {}
        response = s3.get_object(Bucket=ContainerName, Key=file_key)
        file_content = response['Body'].read()
        key2=key.encode('utf-8')
        fernet = Fernet(key2)
        decrypted_data = fernet.decrypt(file_content)
        decrypted_data = decrypted_data.decode('utf-8')
        lines = decrypted_data.split('\n')
        index=lines.index('[postgresql]\r')
        data=lines[index+1:index+8]

        for i in data:
            a=i.split('=')
            db[a[0]]=a[1].replace('\r','')

    else:
        
        ContainerName = keys['Bucket']
        file_key = 'Connections/Dopplr_Connection.ini'
        blob_client = s3.get_blob_client(container=ContainerName, blob=file_key)
        az = blob_client.download_blob()
        file_contents = az.readall()
        key2=key.encode('utf-8')
        fernet = Fernet(key2)
        decrypted_data = fernet.decrypt(file_contents)
        decrypted_data = decrypted_data.decode('utf-8')
        lines = decrypted_data.split('\n')
        index = lines.index('[postgresql]\r')
        data = lines[index + 1: index + 8]
        db = {}
        for i in data:
            a = i.split('=')
            db[a[0]]=a[1].replace('\r', '')
        

    return keys,db,s3

def encrypt_keys(key,user,paswrd,date):
    s_key="MyComplexKey"
    message=f"key:{key}|user:{user}|paswrd:{paswrd}|date:{date}"
    key = hashlib.md5(s_key.encode("utf-8")).digest()
    cipher = DES3.new(key, DES3.MODE_ECB)
    padded_text = pad(message.encode("utf-8"), DES3.block_size)
    encrypted_bytes = cipher.encrypt(padded_text)
    encrypted_text = base64.b64encode(encrypted_bytes).decode("utf-8")
    return encrypted_text

def get_access_token(enc_text,fapi):
    response = requests.post('http://'+fapi + "/token",data={"username": enc_text},)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Failed to get access token. Status code: {response.status_code}")


def putFileTomywrkspace(filePath,file_type,loginName,Project_name,de_key):
    try:
        keys,db,client=decrypt_keys(de_key)
        api=db['api']
        fapi=db['fastapi']
        Cloud=keys['Cloud']
        query="select DOR.\"OrgName\",Du.\"UserKey\",P.\"Project_key\" FROM dopplr.\"DopplrUser\" Du join dopplr.\"DopplrOrg\" DOR on DOR.\"OrgId\"=Du.\"OrgId\" \
join dopplr.\"DopplrProject\" P on P.\"UserKey\"=Du.\"UserKey\" where Du.\"LoginName\"='{0}' and p.\"ProjectName\"='{1}'".format(loginName,Project_name)
        
        ContainerName = keys['Bucket']


        cnxn = psycopg2.connect(host=db['host'],database=db['database'],user=db['user'],password=db['password'],port=db['port'])
    
        cur=cnxn.cursor()
        cur.execute(query)
        results = cur.fetchone()
      

        OrgName=results[0]
        
        UserKey=results[1]
        ProjectKey=results[2]
        
        cur=cnxn.cursor()
      
        file_name = os.path.basename(filePath)
        file_name=file_name.lower()
        
        query="select count(\"TableName\") from dopplr.\"DopplrLake\" DL join dopplr.\"DopplrUser\" US on DL.\"UserKey\"=US.\"UserKey\" where \"TableName\"="+"'"+file_name+"'"+" and US.\"LoginName\"="+"'"+loginName+"'"
        cur.execute(query)
        results = cur.fetchone()
        if results[0]<1:
        
            insert_query = "INSERT INTO dopplr.\"DopplrLake\"(\"UserKey\", \"TableName\",\"ResourceType\",\"DopplrConnectionDetailsKey\",\"Projectid\",\"Status\",\"Schema\",\"Source\",\"CreatedTs\") \
VALUES ("+str(UserKey)+",'"+file_name+"','"+file_type+"',null,'"+str(ProjectKey)+"','Uploaded','"+loginName+'_schema'+"','MLStudio',CURRENT_TIMESTAMP)"
            cur.execute(insert_query)
            cnxn.commit()
        else:
            pass
                    
        cur1=cnxn.cursor()
        insert_query1 = "SELECT max(\"SourceKey\") as \"SourceKey\" FROM dopplr.\"DopplrLake\" where \"UserKey\"="+str(UserKey)+" and \"TableName\"='"+file_name+"'"
        
        cur1.execute(insert_query1)
        results = cur1.fetchone()
        SourceKey=results[0]
        SourceKey=str(SourceKey)
        if file_type == 'csv' or file_type == 'xlsx':
            df = pd.read_csv(filePath+'.'+file_type)

            cur_del=cnxn.cursor()
            delete="DELETE FROM Dopplr.\"DopplrSchema\" WHERE\"SourceKey\"="+SourceKey
            cur_del.execute(delete)
            cnxn.commit()
            cur_sch=cnxn.cursor()
            for name, dtype in df.dtypes.items():
                if(dtype == 'datetime64[ns]'):
                    dtype = 'Datetime'
                elif dtype=='object':
                    dtype='string'
                elif dtype=='float64':
                    dtype='DOUBLE'
                elif dtype=='int64':
                    dtype='long'                
                else:
                    dtype='long'
                maxlength = max(df[name].map(str).apply(len))
                tpp=str(maxlength)
                tp=str(dtype)
                insert1="INSERT INTO dopplr.\"DopplrSchema\"(\"SourceKey\",\"Column\" ,\"Type\",\"Length\") VALUES ({},'{}','{}','{}')".format(SourceKey,name,tp,tpp)
                cur_sch.execute(insert1)
                cnxn.commit()

        ConnectionString = str(OrgName)+"/"+str(loginName).upper()+"/"+(str(SourceKey).lstrip()+'/Source/'+file_name+'.'+file_type)
        update_query = "UPDATE dopplr.\"DopplrLake\" set \"ConnectionString\"='"+ConnectionString+"',\"UpdatedTs\"=CURRENT_TIMESTAMP where \"SourceKey\"="+str(SourceKey)
        cur2=cnxn.cursor()

        cur2.execute(update_query)
        cnxn.commit()


        
        if Cloud =='AWS':
            
            client.upload_file(filePath+'.'+file_type, ContainerName, ConnectionString)
            # Generate a pre-signed URL        
            client.put_object_acl(ACL='public-read',
                              Bucket=ContainerName,
                              Key=ConnectionString)
            url = f"s3://{ContainerName}/{ConnectionString}"
            print("uri : ",url)
        elif Cloud == 'MinIO':
            client.upload_file(filePath+'.'+file_type, ContainerName, ConnectionString)
            # Generate a pre-signed URL
            endpoint_url=keys['endpoint_url']
            presigned_url = client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': ContainerName,
                    'Key': ConnectionString
                },
                ExpiresIn=3600  # URL expiration time in seconds (e.g., 1 hour)
            )
            url = presigned_url#f"http://{endpoint_url}/{ContainerName}/{ConnectionString}"            
            print("uri : ",url)
        else:

            blob_client = client.get_blob_client(container=ContainerName, blob=ConnectionString)
            with open(filePath+'.'+file_type, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            blob_url = blob_client.url
            print("blob_url : ",blob_url)
            
        cnxn.close()
           
            
    except Exception as error:
        if 'NoneType' in str(error):
            dopplrsource= 'File does not exists'
            print("Error : ", dopplrsource)
            sys.exit()
        else:
            print("Error : ",error)

def putFileTomywrkspace_Ingestion(filePath,file_type,loginName,Project_name,Option,de_key):
    try:
        keys,db,client=decrypt_keys(de_key)
        api=db['api']
        fapi=db['fastapi']
        Cloud=keys['Cloud']
        query="select DOR.\"OrgName\",Du.\"UserKey\",P.\"Project_key\" FROM dopplr.\"DopplrUser\" Du join dopplr.\"DopplrOrg\" DOR on DOR.\"OrgId\"=Du.\"OrgId\" \
join dopplr.\"DopplrProject\" P on P.\"UserKey\"=Du.\"UserKey\" where Du.\"LoginName\"='{0}' and p.\"ProjectName\"='{1}'".format(loginName,Project_name)
        
        ContainerName = keys['Bucket']

        cnxn = psycopg2.connect(host=db['host'],database=db['database'],user=db['user'],password=db['password'],port=db['port'])
    
        cur=cnxn.cursor()
        cur.execute(query)
        results = cur.fetchone()
      

        OrgName=results[0]
        
        UserKey=results[1]
        ProjectKey=results[2]
        
        cur=cnxn.cursor()
      
        file_name = os.path.basename(filePath)
        file_name=file_name.lower()
        query="select count(\"TableName\") from dopplr.\"DopplrLake\" DL join dopplr.\"DopplrUser\" US on DL.\"UserKey\"=US.\"UserKey\" where \"TableName\"="+"'"+file_name+"'"+" and US.\"LoginName\"="+"'"+loginName+"'"
        cur.execute(query)
        results = cur.fetchone()
        if results[0]<1:
        
            insert_query = "INSERT INTO dopplr.\"DopplrLake\"(\"UserKey\", \"TableName\",\"ResourceType\",\"DopplrConnectionDetailsKey\",\"Projectid\",\"Status\",\"Schema\",\"Source\",\"CreatedTs\") \
VALUES ("+str(UserKey)+",'"+file_name+"','"+file_type+"',null,'"+str(ProjectKey)+"','Uploaded','"+loginName+'_schema'+"','MLStudio',CURRENT_TIMESTAMP)"
            cur.execute(insert_query)
            cnxn.commit()
        else:
            pass
                    
        cur1=cnxn.cursor()
        insert_query1 = "SELECT max(\"SourceKey\") as \"SourceKey\" FROM dopplr.\"DopplrLake\" where \"UserKey\"="+str(UserKey)+" and \"TableName\"='"+file_name+"'"
        
        cur1.execute(insert_query1)
        results = cur1.fetchone()
        SourceKey=results[0]
        SourceKey=str(SourceKey)
        if file_type == 'csv' or file_type == 'xlsx':
            df = pd.read_csv(filePath+'.'+file_type)
            
            cur_del=cnxn.cursor()
            delete="DELETE FROM Dopplr.\"DopplrSchema\" WHERE\"SourceKey\"="+SourceKey
            cur_del.execute(delete)
            cnxn.commit()
            cur_sch=cnxn.cursor()
            for name, dtype in df.dtypes.items():
                if(dtype == 'datetime64[ns]'):
                    dtype = 'Datetime'
                elif dtype=='object':
                    dtype='string'
                elif dtype=='float64':
                    dtype='DOUBLE'
                elif dtype=='int64':
                    dtype='long'                
                else:
                    dtype='long'
                maxlength = max(df[name].map(str).apply(len))
                tpp=str(maxlength)
                tp=str(dtype)
                insert1="INSERT INTO dopplr.\"DopplrSchema\"(\"SourceKey\",\"Column\" ,\"Type\",\"Length\") VALUES ({},'{}','{}','{}')".format(SourceKey,name,tp,tpp)
                cur_sch.execute(insert1)
                cnxn.commit()

        ConnectionString = str(OrgName)+"/"+str(loginName).upper()+"/"+(str(SourceKey).lstrip()+'/Source/'+file_name+'.'+file_type)
        update_query = "UPDATE dopplr.\"DopplrLake\" set \"ConnectionString\"='"+ConnectionString+"' where \"SourceKey\"="+str(SourceKey)
        cur2=cnxn.cursor()

        cur2.execute(update_query)
        cnxn.commit()


        
        if Cloud =='AWS':
            
            client.upload_file(filePath+'.'+file_type, ContainerName, ConnectionString)
            # Generate a pre-signed URL        
            client.put_object_acl(ACL='public-read',
                              Bucket=ContainerName,
                              Key=ConnectionString)
            url = f"s3://{ContainerName}/{ConnectionString}"
            print("uri : ",url)
        elif Cloud == 'MinIO':
            client.upload_file(filePath+'.'+file_type, ContainerName, ConnectionString)
            # Generate a pre-signed URL
            endpoint_url=keys['endpoint_url']
            presigned_url = client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': ContainerName,
                    'Key': ConnectionString
                },
                ExpiresIn=3600  # URL expiration time in seconds (e.g., 1 hour)
            )
            url = presigned_url#f"http://{endpoint_url}/{ContainerName}/{ConnectionString}"            
            print("uri : ",url)
        else:

            blob_client = client.get_blob_client(container=ContainerName, blob=ConnectionString)
            with open(filePath+'.'+file_type, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            blob_url = blob_client.url
            print("blob_url : ",blob_url)
            
        

        if Option.upper()=='YES':

              
            if file_type == 'csv' or file_type == 'xlsx':
                api=f"http://{api}/Workflow/WorkflowDruidSave?SourceID="+(str(SourceKey).lstrip())
                response=requests.get(api,verify=False)

                row_count, column_count = df.shape
                update_query = "UPDATE dopplr.\"DopplrLake\" set \"Status\"='Ready',\"FieldCount\"='"+str(column_count)+"',\"RowCount\"='"+str(row_count)+"' where \"SourceKey\"="+str(SourceKey)
                cur3=cnxn.cursor()

                cur3.execute(update_query)
                cnxn.commit()
            
                
            
        cnxn.close()
            
        
    except Exception as error:
        if 'NoneType' in str(error):
            dopplrsource= 'File does not exists'
            print("Error : ", dopplrsource)
            sys.exit()
        else:
            print("Error : ",error)
def putFileTomywrkspace_Profiling(filePath,file_type,loginName,Project_name,Option,de_key):
    try:
        keys,db,client=decrypt_keys(de_key)
        api=db['api']
        fapi=db['fastapi']
        Cloud=keys['Cloud']
        query="select DOR.\"OrgName\",Du.\"UserKey\",P.\"Project_key\",Du.\"FirstName\" FROM dopplr.\"DopplrUser\" Du join dopplr.\"DopplrOrg\" DOR on DOR.\"OrgId\"=Du.\"OrgId\" \
join dopplr.\"DopplrProject\" P on P.\"UserKey\"=Du.\"UserKey\" where Du.\"LoginName\"='{0}' and p.\"ProjectName\"='{1}'".format(loginName,Project_name)
        
        ContainerName = keys['Bucket']

        cnxn = psycopg2.connect(host=db['host'],database=db['database'],user=db['user'],password=db['password'],port=db['port'])
    
        cur=cnxn.cursor()
        cur.execute(query)
        results = cur.fetchone()
      

        OrgName=results[0]
        
        UserKey=results[1]
        ProjectKey=results[2]
        FirstName=results[3]
        
        cur=cnxn.cursor()
      
        file_name = os.path.basename(filePath)
        file_name=file_name.lower()
        query="select count(\"TableName\") from dopplr.\"DopplrLake\" DL join dopplr.\"DopplrUser\" US on DL.\"UserKey\"=US.\"UserKey\" where \"TableName\"="+"'"+file_name+"'"+" and US.\"LoginName\"="+"'"+loginName+"'"
        cur.execute(query)
        results = cur.fetchone()
        if results[0]<1:
        
            insert_query = "INSERT INTO dopplr.\"DopplrLake\"(\"UserKey\", \"TableName\",\"ResourceType\",\"DopplrConnectionDetailsKey\",\"Projectid\",\"Status\",\"Schema\",\"Source\",\"CreatedTs\") \
VALUES ("+str(UserKey)+",'"+file_name+"','"+file_type+"',null,'"+str(ProjectKey)+"','Uploaded','"+loginName+'_schema'+"','MLStudio',CURRENT_TIMESTAMP)"
            cur.execute(insert_query)
            cnxn.commit()
        else:
            pass
                    
        cur1=cnxn.cursor()
        insert_query1 = "SELECT max(\"SourceKey\") as \"SourceKey\" FROM dopplr.\"DopplrLake\" where \"UserKey\"="+str(UserKey)+" and \"TableName\"='"+file_name+"'"
        
        cur1.execute(insert_query1)
        results = cur1.fetchone()
        SourceKey=results[0]
        SourceKey=str(SourceKey)
        if file_type == 'csv' or file_type == 'xlsx':
            df = pd.read_csv(filePath+'.'+file_type)
            cur_del=cnxn.cursor()
            delete="DELETE FROM Dopplr.\"DopplrSchema\" WHERE\"SourceKey\"="+SourceKey
            cur_del.execute(delete)
            cnxn.commit()
            cur_sch=cnxn.cursor()
            for name, dtype in df.dtypes.items():
                if(dtype == 'datetime64[ns]'):
                    dtype = 'Datetime'
                elif dtype=='object':
                    dtype='string'
                elif dtype=='float64':
                    dtype='DOUBLE'
                elif dtype=='int64':
                    dtype='long'                
                else:
                    dtype='long'
                maxlength = max(df[name].map(str).apply(len))
                tpp=str(maxlength)
                tp=str(dtype)
                insert1="INSERT INTO dopplr.\"DopplrSchema\"(\"SourceKey\",\"Column\" ,\"Type\",\"Length\") VALUES ({},'{}','{}','{}')".format(SourceKey,name,tp,tpp)
                cur_sch.execute(insert1)
                cnxn.commit()

        ConnectionString = str(OrgName)+"/"+str(loginName).upper()+"/"+(str(SourceKey).lstrip()+'/Source/'+file_name+'.'+file_type)
        update_query = "UPDATE dopplr.\"DopplrLake\" set \"ConnectionString\"='"+ConnectionString+"' where \"SourceKey\"="+str(SourceKey)
        cur2=cnxn.cursor()

        cur2.execute(update_query)
        cnxn.commit()


        
        if Cloud =='AWS':
            
            client.upload_file(filePath+'.'+file_type, ContainerName, ConnectionString)
            # Generate a pre-signed URL        
            client.put_object_acl(ACL='public-read',
                              Bucket=ContainerName,
                              Key=ConnectionString)
            url = f"s3://{ContainerName}/{ConnectionString}"
            print("uri : ",url)
        elif Cloud == 'MinIO':
            client.upload_file(filePath+'.'+file_type, ContainerName, ConnectionString)
            # Generate a pre-signed URL
            endpoint_url=keys['endpoint_url']
            presigned_url = client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': ContainerName,
                    'Key': ConnectionString
                },
                ExpiresIn=3600  # URL expiration time in seconds (e.g., 1 hour)
            )
            url = presigned_url#f"http://{endpoint_url}/{ContainerName}/{ConnectionString}"            
            print("uri : ",url)
        else:

            blob_client = client.get_blob_client(container=ContainerName, blob=ConnectionString)
            with open(filePath+'.'+file_type, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            blob_url = blob_client.url
            print("blob_url : ",blob_url)
            
        cnxn.close()

        if Option.upper()=='YES':
              
            if file_type == 'csv' or file_type == 'xlsx':
                api=f"http://{api}/Workflow/WorkflowDruidSave?SourceID="+(str(SourceKey).lstrip())
              
                response=requests.get(api,verify=False)
                #print(response)

                date=datetime.now()
                enc_text=encrypt_keys(SourceKey,loginName,FirstName,date)

                token=get_access_token(enc_text,fapi)

                    
                headers = {"Authorization": f"Bearer {token}"}
                
                fapi=f"http://{fapi}/Profiling/?sourcekey="+(str(SourceKey).lstrip())
                response=requests.get(fapi,headers=headers,verify=False)
                #print(response)

                
            print("Ingestion Done")
            

        
            
    except Exception as error:
        if 'NoneType' in str(error):
            dopplrsource= 'File does not exists'
            print("Error : ", dopplrsource)
            sys.exit()
        else:
            print("Error : ",error)
            
def putFolderTomywrkspace(folderPath,Targetname,loginName,Project_name,de_key):
     try:
        keys,db,client=decrypt_keys(de_key)
        api=db['api']
        fapi=db['fastapi']
        Cloud=keys['Cloud']
        query="select DOR.\"OrgName\",Du.\"UserKey\",P.\"Project_key\" FROM dopplr.\"DopplrUser\" Du join dopplr.\"DopplrOrg\" DOR on DOR.\"OrgId\"=Du.\"OrgId\" \
join dopplr.\"DopplrProject\" P on P.\"UserKey\"=Du.\"UserKey\" where Du.\"LoginName\"='{0}' and p.\"ProjectName\"='{1}'".format(loginName,Project_name)
        
        ContainerName = keys['Bucket']

        cnxn = psycopg2.connect(host=db['host'],database=db['database'],user=db['user'],password=db['password'],port=db['port'])
    
        cur=cnxn.cursor()
        cur.execute(query)
        results = cur.fetchone()
      
        OrgName=results[0]     
        UserKey=results[1]
        ProjectKey=results[2]
        
        cur=cnxn.cursor()
        query="select count(\"TableName\") from dopplr.\"DopplrLake\" DL join dopplr.\"DopplrUser\" US on DL.\"UserKey\"=US.\"UserKey\" where \"TableName\"="+"'"+Targetname+"'"+" and US.\"LoginName\"="+"'"+loginName+"'"
        cur.execute(query)
        results = cur.fetchone()
        if results[0]<1:     
            insert_query = "INSERT INTO dopplr.\"DopplrLake\"(\"UserKey\", \"TableName\",\"ResourceType\",\"DopplrConnectionDetailsKey\",\"Projectid\",\"Status\",\"Schema\",\"Source\",\"CreatedTs\")\
            VALUES ("+str(UserKey)+",'"+Targetname+"','folder',null,'"+str(ProjectKey)+"','Ready','"+loginName+'_schema'+"','folder',CURRENT_TIMESTAMP)"
            cur.execute(insert_query)
           
            cnxn.commit()
        else:
            pass

        cur1=cnxn.cursor()
        insert_query1 = "SELECT max(\"SourceKey\") as \"SourceKey\" FROM dopplr.\"DopplrLake\" where \"UserKey\"="+str(UserKey)+" and \"TableName\"='"+Targetname+"'"
        
        cur1.execute(insert_query1)
        results = cur1.fetchone()
        SourceKey=results[0]
        SourceKey=str(SourceKey)
        ConnectionString = str(OrgName)+"/"+str(loginName).upper()+"/"+(str(SourceKey).lstrip()+'/Source/'+Targetname)
        update_query = "UPDATE dopplr.\"DopplrLake\" set \"ConnectionString\"='"+ConnectionString+"' ,\"UpdatedTs\"=CURRENT_TIMESTAMP where \"SourceKey\"="+str(SourceKey)
        cur2=cnxn.cursor()

        cur2.execute(update_query)
        cnxn.commit()
        cnxn.close()  

        file_count =0
        
        for root, dirs, files in os.walk(folderPath):
            for file in files:
                #file_count = file_count +1
                if file.endswith('.csv') or file.endswith('.xlsx'):
                    file=file.lower()
                local_file_path = os.path.join(root, file)
                s3_file_key = os.path.join(ConnectionString, os.path.relpath(local_file_path, folderPath)).replace("\\", "/")

                if Cloud =='AWS':
                    
                    client.upload_file(local_file_path, ContainerName, s3_file_key)
                    file_count = file_count +1
                    # Generate a pre-signed URL        
                    client.put_object_acl(ACL='public-read',
                                    Bucket=ContainerName,
                                    Key=s3_file_key)
                    url = f"s3://{ContainerName}/{s3_file_key}"
                    #print("uri : ",url)
                elif Cloud == 'MinIO':

                    client.upload_file(local_file_path, ContainerName, s3_file_key)
                    file_count = file_count +1
                    # Generate a pre-signed URL
                    endpoint_url=keys['endpoint_url']
                    presigned_url = client.generate_presigned_url(
                        'get_object',
                        Params={
                            'Bucket': ContainerName,
                            'Key': s3_file_key
                        },
                        ExpiresIn=3600  # URL expiration time in seconds (e.g., 1 hour)
                    )
                    url = presigned_url#f"http://{endpoint_url}/{ContainerName}/{ConnectionString}"            
                    print("uri : ",url)
                else:
                    container_client = client.get_container_client(ContainerName)
                    local_file_path = os.path.join(root, file)
                    #blob_name = os.path.relpath(local_file_path, folderPath).replace("\\", "/")
                    blob_name = os.path.join(ConnectionString,os.path.relpath(local_file_path, folderPath)).replace("\\", "/")
                    blob_client = container_client.get_blob_client(blob_name)

                    with open(local_file_path, "rb") as data:
                        blob_client.upload_blob(data, overwrite=True)
                        file_count += 1

                    blob_url = blob_client.url
                    #print("Blob URL:", blob_url)

        if Cloud =='AWS' or Cloud == 'MinIO':
            presigned_url = client.generate_presigned_url(
                ClientMethod='get_object',
                Params={'Bucket': ContainerName, 'Key': ConnectionString},
                ExpiresIn=3600  # Expiration time in seconds
            )

            presigned_url=presigned_url.split('?')
            
            print(str(file_count) + " files uploaded successfully")
            return presigned_url[0]
        elif Cloud == 'AZURE':
            print(str(file_count) + " files uploaded successfully")
            

            
     except Exception as error:
        if 'NoneType' in str(error):
            dopplrsource= 'File does not exists'
            print("Error : ", dopplrsource)
            sys.exit()
        else:
            print("Error : ",error)


def getWorkspaceFile(fileName,destination,loginName,de_key):
    try:

        def is_file_name_same(file_path, expected_file_name):
            file_name = os.path.basename(file_path)
            return file_name == expected_file_name

        keys,db,client=decrypt_keys(de_key)

        file_Name=fileName.split(".")      
        
        query="select DOR.\"OrgName\",Du.\"UserKey\",DL.\"SourceKey\" FROM dopplr.\"DopplrUser\" Du join dopplr.\"DopplrOrg\" DOR on DOR.\"OrgId\"=Du.\"OrgId\" \
join dopplr.\"DopplrLake\" DL on DL.\"UserKey\"=Du.\"UserKey\"\
where Du.\"LoginName\"="+"'"+loginName+"'"+" and DL.\"TableName\"="+"'"+file_Name[0]+"'"+""
        ContainerName = keys['Bucket']
        Cloud=keys['Cloud']
        cnxn = psycopg2.connect(host=db['host'],database=db['database'],user=db['user'],password=db['password'],port=db['port'])
        cur=cnxn.cursor()
        cur.execute(query)
        results = cur.fetchone()
        UserKey=results[1]
        OrgName=results[0]
        sourcekey=results[2]
        folder_prefix = OrgName+'/'+loginName.upper()+'/'+str(sourcekey)
        # Check if the file exists
        if os.path.exists(destination):
            print('folder exists')
        else:
            os.mkdir(destination)
        if Cloud == 'MinIO'or Cloud =='AWS':
            response = client.list_objects_v2(Bucket=ContainerName, Prefix=folder_prefix)
            destination=destination+'/'+fileName
            for obj in response['Contents']:
                key = obj['Key']               
                is_same = is_file_name_same(key, fileName)
                if(is_same):
                    client.download_file(ContainerName, key, destination)
                    print("downloaded")
        else:
            container_client = client.get_container_client(ContainerName)

            destination=destination+'/'+fileName
            blobs = container_client.list_blobs()
            for blob in blobs:
                #print(blob.name)
                is_same = is_file_name_same(blob.name, fileName)
                if(is_same):                  
                    with open(destination, "wb") as my_blob:
                        blob_client = container_client.get_blob_client(blob.name)
                        blob_data = blob_client.download_blob()
                        blob_data.readinto(my_blob)
                        print("downloaded")
                        
    except Exception as error:
        print("Error : ",error)
        
def getWorkspaceFolderFiles(folder,destination,loginName,de_key):
    try:
        keys,db,client=decrypt_keys(de_key)
        query="select DOR.\"OrgName\",Du.\"UserKey\",DL.\"SourceKey\" FROM dopplr.\"DopplrUser\" Du join dopplr.\"DopplrOrg\" DOR on DOR.\"OrgId\"=Du.\"OrgId\" \
join dopplr.\"DopplrLake\" DL on DL.\"UserKey\"=Du.\"UserKey\"\
where Du.\"LoginName\"="+"'"+loginName+"'"+" and DL.\"TableName\"="+"'"+folder+"'"+""


        cnxn = psycopg2.connect(host=db['host'],database=db['database'],user=db['user'],password=db['password'],port=db['port'])
        cur=cnxn.cursor()
        cur.execute(query)
        results = cur.fetchone()
        UserKey=results[1]
        OrgName=results[0]
        sourcekey=results[2]
        folder_prefix = OrgName+'/'+loginName.upper()+'/'+str(sourcekey)
        ContainerName = keys['Bucket']
        Cloud=keys['Cloud']
        if Cloud == 'MinIO' or Cloud == 'AWS':
            file_count = 0
            continuation_token = None
            while True:
            # Use ContinuationToken for paginated results
                if continuation_token:
                    response = client.list_objects_v2(Bucket=ContainerName, Prefix=folder_prefix, ContinuationToken=continuation_token)
                else:
                    response = client.list_objects_v2(Bucket=ContainerName, Prefix=folder_prefix)

                for obj in response.get('Contents', []):
                    key = obj['Key']
                    if not key.endswith('/'):  # Exclude subdirectories
                        file_name = os.path.join(destination, os.path.basename(key))
                        client.download_file(ContainerName, key, file_name)  # Download the file
                        file_count += 1
                        
                if 'NextContinuationToken' in response:
                    continuation_token = response['NextContinuationToken']
                else:
                    break  # No more pages

            print("Downloaded files:", file_count)
        else:
            
            #folder_prefix = OrgName+'/'+loginName.upper()+'/'+folder
            container_client = client.get_container_client(ContainerName)
            blobs = container_client.list_blobs(name_starts_with=folder_prefix)

            for blob in blobs:
                blob_client = container_client.get_blob_client(blob.name)
                file_path = os.path.join(destination, os.path.basename(blob.name))
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "wb") as file:
                    file.write(blob_client.download_blob().readall())
            print("downloaded")

        
    except Exception as error:
        print("Error : ",error)

def getWorkspaceFile_URL(fileName,loginName,de_key):
    try:
        keys,db,client=decrypt_keys(de_key)
        
        query="select DOR.\"OrgName\",Du.\"UserKey\",DOR.\"Region\",DOR.\"ContainerName\",DOR.\"AwsAccessKey\",DOR.\"AwsSecretKey\" FROM dopplr.\"DopplrUser\" Du join dopplr.\"DopplrOrg\" DOR on DOR.\"OrgId\"=Du.\"OrgId\" where Du.\"LoginName\"="+"'"+loginName+"'"+""
        ContainerName = keys['Bucket']
        cnxn = psycopg2.connect(host=db['host'],database=db['database'],user=db['user'],password=db['password'],port=db['port'])
        cur=cnxn.cursor()
        cur.execute(query)
        results = cur.fetchone()
        UserKey=results[1]
        OrgName=results[0]
        Region=results[2]

        file_name = os.path.basename(fileName)
        file_name1=file_name.split('.')
        cur1=cnxn.cursor()
        query1 = "SELECT max(\"SourceKey\") as \"SourceKey\" FROM dopplr.\"DopplrLake\" where \"UserKey\"="+str(UserKey)+" and \"TableName\"='"+file_name1[0]+"'"
        cur1.execute(query1)
        results = cur1.fetchone()
        SourceKey=results[0]
        SourceKey=str(SourceKey)

        ConnectionString = str(OrgName)+"/"+str(loginName).upper()+"/"+(str(SourceKey).lstrip()+'/Source/'+fileName)
        

        if keys['Cloud'] == 'MinIO'or keys['Cloud'] =='AWS':

            
            try:
                presigned_url = client.generate_presigned_url(
                    ClientMethod='get_object',
                    Params={'Bucket': ContainerName, 'Key': ConnectionString},
                    ExpiresIn=3600  # Expiration time in seconds
                )

                presigned_url=presigned_url.split('?')
                return presigned_url[0]
            except Exception as e:
                print(f'Error generating pre-signed URL: {e}')
            
        else:
            try:
                sas_expiry_time = datetime.utcnow() + timedelta(hours=1)

                sas_token = generate_blob_sas(
                    account_name=keys['Access'],
                    container_name=ContainerName,
                    blob_name=fileName,
                    account_key=keys['Secret'],
                    permission=BlobSasPermissions(read=True),
                    expiry=sas_expiry_time
                )

                blob_url = client.get_blob_client(ContainerName, ConnectionString).url
                presigned_url = f"{blob_url}?{sas_token}"
                print("presigned ",presigned_url.split('?')[0])

                return presigned_url.split('?')[0]
            except Exception as e:
                print(f"Error generating pre-signed URL: {e}")
                return None
            
                        
    except Exception as error:
        print("Error : ",error)

def getWorkspaceFile_URL_WithSourceKey(Sourcekey,loginName,de_key):
    try:
        keys,db,client=decrypt_keys(de_key)
        
        query="select DOR.\"OrgName\",Du.\"UserKey\",DOR.\"Region\",DOR.\"ContainerName\",DOR.\"AwsAccessKey\",DOR.\"AwsSecretKey\" FROM dopplr.\"DopplrUser\" Du join dopplr.\"DopplrOrg\" DOR on DOR.\"OrgId\"=Du.\"OrgId\" where Du.\"LoginName\"="+"'"+loginName+"'"+""
        ContainerName = keys['Bucket']
        cnxn = psycopg2.connect(host=db['host'],database=db['database'],user=db['user'],password=db['password'],port=db['port'])
        cur=cnxn.cursor()
        cur.execute(query)
        results = cur.fetchone()
        UserKey=results[1]
        OrgName=results[0]
        Region=results[2]

        if keys['Cloud'] == 'MinIO'or keys['Cloud'] =='AWS':
            try:
                query="select \"TableName\",\"ResourceType\" FROM dopplr.\"DopplrLake\"  where \"SourceKey\"="+"'"+str(Sourcekey)+"'"+""
                cur=cnxn.cursor()
                cur.execute(query)
                results = cur.fetchone()
                fileName=results[0]
                ResourceType=results[1]
                SourceKey = Sourcekey

                ConnectionString = str(OrgName)+"/"+str(loginName).upper()+"/"+(str(SourceKey).lstrip()+'/Source/'+fileName+'.'+ResourceType)
            
            
                presigned_url = client.generate_presigned_url(
                    ClientMethod='get_object',
                    Params={'Bucket': ContainerName, 'Key': ConnectionString},
                    ExpiresIn=3600  # Expiration time in seconds
                )

                presigned_url=presigned_url.split('?')
                print("presigned_url ",presigned_url[0])
                return presigned_url[0]
            except Exception as e:
                print(f'Error generating pre-signed URL: {e}')
            
        else:
            query="select \"TableName\",\"ResourceType\" FROM dopplr.\"DopplrLake\"  where \"SourceKey\"="+"'"+str(Sourcekey)+"'"+""
            cur=cnxn.cursor()
            cur.execute(query)
            results = cur.fetchone()
            fileName=results[0]
            ResourceType=results[1]
            SourceKey = Sourcekey

            ConnectionString = str(OrgName)+"/"+str(loginName).upper()+"/"+(str(SourceKey).lstrip()+'/Source/'+fileName+'.'+ResourceType)
            
            sas_expiry_time = datetime.utcnow() + timedelta(hours=1)

            sas_token = generate_blob_sas(
                account_name=keys['Access'],
                container_name=ContainerName,
                blob_name=fileName,
                account_key=keys['Secret'],
                permission=BlobSasPermissions(read=True),
                expiry=sas_expiry_time
            )

            blob_url = client.get_blob_client(ContainerName, ConnectionString).url
            presigned_url = f"{blob_url}?{sas_token}"

            return presigned_url.split('?')[0]
            
                        
    except Exception as error:
        print("Error : ",error)      



