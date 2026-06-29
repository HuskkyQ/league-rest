import subprocess
import sys
import sysconfig
import site
import shutil
from pathlib import Path


def test_smoke_command_prints_ok():
    result = subprocess.run(
        [sys.executable, "-m", "league_rest", "--smoke"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "league-rest smoke ok" in result.stdout


def test_installed_console_script_prints_ok():
    script_name = "league-rest.exe" if sys.platform == "win32" else "league-rest"
    user_bin = "Scripts" if sys.platform == "win32" else "bin"
    candidates = [
        Path(sysconfig.get_path("scripts")) / script_name,
        Path(site.USER_BASE) / user_bin / script_name,
    ]
    script_path = next((str(path) for path in candidates if path.exists()), None)
    if script_path is None:
        script_path = shutil.which(script_name)

    assert script_path is not None

    result = subprocess.run(
        [script_path, "--smoke"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "league-rest smoke ok" in result.stdout
