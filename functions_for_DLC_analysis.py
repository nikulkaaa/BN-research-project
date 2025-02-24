# Importing the toolbox (takes several seconds)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Have this file in the same folder as the notebook
import time_in_each_roi
import time_within_certain_dist

#import image_draw
import matplotlib
matplotlib.use('Agg')

from collections import namedtuple
from matplotlib.patches import Circle
from typing import Tuple, List, Dict
import copy
import cv2 as cv
import image_draw
import os

from image_draw import ratio_calc, get_first_frame, double_click_draw 

def get_filenames(directory, filetype: str):
    """Returns a list of all .mp4 file names in the specified directory."""
    return [f for f in os.listdir(directory) if f.endswith(f'.{filetype}')]


def get_bodyparts(df: pd.DataFrame, DLCscorer: str, fps: int, bpt_names: List[str])-> List[Dict]:
    """
    Creates a list of dictionaries for each body part. 

    Each dictionary includes the name, velocity,
    time in the frames coordinates of the bofy part
    """
    bpts = []
    for bpt in bpt_names:
        # Calculate the velocity of each body part
        vel = time_in_each_roi.calc_distance_between_points_in_a_vector_2d(np.vstack([df[DLCscorer][bpt]['x'].values.flatten(), df[DLCscorer][bpt]['y'].values.flatten()]).T)
        # Total time of the video calculated by frames per second and velocity
        time=np.arange(len(vel))*1./fps
        # Extract coordinates for each body part from dataframe, y coordinates were flipped
        x_coordinates=df[DLCscorer][bpt]['x'].values
        y_coordinates=720-df[DLCscorer][bpt]['y'].values

        bpts.append({"name":bpt, "velocity": vel, "time": time, "x": x_coordinates, "y": y_coordinates})
    return bpts

def get_center_coordinates(df: pd.DataFrame,  DLCscorer: str, object_name: str) -> Tuple [float, float]:
    """
    Extracts coordinates of a centre of a circular object.
    Returns a tuple of coordiates
    """
    object_center = object_name + ' centre'
    xs=df[DLCscorer][object_center]['x'].values
    ys=df[DLCscorer][object_center]['y'].values
    x = np.mean(xs)
    y = 720- np.mean(ys)
    return (x, y)

def get_radius(df: pd.DataFrame, DLCscorer: str, object_name: str) -> float:
    """
    Extracts radius of a certain object. 

    Returns the radius + a distance from the object,
    which we desire to take into account for a region of interest.
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
    Returns a list of ROIs.

    Each datapoint in the list is a dictionary
    containing the name, the actual ROI,
    the center coordinates
    and the radius of each region of interest.
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

# Plotting
def plot_velocity_of_bpt(bpts, fps: int):
    """
    Plots velocity of a body part through time. 
    """
    for bpt in bpts:
        plt.plot(bpt.get('time'),bpt.get("velocity")*1./fps)
        plt.xlabel('Time in seconds')
        plt.ylabel('Speed in pixels per second')
        plt.title(f'{bpt.get("name")}')
        plt.show()

def plot_rois_and_bpt_movements(bpts, rois):
    """
    Plots all positions of bpt through out the video.
    Plots outlines of ROIs.
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

def get_total_exploration_time(rois, rois_substracting, bpt_plus, bpt_minus):
    """
    Returns the total exploration time 
    """
    exploration = []
    for roi in rois:
        roi_name = roi.get("name")
        substracting_roi = next((r for r in rois_substracting if r.get("name") == roi_name), None)

        if substracting_roi is None:
            print(f"Warning: No matching subtracting ROI found for {roi_name}. Skipping subtraction.")
            continue  

        # Extract first value from tuple (modify index if needed)
        plus = [time_within_certain_dist.calculate_time_within_distance(
            bpt.get('x'), bpt.get('y'),
            roi.get("center")[0], roi.get("center")[1], roi.get("radius"),
            min_frames=4, fps=30
        )[0] for bpt in bpt_plus]  # Taking the first value of the tuple

        minus = [time_within_certain_dist.calculate_time_within_distance(
            bpt.get('x'), bpt.get('y'),
            substracting_roi.get("center")[0], substracting_roi.get("center")[1], substracting_roi.get("radius"),
            min_frames=4, fps=30
        )[0] for bpt in bpt_minus]  # Taking the first value of the tuple

        # Compute total exploration time
        total_exploration_time = max(plus, default=0) - max(minus, default=0)

        if total_exploration_time < 0.0:
            total_exploration_time = 0

        exploration.append({"name": roi_name, "exploration time":total_exploration_time})
        
    return exploration

def get_cm_to_pixel_ratio(actual_width: float, video_name, video_type):
    """
    Lets the user choose 2 datapoints of the width of the arena
    and calculates the cm to pixel ration for calculations
    """
    # Takes the first frame and shows it. after two points or esc closes. 
    videoname = video_name + video_type
    image_draw.get_first_frame(videoname)
    image_draw.double_click_draw()


    # Used to calculate distance to pixel ratio ( in cm here) to change edit the text.
    actual_distance = 40
    ratio_cm_to_pixel = image_draw.ratio_calc(actual_distance)

def get_exploration_time(rois, rois_substracting, bpt_plus, bpt_minus, fps:float):
    """
    Returns the total exploration time 
    """
    exploration = []
    for roi in rois:
        roi_name = roi.get("name")
        substracting_roi = next((r for r in rois_substracting if r.get("name") == roi_name), None)

        if substracting_roi is None:
            print(f"Warning: No matching subtracting ROI found for {roi_name}. Skipping subtraction.")
            continue  

        # Calculate the total exploration time for each ROI
        total_exploration_time = time_within_certain_dist.calculate_exploration_time(
            bpt_plus[0].get('x'), bpt_plus[0].get('y'),
            roi.get("center")[0], roi.get("center")[1], roi.get("radius"),
            xleft=bpt_minus[0].get('x'), yleft=bpt_minus[0].get('y'),
            xright=bpt_minus[0].get('x'), yright=bpt_minus[0].get('y'),
            radius2 = substracting_roi.get("radius"),
            min_frames=4, fps=fps
        )
        exploration.append({"name": roi_name, "exploration time":total_exploration_time})

        
    return exploration