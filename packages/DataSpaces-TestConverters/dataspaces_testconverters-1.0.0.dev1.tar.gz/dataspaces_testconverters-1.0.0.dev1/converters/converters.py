import pandas as pd

def double(v):
    return v * 2

def multiply(x, y):
    return x * y

def to_knudsen(v):
    """
    Convert a given value to the Knudsen number using a specific conversion factor.

    Parameters:
    v (float or pd.Series): The value or pandas Series to be converted.

    Returns:
    float or pd.Series: The converted value(s) as the Knudsen number.
    """
    return (v * (1.805 / 1.80655)) + 0.03

def str_to_float(vector):
    """
    Convert a pandas Series of strings to a list of floats.

    Parameters:
    vector (pd.Series): A pandas Series containing string representations of numbers.

    Returns:
    list: A list of floats converted from the input Series.
    """
    return vector.astype(float).tolist()

def calc_cell_center_depth(blanking, cell_size, sensor_depth, velocity):
    """
    Calculate the center depth of cells in a velocity profile and update the DataFrame column names.

    Parameters:
    blanking (float): The blanking distance from the sensor to the first measurement cell.
    cell_size (float): The size of each measurement cell.
    sensor_depth (float): The depth of the sensor.
    velocity (pd.DataFrame): DataFrame containing velocity measurements.

    Returns:
    pd.DataFrame: DataFrame with updated column names reflecting the center depths of the cells.
    """
    for df_ in [velocity]:
        df_.columns = [
            sensor_depth
            + blanking
            + (cell_size / 2)
            + (c * cell_size)
            for c in range(len(df_.columns))
        ]
    return velocity

def cell_center_depth(blanking, cell_size, sensor_depth, velocity):
    """
    Calculate the depth of the center of each cell in a velocity profile.

    Parameters:
    blanking (float): The blanking distance from the sensor to the first cell.
    cell_size (float): The size of each cell.
    sensor_depth (float): The depth of the sensor.
    velocity (DataFrame): A DataFrame containing velocity data, where each column represents a cell.

    Returns:
    list: A list of depths for the center of each cell.
    """
    new_column_names = [
        sensor_depth
        + blanking
        + (cell_size / 2)
        + (c * cell_size)
        for c in range(len(velocity.columns))
    ]
    return new_column_names

def create_dataframe(*columns):
    """
    This function takes multiple columns as separate parameters and returns a DataFrame by concatenating them.

    Parameters:
    *columns: Variable length argument list of pandas Series or DataFrame objects

    Returns:
    pd.DataFrame: A DataFrame created by concatenating the input columns
    """
    # Concatenate the columns along axis=1 (columns)
    df = pd.concat(columns, axis=1)

    return df
