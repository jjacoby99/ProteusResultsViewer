supported_filenames = ["tensions.dat",
                       "position.dat",
                       "forces.dat",
                       "rigidBodyForceConnection.dat",
                       "rigidBodyMomentConnection.dat",
                       "rigidBodyABAConnection.dat"]

class DataColumns:
    def __init__(self, filename: str, num_columns: int):
        self.filename = filename
        self.num_columns = num_columns

        self.force_units = "N"
        self.moment_units = "N-m"
        self.lin_units = "m"
        self.ang_units = "deg"

    def set_force_units(self, force_units: str):
        self.force_units = force_units

    def set_moment_units(self, moment_units: str):
        self.moment_units = moment_units

    def set_lin_units(self, lin_units: str):
        self.lin_units = lin_units

    def set_ang_units(self, ang_units: str):
        self.ang_units = ang_units

    def set_filename(self, filename: str):
        self.filename = filename

    def set_num_columns(self, num_columns: int):
        self.num_columns = num_columns

    def get_column_names(self):
        columns = []
        if self.filename == "tensions.dat":
            columns.append("t [s]")
            for i in range(1, self.num_columns):
                columns.append(f"T_{i} [N]")
            return columns
        if self.filename == "position.dat":
            columns = ["t [s]", f"x {self.lin_units}", f"y {self.lin_units}", f"z {self.lin_units}",
                       f"phi {self.ang_units}", f"theta {self.ang_units}", f"psi {self.ang_units}"]
            return columns

        if self.filename == "forces.dat":
            columns = ["t [s]", f"FXG {self.force_units}", f"FYG {self.force_units}", f"FZG {self.force_units}",
                       f"MXG {self.moment_units}", f"MYG {self.moment_units}", f"MZG {self.moment_units}",
                       f"FX {self.force_units}", f"FY {self.force_units}", f"FZ {self.force_units}",
                       f"MX {self.moment_units}", f"MY {self.moment_units}", f"MZ {self.moment_units}"]
            return columns

        if self.filename == "rigidBodyForceConnection.dat":
            columns = ["t [s]", f"dx {self.lin_units}", f"dy {self.lin_units}", f"dz {self.lin_units}",
                       f"Fx {self.force_units}", f"Fy {self.force_units}", f"Fz {self.force_units}"]
            return columns

        if self.filename == "rigidBodyMomentConnection.dat":
            columns = ["t [s]", f"rx {self.ang_units}", f"ry {self.ang_units}", f"rz {self.ang_units}",
                       f"Mx {self.moment_units}", f"My {self.moment_units}", f"Mz {self.moment_units}"]
            return columns

        if self.filename == "rigidBodyABAConnection.dat":
            pass
        return columns


def GetColumns(filename: str, num_columns: int):
    columns = []
    if filename == "tensions.dat":
        columns.append("t [s]")
        for i in range(1, num_columns):
            columns.append(f"T_{i} [N]")
        return columns
    if filename == "position.dat":
        columns = ["t", "x", "y", "z", "phi", "theta", "psi"]
        return columns

    if filename == "forces.dat":
        columns = ["t", "FXG", "FYG", "FZG", "MXG", "MYG", "MZG", "FX", "FY", "FZ", "MX", "MY", "MZ"]
        return columns

    if filename == "rigidBodyForceConnection.dat":
        columns = ["t", "dx", "dy", "dz", "Fx", "Fy", "Fz"]
        return columns

    if filename == "rigidBodyMomentConnection.dat":
        columns = ["t", "rx", "ry", "rz", "Mx", "My", "Mz"]
        return columns

    if filename == "reactionLoads.dat":
        columns = ["t", "FX0", "FY0", "FZ0", "MX0", "MY0", "MZ0", "FXN", "FYN", "FZN", "MXN", "MYN", "MZN"]
        return columns

    if filename == "rigidBodyABAConnection.dat":
        columns = ["t", "FXu", "FYu", "FZu", "MXu", "MYu", "MZu", "FXd", "FYd", "FZd", "MXd", "MYd", "MZd"]
        return columns

    if filename == "cablePointConnection.dat":
        columns = ["t", "Fx", "Fy", "Fz", "Mx", "My", "Mz"]
        return columns
    return columns
