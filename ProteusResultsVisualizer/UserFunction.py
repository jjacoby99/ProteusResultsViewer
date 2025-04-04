import numpy as np
import pandas as pd

def add_computed_column(
        df: pd.DataFrame,
        selected_columns: list,
        formula: str,
        new_column_name: str
) -> pd.DataFrame:
    """
    Evaluates a user-provided formula to compute a new column for the DataFrame.

    Parameters:
        df (pd.DataFrame): The original DataFrame.
        selected_columns (list): A list of column names that are allowed in the formula.
        formula (str): A string formula that can reference the selected columns and uses numpy as np.
                       Example: "np.sqrt(dx**2 + dy**2)".
        new_column_name (str): The name of the new computed column.

    Returns:
        pd.DataFrame: The updated DataFrame with the new column added.

    Raises:
        ValueError: If the formula evaluation fails.
    """
    # Build a restricted local environment with only the allowed columns
    local_env = {col: df[col] for col in selected_columns if col in df.columns}
    local_env["np"] = np  # Allow numpy functions

    try:
        # Evaluate the formula safely with no builtins
        result = eval(formula, {"__builtins__": {}}, local_env)

        # Ensure the result is a pandas Series; if not, convert it.
        if not isinstance(result, pd.Series):
            result = pd.Series(result)
    except Exception as e:
        raise ValueError(f"Error evaluating formula: {e}")

    # Update the DataFrame with the new computed column
    df[new_column_name] = result
    return df
