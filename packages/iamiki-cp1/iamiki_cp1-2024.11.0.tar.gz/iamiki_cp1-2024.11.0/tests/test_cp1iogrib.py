# tests/test_cp1iogrib.py

import pytest

@pytest.mark.grib
def test_grib_function():
    try:
        from cp1.io.cp1iogrib import cp_w0
        cp_w0([50, 52, -5, -4], 51, 355)
    except ImportError:
        pytest.skip("The 'grib' module is not installed.")