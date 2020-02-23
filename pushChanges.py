#!/usr/bin/python3

import argparse

import utils
import constants


def main():
    apiClient = utils.getApiClient()
    targetFolderId = utils.getIdFromPath(constants.DRIVE_FOLDER, apiClient)
    utils.pushFolder(constants.LOCAL_FOLDER, targetFolderId, apiClient)


def emptyTrash():
    apiClient = utils.getApiClient()
    _ = apiClient.files().emptyTrash().execute()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--yes", help=constants.CAUTION_TEXT_PUSH, action="store_true")
    parser.add_argument("-e", "--empty", help="Empty the trash", action="store_true")
    args = parser.parse_args()
    if args.empty:
        emptyTrash()
    if not args.yes:
        exit()
    main()
