# GDSyncOffline
GDSyncOffline is a tool to synchronize the folder present in your google drive with a local folder in your pc.

## How to use:
* Run `python3 -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib `
* Turn on the Drive API for you account from here(https://developers.google.com/drive/api/v3/quickstart/python) and download the credentials.json in the repository.
* Modify the `LOCAL_FOLDER` and `DRIVE_FOLDER` in main.py with your requirement.
* Run `python3 main.py`

## Features implemented:
* Downloads the missing files/folders in the local folder.
* Uploads the missing files/folders in the local folder.

## Features to be added:
* Synchronize deletion 
* Synchronize modification in a file 
