# executor.py
import subprocess
import tempfile
import os
from typing import Tuple

DOCKER_IMAGE = "python:3.11-slim"

# Limits (you can adjust)
TIMEOUT_SECONDS = 10
MEMORY_LIMIT = "128m"
CPUS = "0.5"
PIDS_LIMIT = "64"


class ExecutionError(Exception):
    """Custom exception for execution failures."""
    def __init__(self, message: str, details: str | None = None):
        super().__init__(message)
        self.details = details or ""


def run_code_in_docker(code: str) -> Tuple[str, str]:
    """
    Run the given Python code in a Docker container.
    Returns (stdout, stderr).
    Raises ExecutionError on timeout or docker-related errors.
    """
    # 1. Create a temporary directory to hold the script
    with tempfile.TemporaryDirectory() as tmpdir:
        script_path = os.path.join(tmpdir, "code.py")

        # 2. Write user code to file
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code)

        # 3. Build docker run command
        # NOTE: Docker doesn't have a real --timeout flag for run, so we use
        # Python's subprocess timeout instead.
        cmd = [
            "docker",
            "run",
            "--rm",                    # remove container after exit
            "--network", "none",       # no network access
            "--memory", MEMORY_LIMIT,  # memory limit
            "--cpus", str(CPUS),       # CPU limit
            "--pids-limit", str(PIDS_LIMIT),  # limit processes/threads
            # For step 3 experiments, you can add '--read-only' here:
            # "--read-only",
            "-v", f"{tmpdir}:/app",    # mount temp dir into container
            "-w", "/app",              # workdir inside container
            DOCKER_IMAGE,
            "python", "code.py",
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired as e:
            # Container did not finish within TIMEOUT_SECONDS
            raise ExecutionError(
                f"Execution timed out after {TIMEOUT_SECONDS} seconds"
            ) from e
        except FileNotFoundError as e:
            # Docker not installed or not in PATH
            raise ExecutionError(
                "Docker is not installed or not available in PATH"
            ) from e
        except Exception as e:
            raise ExecutionError("Internal error while running code") from e

        stdout = result.stdout
        stderr = result.stderr

        # Non-zero return code: likely Python error (syntax/runtime)
        if result.returncode != 0:
            # We return stdout and stderr; API can decide how to show it
            return stdout, stderr

        return stdout, stderr
