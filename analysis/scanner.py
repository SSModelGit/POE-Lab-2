import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from scipy.spatial.transform import Rotation
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns



class scanner:
    def __init__(self):
        self.calibration_data = None
        self.cs = None

    def calibrate(self, path: str):
        """
        Sets the internal cubic spline function from a calibration file
        """
        self.calibration_data = pd.read_csv(path, names=["distance", "voltage"])
        
        # Set the indepdent variable to be voltage
        self.calib_xs = self.calibration_data['voltage'].to_numpy()[3:] * -2.54

        # So that we get a distance as an output
        self.calib_ys = self.calibration_data['distance'].to_numpy()[3:]

        self.cs = CubicSpline(self.calib_xs, self.calib_ys)

    def plot_calibration_curve(self):
        """
        Plots the scanners associated calibration curve
        """
        fig = plt.figure()
        xs = np.linspace(0, self.calib_xs.max());
        ys = self.cs(xs)

        plt.plot(xs, ys, color='blue', label="Calibration Curve")
        plt.plot(self.calib_xs, self.calib_ys, label="Raw Data", color="red")
        plt.xlabel("Input Voltage")
        plt.ylabel("Expected Distance")
        plt.title("Calibration Function")
        plt.legend()
        plt.show()
        return fig

    def plot_image(self, path: str) -> pd.DataFrame:
        """
        Loads in the scan data from the csv and converts it to a dataframe
        """
        data = pd.read_csv(path, names=["theta", "phi", "distance"])

        data.mask(data['distance']>81)

        theta1 = data["theta"].to_numpy(dtype=np.float)
        theta2 = data["phi"].to_numpy(dtype=np.float)
        dist = self.cs(-1.0 * data["distance"].to_numpy(dtype=np.float))

        plt.tripcolor(-1.0 * theta1, -1.0 * theta2, dist)

        plt.show()

def run():
    # Make a new scanner object with intrinsics
    my_scanner = scanner()

    # Calibrate the linearization from a file
    my_scanner.calibrate("data/calibration.csv")
    my_scanner.plot_calibration_curve()

    # Plot the image
    my_scanner.plot_image("data/scan2d.csv")


if __name__ == "__main__":
    run()
