import streamlit as st
import os
import pandas as pd

st.title("Aggregated Analysis Across Cases and Realizations")

st.markdown(
    """
    This page allows you to compute maxima for a given file across all instances
    in a base folder.
    
    For instance, you may want to find the maximum node 0 tension for a dCable called M1
    across all realizations within the base folder.
    """
)

# Directory selection using the file selector component
base_folder = st.text_input("Enter the path to the base folder", value="/path/to/base/folder")

if base_folder:
    st.write("Selected base folder:", base_folder)
    if os.path.isdir(base_folder):
        # (The rest of your folder traversal and aggregation logic goes here)
        case_folders = sorted(
            [os.path.join(base_folder, d) for d in os.listdir(base_folder)
             if d.startswith("Case") and os.path.isdir(os.path.join(base_folder, d))]
        )

        realization_folders = sorted(
            [os.path.join(os.path.join(base_folder, case_folders[0]), d) for d in os.listdir(case_folders[0])
             if d.startswith("Realization") and os.path.isdir(os.path.join(os.path.join(base_folder, case_folders[0]), d))]
        )

        st.write(f"Found {len(case_folders)} cases and {len(realization_folders)} realizations.")

        # ... continue as before ...
    else:
        st.error("The selected path is not a valid directory.")
