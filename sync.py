#!/usr/bin/python3

import utils
import constants


def main():
    apiClient = utils.getApiClient()
    targetFolderId = utils.getIdFromPath(constants.DRIVE_FOLDER, apiClient)
    utils.syncFolder(constants.LOCAL_FOLDER, targetFolderId, apiClient)


if __name__ == '__main__':
    main()
