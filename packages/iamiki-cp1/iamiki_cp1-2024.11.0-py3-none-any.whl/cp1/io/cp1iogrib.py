
"""
Module cp1iogrib

This module provides functionalities for handling GRIB files.

Functions:
    function_name(args): Description of the function.
"""

__version__ = "2024.11.0"

# required 'eccodes' package
# !pip install eccodes
# nice alernatives may be : {'xarray': '2024.5.0', 'cfgrib': '0.9.14.1', 'eccodes': '2.38.3'}

# Import the necessary libraries
import cfgrib
import eccodes
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta, datetime
import warnings
from ..cp1am import cp_bool2pos2ind #, cp_profileval, cp_profilz

# Define the date format
DATE_FORMAT = '%Y-%m-%d %H:%M' # Default Date format ; to be added to CPC

# List all functions in the eccodes package
# eccodes_functions = [func for func in dir(eccodes) if callable(getattr(eccodes, func))]

# qgrib = "Import/grib/ARPEGE_GLOB025_20231231180000_ech0a5_T_HU_2m.grb"

# Compile the DataFrame
# grib_files_df = compile_grib_files("Import/grib")
# Example usage of gribfilepath function
# fullpathname = gribfilepath("MODELE", "RESOLUTION", "YYYYMMDD", "HH", "HAUTEUR")

# Main 
def cp_extract_grib_data(dateheure, mask_vector, short_varnames=["sp", "2t", "r", "10u", "10v", "t"], dataset="Import/grib", step_num=0, cp1_as_pd=False):
    """
    Extracts data from GRIB files and compiles it into a numpy array or pandas DataFrame.

    Parameters
    ----------
    dateheure : str
        The date and time string to match GRIB files (e.g., "2023123118").
    mask_vector : numpy.ndarray
        A boolean vector indicating the mask to apply on the data like a geo or landsea mask
        May be produced by cp1iogrib.cp_lsmmodel
    short_varnames : list of str, optional
        List of variable short names to extract (default is ["sp", "2t", "r", "10u", "10v", "t"]).
    dataset : str, optional
        Path to the directory containing GRIB files (default is "Import/grib").
    step_num : int, optional
        The step number to select from the GRIB files (default is 0).
    cp1_as_pd : bool, optional
        If True, returns the data as a pandas DataFrame instead of a numpy array (default is False).

    Returns
    -------
    maskeddataarrays : dict
        A dictionary containing the extracted data and metadata:
        - "metdata": numpy.ndarray or pandas.DataFrame, the extracted data.
        - "met_model": str, the meteorological model used.
        - "valid_time": datetime, the valid time of the data.
        - "mask_vector": numpy.ndarray, the mask vector used.
        - "grib_files": list of str, the list of GRIB files processed.
        - "column_names": list of str, the names of the columns in the data.
        - "GRIB_typeOfLevel": str, the type of level in the GRIB files.
        - "height_above_ground_values": list of float, the height above ground values.
        - "units": list of str, the units of the variables.

    Example
    -------
    >>> dateheure = "2023123118"
    >>> short_varnames = ["sp", "2t", "r", "10u", "10v", "t"]
    >>> dataset = "Import/grib"
    >>> step_num = 0
    >>> cp1_as_pd = False
    >>> maskeddataarrays = cp_extract_grib_data(dateheure, mask_vector, short_varnames, dataset, step_num, cp1_as_pd)
    """
    # Define the path to the GRIB files
    grib_path = os.path.join(dataset)

    # List all GRIB files matching the pattern
    grib_files = [os.path.join(grib_path, f) for f in os.listdir(grib_path) if dateheure in f and f.endswith(".grb")]

    # Initialize the arrays with the mask_vector where mask_vector is True
    arrays = mask_vector[mask_vector][:, np.newaxis]

    # Initialize a list to keep track of column names
    column_names = ["mask_vector"]

    # Initialize a list to keep track of heightAboveGround values
    typeOfLevel = []

    # Initialize a list to keep track of heightAboveGround flags
    height_above_ground = []

    # Initialize a list to keep track of units
    units = []

    # Iterate over each GRIB file
    for grib_file in grib_files:
        # Open the GRIB file using cfgrib
        ds_list = cfgrib.open_datasets(grib_file)
        
        # Iterate over each dataset in the list
        for ds in ds_list:
            # Check if the dataset has dimensions (step, latitude, longitude)
            valid_time = ds.valid_time.values[step_num]
            if set(ds.dims) == {"step", "latitude", "longitude"}:
                # Select the specified step
                selected_step = ds.step.values[step_num]
                ds_selected_step = ds.sel(step=selected_step)
                
                # Iterate over each variable in the dataset
                for var in ds_selected_step.data_vars:
                    # Check if the variable's short name is in the list to keep
                    if ds_selected_step[var].attrs.get("GRIB_shortName") in short_varnames:
                        # Convert the variable to a numpy array and flatten it row-first
                        array = ds_selected_step[var].values.flatten(order='C')
                        # Keep only the values where mask_vector is True
                        array = array[mask_vector]
                        # Append the new array as a new column
                        arrays = np.column_stack((arrays, array))
                        # Append the variable name to the column names list
                        column_names.append(ds_selected_step[var].attrs.get("GRIB_shortName"))
                        # Get the heightAboveGround value
                        typeOfLevel = ds_selected_step[var].attrs.get("GRIB_typeOfLevel", "N/A")
                        # Append the heightAboveGround value to the list
                        height_above_ground.append(0. if typeOfLevel == "surface" else ds.variables['heightAboveGround'].data)
                        # Get the unit of the variable
                        unit = ds_selected_step[var].attrs.get("GRIB_units", "N/A")
                        # Append the unit to the units list
                        units.append(unit)

    # Create the maskeddataarrays object
    maskeddataarrays = {
        "met_model": "ARPEGE_GLOB025",
        "valid_time": valid_time,
        "mask_vector": mask_vector,
        "grib_files": grib_files,
        "column_names": column_names,
        "GRIB_typeOfLevel": typeOfLevel,
        "height_above_ground": height_above_ground,
        "units": units,
        "metdata": arrays
    }

    # If cp1_as_pd is True, convert arrays to a pandas DataFrame
    if cp1_as_pd:
        indices = np.where(mask_vector)[0]
        df = pd.DataFrame(arrays, index=indices, columns=column_names)
        # Calculate the v2 wind speed
        if "10u" in df.columns and "10v" in df.columns:
            df["v2"] = np.sqrt(df["10u"]**2 + df["10v"]**2)
        
        # Convert 2t and t from Kelvin to Celsius
        if "2t" in df.columns:
            df["2t"] = df["2t"] - 273.15
        if "t" in df.columns:
            df["t"] = df["t"] - 273.15
        
        # Convert sp from Pascal to hectoPascal
        if "sp" in df.columns:
            df["sp"] = df["sp"] / 100.0
        
        # Rename columns
        df.rename(columns={"sp": "pzp", "2t": "tc1", "r": "h1", "t": "tc0"}, inplace=True)
        
        # Drop 10u and 10v columns
        df.drop(columns=["10u", "10v"], inplace=True)
        
        maskeddataarrays["metdata"] = df

    # Return the maskeddataarrays object
    return maskeddataarrays


