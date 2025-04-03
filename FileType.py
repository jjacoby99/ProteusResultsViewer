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
