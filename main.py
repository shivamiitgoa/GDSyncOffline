#!/usr/bin/python3

from __future__ import print_function
import os 
import io
import pickle
import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import shutil 

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

# Global Variables 
LOCAL_FOLDER = '/home/shivam/Desktop/Mobile'
DRIVE_FOLDER = 'Mobile'

def getApiClient():
    credentials = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    return build('drive', 'v3', credentials=credentials)


def getIdFromPath(drivePath, apiClient):
    segmentedPath = drivePath.split()
    currentID = 'root'
    for folderName in segmentedPath:
        if len(folderName) > 0:
            query = "('%s' in parents) and (name = '%s')" % (currentID, folderName)
            result = apiClient.files().list(q=query).execute()
            currentID = result['files'][0]['id']
    return currentID


def getLocalFilesFolders(localPath):
    localFilesFolders = os.listdir(localPath)
    localFiles = [path for path in localFilesFolders if os.path.isfile(os.path.join(localPath, path))]
    localFolders = [path for path in localFilesFolders if os.path.isdir(os.path.join(localPath, path))]
    localFilePaths = [os.path.join(localPath, name) for name in localFiles]
    localFolderPaths = [os.path.join(localPath, name) for name in localFolders]
    return localFilePaths, localFolderPaths, set(localFiles), set(localFolders)


def getDriveFilesFolders(driveId, apiClient):
    query = "'%s' in parents" % driveId
    driveFilesFolders = apiClient.files().list(q=query, pageSize = 1000).execute()['files']
    driveFiles = []
    driveFolders = []
    for item in driveFilesFolders:
        if item['mimeType'] == "application/vnd.google-apps.folder":
            driveFolders.append(item)
        else:
            driveFiles.append(item)
    driveFilesSet = set([item['name'] for item in driveFiles])
    driveFoldersSet = set([item['name'] for item in driveFolders])
    return driveFiles, driveFolders, driveFilesSet, driveFoldersSet


def downloadMissingLocalFiles(apiClient, localPath, localFilesSet, driveFilesData):
    for item in driveFilesData:
        if item['name'] not in localFilesSet:
            try:
                file_id = item['id']
                request = apiClient.files().get_media(fileId=file_id)
                localFilePath = os.path.join(localPath, item['name'])
                fileIO = io.FileIO(localFilePath, 'wb')
                downloader = MediaIoBaseDownload(fileIO, request, chunksize=1024*1024)
                done = False
                print("\nDownloading %s" % item['name'])
                while not done:
                    status, done = downloader.next_chunk()
                    print ("\r%d%%" % int(status.progress() * 100), end="")
            except Exception as e:
                print("\nFollowing exception occurred:")
                print(e)


def recursivelySyncDriveFolders(apiClient, localPath, localFoldersSet, driveFoldersData):
    for item in driveFoldersData:
        localFolderPath = os.path.join(localPath, item['name'])
        if item['name'] not in localFoldersSet:
            os.mkdir(localFolderPath)
        syncFolder(localFolderPath, item['id'], apiClient)


def uploadMissingDriveFiles(apiClient, localFilePaths, driveId, driveFilesSet):
    for localItemPath in localFilePaths:
        itemName = os.path.basename(localItemPath)
        if itemName not in driveFilesSet:
            fileMetadata = {
                'name': itemName,
                'parents': [driveId]
            }
            media = MediaFileUpload(localItemPath)
            print("\nUploading %s" % itemName)
            created = apiClient.files().create(body=fileMetadata, media_body = media, fields='id').execute()
            print("\nFile uploaded with ID: %s" % created.get('id'))


def recursivelySyncMissingDriveFolders(apiClient, localFolderPaths, driveId, driveFoldersSet):
    for itemPath in localFolderPaths:
        itemName = os.path.basename(itemPath)
        if itemName not in driveFoldersSet:
            folderMetadata = {
                'name' : itemName,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [driveId]
            }
            created = apiClient.files().create(body=folderMetadata, fields='id').execute()
            syncFolder(itemPath, created.get('id'), apiClient)


def syncFolder(localPath, driveId, apiClient):
    localFilePaths, localFolderPaths, localFilesSet, localFoldersSet = getLocalFilesFolders(localPath)
    driveFilesData, driveFoldersData, driveFilesSet, driveFoldersSet = getDriveFilesFolders(driveId, apiClient)
    downloadMissingLocalFiles(apiClient, localPath, localFilesSet, driveFilesData)
    recursivelySyncDriveFolders(apiClient, localPath, localFoldersSet, driveFoldersData)
    uploadMissingDriveFiles(apiClient, localFilePaths, driveId, driveFilesSet)
    recursivelySyncMissingDriveFolders(apiClient, localFolderPaths, driveId, driveFoldersSet)


def main():
    apiClient = getApiClient()
    targetFolderId = getIdFromPath(DRIVE_FOLDER, apiClient)
    syncFolder(LOCAL_FOLDER, targetFolderId, apiClient)


if __name__ == '__main__':
    main()


# For files in (FI1 and FI2), compare both the copies to check if they are the same. If not then replace the older one with the latest one 
# For each folder in (FO1 and FO2), update the root folder to this new folder and do the same thing that we have done with the root folder 