# simple census : dataset/.../*.grb recense
# useful since GRIB does not define official file extension
def cp_infodataset(racine, pattern="*.grb"):
    """
    cp_infodataset

    :param args: Description of the parameters
    :type args: type of the parameters
    :return: Description of the return value
    :rtype: type of the return value
    """
    """
    cp_infodataset

    :param args: Description of the parameters
    :type args: type of the parameters
    :return: Description of the return value
    :rtype: type of the return value
    """
    """
    Lists files in a directory and its subdirectories matching a given pattern.
    (useful since GRIB has no official file extension)

    Parameters
    ----------
    racine : str
        The path of the root directory to explore.
    pattern : str, optional
        The file pattern to search for (default is "*.grb").

    Returns
    -------
    pd.DataFrame
        A DataFrame containing information about the found files, with columns:
        - "dossier": the path of the directory containing the file
        - "filename": the name of the file
        - "filesize": the size of the file in bytes

    **Use Case:**

    .. code-block:: python

      dataset = "Import/grib"
      grib_files_df = cp_infodataset(dataset, "*.grb")
    """
    # List to store file information
    file_info = []

    # Walk through the directory
    for root, dirs, files in os.walk(racine):
        for file in files:
            if file.endswith(pattern.split("*")[-1]):
                file_path = os.path.join(root, file)
                file_info.append(
                    {
                        "dossier": root,
                        "filename": file,
                        "filesize": os.path.getsize(file_path),
                    }
                )

    # Create a DataFrame
    return pd.DataFrame(file_info)


# Function to compile a pandas DataFrame of GRIB files
def compile_grib_files(directory):
    """
    compile_grib_files

    :param args: Description of the parameters
    :type args: type of the parameters
    :return: Description of the return value
    :rtype: type of the return value
    """
    """
    compile_grib_files

    :param args: Description of the parameters
    :type args: type of the parameters
    :return: Description of the return value
    :rtype: type of the return value
    """
    data = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".grb"):
                parts = file.split("_")
                if len(parts) >= 6:
                    modele = parts[0]
                    resolution = parts[1]
                    datetime_str = parts[2]
                    echeance = parts[3]
                    params = "_".join(parts[4:-1])
                    hauteur = parts[-1].split(".")[0]
                    filesize = os.path.getsize(os.path.join(root, file))
                    data.append(
                        {
                            "dossier": root,
                            "filename": file,
                            "MODELE": modele,
                            "RESOLUTION": resolution,
                            "YYYYMMDDHH": datetime_str[:10],
                            "ECHEANCE": echeance,
                            "PARAMS": params,
                            "HAUTEUR": hauteur,
                            "filesize": filesize,
                        }
                    )
    return pd.DataFrame(data)


def qgribdate(grib_files_df, dateheure, echeance="ech0a5"):
    """
    qgribdate

    :param args: Description of the parameters
    :type args: type of the parameters
    :return: Description of the return value
    :rtype: type of the return value
    """
    """
    qgribdate

    :param args: Description of the parameters
    :type args: type of the parameters
    :return: Description of the return value
    :rtype: type of the return value
    """
    """
    Renvoie les fullpath des fichiers grib qui correspondent à une dateheure et à une échéance données.

    :param dateheure: La date et l'heure au format 'YYYYMMDDHH'
    :param echeance: L'échéance au format 'echXaY'
    :return: Liste des fullpath des fichiers correspondants

    **Use Case:**

    .. code-block:: python

      qgribdate("2023123118", "ech0a5")
    """
    # Filtrer le DataFrame pour les lignes correspondant à la dateheure et à l'échéance données
    filtered_df = grib_files_df[
        (grib_files_df["YYYYMMDDHH"] == dateheure)
        & (grib_files_df["ECHEANCE"] == echeance)
    ]

    # Construire les fullpath
    fullpaths = filtered_df.apply(
        lambda row: f"{row['dossier']}/{row['filename']}", axis=1
    ).tolist()

    return fullpaths


# Function to get the full pathname of a GRIB file
def gribfilepath(modele, resolution, date, heure, hauteur):
    """
    gribfilepath

    :param args: Description of the parameters
    :type args: type of the parameters
    :return: Description of the return value
    :rtype: type of the return value
    """
    """
    gribfilepath

    :param args: Description of the parameters
    :type args: type of the parameters
    :return: Description of the return value
    :rtype: type of the return value
    """
    """
    gribfilepath - look for a specific grib within an subfolder

    :param args: Description of the parameters
    :type args: type of the parameters
    :return: Description of the return value
    :rtype: type of the return value
    """
    datetime_str = date + heure
    for root, dirs, files in os.walk("Import/grib"):
        for file in files:
            if file.startswith(
                f"{modele}_{resolution}_{datetime_str}"
            ) and file.endswith(f"{hauteur}.grb"):
                return os.path.join(root, file)
    return None


