# Importing the toolbox (takes several seconds)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
from matplotlib.patches import Circle
from typing import Tuple, List, Dict
import copy
import matplotlib
matplotlib.use('Agg')

### -------- FUNCTIONS TO DEFINE AND CREATE BODYPARTS AND ROIs --------
def get_bodyparts(df: pd.DataFrame, DLCscorer: str, fps: int, bpt_names: List[str])-> List[Dict]:
    """
    Extracts body part data from a given DataFrame and calculates their velocities over time.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing tracking data for body parts.
        DLCscorer (str): Name of the scorer used in DeepLabCut for tracking.
        fps (int): Frames per second of the video.
        bpt_names (List[str]): List of body part names to extract data for.
    
    Returns:
        List[Dict]: A list of dictionaries, each containing:
            - 'name': Name of the body part.
            - 'velocity': Computed velocity of the body part.
            - 'time': Time points corresponding to the frames.
            - 'x': X-coordinates of the body part.
            - 'y': Y-coordinates of the body part (flipped vertically for consistency).
    """
    bpts = []
    for bpt in bpt_names:
        # Calculate the velocity of each body part
        vel = calculate_velocity(np.vstack([df[DLCscorer][bpt]['x'].values.flatten(), df[DLCscorer][bpt]['y'].values.flatten()]).T)
        # Total time of the video calculated by frames per second and velocity
        time=np.arange(len(vel))*1./fps
        # Extract coordinates for each body part from dataframe, y coordinates were flipped
        x_coordinates=df[DLCscorer][bpt]['x'].values
        y_coordinates=720-df[DLCscorer][bpt]['y'].values

        bpts.append({"name":bpt, "velocity": vel, "time": time, "x": x_coordinates, "y": y_coordinates})
    return bpts

def calculate_velocity(v1):
    '''calc_distance_between_points_in_a_vector_2d [for each consecutive pair of points, p1-p2, in a vector, get euclidian distance]

    This function can be used to calculate the velocity in pixel/frame from tracking data (X,Y coordinates)
    
    Arguments:
        v1 {[np.array]} -- [2d array, X,Y position at various timepoints]
    
    Raises:
        ValueError
    
    Returns:
        [np.array] -- [1d array with distance at each timepoint]

    >>> v1 = [0, 10, 25, 50, 100]
    >>> d = calc_distance_between_points_in_a_vector_2d(v1)
    '''
    # Check data format
    if isinstance(v1, dict) or not np.any(v1) or v1 is None:
            raise ValueError(
                'Feature not implemented: cant handle with data format passed to this function')

    # If pandas series were passed, try to get numpy arrays
    try:
        v1, v2 = v1.values, v2.values
    except:  # all good
        pass
    # loop over each pair of points and extract distances
    dist = []
    for n, pos in enumerate(v1):
        # Get a pair of points
        if n == 0:  # get the position at time 0, velocity is 0
            p0 = pos
            dist.append(0)
        else:
            p1 = pos  # get position at current frame

            # Calc distance
            dist.append(np.abs(distance.euclidean(p0, p1)))

            # Prepare for next iteration, current position becomes the old one and repeat
            p0 = p1

    return np.array(dist)

def get_center_coordinates(df: pd.DataFrame,  DLCscorer: str, object_name: str) -> Tuple [float, float]:
    """
    Computes the center coordinates of a circular object from tracking data.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing object tracking data.
        DLCscorer (str): Name of the scorer used in DeepLabCut for tracking.
        object_name (str): Name of the tracked object.
    
    Returns:
        Tuple[float, float]: The (x, y) coordinates of the object's center.
    """

    # Specify the centre to extract correct data from the dataframe
    object_center = object_name + ' centre'
    # Extract x values
    xs=df[DLCscorer][object_center]['x'].values
    # Extract x values
    ys=df[DLCscorer][object_center]['y'].values
    # Calculate mean of all x values for accuracy
    x = np.mean(xs)
    # Calculate mean of all y values for accuracy (flips values back)
    y = 720-np.mean(ys)
    # Return a tuple of the centre coordinates
    return (x, y)

