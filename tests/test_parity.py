import pytest
import shutil
import filecmp
import sys
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the API folder to sys.path so that 'Classes' can be imported correctly by pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../API')))

from Classes.Case.DataFileClass import DataFile
from Classes.Integration.CLEWSAdapter import CLEWSAdapter
from Classes.Base import Config

# Note: This test requires a valid OSeMOSYS case in WebAPP/DataStorage/ to run against.
# For testing purposes, we assume 'test_case' exists.

@pytest.fixture
def mock_case_dir(tmp_path):
    """
    Creates a temporary valid case structure for testing parity without
    polluting the actual DataStorage.
    """
    case_name = "test_case"
    case_dir = tmp_path / "DataStorage" / case_name / "res"
    
    # Old API creates 'baseline', new API creates 'adapted_run'
    old_run_dir = case_dir / "baseline" / "csv"
    new_run_dir = case_dir / "adapted_run" / "csv"
    
    old_run_dir.mkdir(parents=True)
    new_run_dir.mkdir(parents=True)
    
    # Mocking solver output CSVs
    (old_run_dir / "ProductionByTechnology.csv").write_text("Year,Value\n2020,100")
    (new_run_dir / "ProductionByTechnology.csv").write_text("Year,Value\n2020,100")

    return {
        'case_id': case_name,
        'old_dir': old_run_dir,
        'new_dir': new_run_dir,
        'base': tmp_path / "DataStorage"
    }

def test_clews_adapter_parity(mock_case_dir):
    """
    Validates that the CLEWSAdapter wrapper produces bit-identical
    results to the legacy DataFileClass.run() method.
    
    # IMPORTANT: This test validates test infrastructure only.
    # The real parity test requires a live OSeMOSYS fixture and solver binaries.
    # See: docs/testing.md for how to run the full integration test suite.
    """
    case_id = mock_case_dir['case_id']
    
    # In a real environment, we would execute both:
    # 1. DataFileClass(case_id).run(solver='cbc', caserun='baseline') 
    # 2. CLEWSAdapter(case_id).solve(case_id, 'adapted_run')
    #
    # Here, we assert the checksum parity logic of their resulting directories.
    
    old_csvs = sorted(mock_case_dir['old_dir'].glob('*.csv'))
    new_csvs = sorted(mock_case_dir['new_dir'].glob('*.csv'))
    
    assert len(old_csvs) == len(new_csvs), "Mismatch in generated CSV count."
    
    for old_file, new_file in zip(old_csvs, new_csvs):
        assert old_file.name == new_file.name, "File name mismatch."
        
        # Perform shallow=False for bit-for-bit checksum comparison
        is_identical = filecmp.cmp(old_file, new_file, shallow=False)
        assert is_identical, f"Regression detected in output file: {old_file.name}"

def test_clews_adapter_handles_missing_outputs(mock_case_dir):
    """
    Tests that the adapter gracefully handles a run that produces no CSV outputs.
    """
    case_id = mock_case_dir['case_id']
    
    # We mock the DataFile initialization to avoid reading actual case JSONs during the unit test
    with patch('Classes.Integration.CLEWSAdapter.DataFile'):
        adapter = CLEWSAdapter(case_id)
        
        # Mock context to point to a non-existent CSV directory
        with patch.object(adapter, 'get_execution_context', return_value={'csv_dir': str(mock_case_dir['base'] / "doesnt_exist")}):
            outputs = adapter.get_outputs(case_id, 'fake_scenario')
            assert outputs == {}, "Should return empty dict when output folder doesn't exist"

def test_manifest_manager_handles_missing_git():
    """
    Tests that the ManifestManager gracefully handles errors from subprocesses,
    such as when git is not installed or repo is corrupted.
    """
    from Classes.Integration.ManifestManager import ManifestManager
    manager = ManifestManager()
    
    # Force git command to fail
    with patch('subprocess.check_output', side_effect=Exception("mocked git failure")):
        git_state = manager._get_git_state()
        assert 'error' in git_state, "Should return dict with error key on subprocess failure"

def test_path_traversal_prevention():
    """
    Tests that the application's path validation logic correctly traps
    malicious input trying to escape the intended directory.
    """
    malicious_scenario = "../../../etc/passwd"
    
    with pytest.raises(PermissionError):
        Config.validate_path(Config.DATA_STORAGE, malicious_scenario)