# recense les paramètres météo contenu dans qgrib = "Import/grib/ARPEGE_GLOB025_20231231180000_ech0a5_T_HU_2m.grb"
# Example usage
# qgrib = 'Import/grib/ARPEGE_GLOB025_20231231180000_ech0a5_T_HU_2m.grb'
# parameters, grib_data, latitudes, longitudes = cp_gribdata(qgrib)
def cp_gribdata(qgrib):
    """
    cp_gribdata

    :param args: Description of the parameters
    :type args: type of the parameters
    :return: Description of the return value
    :rtype: type of the return value
    """
    """
    cp_gribdata

    :param args: Description of the parameters
    :type args: type of the parameters
    :return: Description of the return value
    :rtype: type of the return value
    """
    # Open the GRIB file
    with open(qgrib, "rb") as f:
        parameters = []
        grib_data = {}
        latitudes = []
        longitudes = []
        while True:
            gid = eccodes.codes_grib_new_from_file(f)
            if gid is None:
                break
            param = eccodes.codes_get(gid, "shortName")
            if param not in parameters:
                parameters.append(param)
                grib_data[param] = {
                    "name": eccodes.codes_get(gid, "name"),
                    "units": eccodes.codes_get(gid, "units"),
                    "dataDate": eccodes.codes_get(gid, "dataDate"),
                    "dataTime": eccodes.codes_get(gid, "dataTime"),
                    "stepRange": eccodes.codes_get(gid, "stepRange"),
                    "values": eccodes.codes_get_values(gid),
                }
            if len(latitudes) == 0 and len(longitudes) == 0:
                latitudes = eccodes.codes_get_array(gid, "distinctLatitudes")
                longitudes = eccodes.codes_get_array(gid, "distinctLongitudes")
            eccodes.codes_release(gid)

    return parameters, grib_data, latitudes, longitudes


def cp_gribinfo(gribfullpath):
    """
    cp_gribinfo

    :param args: Description of the parameters
    :type args: type of the parameters
    :return: Description of the return value
    :rtype: type of the return value
    """
    """
    Extracts detailed information about meteorological parameters from a GRIB file.

    Parameters
    ----------
    gribfullpath : str
        The full path to the GRIB file.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame containing detailed information about each parameter in the GRIB file.
        The DataFrame includes the following columns:
        - file_path: str, the full path to the GRIB file
        - param_name: str, the short name of the parameter
        - bits_per_value: int, the number of bits per value
        - units: str, the units of the parameter
        - min_val: float, the minimum value of the parameter
        - max_val: float, the maximum value of the parameter
        - data_date: int, the date of the data
        - data_time: int, the time of the data
        - step_range: str, the step range of the data
        - grid_type: str, the type of grid
        - level_type: str, the type of level
        - level: int, the level of the data
        - number_of_points: int, the number of data points
        - packing_type: str, the packing type
        - missing_value: int, the missing value indicator
        - decimal_scale_factor: int, the decimal scale factor
        - binary_scale_factor: int, the binary scale factor
        - reference_value: float, the reference value
        - latitude_of_first_grid_point: int, the latitude of the first grid point
        - longitude_of_first_grid_point: int, the longitude of the first grid point
        - latitude_of_last_grid_point: int, the latitude of the last grid point
        - longitude_of_last_grid_point: int, the longitude of the last grid point
        - j_direction_increment: int, the increment in the j direction
        - i_direction_increment: int, the increment in the i direction
    """
    # Liste pour stocker les informations des paramètres
    # Exemple d'utilisation : params_df = cp_gribinfo(qgrib)
    params_info = []

    # Ouvrir le fichier GRIB
    with open(gribfullpath, "rb") as f:
        while True:
            gid = eccodes.codes_grib_new_from_file(f)
            if gid is None:
                break

            # Récupérer les informations du paramètre
            param_info = {}
            param_info["file_path"] = gribfullpath
            param_info["param_name"] = eccodes.codes_get(gid, "shortName")
            param_info["bits_per_value"] = eccodes.codes_get(gid, "bitsPerValue")
            param_info["units"] = eccodes.codes_get(gid, "units")
            param_info["min_val"] = eccodes.codes_get(gid, "min")
            param_info["max_val"] = eccodes.codes_get(gid, "max")
            param_info["data_date"] = eccodes.codes_get(gid, "dataDate")
            param_info["data_time"] = eccodes.codes_get(gid, "dataTime")
            param_info["step_range"] = eccodes.codes_get(gid, "stepRange")
            param_info["grid_type"] = eccodes.codes_get(gid, "gridType")
            param_info["level_type"] = eccodes.codes_get(gid, "typeOfLevel")
            param_info["level"] = eccodes.codes_get(gid, "level")
            param_info["number_of_points"] = eccodes.codes_get(
                gid, "numberOfDataPoints"
            )
            param_info["packing_type"] = eccodes.codes_get(gid, "packingType")
            param_info["missing_value"] = eccodes.codes_get(gid, "missingValue")
            param_info["decimal_scale_factor"] = eccodes.codes_get(
                gid, "decimalScaleFactor"
            )
            param_info["binary_scale_factor"] = eccodes.codes_get(
                gid, "binaryScaleFactor"
            )
            param_info["reference_value"] = eccodes.codes_get(gid, "referenceValue")
            param_info["packingError"] = eccodes.codes_get(gid, 'packingError')
            param_info["decimalPrecision"] =  eccodes.codes_get(gid, 'decimalPrecision')
            param_info["latitude_of_first_grid_point"] = eccodes.codes_get(
                gid, "latitudeOfFirstGridPoint"
            )
            param_info["longitude_of_first_grid_point"] = eccodes.codes_get(
                gid, "longitudeOfFirstGridPoint"
            )
            param_info["latitude_of_last_grid_point"] = eccodes.codes_get(
                gid, "latitudeOfLastGridPoint"
            )
            param_info["longitude_of_last_grid_point"] = eccodes.codes_get(
                gid, "longitudeOfLastGridPoint"
            )
            param_info["j_direction_increment"] = eccodes.codes_get(
                gid, "jDirectionIncrement"
            )
            param_info["i_direction_increment"] = eccodes.codes_get(
                gid, "iDirectionIncrement"
            )

            # Ajouter les informations à la liste
            params_info.append(param_info)

            # Libérer la mémoire pour ce message GRIB
            eccodes.codes_release(gid)

    # Convertir la liste en DataFrame pandas
    params_df = pd.DataFrame(params_info)
    return params_df


