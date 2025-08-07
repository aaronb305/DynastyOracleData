###############################################################
# tests/test_data_fetcher_core.py
#
# Tests for core/data_fetcher_core.py shared logic.
#
# Author: Dynasty Oracle
# Date: August 6, 2025
###############################################################

import pytest
import pandas as pd
from core import data_fetcher_core

def test_normalize_name_basic():
    # Test normalization of player names
    
    assert data_fetcher_core.normalize_name('Patrick Mahomes II') == 'patrick mahomes'
    assert data_fetcher_core.normalize_name('Justin Jefferson Jr.') == 'justin jefferson'
    assert data_fetcher_core.normalize_name('Saquon Barkley') == 'saquon barkley'
    assert data_fetcher_core.normalize_name('') == ''
    assert data_fetcher_core.normalize_name(None) == ''

# --- Test clean_and_merge_data ---
def test_clean_and_merge_data_merges():
    # Test merging and cleaning of sample data
    sleeper_df = pd.DataFrame({
        'full_name': ['Patrick Mahomes', 'Justin Jefferson'],
        'position': ['QB', 'WR'],
        'player_id': ['1', '2'],
        'team': ['KC', 'MIN']
    })
    ktc_df = pd.DataFrame({
        'name': ['Patrick Mahomes', 'Justin Jefferson'],
        'position': ['QB', 'WR'],
        'value': [9000, 8500]
    })
    merged = data_fetcher_core.clean_and_merge_data(sleeper_df, ktc_df)
    assert 'norm_name' in merged.columns
    assert 'value' in merged.columns
    assert 'team' in merged.columns
    assert len(merged) == 2

# --- Test fetch_sleeper_players and fetch_ktc_player_data ---
# These should be mocked for network/Selenium reliability
import types

def test_fetch_sleeper_players_mock(monkeypatch):
    # Mock Sleeper API response for testing
    def mock_get(*args, **kwargs):
        class MockResp:
            def raise_for_status(self): pass
            def json(self):
                return {
                    '1': {'full_name': 'Patrick Mahomes', 'position': 'QB', 'player_id': '1', 'team': 'KC'},
                    '2': {'full_name': 'Justin Jefferson', 'position': 'WR', 'player_id': '2', 'team': 'MIN'}
                }
        return MockResp()
    monkeypatch.setattr(data_fetcher_core.requests, 'get', mock_get)
    df = data_fetcher_core.fetch_sleeper_players()
    assert 'full_name' in df.columns
    assert len(df) == 2

def test_fetch_ktc_player_data_mock(monkeypatch):
    # Mock Selenium driver for testing KTC fetch
    def mock_driver(*args, **kwargs):
        class MockDriver:
            def get(self, url): pass
            @property
            def page_source(self):
                # Use single quotes for the HTML and escape the inner double quote
                return "<div id='rankings-page-rankings'><div class='player-name-wrapper'><p class='player-name'>Patrick Mahomes</p><p class='player-details'>QB – KC – 28 y.o. – 6\'3</p></div></div>"
            def quit(self): pass
            def find_element(self, by, value):
                # Stub for WebDriverWait/EC
                class DummyElement:
                    pass
                return DummyElement()
        return MockDriver()
    monkeypatch.setattr(data_fetcher_core.webdriver, 'Chrome', mock_driver)
    df = data_fetcher_core.fetch_ktc_player_data()
    assert 'name' in df.columns or 'playerName' in df.columns or 'norm_name' in df.columns
    assert len(df) >= 1
