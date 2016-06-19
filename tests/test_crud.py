# -*- coding: utf-8 -*-
"""
CRUD tests for row maniupulation.
"""

import logging
import os
import time

import sheetsync

import pytest


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler)
logging.basicConfig()

# ARSENAL_0304 = {'14': {'Apps': '39', 'Goals': '39', 'Name': 'Thierry Henry', 'Nat.': 'FRA', 'Pos.': 'DF'}}

ARSENAL_0304 = {'1': {'Apps': '54',
       'Goals': '0',
       'Name': 'Jens Lehmann',
       'Nat.': ' GER',
       'Pos.': 'GK'},
 '10': {'Apps': '38',
        'Goals': '5',
        'Name': 'Dennis Bergkamp',
        'Nat.': ' NED',
        'Pos.': 'FW'},
 '11': {'Apps': '22',
        'Goals': '4',
        'Name': 'Sylvain Wiltord',
        'Nat.': ' FRA',
        'Pos.': 'FW'},
 '12': {'Apps': '47',
        'Goals': '0',
        'Name': 'Lauren',
        'Nat.': ' CMR',
        'Pos.': 'DF'},
 '14': {'Apps': '39',
        'Goals': '39',
        'Name': 'Thierry Henry',
        'Nat.': ' FRA',
        'Pos.': 'DF'},
 '15': {'Apps': '38',
        'Goals': '0',
        'Name': 'Ray Parlour',
        'Nat.': ' ENG',
        'Pos.': 'MF'},
 '16': {'Apps': '11',
        'Goals': '0',
        'Name': 'Giovanni van Bronckhorst',
        'Nat.': ' NED',
        'Pos.': 'MF'},
 '17': {'Apps': '48',
        'Goals': '7',
        'Name': 'Edu',
        'Nat.': ' BRA',
        'Pos.': 'MF'},
 '18': {'Apps': '24',
        'Goals': '0',
        'Name': 'Pascal Cygan',
        'Nat.': ' FRA',
        'Pos.': 'DF'},
 '19': {'Apps': '46',
        'Goals': '4',
        'Name': 'Gilberto Silva',
        'Nat.': ' BRA',
        'Pos.': 'MF'},
 '22': {'Apps': '22',
        'Goals': '0',
        'Name': 'Ga\xebl Clichy',
        'Nat.': ' FRA',
        'Pos.': 'DF'},
 '23': {'Apps': '50',
        'Goals': '1',
        'Name': 'Sol Campbell',
        'Nat.': ' ENG',
        'Pos.': 'DF'},
 '25': {'Apps': '24',
        'Goals': '3',
        'Name': 'Nwankwo Kanu',
        'Nat.': ' NGR',
        'Pos.': 'FW'},
 '27': {'Apps': '3',
        'Goals': '0',
        'Name': 'Efstathios Tavlaridis',
        'Nat.': ' GRE',
        'Pos.': 'DF'},
 '28': {'Apps': '55',
        'Goals': '3',
        'Name': 'Kolo Tour\xe9',
        'Nat.': ' CIV',
        'Pos.': 'DF'},
 '3': {'Apps': '47',
       'Goals': '1',
       'Name': 'Ashley Cole',
       'Nat.': ' ENG',
       'Pos.': 'DF'},
 '30': {'Apps': '15',
        'Goals': '4',
        'Name': 'J\xe9r\xe9mie Aliadi\xe8re',
        'Nat.': ' FRA',
        'Pos.': 'FW'},
 '32': {'Apps': '1',
        'Goals': '0',
        'Name': 'Michal Papadopulos',
        'Nat.': ' CZE',
        'Pos.': 'FW'},
 '33': {'Apps': '5',
        'Goals': '0',
        'Name': 'Graham Stack',
        'Nat.': ' IRL',
        'Pos.': 'GK'},
 '39': {'Apps': '8',
        'Goals': '1',
        'Name': 'David Bentley',
        'Nat.': ' ENG',
        'Pos.': 'MF'},
 '4': {'Apps': '44',
       'Goals': '3',
       'Name': 'Patrick Vieira',
       'Nat.': ' FRA',
       'Pos.': 'MF'},
 '45': {'Apps': '3',
        'Goals': '0',
        'Name': 'Justin Hoyte',
        'Nat.': ' ENG',
        'Pos.': 'DF'},
 '5': {'Apps': '15',
       'Goals': '0',
       'Name': 'Martin Keown',
       'Nat.': ' ENG',
       'Pos.': 'DF'},
 '51': {'Apps': '1',
        'Goals': '0',
        'Name': 'Frank Simek',
        'Nat.': ' USA',
        'Pos.': 'DF'},
 '52': {'Apps': '1',
        'Goals': '0',
        'Name': 'John Spicer',
        'Nat.': ' ENG',
        'Pos.': 'FW'},
 '53': {'Apps': '3',
        'Goals': '0',
        'Name': 'Jerome Thomas',
        'Nat.': ' ENG',
        'Pos.': 'MF'},
 '54': {'Apps': '3',
        'Goals': '0',
        'Name': 'Quincy Owusu-Abeyie',
        'Nat.': ' GHA',
        'Pos.': 'FW'},
 '55': {'Apps': '1',
        'Goals': '0',
        'Name': '\xd3lafur Ingi Sk\xfalason',
        'Nat.': ' ISL',
        'Pos.': 'MF'},
 '56': {'Apps': '3',
        'Goals': '0',
        'Name': 'Ryan Smith',
        'Nat.': ' ENG',
        'Pos.': 'FW'},
 '57': {'Apps': '3',
        'Goals': '1',
        'Name': 'Cesc F\xe0bregas',
        'Nat.': ' ESP',
        'Pos.': 'MF'},
 '7': {'Apps': '51',
       'Goals': '19',
       'Name': 'Robert Pir\xe8s',
       'Nat.': ' FRA',
       'Pos.': 'MF'},
 '8': {'Apps': '44',
       'Goals': '10',
       'Name': 'Fredrik Ljungberg',
       'Nat.': ' SWE',
       'Pos.': 'MF'},
 '9': {'Apps': '21',
       'Goals': '5',
       'Name': 'Jos\xe9 Antonio Reyes',
       'Nat.': ' FRA',
       'Pos.': 'FW'}}