############################### Specific to ERA5 Reanalyses
# extracted from https://www.ecmwf.int/en/forecasts/datasets
# and https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=download
# with or without [import cdsapi] usage
# Helper function to get the short name
def cp_era5_get_short_name(var):
    """
    Retrieve the short name of a variable from its attributes.

    Parameters:
    var (xarray.DataArray): The variable from which to extract the short name.

    Returns:
    str: The short name of the variable. If 'short_name' does not exist, 
         it will try 'GRIB_shortName' or 'GRIB_cfVarName'. If none of these 
         exist, it returns 'unknown'.
    """
    return var.attrs.get('short_name', var.attrs.get('GRIB_shortName', var.attrs.get('GRIB_cfVarName', 'unknown')))


# Function to get the time index from a date string
def cp_era5_get_time_index(ds, date_str, formatstr=DATE_FORMAT):
    """
    Get the closest time index in the dataset for a given date string.

    Parameters:
    ds (xarray.Dataset): The dataset containing the time variable.
    date_str (str): The date string to find the closest time index for.
    formatstr (str): The format of the date string (default is '%Y-%m-%d %H:%M').

    Returns:
    int: The index of the closest time in the dataset.
    numpy.timedelta64: The difference between the closest time in the dataset and the given date.
    """
    date_time = pd.to_datetime(date_str, format=formatstr).to_numpy()
    time_diff = (ds.time.values - date_time)
    closest_index = np.abs(time_diff).argmin()
    time_diff = ds.time.values[closest_index] - date_time
    return closest_index, time_diff


def cp_era5_bboxnranges(ds):
    """
    Calculate the bounding box and ranges for time, step, and valid_time from an ERA5 dataset.

    Parameters:
    ds (xarray.Dataset): The dataset from which to calculate the bounding box and ranges.

    Returns:
    tuple: A tuple containing:
        - bbox (tuple): The bounding box as (lat_min, lat_max, lon_min, lon_max).
        - time_range (tuple or None): The range of time as (min_time, max_time) or None if 'time' does not exist.
        - step_range_h (tuple or None): The range of step in hours as (min_step, max_step) or None if 'step' does not exist.
        - valid_time_range (tuple or None): The range of valid_time as (min_valid_time, max_valid_time) or None if 'valid_time' does not exist.
    """
    # Calculate the bounding box (bbox)
    lat_min = ds.latitude.values.min()
    lat_max = ds.latitude.values.max()
    lon_min = ds.longitude.values.min()
    lon_max = ds.longitude.values.max()
    bbox = (lat_min, lat_max, lon_min, lon_max)

    # Calculate the ranges for time, step, and valid_time if they exist
    time_range = (ds.time.values.min(), ds.time.values.max()) if 'time' in ds else None
    valid_time_range = (ds.valid_time.values.min(), ds.valid_time.values.max()) if 'valid_time' in ds else None
    # Convert step_range to hours
    h = np.timedelta64(1, 'h') # into_hours
    step_range_h = (ds.step.values.min()/h, ds.step.values.max()/h) if 'step' in ds else None

    return bbox, time_range, step_range_h, valid_time_range


def cp_era5_plot_monovariable(variable, time_index, formatted_time):
    """
    Plots a given variable at a specified time index with a formatted time in the title.

    Parameters:
    - variable: xarray.DataArray, the variable to plot
    - time_index: int, the time index to plot
    - formatted_time: str, the formatted time string for the title
    """
    plt.contourf(variable.longitude, variable.latitude, variable.isel(time=time_index), cmap='viridis')
    plt.colorbar(label=f"{variable.units}")
    plt.title(f"{cp_era5_get_short_name(variable)} [{variable.attrs['units']}] {variable.attrs['long_name']}\nValid Time: {formatted_time}")
    plt.gca().set_aspect('equal', adjustable='box')  # Set the aspect ratio to be square
    
    return


def cp_era5_plot_variables(ds, time_input, var_str=None, num_cols=2):
    """
    Plots specified variables from the dataset at a given time index or date string.

    Parameters:
    - ds: xarray.Dataset, the dataset containing the variables
    - time_input: int or str, the time index or date string to plot
    - var_str: list of str, the list of variable names to plot (default is all data variables with dimensions time, latitude, and longitude)
    - num_cols: int, the number of columns in the plot grid (default is 2)
    """
    # Example usage:
    # cp_era5_plot_variables(ds, 23)
    # cp_era5_plot_variables(ds, '2023-12-01 12:00', ('u10', 'v10'))
    # cp_era5_plot_variables(ds, '2023-12-01 12:00', num_cols=2))
    
    # Determine the time index
    if isinstance(time_input, str):
        time_index, time_diff = cp_era5_get_time_index(ds, time_input)
        # Check if time_diff is greater than 1/2 hour
        if np.abs(time_diff) > np.timedelta64(30, 'm'):
            warnings.warn(f"The time difference is greater than 1/2 hour: {time_diff}")
    else:
        time_index = time_input

    time = ds.time.values[time_index]
    # Convert time to desired format
    formatted_time = pd.to_datetime(time).strftime(DATE_FORMAT)

    # Determine the variables to plot
    if var_str is None:
        var_str = [var for var in ds.data_vars if set(ds[var].dims) == {'time', 'latitude', 'longitude'}]

    # Get latitude and longitude ranges
    lat_range = ds.latitude.values.max() - ds.latitude.values.min()
    lon_range = ds.longitude.values.max() - ds.longitude.values.min()

    # Plot the variables
    num_vars = len(var_str)
    num_rows = (num_vars + num_cols - 1) // num_cols

    plt.figure(figsize=(12 * lon_range / lat_range, 6 * num_rows))
    for idx, var_name in enumerate(var_str):
        plt.subplot(num_rows, num_cols, idx + 1)
        cp_era5_plot_monovariable(ds[var_name], time_index, formatted_time)

    plt.tight_layout()
    plt.show()
    
    return


