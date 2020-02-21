#!/usr/bin/python3

import argparse

import utils
import constants


def main():
    apiClient = utils.getApiClient()
    targetFolderId = utils.getIdFromPath(constants.DRIVE_FOLDER, apiClient)
    utils.pushFolder(constants.LOCAL_FOLDER, targetFolderId, apiClient)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--yes", help=constants.CAUTION_TEXT_PUSH, action="store_true")
    args = parser.parse_args()
    if not args.yes:
        ans = input("%s\nDo you want to continue(y/n):" % constants.CAUTION_TEXT_PUSH)
        if ans != 'y':
            exit()
    main()