def get_radius(df: pd.DataFrame, DLCscorer: str, object_name: str) -> float:
    """
    Calculates the radius of a circular object based on tracked positions.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing object tracking data.
        DLCscorer (str): Name of the scorer used in DeepLabCut for tracking.
        object_name (str): Name of the tracked object.
    
    Returns:
        float: The computed radius, including an additional margin for the region of interest.
    """

    # Get name of each position
    object_3 = object_name + " 3"
    object_6 = object_name + " 6"
    object_9 = object_name + " 9"
    object_12 = object_name + " 12"

    # Get x and y values of the position at 3 and 9 o'clock
    x_3=df[DLCscorer][object_3]['x'].values
    x_9=df[DLCscorer][object_9]['x'].values

    # Get x and y values of the position at 6 and 12 o'clock
    y_6=df[DLCscorer][object_6]['y'].values
    y_12=df[DLCscorer][object_12]['y'].values
    
    radius = (np.mean(x_3 - x_9) + np.mean(y_6 - y_12)) / 4.0
    return radius

def create_rois(df, DLCscorer: str, distance: float, names: List[str], cm_to_pixel_ratio:float) -> List[Dict]:
    """
    Creates regions of interest (ROIs) based on detected objects in the tracking data.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing object tracking data.
        DLCscorer (str): Name of the scorer used in DeepLabCut for tracking.
        distance (float): Additional margin to include in ROI size.
        names (List[str]): List of object names for which ROIs should be created.
        cm_to_pixel_ratio (float): Conversion ratio from centimeters to pixels.
    
    Returns:
        List[Dict]: A list of ROI dictionaries, each containing:
            - 'name': Name of the ROI.
            - 'roi': ROI shape as a matplotlib Circle object.
            - 'center': (x, y) coordinates of the ROI center.
            - 'radius': Radius of the ROI (including margin).
    """

    # Create an empty list of ROIs
    rois = []
    for name in names:
        # Get the center position of each ROI
        center = get_center_coordinates(df = df, DLCscorer=DLCscorer, object_name=name)
        # Get the radius of each ROI
        radius = get_radius(df = df, DLCscorer=DLCscorer, object_name=name)
        radius = radius + (distance*cm_to_pixel_ratio)
        # Create each ROI with given parameters
        roi = Circle(center, radius, facecolor='none', edgecolor='red', zorder=1)
        # Append each ROI
        rois.append({"name": name, "roi": roi, "center": center, "radius": radius})
    return rois

### -------- FUNCTIONS FOR PLOTTING --------
def plot_velocity_of_bpt(bpts, fps: int):
    """
    Plots the velocity of each body part over time.
    
    Parameters:
        bpts (List[Dict]): List of body part data dictionaries.
        fps (int): Frames per second of the video.
    """
    for bpt in bpts:
        plt.plot(bpt.get('time'),bpt.get("velocity")*1./fps)
        plt.xlabel('Time in seconds')
        plt.ylabel('Speed in pixels per second')
        plt.title(f'{bpt.get("name")}')
        plt.show()

def plot_rois_and_bpt_movements(bpts, rois):
    """
    Plots the movement of body parts along with the outlines of their respective ROIs.
    
    Parameters:
        bpts (List[Dict]): List of body part data dictionaries.
        rois (List[Dict]): List of ROI dictionaries.
    """

    for bpt in bpts:
        fig, ax = plt.subplots()  # Create a new figure for each body part

        # Add ROIs to the current figure
        for roi in rois:
            ax.add_patch(copy.deepcopy(roi.get("roi")))

        ax.set_aspect('equal')
        ax.set_facecolor('none')

        # Plot the current body part
        plt.plot(bpt.get("x"), bpt.get("y"), '.-', zorder=0)

        # Set limits and title for this body part
        plt.ylim(0, 700)
        plt.xlim(150, 1100)
        plt.title(bpt.get("name"))

        # Show each figure separately
        plt.show()