############################### Calculation MASKS AND WINDOWS
############################### MASKS AND WINDOWS based upon LandSeaMask.grib2
def cp_lsmmodel(fullname, lsm_str="lsm", height_str="h", method_str=None, saveas_npz=None):
    """
    Create a land-sea mask model from a GRIB file.

    Parameters
    ----------
    fullname : str
        Full path of the GRIB file to read.
    lsm_str : str, optional
        Name of the land-sea mask variable in the GRIB file (default is "lsm").
    height_str : str, optional
        Name of the height variable in the GRIB file (default is "h").
    method_str : str, optional
        Method to apply to the land-sea mask (default is None).
    saveas_npz : str, optional
        Filename to save the output variables as a .npz file (default is None).

    Returns
    -------
    lsmmodel : dict
        Dictionary containing the land-sea mask model with keys 'latitudes', 'longitudes', 'height', and 'lsm'.
    latitudes : array
        Array of latitudes.
    longitudes : array
        Array of longitudes.
    lsm : array
        Boolean array of the land-sea mask.
    height : array
        Float32 array of the height.
    """
    # Check if the file exists
    if not os.path.isfile(fullname):
        raise FileNotFoundError(f"The file {fullname} does not exist.")
    
    # Initialize variables
    latitudes, longitudes, lsm, height = None, None, None, None
    
    # Check if the file is a .npz file
    if fullname.endswith('.npz'):
        try:
            data = np.load(fullname)
            latitudes = data['latitudes']
            longitudes = data['longitudes']
            lsm = data['lsm']
            height = data['height']
        except KeyError as e:
            raise KeyError(f"Missing variable in .npz file: {e}")
        except Exception as e:
            raise IOError(f"Error accessing .npz file: {e}")
    else:
        # Indicate the version of GRIB with eccodes # @IAM: check for readeability
        with open(fullname, 'rb') as f:
            gid = eccodes.codes_grib_new_from_file(f)
            if gid is None:
                raise ValueError("Unable to read GRIB file with eccodes.")
            grib_edition = eccodes.codes_get(gid, 'edition')
            eccodes.codes_release(gid)
        print(f"GRIB edition: {grib_edition}")
        
        # Extract necessary variables
        parameters, masktm, latitudes, longitudes = cp_gribdata(fullname)
        
        # Check if parameters contain lsm_str and height_str
        if lsm_str not in parameters or height_str not in parameters:
            raise ValueError(f"Parameters must contain {lsm_str} and {height_str}")
        
        lsm = masktm[lsm_str]['values']
        height = masktm[height_str]['values']
            
        # Apply method if specified
        if method_str == "cp1_arp025":
            # Apply some specific method to lsm
            lsm = some_method(lsm) # @IAM: TobeDone
        
        # Reshape lsm as a boolean array with dimensions of latitudes and longitudes
        lsm = np.reshape(lsm, (len(latitudes), len(longitudes)), order='C').astype(bool)
        
        # Reshape height as a float32 array with dimensions of latitudes and longitudes
        height = np.reshape(height, (len(latitudes), len(longitudes)), order='C').astype(np.float32)
    
    # Create the lsmmodel dictionary
    lsmmodel = {
        'latitudes': latitudes,
        'longitudes': longitudes,
        'height': height,
        'lsm': lsm
    }
    
    # Save the variables to a .npz file if saveas_npz is not None
    if saveas_npz is not None:
        np.savez(saveas_npz, latitudes=latitudes, longitudes=longitudes, lsm=lsm, height=height, allow_pickle=False)
        print(f"save as {os.path.abspath(saveas_npz)}")
    
    return lsmmodel, latitudes, longitudes, lsm, height


def cp_w0(w0, qlat, qlon):
    lat_min, lat_max, lon_min, lon_max = w0
    
    # Find the indices for the latitude range
    ilat = np.where((qlat >= lat_min) & (qlat <= lat_max))[0]
    
    # Find the indices for the longitude range considering the modulo condition
    ilon = np.where(((qlon >= lon_min) & (qlon <= lon_max)) | 
                    ((qlon >= (lon_min + 360)) & (qlon <= (lon_max + 360))))[0]
    
    return ilat, ilon


def cp_windows(lsmmodel, w):
    """
    Generate a boolean mask for a given latitude and longitude window.

    Parameters
    ----------
    lsmmodel : dict
        A dictionary containing 'latitudes' and 'longitudes' as keys with corresponding arrays.
    w : tuple
        A tuple containing (lat_min, lat_max, lon_min, lon_max) which defines the window.
        Note: lon_min and lon_max can be expressed in the range -180 to 360 even if lsmmodel
        references longitudes between 0 and 360.

    Returns
    -------
    mask : numpy.ndarray
        A 2D boolean numpy array where True indicates the points within the specified window.
    """
    lat_min, lat_max, lon_min, lon_max = w
    qlat = lsmmodel['latitudes']
    qlon = lsmmodel['longitudes']
    
    # Create a boolean mask for the latitude range
    lat_mask = (qlat >= lat_min) & (qlat <= lat_max)
    
    # Create a boolean mask for the longitude range considering the modulo condition
    lon_mask = ((qlon >= lon_min) & (qlon <= lon_max)) | ((qlon >= (lon_min + 360)) & (qlon <= (lon_max + 360)))
    
    # Combine the latitude and longitude masks
    mask = np.outer(lat_mask, lon_mask)
    
    return mask