def test_soft_delete(new_from_arsenal_template):
    target = new_from_arsenal_template
    print('Soft delete rows from the spreadsheet')
    raw_data = target.data()
    # Delete Giovanni
    assert "16" in raw_data
    del raw_data["16"]
    target.sync(raw_data)
    # Check new data has "16 (DELETED)" in it. 
    new_raw_data = target.data()
    assert "1" in new_raw_data
    assert "16" not in new_raw_data
    assert "16 (DELETED)" in new_raw_data
 
def test_full_delete(new_from_arsenal_template):
    target = new_from_arsenal_template
    print('Test hard deletes of rows from the spreadsheet.')
    raw_data = target.data()
    target.flag_delete_mode = False
    # Turn on full deletion.
    assert "16" in raw_data
    del raw_data["16"]
    target.sync(raw_data)
    # Check we deleted "16" for real.
    new_raw_data = target.data()
    assert "1" in new_raw_data
    assert "16" not in new_raw_data
    assert "16 (DELETED)" not in new_raw_data

def test_change_row(new_from_arsenal_template):
    target = new_from_arsenal_template
    print('Test changing multiple rows.')
    correct_data = {}
    correct_data.update(ARSENAL_0304)
    correct_data["14"]["Apps"] = 51
    correct_data["14"]["Pos."] = "FW"
    correct_data["9"]["Nat."] = "ENG"
    target.sync(correct_data)
    new_raw_data = target.data()
    assert new_raw_data["14"]["Apps"] == '51'
    assert new_raw_data["14"]["Pos."] == "FW"
    assert new_raw_data["9"]["Nat."] == "ENG"

def test_extend_header(new_from_arsenal_template):
    target = new_from_arsenal_template
    print('Add additional columns, include expanding the spreadsheet.')
    full_data = {}
    full_data.update(ARSENAL_0304)
    # Add a column.
    for row in list(full_data.values()):
        row["Club"] = "Arsenal"
    target.sync(full_data)
    new_raw_data = target.data()
    assert "Club" in target.header
    assert new_raw_data["1"]["Club"] == "Arsenal"

def test_inject_only(new_from_arsenal_template):
    target = new_from_arsenal_template
    print('Test injecting partial rows, check no deleting.')
    extra_players = { "57" : {}, "32" : {} }
    extra_players["57"].update( ARSENAL_0304["57"] )
    extra_players["32"].update( ARSENAL_0304["32"] )
    target.inject(extra_players)
    new_raw_data = target.data()
    assert "1" in new_raw_data
    assert "19" in new_raw_data
    assert "57" in new_raw_data
    assert "32" in new_raw_data
    assert new_raw_data["57"]["Name"] == 'Cesc F\xe0bregas'

