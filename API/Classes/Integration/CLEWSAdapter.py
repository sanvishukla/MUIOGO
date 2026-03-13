import os
import shutil
from pathlib import Path

from Classes.Integration.BaseModel import AbstractModel
from Classes.Case.DataFileClass import DataFile
from Classes.Base import Config

class CLEWSAdapter(AbstractModel):
    """
    Adapter that allows the WorkflowOrchestrator to run OSeMOSYS scenarios.
    It wraps the existing DataFileClass to expose a clean, stateless interface
    without modifying the 4000+ line legacy code.
    """

    def __init__(self, case_id: str):
        self.case_id = case_id
        # We instantiate the legacy class but do not run it immediately.
        self.runner = DataFile(case_id)

    def solve(self, case_id: str, scenario: str) -> dict:
        """
        Executes the legacy OSeMOSYS modeling pipeline.
        
        Args:
            case_id: The project name (e.g., 'ghana_case')
            scenario: The unique run identifier (e.g., 'baseline_v1')
            
        Returns:
            dict: Status summary containing the exit code and messages.
        """
        # We default to 'cbc' as it is the standard open-source solver in MUIOGO
        # The 'scenario' argument serves as the 'caserun' in legacy terminology
        
        # 1. Generate the data.txt first (legacy requirement)
        self.runner.generateDatafile(scenario)
        
        # 2. Run the actual solver pipeline
        # DataFileClass.run() returns a dictionary with 'status_code' and messages
        result = self.runner.run(solver='cbc', caserun=scenario)
        
        return {
            'status': result.get('status_code', 'unknown'),
            'messages': result.get('timer', result.get('error_message', '')),
            'raw_output': result
        }

    def get_outputs(self, case_id: str, scenario: str) -> dict:
        """
        Retrieves all generated CSVs from the scenario result directory.
        """
        context = self.get_execution_context(scenario)
        csv_dir = Path(context['csv_dir'])
        
        outputs = {}
        if csv_dir.exists():
            for csv_file in csv_dir.glob('*.csv'):
                outputs[csv_file.name] = str(csv_file.resolve())
                
        return outputs

    def get_execution_context(self, scenario: str) -> dict:
        """
        Calls the helper method injected into DataFileClass to locate files safely.
        """
        return self.runner.get_execution_context(scenario)

    def set_params(self, params: dict) -> None:
        """
        Inject parameters into OSeMOSYS. 
        For Phase 3 (Coupling), this will modify the generated `data.txt` 
        before `solve()` is called. 
        Note: Implementation of injection logic happens in Phase 3.
        """
        raise NotImplementedError(
            "CLEWSAdapter.set_params() is not yet implemented. "
            "Parameter injection is scheduled for Phase 3."
        )