def cp_maskunique(lsmmodel):
    """
    Generate a unique mask for the land-sea model grid.

    This function returns a boolean mask with the same dimensions as `lsmmodel['lsm']`.
    The mask is set to False for redundant grid points, specifically:
    - At the poles (latitudes -90 or 90), all points are set to False except the first point.
    - For longitudes, if the last longitude is equivalent to the first longitude modulo 360,
      the entire last column is set to False.

    Parameters
    ----------
    lsmmodel : dict
        A dictionary containing the land-sea model data with keys:
        - 'lsm': 2D array of land-sea mask values.
        - 'latitudes': 1D array of latitude values.
        - 'longitudes': 1D array of longitude values.

    Returns
    -------
    mask : 2D numpy array of bool
        A boolean mask with the same shape as `lsmmodel['lsm']`, where redundant points are False.

    Example
    -------
    >>> maskuniq = cp_maskunique(lsmmodel)
    """
    lsm = lsmmodel['lsm']
    latitudes = lsmmodel['latitudes']
    longitudes = lsmmodel['longitudes']
    
    mask = np.ones(lsm.shape, dtype=bool)
    
    # Handle latitudes at -90 or 90
    for lat in [-90, 90]:
        if lat in latitudes:
            lat_index = np.where(latitudes == lat)[0][0]
            mask[lat_index, :] = False
            mask[lat_index, 0] = True  # Keep only the first point as True
    
    # Handle longitudes with modulo
    longitudes_mod = np.mod(longitudes, 360)
    if longitudes_mod[-1] == longitudes_mod[0]:
        mask[:, -1] = False
    
    # Calculate the sum of the mask
    true_count = np.sum(mask)
    false_count = mask.size - true_count
    #print(f"Results: True: {true_count}, False: {false_count}, Over {mask.size}")
    
    return mask


def cp_maskstyle(lsmmodel, mask):
    """
    Convert a boolean mask into three different forms: a 2D numpy array, a 1D boolean vector, 
    and a 1D numpy array of indices where the mask is True.

    Parameters
    ----------
    lsmmodel : dict
        A dictionary containing 'latitudes' and 'longitudes' keys with corresponding lists.
    mask : numpy.ndarray or list
        A boolean mask which can be in one of the following forms:
        - 2D numpy array of dimensions (nblat, nblon)
        - 1D boolean numpy array of length nblat * nblon
        - 1D numpy array of indices where the mask is True

    Returns
    -------
    mask_matrix : numpy.ndarray
        A 2D numpy array of dimensions (nblat, nblon) where nblat = len(lsmmodel['latitudes']) 
        and nblon = len(lsmmodel['longitudes']).
    mask_vector : numpy.ndarray
        A 1D boolean numpy array of length nblat * nblon.
    mask_indices : numpy.ndarray
        A 1D numpy array of indices where the mask is True.
    """
    nblat = len(lsmmodel['latitudes'])
    nblon = len(lsmmodel['longitudes'])
    
    if isinstance(mask, np.ndarray):
        if mask.ndim == 2:
            # Mask is already a 2D array
            assert mask.shape == (nblat, nblon), "Mask dimensions do not match the model dimensions"
            mask_matrix = mask
            mask_vector = mask.flatten(order='C')
        elif mask.ndim == 1:
            if mask.dtype == bool:
                # Mask is a 1D boolean vector
                assert mask.size == nblat * nblon, "Mask length does not match the model dimensions"
                mask_vector = mask
                mask_matrix = mask.reshape((nblat, nblon), order='C')
            else:
                # Mask is a 1D array of indices
                mask_indices = mask
                mask_vector = np.zeros(nblat * nblon, dtype=bool)
                mask_vector[mask_indices] = True
                mask_matrix = mask_vector.reshape((nblat, nblon), order='C')
        else:
            raise ValueError("Invalid mask dimensions")
    elif isinstance(mask, list):
        # Mask is a list of indices
        mask_indices = np.array(mask)
        mask_vector = np.zeros(nblat * nblon, dtype=bool)
        mask_vector[mask_indices] = True
        mask_matrix = mask_vector.reshape((nblat, nblon), order='C')
    else:
        raise TypeError("Mask must be a numpy array or a list of indices")
    
    # Get indices where mask is True
    mask_indices = np.where(mask_vector)[0]
    
    return mask_matrix, mask_vector, mask_indices


def cp_mask_or(lsmmodel, *masks):
    # Apply cp_maskstyle to each mask to ensure they are in a homogeneous form
    styled_masks = [cp_maskstyle(lsmmodel, mask)[0] for mask in masks]
    # Perform logical OR operation across all masks
    result_mask = np.logical_or.reduce(styled_masks)
    return result_mask

def cp_mask_and(lsmmodel, *masks):
    # Apply cp_maskstyle to each mask to ensure they are in a homogeneous form
    styled_masks = [cp_maskstyle(lsmmodel, mask)[0] for mask in masks]
    # Perform logical AND operation across all masks
    result_mask = np.logical_and.reduce(styled_masks)
    return result_mask

def cp_mask_xor(lsmmodel, *masks):
    # Apply cp_maskstyle to each mask to ensure they are in a homogeneous form
    styled_masks = [cp_maskstyle(lsmmodel, mask)[0] for mask in masks]
    # Perform logical XOR operation across all masks
    result_mask = np.logical_xor.reduce(styled_masks)
    return result_mask

