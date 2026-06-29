import subprocess
import sys


def test_smoke_command_prints_ok():
    result = subprocess.run(
        [sys.executable, "-m", "league_rest", "--smoke"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "league-rest smoke ok" in result.stdout
