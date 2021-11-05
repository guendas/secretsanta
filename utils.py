import csv,os, random
import pandas as pd
import streamlit as st
from azure.storage.blob import BlobServiceClient
from pandas.io.parsers import read_csv

#TODO: association of secrets one by one not batch
def CreateYourSecretSantaList(names,headers,file_name,default_id_number):
    # id = default_id_number
    # data =[]
    # #add id and set secret to 0
    # for n in names:
    #     id = id + 1
    #     data.append([id,n,-1])
    # with open(file_name,"w") as csv_file:
    #     csv_writer = csv.writer(csv_file)
    #     csv_writer.writerow(headers) # write header
    #     for row in data:
    #         csv_writer.writerow(row) # write each row
    return print("todo")

def UploadFileToBlob(filePath,connectionString,containerName,blobName):
    service = BlobServiceClient.from_connection_string(conn_str=connectionString,container_name=containerName,blob_name=blobName)
    blob_client = service.get_blob_client(container=containerName,blob=blobName)
    with open(filePath, "rb") as data:
        blob_client.upload_blob(data)
        print("File uploaded!")

def DownloadBlob(connectionString,containerName,blobName,file_path):
    service = BlobServiceClient.from_connection_string(conn_str=connectionString, container_name=containerName,blob_name=blobName)
    blob_client = service.get_blob_client(container=containerName,blob=blobName)
    with open(file_path, "wb") as my_blob:
        blob_data = blob_client.download_blob()
        blob_data.readinto(my_blob)
    print("File downloaded!")
    return file_path

def DownloadBlobToStreamlit(connectionString,containerName,blobName,file_path):
    service = BlobServiceClient.from_connection_string(conn_str=connectionString, container_name=containerName,blob_name=blobName)
    blob_client = service.get_blob_client(container=containerName,blob=blobName)
    file_path = os.path.join(file_path)
    with open(file_path, "wb") as my_blob:
        blob_data = blob_client.download_blob()
        blob_data.readinto(my_blob)
    print("File downloaded!")
    return file_path

#TODO: updates just single value
def UpdateCSVValue(filename,secret_id):
    df = pd.read_csv(filename)
    # updating the column value/data
    df.loc[3, 'secret'] = secret_id
    # writing into the file
    df.to_csv(filename, index=False)

def AssociateSecrets(df):
    ids = [1, 2, 3, 4, 5, 6, 7, 8] #TODO generalize based on the santas list
    for index, row in df.iterrows():
        newSecret = True
        if row["secret"] == -1:
            while(newSecret):
                secret = random.choice(ids)
                if df.loc[df["secret"] == secret].empty and row["id"] != secret:
                    newSecret = False
            df.loc[index,"secret"] = secret
    return df

def WhatsMySecret(name,df):
    user_found = df.loc[df["name"] == name]
    user_secret = user_found["secret"].values[0]
    if not user_found.empty and user_secret != -1:
        secret_name = df.loc[df["id"]==user_secret]
        secret = secret_name["name"].values[0]
    elif user_found["secret"] == -1:
        st.write("Secret not associated! Contatct admin")
        secret = ""
    else:
        st.write("User not found! Did you write your name correctly?")
        secret = ""
    return secret

def WhatsMySecretSecured(name,pin,df):
    user_found = df.loc[df["name"] == name]
    user_pin = user_found["pins"].values[0]
    user_secret = user_found["secret"].values[0]
    print(user_pin)
    if not user_found.empty and user_secret != -1 and user_pin == pin:
        secret_name = df.loc[df["id"]==user_secret]
        secret = secret_name["name"].values[0]
    elif user_secret == -1:
        st.write("Secret not associated! Contatct admin")
        secret = ""
    else:
        st.write("User not found! Did you write your name correctly?")
        secret = ""
    return secret

def GenerateSecretSantaFile(df,file_path,connection_string,container_name):
    df = read_csv(file_path)
    AssociateSecrets(df)
    df.to_csv("kartoffel.csv",index=False)
    UploadFileToBlob(file_path,connection_string,container_name,file_path)

def ShowSecretSanta(file_path,connection_string,container_name,blob_name,username):
    file_path = DownloadBlob(connection_string,container_name,blob_name,file_path)
    df = pd.read_csv(file_path)
    secret = WhatsMySecret(username,df)
    return secret

def ShowSecretSantaSecured(file_path,connection_string,container_name,blob_name,username,pin):
    file_path = DownloadBlob(connection_string,container_name,blob_name,file_path)
    df = pd.read_csv(file_path)
    secret = WhatsMySecretSecured(username,pin,df)
    return secret