def cp_maskinfo(lsmmodel, mask):
    # Ensure the mask is a boolean ndarray
    mask, _, _ = cp_maskstyle(lsmmodel, mask)
    
    # Count true and false values in the mask
    true_count = np.sum(mask)
    false_count = mask.size - true_count
    
    # Find the amplitude of true points in the mask
    true_indices = np.argwhere(mask)
    lat_min = lsmmodel['latitudes'][true_indices[:, 0].min()]
    lat_max = lsmmodel['latitudes'][true_indices[:, 0].max()]
    lon_min = lsmmodel['longitudes'][true_indices[:, 1].min()]
    lon_max = lsmmodel['longitudes'][true_indices[:, 1].max()]
    
    # Prepare the result strings
    result_line1 = f"Results: True: {true_count}, False: {false_count}, Over {mask.size}"
    result_line2 = f"Amplitude w = [lat_min: {lat_min}, lat_max: {lat_max}, lon_min: {lon_min}, lon_max: {lon_max}]"
    
    return [true_count, false_count], [lat_min, lat_max, lon_min, lon_max]

def cp_maskindlatlon(lsmmodel, maskindlatlon):
    """
    Extract indices and coordinates of True values in a mask.

    Parameters
    ----------
    lsmmodel : dict
    maskindlatlon : array_like
    
    Returns
    -------
    mi : ndarray
        A 1D array of indices where the mask is True, using 'row first' convention.
    coords : ndarray
        A 2D array where the first row contains the latitudes and the second row contains
        the longitudes of the True points in the mask.

    Notes
    -----
    The indices returned by cp_maskstyle use the 'row first' convention and are relative
    to a numpy array with dimensions nblat = len(lsmmodel['latitudes']) and 
    nblon = len(lsmmodel['longitudes']).
    """
    # Use cp_maskstyle to get the indices of True values in the mask
    _, _, mi = cp_maskstyle(lsmmodel, maskindlatlon)
    
    # Get the latitudes and longitudes from the model
    latitudes = lsmmodel['latitudes']
    longitudes = lsmmodel['longitudes']
    
    # Convert 'row first' indices to 2D indices
    nblat = len(latitudes)
    nblon = len(longitudes)
    rows, cols = np.unravel_index(mi, (nblat, nblon), order='C') # defaut order but...
    
    # Get the coordinates of the True points in the mask
    lat_coords = latitudes[rows]
    lon_coords = longitudes[cols]
    
    # Combine the coordinates into a single array
    coords = np.vstack((lat_coords, lon_coords))
    
    return mi, coords


def cp_maskundersample(lsmmodel, n, m=None, i=1, j=1):
    """
    Create a mask that undersamples the latitude and longitude grid of the lsmmodel.

    Parameters
    ----------
    lsmmodel : dict
        A dictionary containing 'latitudes' and 'longitudes' keys with corresponding arrays.
    n : int
        The undersampling factor for latitude.
    m : int, optional
        The undersampling factor for longitude. If None, it defaults to the value of `n`.
    i : int, optional
        The starting index for latitude undersampling (0 <= i < n). Default is 1.
    j : int, optional
        The starting index for longitude undersampling (0 <= j < m). Default is 1.

    Returns
    -------
    mask : ndarray
        A boolean mask array with the same shape as the latitude and longitude arrays in lsmmodel,
        where True indicates the selected points based on the undersampling criteria.

    Raises
    ------
    ValueError
        If `i` or `j` are not within the valid range (0 <= i < n and 0 <= j < m).

    Examples
    --------
    >>> lsmmodel = {
    ...     'latitudes': np.array([10, 20, 30, 40, 50]),
    ...     'longitudes': np.array([100, 110, 120, 130, 140])
    ... }
    >>> cp_maskundersample(lsmmodel, 2, 2, 0, 0)
    array([[ True, False,  True, False,  True],
           [False, False, False, False, False],
           [ True, False,  True, False,  True],
           [False, False, False, False, False],
           [ True, False,  True, False,  True]])
    """
    if m is None:
        m = n
    
    latitudes = lsmmodel['latitudes']
    longitudes = lsmmodel['longitudes']
    
    # Ensure i and j are within the valid range
    if not (0 <= i < n) or not (0 <= j < m):
        raise ValueError("i and j must be within the range 0 to n-1 and 0 to m-1 respectively")
    
    # Create a mask with the same shape as latitudes and longitudes
    mask = np.zeros((len(latitudes), len(longitudes)), dtype=bool)
    
    # Apply the undersampling
    mask[i::n, j::m] = True
    
    return mask


############################### CFGRIB
# ds = cfgrib.open_file(fullpath)
# fullpath = "Import/grib/ARPEGE_GLOB025_20231231180000_ech0a5_U_V_10m.grb"
# ou : gribin = cp1iogrib.compile_grib_files(dataset_directory)
# fullpath = os.path.join(gribin.iloc[0,0], gribin.iloc[0,1])

