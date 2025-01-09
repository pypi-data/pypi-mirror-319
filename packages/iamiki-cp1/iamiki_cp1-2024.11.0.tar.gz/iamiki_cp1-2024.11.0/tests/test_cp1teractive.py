# tests/test_cp1teractive.py

import pytest

@pytest.mark.interactive
def test_plot_function():
    try:
        from cp1.interactive.cp1teractive import cp_ductplot
        #cp_ductplot
    except ImportError:
        pytest.skip("The 'plot' module is not installed.")