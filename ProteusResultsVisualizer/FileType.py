import os
import streamlit as st
def is_connection(file_name: str):
    return file_name in ["rigidBodyForceConnection.dat",
                         "rigidBodyMomentConnection.dat",
                         "rigidBodyABAConnection.dat",
                         "cablePointConnection.dat"]

def supported_file_types():
    return ["tensions.dat",
            "position.dat",
            "forces.dat",
            "rigidBodyForceConnection.dat",
            "rigidBodyMomentConnection.dat",
            "rigidBodyABAConnection.dat",
            "reactionLoads.dat",
            "cablePointConnection.dat"]

def get_skip_rows(filename: str):
    if filename == "cablePointConnection.dat":
        return 4
    return 2 if filename in ["tensions.dat", "position.dat", "forces.dat"] else 3


def not_feature_dirs():
    '''
    Returns a list of directory names that are generated from proteus
    but are not features (so they can be ignored).
    '''
    return ["TerminalIC",
            "SolverData",
            "Restart",
            "Initial"]

import os

def feature_paths(base_folder: str, feature: str, filename: str):
    '''
    Returns a list of file-paths pertaining to each instance of the given
    feature's filename assuming path structure:
    base_folder/Case*/Realization*/Results/feature/filename
    '''
    file_paths = []
    for case in os.listdir(base_folder):
        case_path = os.path.join(base_folder, case)
        if case.startswith("Case") and os.path.isdir(case_path):
            for realization in os.listdir(case_path):
                realization_path = os.path.join(case_path, realization)
                if realization.startswith("Realization") and os.path.isdir(realization_path):
                    results_folder = os.path.join(realization_path, "Results")
                    feature_folder = os.path.join(results_folder, feature)
                    file_path = os.path.join(feature_folder, filename)
                    file_paths.append(file_path)
    return file_paths


import os
from io import BytesIO

def file_path_to_uploaded_file(file_path: str):
    # Open the file in binary mode
    with open(file_path, "rb") as f:
        data = f.read()
    # Wrap the bytes in a BytesIO object
    file_obj = BytesIO(data)
    # Add a name attribute to mimic the uploaded file object
    file_obj.name = os.path.basename(file_path)
    return file_obj