import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from FileType import is_connection, get_skip_rows, supported_file_types
from GetColumns import GetColumns
from UserFunction import add_computed_column

# Constants for units (can be moved to a config file if they grow)
FORCE_UNITS = ["N", "kN", "MN", "T", "kg", "lbf", "kip"]
MOMENT_UNITS = ["N-m", "kN-m", "MN-m", "lb-ft", "lb-in", "kip-ft"]
LIN_UNITS = ["m", "mm", "cm", "ft", "in"]
ANG_UNITS = ["deg", "rad"]



st.title("ProteusDS Data Visualization Tool")

supported_file_names = supported_file_types()
st.markdown('### Supported Files')
st.write(", ".join(supported_file_names))

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


def determine_columns(selected_index: int, ncols_per_conn: int = 6) -> list:
    """
    Determines the list of columns to load based on the selected connection.
    Always include column 0 (time), then connection-specific columns.
    """
    start_col = 1 + selected_index * ncols_per_conn
    return [0] + list(range(start_col, start_col + ncols_per_conn))


def load_dataframe(uploaded_file, delimiter: str, skip: int, usecols: list) -> pd.DataFrame:
    """
    Loads the DataFrame from the uploaded file using the given delimiter, skip rows, and columns.
    """
    uploaded_file.seek(0)
    return pd.read_csv(uploaded_file, delimiter=delimiter, skiprows=skip, header=None, usecols=usecols)


# File uploader for space-delimited files
uploaded_file = st.file_uploader("Choose a space-delimited file", type=["txt", "tsv", "csv", ".dat"])
st.markdown("---")

if uploaded_file is not None:

    if not uploaded_file.name in supported_file_names:
            st.write(f"Unsopported file name: '{uploaded_file.name}'. Please select a supported file.")
    else:
        # Check if the file is a connection file using the imported helper function
        connection_flag = is_connection(uploaded_file.name)
        base_skip = get_skip_rows(uploaded_file.name)
        if connection_flag:
            uploaded_file.seek(0)
            file_bytes = uploaded_file.getvalue()
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
                    except ValueError as e:
                        st.error(e)

        st.dataframe(df.head())
        st.markdown("---")

        # Plotting and statistics section
        st.write("### Visualization")
        numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()
        if numeric_columns:
            col1, col2 = st.columns([1, 2])  # Adjust the ratio as needed

            with col1:
                # Place smaller inputs on the left column
                x_axis = st.selectbox("Select X-axis", numeric_columns)
                y_axis = st.selectbox("Select Y-axis", numeric_columns)

            with col2:
                # Use the larger column for selecting connection (if applicable) or other inputs
                stats_options = st.multiselect("Select statistics to display",
                                                ["Minimum", 
                                                "Maximum", 
                                                "Mean", 
                                                "Mean + 3 * std",
                                                "Mean - 3 * std"])

            title = st.text_input("Title")
            # Create the plot
            #fig, ax = plt.subplots()
            fig = px.line(df, x=x_axis, y=y_axis, title=title)

            #ax.plot(df[x_axis], df[y_axis], linewidth=1)

            # Determine the x-axis range for horizontal lines
            x_min = df[x_axis].min()
            x_max = df[x_axis].max()

            if "Minimum" in stats_options:
                min_val = df[y_axis].min()
                fig.add_trace(go.Scatter(
                    x=[x_min, x_max],
                    y=[min_val, min_val],
                    mode="lines",
                    name=f"Min: {round(min_val, 2)}",
                    line=dict(dash="dash", color="blue")
                ))

            if "Maximum" in stats_options:
                max_val = df[y_axis].max()
                fig.add_trace(go.Scatter(
                    x=[x_min, x_max],
                    y=[max_val, max_val],
                    mode="lines",
                    name=f"Max: {round(max_val, 2)}",
                    line=dict(dash="dash", color="red")
                ))

            if "Mean" in stats_options:
                mean_val = df[y_axis].mean()
                fig.add_trace(go.Scatter(
                    x=[x_min, x_max],
                    y=[mean_val, mean_val],
                    mode="lines",
                    name=f"Mean: {round(mean_val, 2)}",
                    line=dict(dash="dash", color="green")
                ))

            if "Mean + 3 * std" in stats_options:
                stat_val = df[y_axis].mean() + 3 * df[y_axis].std()
                fig.add_trace(go.Scatter(
                    x=[x_min, x_max],
                    y=[stat_val, stat_val],
                    mode="lines",
                    name=f"Mean+3*std: {round(stat_val, 2)}",
                    line=dict(dash="dash", color="black")
                ))

            if "Mean - 3 * std" in stats_options:
                stat_val = df[y_axis].mean() - 3 * df[y_axis].std()
                fig.add_trace(go.Scatter(
                    x=[x_min, x_max],
                    y=[stat_val, stat_val],
                    mode="lines",
                    name=f"Mean-3*std: {round(stat_val, 2)}",
                    line=dict(dash="dash", color="black")
                ))

            st.plotly_chart(fig, use_container_width=True)

else:
    st.write("No numeric columns found for plotting.")

