# -*- coding: utf-8 -*-
"""
Test advanced CRUD features.
"""

import logging
import os
import time

import sheetsync

import pytest


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler)
logging.basicConfig()

def test_protected_fields(new_from_arsenal_template):
    target = new_from_arsenal_template
    target.protected_fields += ['Apps', 'Goals']
    updates = {"1" : {"Name" : "Jens Lehmann",
                       "Apps" : "0",
                       "Goals" : "0"},
                "4" : {"Name" : "Patrick V",
                       "Apps" : "100",
                       "Pos." : "??"},
                }

    def test_callback_fn(key_tuple, wks_row, raw_row, changed_fields):
        assert "Apps" not in changed_fields
        assert "Goals" not in changed_fields

    target.inject(updates, test_callback_fn)

    new_data = target.data()
    
    assert new_data["4"]["Name"] == "Patrick V"
    assert new_data["1"]["Apps"] == "54"

"""
def test_post_soft_delete():
    print('See how .data and .sync handles soft deleted rows.')
    assert False

def test_logging_large_changes():
    print('Test the truncate function.')
    assert False
"""
