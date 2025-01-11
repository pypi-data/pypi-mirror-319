import pytest
from pathlib import Path
import subprocess
import venv
import shutil

@pytest.fixture(scope="session", autouse=True)
def session_venv(tmp_path_factory):
    """Create and cleanup virtual environment for the entire test session"""
    tmp_path = tmp_path_factory.mktemp("venv_dir")
    venv_path = tmp_path / "venv"
    venv.create(venv_path, with_pip=True)
    
    yield venv_path
    
    # Cleanup after all tests
    if venv_path.exists():
        shutil.rmtree(str(venv_path))

@pytest.fixture
def temp_venv(session_venv):
    """Return python/pip paths from the session venv"""
    if Path.home().joinpath('AppData').exists():  # Windows
        python_path = session_venv / "Scripts" / "python.exe"
        pip_path = session_venv / "Scripts" / "pip.exe"
    else:  # Linux/Mac
        python_path = session_venv / "bin" / "python"
        pip_path = session_venv / "bin" / "pip"
    
    print(f"Python path: {python_path}")
    print(f"Pip path: {pip_path}")
    return session_venv, python_path, pip_path


def test_venv_creation(temp_venv, tmp_path):
    """Test that virtual environment is created correctly"""
    venv_path, python_path, pip_path = temp_venv
    assert venv_path.exists()
    assert python_path.exists()
    assert pip_path.exists()

def test_pip_version(temp_venv):
    """Test that pip is installed and working"""
    venv_path, python_path, pip_path = temp_venv
    result = subprocess.run(
        [str(pip_path), "--version"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "pip" in result.stdout

def test_package_install_uninstall(temp_venv):
    """Test that the package can be uninstalled"""
    venv_path, python_path, pip_path = temp_venv
    
    # First install
    subprocess.run(
        [str(pip_path), "install", "-e", "."],
        cwd=Path(__file__).parent.parent.parent,
        capture_output=True
    )
    
    # Then uninstall
    result = subprocess.run(
        [str(pip_path), "uninstall", "-y", "clipthread"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Installation failed: {result.stderr}"