### -------- FUNCTIONS TO CALCULATE EXPLORATION TIME CORRECTLY --------


def calculate_total_exploration_time(xnose, ynose, center_x, center_y, radius, xleft, yleft, xright, yright, radius2: float,  fps: float, min_frames=8) -> float:
    """
    Computes the total time spent exploring an object, considering both body part and paw positions.
    
    Parameters:
        xnose (np.array): X-coordinates of the nose.
        ynose (np.array): Y-coordinates of the nose.
        center_x (float): X-coordinate of the reference point.
        center_y (float): Y-coordinate of the reference point.
        radius (float): Primary radius threshold for being within range.
        xleft (np.array): X-coordinates of the left paw.
        yleft (np.array): Y-coordinates of the left paw.
        xright (np.array): X-coordinates of the right paw.
        yright (np.array): Y-coordinates of the right paw.
        radius2 (float): Secondary radius for additional condition.
        fps (float): Frames per second of the recording.
        min_frames (int, optional): Minimum frames required to count as exploration. Defaults to 8.
    
    Returns:
        float: Total exploration time in seconds.
    """
    
    # Calculate the Euclidean distance for every frame; the distance of the nose from the center point
    distance_to_object = np.sqrt((xnose - center_x) ** 2 + (ynose - center_y) ** 2)

    # Calculate distance for both left and right paws
    distance_left = np.sqrt((xleft - center_x) ** 2 + (yleft - center_y) ** 2)
    distance_right = np.sqrt((xright - center_x) ** 2 + (yright - center_y) ** 2)


    # Distinguish between quick runby's and actual exploratory behavior by means of setting a frame minimum
    # secutive sequences where the condition is met
    frame_count_with_minimum = 0
    total_frame_count = 0
    
    # Calculate the total amount of frames the body partwas within the radius distance from the center of the object
    for dist_obj, dist_left, dist_right in zip(distance_to_object, distance_left, distance_right):
        if dist_obj <= radius and dist_left >= radius2 and dist_right >= radius2:
            frame_count_with_minimum += 1
        else:
            if frame_count_with_minimum  >= min_frames:
                # Convert frames to seconds
                total_frame_count += frame_count_with_minimum
            # Reset counter when outside the range
            frame_count_with_minimum  = 0 
    # Calculate the total times
    time_with_minimum = total_frame_count/fps

    # Final check in case the sequence ends within the distance
    if frame_count_with_minimum >= min_frames:
        time_with_minimum += frame_count_with_minimum / fps
    
    return time_with_minimum

def get_exploration_time(rois, rois_substracting, bpt_plus, bpt_minus, fps:float):
    """
    Computes the total exploration time of a body part within a given set of ROIs.
    
    Parameters:
        rois (List[Dict]): List of ROI dictionaries.
        rois_substracting (List[Dict]): ROIs to be subtracted from the total.
        bpt_plus (np.array): X, Y coordinates of the exploring body part.
        bpt_minus (np.array): X, Y coordinates of a subtracting body part.
        fps (float): Frames per second of the recording.
    
    Returns:
        float: Total adjusted exploration time.
    """
    exploration = []
    for roi in rois:
        roi_name = roi.get("name")
        substracting_roi = next((r for r in rois_substracting if r.get("name") == roi_name), None)

        if substracting_roi is None:
            print(f"Warning: No matching subtracting ROI found for {roi_name}. Skipping subtraction.")
            continue  

        # Calculate the total exploration time for each ROI
        total_exploration_time = calculate_total_exploration_time(
            bpt_plus[0].get('x'), bpt_plus[0].get('y'),
            roi.get("center")[0], roi.get("center")[1], roi.get("radius"),
            xleft=bpt_minus[0].get('x'), yleft=bpt_minus[0].get('y'),
            xright=bpt_minus[1].get('x'), yright=bpt_minus[1].get('y'),
            radius2 = substracting_roi.get("radius"),
            min_frames=4, fps=fps
        )
        exploration.append({"name": roi_name, "exploration time":total_exploration_time})
    return exploration