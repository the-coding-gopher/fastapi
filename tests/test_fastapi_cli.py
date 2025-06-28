import subprocess
import sys
from unittest.mock import Mock, patch

import fastapi.cli
import pytest


def test_fastapi_cli():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "fastapi",
            "dev",
            "non_existent_file.py",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert result.returncode == 1, result.stdout
    assert "Path does not exist non_existent_file.py" in result.stdout


def test_fastapi_cli_not_installed():
    with patch.object(fastapi.cli, "cli_main", None):
        with pytest.raises(RuntimeError) as exc_info:
            fastapi.cli.main()
        assert "To use the fastapi command, please install" in str(exc_info.value)


def test_fastapi_cli_help():
    result = subprocess.run(
        [sys.executable, "-m", "fastapi", "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert result.returncode == 0 or "fastapi command" in result.stdout


def test_fastapi_main_function_direct():
    with patch.object(fastapi.cli, "cli_main", None):
        with pytest.raises(RuntimeError) as exc_info:
            fastapi.cli.main()
        assert "fastapi[standard]" in str(exc_info.value)


def test_fastapi_main_with_mock_cli():
    mock_cli = Mock()
    with patch.object(fastapi.cli, "cli_main", mock_cli):
        fastapi.cli.main()
        mock_cli.assert_called_once()


def test_fastapi_cli_import_error_message():
    with patch.object(fastapi.cli, "cli_main", None):
        with pytest.raises(RuntimeError) as exc_info:
            fastapi.cli.main()
        error_msg = str(exc_info.value)
        assert 'To use the fastapi command, please install "fastapi[standard]"' in error_msg
        assert "pip install" in error_msg


def test_fastapi_cli_module_execution():
    result = subprocess.run(
        [sys.executable, "-c", "import fastapi.cli; fastapi.cli.main()"],
        capture_output=True,
        encoding="utf-8",
    )
    assert result.returncode != 0
    assert "fastapi[standard]" in result.stderr</str>
