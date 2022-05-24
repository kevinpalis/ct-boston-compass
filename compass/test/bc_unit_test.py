#!/usr/bin/env python3
'''
	Unit tests for Boston Compass

    Run using this command at the main compass directory: python3 -m pytest -v
    Note that these are very simple tests just to show how I would go about developing such a module.
    If given more time, and if this is a module that will eventually process more data, I would add more tests that will cover a good variety of real-life use-cases.
    But for the purpose of this coding exercise, I think the following tests are sufficient.

    @author Kevin Palis <kevin.palis@gmail.com>
'''
from compass import compass
from compass.util.bc_utility import ReturnCodes
import pytest

#Test running the compass with no parameters, ie. everything set as default - AKA Happy-path
def test_compass_main_all_defaults():
    assert compass.main([]) == ReturnCodes.SUCCESS

#Test running the compass with no parameters but verbose
def test_compass_main_all_defaults_verbose():
    assert compass.main(['-v']) == ReturnCodes.SUCCESS

#Test running the compass with all stops printed
def test_compass_main_show_all_stops():
    assert compass.main(['-a']) == ReturnCodes.SUCCESS

#Test running the compass with an invalid source stop
def test_compass_invalid_source_stop():
    assert compass.main(['-s', 'NopeNope']) == ReturnCodes.INVALID_VERTEX

#Test running the compass with an invalid destination stop
def test_compass_invalid_destination_stop():
    assert compass.main(['-d', 'DoesNotExist']) == ReturnCodes.INVALID_VERTEX

#Test running the compass with invalid API key
def test_compass_invalid_api_key():
    assert compass.main(['-k', 'InvalidKey']) == ReturnCodes.API_CALL_FAILED