def cp_dsdatanp(ds, var_str, dateheure, w0=None):
    # extract grib data over a windows and with a mask
    # Example usage:
    # dsvarstep = cp_dsdatanp(ds, 'u10', '2023-10-01T00:00:00', w0=[-10, 10, -20, 20])
    # dsvarstep
    if w0 is not None:
        lat_min, lat_max, lon_min, lon_max = w0
        if not (lat_min <= lat_max and lon_min <= lon_max):
            raise ValueError("lat_min must be <= lat_max and lon_min must be <= lon_max.")
    # If w0 is None, set it to the default window
    if w0 is None:
        w0 = [-np.inf, np.inf, -np.inf, np.inf]
    
    # Convert the dateheure to np.datetime64
    target_datetime = np.datetime64(dateheure)
    
    # Extract the valid_time array and convert to np.datetime64
    gribnpdatetime = np.array([np.datetime64(int(time), 's') for time in ds.variables['valid_time'].data])
    
    # Find the index of the target datetime
    n = np.where(gribnpdatetime == target_datetime)[0]
    if len(n) == 0:
        raise ValueError(f"Date {dateheure} not found in dataset.")
    
    # Convert n to a simple integer
    n = int(n[0])
    
    # Extract the variable data
    var_data = ds.variables[var_str].data
    
    # Check the dimensions of the variable
    var_dims = ds.variables[var_str].dimensions
    
    # Ensure the variable has 'step', 'latitude', and 'longitude' dimensions
    if set(var_dims) != {'step', 'latitude', 'longitude'}:
        raise ValueError("The variable does not contain the required dimensions: 'step', 'latitude', 'longitude'.")
    
    # Identify the position of the 'step' dimension
    step_index = var_dims.index('step')
    
    # Extract the data for the given step
    if step_index == 0:
        dsvarstep = var_data[n, :, :]
    elif step_index == 1:
        dsvarstep = var_data[:, n, :]
    elif step_index == 2:
        dsvarstep = var_data[:, :, n]
    else:
        raise ValueError("Unexpected position of 'step' dimension.")
    
    qlat = ds.variables['latitude'].data
    qlon = ds.variables['longitude'].data
        
    # If w0 is provided, validate and filter the data based on the window
    if w0 is not None:
        lat_min, lat_max, lon_min, lon_max = w0
        if not (lat_min <= lat_max and lon_min <= lon_max):
            raise ValueError("lat_min must be <= lat_max and lon_min must be <= lon_max.")
        
        # Use the cp_w0 function to get the indices
        ilat, ilon = cp_w0(w0, qlat, qlon)
        
        # Filter the dsvarstep data
        dsvarstep = dsvarstep[np.ix_(ilat, ilon)]
        qlat = qlat[np.ix_(ilat)]
        qlon = qlon[np.ix_(ilon)]
    
    return dsvarstep, qlat, qlon, ilat, ilon


############################### PLOT
# Example usage
# cp_gribmapplot(grib_data, latitudes, longitudes) # tous
# cp_gribmapplot(grib_data, latitudes, longitudes, 'r')
# cp_gribmapplot(grib_data, latitudes, longitudes, 0)
#
# Function to plot the weather parameter without extra packages, only matplolib
def plot_weather_parameter(data, title, units, latitudes, longitudes):
    """
    plot_weather_parameter

    :param args: Description of the parameters
    :type args: type of the parameters
    :return: Description of the return value
    :rtype: type of the return value
    """
    """
    plot_weather_parameter

    :param args: Description of the parameters
    :type args: type of the parameters
    :return: Description of the return value
    :rtype: type of the return value
    """
    plt.figure(figsize=(10, 6))
    plt.imshow(
        data,
        cmap="viridis",
        extent=[min(longitudes), max(longitudes), min(latitudes), max(latitudes)],
        origin="upper",
    )
    plt.colorbar(label=units)
    plt.title(title)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.show()


# Function to plot GRIB data
def cp_gribmapplot(grib_data, latitudes, longitudes, qparam=None):
    """
    cp_gribmapplot

    :param args: Description of the parameters
    :type args: type of the parameters
    :return: Description of the return value
    :rtype: type of the return value
    """
    """
    cp_gribmapplot

    :param args: Description of the parameters
    :type args: type of the parameters
    :return: Description of the return value
    :rtype: type of the return value
    """
    if qparam is None:
        params_to_plot = grib_data.keys()
    elif isinstance(qparam, list):
        params_to_plot = qparam
    else:
        params_to_plot = [qparam]

    for param in params_to_plot:
        if isinstance(param, int):
            param_key = list(grib_data.keys())[param]
        else:
            param_key = param

        details = grib_data[param_key]
        data = details["values"]
        # Reshape the data to match latitude and longitude dimensions
        latitude_dimension = len(latitudes)
        longitude_dimension = len(longitudes)
        reshaped_data = np.reshape(data, (latitude_dimension, longitude_dimension))
        title = f"{details['name']} ({param_key}) - {details['dataDate']} {details['dataTime']} - Step: {details['stepRange']} - Unit: {details['units']}"
        plot_weather_parameter(
            reshaped_data, title, details["units"], latitudes, longitudes
        )


# Example usage
# cp_checkplotallgribdata(grib_data, latitudes, longitudes)
# Simple plt function to plot the weather parameter with a blue to red colormap
def plot_weather_parameter(data, title, units, latitudes, longitudes):
    """
    plot_weather_parameter_brutal

    :param args: Description of the parameters
    :type args: type of the parameters
    :return: Description of the return value
    :rtype: type of the return value
    """
    """
    plot_weather_parameter_brutal

    :param args: Description of the parameters
    :type args: type of the parameters
    :return: Description of the return value
    :rtype: type of the return value
    """
    plt.figure(figsize=(10, 6))
    plt.imshow(
        data,
        cmap="bwr",
        extent=[min(longitudes), max(longitudes), min(latitudes), max(latitudes)],
        origin="upper",
    )
    plt.colorbar(label=units)
    plt.title(title)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.show()


# Function to plot all parameters in grib_data with the blue to red colormap
def cp_checkplotallgribdata(grib_data, latitudes, longitudes):
    """
    cp_checkplotallgribdata

    :param args: Description of the parameters
    :type args: type of the parameters
    :return: Description of the return value
    :rtype: type of the return value
    """
    """
    cp_checkplotallgribdata

    :param args: Description of the parameters
    :type args: type of the parameters
    :return: Description of the return value
    :rtype: type of the return value
    """
    for param, details in grib_data.items():
        data = details["values"]
        # Reshape the data to match latitude and longitude dimensions
        latitude_dimension = len(latitudes)
        longitude_dimension = len(longitudes)
        reshaped_data = np.reshape(data, (latitude_dimension, longitude_dimension))
        title = f"{details['name']} ({param}) - {details['dataDate']} {details['dataTime']} - Step: {details['stepRange']} - Unit: {details['units']}"
        plot_weather_parameter_brutal(
            reshaped_data, title, details["units"], latitudes, longitudes
        )


