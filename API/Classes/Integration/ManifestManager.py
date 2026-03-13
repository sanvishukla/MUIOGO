import subprocess
import json
import datetime
import os
import sys
from pathlib import Path

class ManifestManager:
    """
    Captures and stores the scientific 'DNA' of a model run.
    Ensures that every experiment is reproducible by logging
    software versions, git state, and environment snapshots.
    """

    def capture_environment(self, case_id: str, scenario: str) -> dict:
        """
        Capture the current software and hardware environment fingerprint.
        """
        manifest = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'case_id': case_id,
            'scenario': scenario,
            'software_env': {
                'python_version': sys.version,
                'pip_freeze': self._get_pip_freeze()
            },
            'git_state': self._get_git_state(),
            'solvers': self._get_solver_versions()
        }
        return manifest

    def save_manifest(self, manifest: dict, run_dir: Path) -> Path:
        """
        Save the captured manifest as a JSON artifact in the run directory.
        """
        # Ensure run_dir is a Path object
        run_dir_path = Path(run_dir)
        run_dir_path.mkdir(parents=True, exist_ok=True)
        
        timestamp_str = manifest.get('timestamp', datetime.datetime.utcnow().isoformat()).replace(":", "-")
        manifest_path = run_dir_path / f'run_manifest_{timestamp_str}.json'
        
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=4)
        
        return manifest_path

    def log_handoff(self, iteration: int, delta: dict, audit_log: list = None) -> list:
        """
        Append a before/after delta record for exchanged variables.
        Used to track convergence and data transformations between models.
        """
        if audit_log is None:
            audit_log = []
            
        record = {
            'iteration': iteration,
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'deltas': delta
        }
        audit_log.append(record)
        return audit_log

    def save_audit(self, audit_log: list, run_dir: Path) -> Path:
        """
        Save the handoff audit log to 'handoff_audit.json' in the run directory.
        """
        run_dir_path = Path(run_dir)
        run_dir_path.mkdir(parents=True, exist_ok=True)
        
        audit_path = run_dir_path / 'handoff_audit.json'
        
        with open(audit_path, 'w') as f:
            json.dump(audit_log, f, indent=4)
        
        return audit_path

    def _get_pip_freeze(self) -> str:
        try:
            return subprocess.check_output(['pip', 'freeze'], text=True, timeout=15)
        except Exception as e:
            return f"Error capturing pip freeze: {str(e)}"

    def _get_git_state(self) -> dict:
        try:
            commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True, timeout=10).strip()
            diff = subprocess.check_output(['git', 'diff', '--stat'], text=True, timeout=10).strip()
            return {
                'commit': commit,
                'is_dirty': len(diff) > 0,
                'branch': subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], text=True, timeout=10).strip()
            }
        except Exception:
            return {'error': 'Git history not available (not a repository or git missing)'}

    def _get_solver_versions(self) -> dict:
        versions = {}
        for solver in ['glpsol', 'cbc']:
            try:
                # Most solvers return version on stdout/stderr via --version
                out = subprocess.check_output([solver, '--version'], text=True, stderr=subprocess.STDOUT, timeout=5)
                versions[solver] = out.splitlines()[0]
            except Exception:
                versions[solver] = "Not found or executable failed"
        return versions
