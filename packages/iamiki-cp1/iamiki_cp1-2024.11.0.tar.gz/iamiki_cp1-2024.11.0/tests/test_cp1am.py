# tests/test_cp1am.py

import pytest
from cp1.core import get_versions

def test_get_versions():
    versions = get_versions()
    assert "cp1_version" in versions
    assert versions["cp1_version"] is not None