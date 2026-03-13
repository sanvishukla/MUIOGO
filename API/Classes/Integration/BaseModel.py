from abc import ABC, abstractmethod

class AbstractModel(ABC):
    """
    Base generic class for model adapters in the OG-CLEWS integration.
    Ensures a consistent interface for the WorkflowOrchestrator.
    """

    @abstractmethod
    def solve(self, case_id: str, scenario: str) -> dict:
        """
        Execute the solver and return an execution summary.
        
        Args:
            case_id: The ID of the case/scenario.
            scenario: The name of the run/scenario version.
            
        Returns:
            dict: Summary of solver exit code, compute time, and status.
        """
        pass

    @abstractmethod
    def get_outputs(self, case_id: str, scenario: str) -> dict:
        """
        Locate and return paths to relevant output artifacts (e.g., CSVs).
        
        Returns:
            dict: Mapping of artifact names to absolute file paths.
        """
        pass

    @abstractmethod
    def get_execution_context(self, scenario: str) -> dict:
        """
        Return metadata about the internal configuration of the model.
        """
        pass

    @abstractmethod
    def set_params(self, params: dict) -> None:
        """
        Inject exchange variables or parameters into the model
        prior to execution (used during coupled/iterative runs).
        """
        pass
