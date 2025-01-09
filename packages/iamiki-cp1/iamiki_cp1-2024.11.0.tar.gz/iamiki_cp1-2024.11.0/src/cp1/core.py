# src/cp1/core.py

def use_grib():
    is_installed = False
    try:
        from cp1.io.cp1iogrib import cp_gribdata
        from cp1.io.cp1iogrib import __version__ as grib_version
        #grib_function()
        is_installed = True
    except ImportError:
        print("The 'grib' module is not installed. Please install cp1 with the [grib] option.")
        grib_version = None
    return is_installed, grib_version

def use_plot():
    is_installed = False
    try:
        from cp1.interactive.cp1teractive import cp_ductplot
        from cp1.interactive.cp1teractive import __version__ as plot_version
        #plot_function()
        is_installed = True
    except ImportError:
        print("The 'plot' module is not installed. Please install cp1 with the [interactive] option.")
        plot_version = None
    return is_installed, plot_version

def get_versions():
    from cp1 import __version__ as core_version
    grib_installed, grib_version = use_grib()
    plot_installed, plot_version = use_plot()
    
    versions = {
        "cp1_version": core_version,
        "cp_grib_installed": grib_installed,
        "io_grib_version": grib_version,
        "cp_plot_installed": plot_installed,
        "ia_plot_version": plot_version,
    }
    return versions

if __name__ == "__main__":
    versions = get_versions()
    print(versions)