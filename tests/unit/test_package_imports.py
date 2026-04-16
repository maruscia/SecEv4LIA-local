# Copyright 2026 - AI4I. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Test that all package modules can be imported correctly.
This test ensures that all dependencies are properly declared in pyproject.toml
and the package can be installed and used without import errors.
"""

import importlib
import pkgutil
import pytest
import secev4lia as secev


class TestPackageImports:
    """Test suite to verify all secev modules can be imported."""

    def test_main_package_import(self):
        """Test that the main secev package can be imported."""

        assert secev is not None

    def test_cli_main_import(self):
        """Test that the CLI entry point can be imported.

        This is the entry point for the secev CLI command.
        If this fails, users won't be able to run 'secev4lia' commands.
        """
        from secev4lia.cli.main import cli

        assert cli is not None

    def test_agent_import(self):
        """Test that the SecEv4LIA class can be imported."""
        from secev4lia import SecEv4LIA

        assert SecEv4LIA is not None

    def test_client_import(self):
        """Test that the Client class can be imported."""
        from secev4lia import Client

        assert Client is not None

    def test_router_import(self):
        """Test that the AgentRouter can be imported."""
        from secev4lia.router import AgentRouter

        assert AgentRouter is not None

    def test_storage_enums_import(self):
        """Test that storage enums are importable."""
        from secev4lia.server.storage.enums import EvaluationStatusEnum

        assert EvaluationStatusEnum is not None

    def test_attacks_import(self):
        """Test that attacks module can be imported."""
        from secev4lia import attacks

        assert attacks is not None

    def test_utils_import(self):
        """Test that utils module can be imported."""
        from secev4lia import utils

        assert utils is not None

    def test_dateutil_dependency(self):
        """Test that python-dateutil is available.

        This dependency is required for ISO date parsing in models.
        """
        from dateutil.parser import isoparse

        assert isoparse is not None

    def test_pydantic_dependency(self):
        """Test that pydantic v2 is available with email extras.

        This dependency is required for model definitions, client classes,
        and storage records throughout the SDK.
        """
        from pydantic import BaseModel, ConfigDict, PrivateAttr, field_validator

        assert BaseModel is not None
        assert ConfigDict is not None
        assert PrivateAttr is not None
        assert field_validator is not None


class TestAllSubmodulesImportable:
    """Test that all submodules in secev are importable."""

    @pytest.fixture
    def secev4lia_submodules(self):
        """Get list of all secev submodules."""
        import secev4lia

        submodules = []
        package_path = secev4lia.__path__
        prefix = secev4lia.__name__ + "."

        for importer, modname, ispkg in pkgutil.walk_packages(
            package_path, prefix=prefix
        ):
            submodules.append(modname)

        return submodules

    def test_all_submodules_importable(self, secev4lia_submodules):
        """Test that all discovered submodules can be imported.

        This is a comprehensive test that walks through all modules
        in the secev package and attempts to import them.
        This helps catch missing dependencies early.
        """
        failed_imports = []

        for modname in secev4lia_submodules:
            try:
                importlib.import_module(modname)
            except ImportError as e:
                failed_imports.append((modname, str(e)))

        if failed_imports:
            error_msg = "Failed to import the following modules:\n"
            for modname, error in failed_imports:
                error_msg += f"  - {modname}: {error}\n"
            pytest.fail(error_msg)


class TestDependenciesAvailable:
    """Test that all required dependencies are installed."""

    @pytest.mark.parametrize(
        "package_name",
        [
            "requests",
            "pydantic",
            "litellm",
            "openai",
            "rich",
            "click",
            "yaml",  # pyyaml
            "textual",
            "dateutil",  # python-dateutil
            "attrs",
        ],
    )
    def test_dependency_importable(self, package_name):
        """Test that each required dependency can be imported."""
        try:
            importlib.import_module(package_name)
        except ImportError:
            pytest.fail(
                f"Required dependency '{package_name}' is not installed. "
                f"Please add it to pyproject.toml dependencies."
            )
