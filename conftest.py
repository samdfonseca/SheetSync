import os
import shutil
import sys
import time
import logging

import sheetsync

import pytest


# TODO: Use this: http://stackoverflow.com/questions/22574109/running-tests-with-api-authentication-in-travis-ci-without-exposing-api-password

logger = logging.getLogger(__name__)
logging.basicConfig()

CREDENTIAL_CACHE_FILE = 'credentials.json'
CREDENTIAL_CACHE = os.getenv('CREDENTIAL_CACHE')
CLIENT_ID = os.environ['SHEETSYNC_CLIENT_ID']  
CLIENT_SECRET = os.environ['SHEETSYNC_CLIENT_SECRET']
# Optional folder_key that all spreadsheets, and folders, will be created in.
TESTS_FOLDER_KEY = os.environ.get("SHEETSYNC_FOLDER_KEY")
TESTS_FOLDER_NAME = "sheetsync testruns"
TEMPLATE_KEY = "1q83vSWMVHoLCPAUEW70RhK_k-yiD3Zwc9kTIf0cQQzo"
SIMPSONS_KEY = "1-mOUNbmknEuKPs9HVfGu3i6Q_3JZdpUk_WeUhKoLAqI"

@pytest.fixture(scope='session')
def credentials():
    if not os.path.exists(CREDENTIAL_CACHE_FILE) or os.stat(CREDENTIAL_CACHE_FILE).st_size == 0:
        with open(CREDENTIAL_CACHE_FILE, 'w') as f:
            logger.debug('Writing credential cache to file: {}'.format(CREDENTIAL_CACHE_FILE))
            logger.debug('Credential cache: {}'.format(CREDENTIAL_CACHE))
            f.write(CREDENTIAL_CACHE)
    logger.debug('Retrieving OAuth2.0 credentials')
    creds = sheetsync.ia_credentials_helper(CLIENT_ID, CLIENT_SECRET, 
                    credentials_cache_file='credentials.json')
    logger.debug('Retrieved OAuth2.0 credentials')
    return creds


@pytest.yield_fixture
def new_from_arsenal_template(credentials):
    target = None
    try:
        logger.debug('Creating spreadsheet from template key: {}'.format(TEMPLATE_KEY))
        # Copy the template spreadsheet into the prescribed folder.
        new_doc_name = '%s %s' % (__name__, int(time.time()))
        target = sheetsync.Sheet(credentials=credentials,
                                 document_name = new_doc_name,
                                 worksheet_name = 'Arsenal',
                                 folder_key = TESTS_FOLDER_KEY,
                                 template_key = TEMPLATE_KEY,
                                 key_column_headers = ['No.'],
                                 header_row_ix=2,
                                 formula_ref_row_ix=1)
        logger.debug('Created new speadsheet: {}'.format(target.document_name))
        yield target
    finally:
        if target is not None:
            logger.debug('Deleting test spreadsheet: {}'.format(target.document_name))
            target.drive_service.files().delete(fileId=target.document_key).execute()
            logger.debug('Deleted test spreadsheet: {}'.format(target.document_name))


@pytest.yield_fixture
def simpsons_sheet(credentials):
    target = None
    try:
        logger.debug('Opening spreadsheet key: {}'.format(TEMPLATE_KEY))
        target = sheetsync.Sheet(credentials=credentials,
                                 document_key = SIMPSONS_KEY,
                                 folder_key = TESTS_FOLDER_KEY,
                                 worksheet_name = 'Simpsons',
                                 key_column_headers = ['Character'],
                                 header_row_ix=1)
        logger.debug('Opened spreadsheet: {}'.format(target.document_name))
        yield target
    finally:
        pass


@pytest.fixture
def new_sheet_kwargs(credentials):
    new_doc_name = '%s-%s-%s' % ('sheetsync', sys._getframe().f_code.co_name, int(time.time()))
    kwargs = {
            'credentials': credentials,
            'document_name': new_doc_name,
            'folder_key': TESTS_FOLDER_KEY,
            'folder_name': TESTS_FOLDER_NAME,
            'worksheet_name': 'Sheet1',
            }
    return kwargs

            
@pytest.yield_fixture
def new_sheet_getter(credentials):
    def func(sheet_name):
        new_doc_name = '%s-%s-%s' % (sheet_name, sys._getframe().f_code.co_name, int(time.time()))
        target = sheetsync.Sheet(credentials=credentials,
                                 document_name = new_doc_name,
                                 folder_key = TESTS_FOLDER_KEY)
        return target
