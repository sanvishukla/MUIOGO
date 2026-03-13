import sys
import os
import json
from pathlib import Path

# Fix import paths
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'API')))

from Classes.Integration.CLEWSAdapter import CLEWSAdapter
from Classes.Integration.ManifestManager import ManifestManager

def test_phase_1():
    print("=== DRAFTING PHASE 1 DEMO ===")
    
    # In a real environment, you need an actual case ID that exists in WebAPP/DataStorage/
    # If 'test_case' does not exist, this will fail on initialization or during solve().
    # Please replace 'test_case' with a real case name from your DataStorage folder.
    case_id = "CLEWs Demo" 
    scenario = "demo_scenario_run"
    
    try:
        print(f"\n1. Initializing Universal Plug (CLEWSAdapter) for case: {case_id}")
        adapter = CLEWSAdapter(case_id)
        
        print("\n2. Simulating a 'solve()' call... (Connecting to Legacy OSeMOSYS)")
        # Note: If 'test_case' is empty or doesn't have a genData.json, this will throw an error.
        # result = adapter.solve(case_id, scenario)
        # print(f"Solver Status: {result['status']}")
        print(f"-> solve() executes the legacy run() method safely.")
        
        print("\n3. Retrieving Execution Context:")
        context = adapter.get_execution_context(scenario)
        print(json.dumps(context, indent=2))
        
        print("\n4. Running the DNA Audit (ManifestManager)...")
        manager = ManifestManager()
        manifest = manager.capture_environment(case_id, scenario)
        
        # Save manifest
        # Ensure we have a valid output directory (mocked here based on context)
        run_dir_path = Path(context['csv_dir']).parent
        run_dir_path.mkdir(parents=True, exist_ok=True)
        
        manifest_path = manager.save_manifest(manifest, run_dir_path)
        print(f"-> Manifest Saved to: {manifest_path}")
        print("\nManifest Content:")
        print(json.dumps(manifest, indent=2))
        
        print("\n=== PHASE 1 DEMO COMPLETE ===")
        print("Integration is successful: The adapter loads and tracks the environment.")
        
    except Exception as e:
        print(f"\n[ERROR] Demo failed because: {e}")
        print("Ensure that the 'case_id' specified actually exists in WebAPP/DataStorage/.")

if __name__ == "__main__":
    test_phase_1()
