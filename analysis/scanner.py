import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from scipy.spatial.transform import Rotation
from mpl_toolkits.mplot3d import Axes3D



class scanner:
    def __init__(self):
        self.calibration_data = None
        self.cs = None


    def calibrate(self, path: str):
        self.calibration_data = pd.read_csv(path, names=["distance", "voltage"])
        
        # Set the indepdent variable to be voltage
        self.calib_xs = self.calibration_data['voltage'].to_numpy()

        # So that we get a distance as an output
        self.calib_ys = self.calibration_data['distance'].to_numpy();

        self.cs = CubicSpline(self.calib_xs, self.calib_ys)

    def plot_calibration_curve(self):
        fig = plt.figure()
        xs = np.linspace(0, self.calibration_data['distance'].to_numpy().max());
        ys = self.cs(xs)

        plt.plot(xs, ys, color='blue', label="Calibration Curve")
        plt.plot(self.calib_xs, self.calib_ys, label="Raw Data", color="red")
        plt.xlabel("Input Voltage")
        plt.ylabel("Expected Distance")
        plt.title("Calibration Function")
        plt.legend()

        return fig

    def linearize_raw(self, raw_distance):
        interp_shifted = lambda x: self.cs(x) - raw_distance
        interp_shifted.roots()
        pass

    def plot_image(self, path: str) -> pd.DataFrame:
        """
        Loads in the scan data from the csv and converts it to a dataframe
        """
        pd.read_csv(path, names=["r", "theta", "distance"])

        data = np.genfromtxt(path, delimiter=',')
        theta1=data[:,0]-45
        theta2=data[:,1]-45
        dist=data[:,2]

        tf_2 = np.array([np.zeros(dist.shape), dist, np.zeros(dist.shape)]).T
        theta_mat = np.array([theta1, theta2]).T * (np.pi/180)
        theta_mat

        r = Rotation.from_euler('xz', theta_mat)
        r.apply(tf_2)


        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(theta1, theta2, dist)
        plt.xlabel("yoink")
        plt.ylabel("yeet")


        pass


if __name__ == "__main__":
    # Make a new scanner object with intrinsics
    my_scanner = scanner()

    # Calibrate the linearization from a file
    my_scanner.calibrate("data/calibrate.csv")
    my_scanner.plot_calibration_curve()

    # Load in scanner data and plot it
    my_scanner.plot_image()




