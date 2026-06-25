"""Smoke tests for Phase 2 environment and imports."""

import importlib
import platform

import pytest


def test_settings_defaults_load():
    from src.utils.config import get_settings

    settings = get_settings()
    assert "postgresql" in settings.database_url
    assert settings.wandb_project == "pk-pr-simulator"


@pytest.mark.parametrize(
    "module",
    [
        "pandas",
        "networkx",
        "mesa",
        "pymc",
        "sklearn",
        "fastapi",
        "duckdb",
        "plotly",
        "streamlit",
    ],
)
def test_core_dependency_imports(module: str):
    importlib.import_module(module)


def test_torch_import_optional():
    """Torch may fail DLL init on Windows without CUDA/VC++ redist; install still valid."""
    try:
        importlib.import_module("torch")
    except OSError as exc:
        if platform.system() == "Windows":
            pytest.skip(f"torch DLL not loadable in this environment: {exc}")
        raise


def test_transformers_import_optional():
    try:
        importlib.import_module("transformers")
    except OSError as exc:
        if platform.system() == "Windows":
            pytest.skip(f"transformers/torch DLL not loadable: {exc}")
        raise
