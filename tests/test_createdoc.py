# -*- coding: utf-8 -*-
"""
Test document creation:
    - Create new blank spreadsheets.
    - Creating from a template copy.
    - Creating in an existing folder (and removing it from the root container!)
"""

import logging
import os
import time

import sheetsync

import pytest


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler)
logging.basicConfig()

"""
def test_create_from_copy_template_key():
    print('TODO: Create by copying template sheet.')
    assert False


def test_create_from_copy_template_name():
    print('TODO: Create by copying template sheet.')
    assert False

"""

def test_move_to_folder_by_key(new_sheet_kwargs):
    kwargs = new_sheet_kwargs
    kwargs.pop('folder_name')
    target = sheetsync.Sheet(**kwargs)
    # Delete the doc
    target.drive_service.files().delete(fileId=target.document_key).execute()


def test_move_to_folder_by_name(new_sheet_kwargs):
    kwargs = new_sheet_kwargs
    kwargs.pop('folder_key')
    target = sheetsync.Sheet(**kwargs)
    # Delete the doc
    target.drive_service.files().delete(fileId=target.document_key).execute()


def test_move_to_new_folder_by_name(new_sheet_kwargs):
    kwargs = new_sheet_kwargs
    kwargs.pop('folder_key')
    kwargs.pop('folder_name')
    new_folder_name = 'sheetsync testrun %s' % int(time.time())
    kwargs['folder_name'] = new_folder_name
    target = sheetsync.Sheet(**kwargs)
    # Delete the doc
    target.drive_service.files().delete(fileId=target.document_key).execute()

    # Delete the new folder too..
    assert new_folder_name == target.folder['title']
    target.drive_service.files().delete(fileId=target.folder['id']).execute()


def test_the_kartik_test(new_sheet_kwargs):
    # The most basic usage of creating a new sheet and adding data to it.
    # From April, Google defaults to using new-style sheets which requires
    # workarounds right now.
    kwargs = new_sheet_kwargs
    target = sheetsync.Sheet(credentials = kwargs['credentials'],
                             document_name = kwargs['document_name'])
    # Check we can sync data to the newly created sheet.
    data = {"1" : {"name" : "Gordon", "color" : "Green"},
            "2" : {"name" : "Thomas", "color" : "Blue" } }
    target.sync(data)
    
    retrieved_data = target.data()
    assert "1" in retrieved_data
    assert retrieved_data["1"]["name"] == "Gordon"
    assert "2" in retrieved_data
    assert retrieved_data["2"]["color"] == "Blue"
    assert retrieved_data["2"]["Key"] == "2"

    # Try opening the doc with a new instance (thereby guessing key columns)
    test_read = sheetsync.Sheet(credentials = kwargs['credentials'],
                                document_name = kwargs['document_name'])
    retrieved_data_2 = test_read.data()
    assert "1" in retrieved_data_2
    assert "2" in retrieved_data_2
    assert retrieved_data["2"]["color"] == "Blue"

    # Delete the doc
    target.drive_service.files().delete(fileId=target.document_key).execute()
