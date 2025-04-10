import pandas as pd
import streamlit as st
from ProteusResultsVisualizer.FileType import get_skip_rows, is_connection, get_skip_rows
from ProteusResultsVisualizer.GetColumns import GetColumns
from ProteusResultsVisualizer.UserFunction import add_computed_column

def extract_connection_info(uploaded_file) -> tuple:
    """
    Extracts the connection names and returns the list of connection names along with the header skip count.
    Assumes connection information is on the third line of the file.
    """
    file_bytes = uploaded_file.getvalue()
    all_lines = file_bytes.decode("utf-8").splitlines()
    if len(all_lines) < 3:
        st.error("The file does not have enough lines to extract connection info.")
        return None, None

    # Process third line for connection names
    connection_line_index = get_skip_rows(uploaded_file.name) - 1
    connection_line = all_lines[connection_line_index].lstrip("#").strip()
    connection_names = connection_line.split()
    return connection_names, 3  # header skip is 3 rows for files with connections


def load_dataframe(uploaded_file, delimiter: str, skip: int, usecols: list) -> pd.DataFrame:
    """
    Loads the DataFrame from the uploaded file using the given delimiter, skip rows, and columns.
    """
    uploaded_file.seek(0)
    return pd.read_csv(uploaded_file, delimiter=delimiter, skiprows=skip, header=None, usecols=usecols)

def determine_columns(selected_index: int, ncols_per_conn: int = 6) -> list:
    """
    Determines the list of columns to load based on the selected connection.
    Always include column 0 (time), then connection-specific columns.
    """
    start_col = 1 + selected_index * ncols_per_conn
    return [0] + list(range(start_col, start_col + ncols_per_conn))


def initialize_dataframe(uploaded_file) -> pd.DataFrame:
    base_skip = get_skip_rows(uploaded_file.name)
    if is_connection(uploaded_file.name):
        uploaded_file.seek(0)
        connection_names, header_skip = extract_connection_info(uploaded_file)
        if connection_names is None:
            st.stop()

        # User selects a connection
        selected_connection = st.selectbox("Select a connection", connection_names)
        connection_index = connection_names.index(selected_connection)

        cols_per_group = 12 if uploaded_file.name == "rigidBodyABAConnection.dat" else 6
        cols_to_use = determine_columns(connection_index, cols_per_group)
    else:
        # For non-connection files, assume the header is on line 3 (index 2)
        uploaded_file.seek(0)
        file_bytes = uploaded_file.getvalue()
        all_lines = file_bytes.decode("utf-8").splitlines()
        if len(all_lines) < 3:
            st.error("The file does not have enough lines to determine columns.")
            st.stop()

        data_line = all_lines[base_skip]
        data = data_line.split()
        cols_to_use = list(range(len(data)))

    # Ask user for additional rows to skip after header
    st.write("### Data Preview")
    rows_to_skip = st.number_input("Rows to skip", min_value=0, value=0, step=1)
    total_skip = base_skip + int(rows_to_skip)

    # Load the DataFrame (assuming space-delimited data)
    df = load_dataframe(uploaded_file, delimiter=" ", skip=total_skip, usecols=cols_to_use)

    # Set DataFrame columns using GetColumns helper
    df.columns = GetColumns(uploaded_file.name, len(df.columns))

    # Optional section for creating a computed column
    if st.checkbox("Create a new computed column?"):
        st.write("### New Computed Column Settings")

        # Let the user select which columns to use in the formula
        selected_columns = st.multiselect("Select columns to use in your formula", df.columns.tolist())

        # Input field for the formula (e.g., "np.sqrt(dx**2 + dy**2)")
        formula = st.text_input("Enter formula (e.g., np.sqrt(dx**2 + dy**2))", value="")

        # Input field for the new column name
        new_column_name = st.text_input("New column name", value="Computed")

        if st.button("Add Computed Column"):
            if not selected_columns:
                st.error("Please select at least one column.")
            elif not formula:
                st.error("Please enter a formula.")
            else:
                try:
                    df = add_computed_column(df, selected_columns, formula, new_column_name)
                    st.success(f"Column '{new_column_name}' added!")
                    st.session_state['df'] = df
                except ValueError as e:
                    st.error(e)
    return df



