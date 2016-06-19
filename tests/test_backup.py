# -*- coding: utf-8 -*-
"""
Test the "backup" function, which saves sheet data to file.
"""

import logging
import os
import time

import sheetsync

import pytest


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler)
logging.basicConfig()

def test_backup(simpsons_sheet, credentials):
    backup_name = 'backup test: %s' % int(time.time())
    backup_key = simpsons_sheet.backup(backup_name, folder_name="sheetsync backups")

    backup_sheet = sheetsync.Sheet(credentials=credentials,
                                   document_key = backup_key,
                                   worksheet_name = 'Simpsons',
                                   key_column_headers = ['Character'],
                                   header_row_ix=1)

    backup_data = backup_sheet.data() 
    assert "Bart Simpson" in backup_data
    assert backup_data["Bart Simpson"]["Voice actor"] == "Nancy Cartwright"

    logger.debug('Deleting backup spreadsheet: {}'.format(backup_sheet.document_name))
    backup_sheet.drive_service.files().delete(fileId=backup_sheet.document_key).execute()
    logger.debug('Deleted backup spreadsheet: {}'.format(backup_sheet.document_name))
