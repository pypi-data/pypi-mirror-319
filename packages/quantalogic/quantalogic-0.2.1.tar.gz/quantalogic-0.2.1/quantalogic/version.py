from pathlib import Path

import toml


def get_version() -> str:
    """Get the current version of the package from pyproject.toml."""
    try:
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        with open(pyproject_path) as f:
            pyproject = toml.load(f)
            return pyproject["tool"]["poetry"]["version"]
    except Exception as e:
        raise RuntimeError(f"Failed to read version from pyproject.toml: {e}")
