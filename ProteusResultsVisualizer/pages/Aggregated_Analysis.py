from argparse import FileType
import streamlit as st
import os
import pandas as pd
from ProteusResultsVisualizer import is_connection, supported_file_types, not_feature_dirs, feature_paths, load_dataframe
from ProteusResultsVisualizer import Aggregator, ComponentWiseExtremaAggregator, MeanAggregator
from ProteusResultsVisualizer import initialize_dataframe
from ProteusResultsVisualizer import file_path_to_uploaded_file

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
base_folder = st.text_input("Enter the path to the base folder", value="/Users/joshjacoby/Downloads/Sim1_results")

if base_folder:
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

        results_folder = os.path.join(realization_folders[0], "Results")
        feature_folders = sorted(
            [os.path.join(results_folder, d) for d in os.listdir(results_folder)
             if os.path.isdir(os.path.join(results_folder, d))]
        )
        feature_names = [os.path.basename(file) for file in feature_folders
                         if os.path.basename(file) not in not_feature_dirs()]

        feature = st.selectbox("Select feature", feature_names)

        selected_feature_path = os.path.join(results_folder, feature)
        supported_files = sorted(
            [os.path.basename(folder) for folder in os.listdir(selected_feature_path)
             if os.path.basename(folder) in supported_file_types()]
        )

        file_type = st.selectbox("Select file type", supported_files)

        all_file_paths = feature_paths(base_folder, feature, file_type)
        assert len(all_file_paths) == len(realization_folders) * len(case_folders)

        st.markdown('### Analysis')
        st.markdown('Select data-aggregation type')

        aggregation_type = st.radio(
            "Select aggregation method",
            options=[
                "Component-wise Maxima/Minima",
                "Average",
                "Median",
                "Custom (select columns)"
            ]
        )

        if aggregation_type == "Component-wise Maxima/Minima":
            aggregator = ComponentWiseExtremaAggregator()
        if aggregation_type == "Average":
            aggregator = MeanAggregator()

        real_results = {}
        df = initialize_dataframe(file_path_to_uploaded_file(all_file_paths[0]),"key")
        st.markdown('### Data Preview')
        st.dataframe(df.head())
        #for i, file in enumerate(all_file_paths):
        #    st.markdown(f'Given file path: {file}')
        #    df = initialize_dataframe(file_path_to_uploaded_file(file), f"cols_to_skip_agg_{i}")

        #    if 'df' in st.session_state:
        #        df = st.session_state['df']

        #    result = aggregator.aggregate(df)
        #    real_results[file] = result

    else:
        st.error("The selected path is not a valid directory.")
