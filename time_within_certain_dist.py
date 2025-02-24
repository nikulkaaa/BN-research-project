import pandas as pd
import numpy as np

def calculate_time_within_distance(xnose, ynose, center_x, center_y, radius, min_frames=8, fps=30):
    """
    Calculate the time spent within a certain distance of a given center point by the specified body part.
    
    Parameters:
        data (pd.DataFrame): DataFrame containing the body part's x, y coordinates per frame.
        center (tuple): A tuple (center_x, center_y) defining the reference point.
        distance (float): The radius within which to measure time spent.
        bp_tracking.t (str): The body part to track (default: 'nose').
        min_frames (int): Minimum consecutive frames within the distance to count time (default: 8).
        fps (int): Frames per second of the recording (default: 30).
        
    Returns:
        float: Time (in seconds) spent within the specified distance.
    """
    
    # Calculate the Euclidean distance for every frame; the distance of the nose from the center point
    distance_to_object = np.sqrt((xnose - center_x) ** 2 + (ynose - center_y) ** 2)

    # The amount of frames where a body part is in within a radius distance from the center of the object
    frame_count_within_distance = 0

    # Calculate the total amount of frames the body partwas within the radius distance from the center of the object
    for distance in distance_to_object:
        if distance <= radius:
            frame_count_within_distance += 1

    # Count of total seconds that the nose was in the designated radius
    total_time_within_distance = frame_count_within_distance/fps

    # Distinguish between quick runby's and actual exploratory behavior by means of setting a frame minimum
    # secutive sequences where the condition is met
    time_with_minimum = 0
    frame_count_with_minimum = 0
    
    for distance in distance_to_object:
        if distance <= radius:
            frame_count_with_minimum += 1
        else:
            if frame_count_with_minimum  >= min_frames:
                # Convert frames to seconds
                time_with_minimum += frame_count_with_minimum / fps
            # Reset counter when outside the range
            frame_count_with_minimum  = 0 
    
    # Final check in case the sequence ends within the distance
    if frame_count_with_minimum >= min_frames:
        time_with_minimum += frame_count_with_minimum / fps
    
    return time_with_minimum, total_time_within_distance

def calculate_exploration_time(xnose, ynose, center_x, center_y, radius, xleft, yleft, xright, yright, radius2: float,  fps: float, min_frames=8) -> float:
    """
    Calculate the time spent within a certain distance of a given center point by the specified body part.
    
    Parameters:
        data (pd.DataFrame): DataFrame containing the body part's x, y coordinates per frame.
        center (tuple): A tuple (center_x, center_y) defining the reference point.
        distance (float): The radius within which to measure time spent.
        bp_tracking.t (str): The body part to track (default: 'nose').
        min_frames (int): Minimum consecutive frames within the distance to count time (default: 8).
        fps (float): Frames per second of the recording (default: 25).
        
    Returns:
        float: Time (in seconds) spent within the specified distance.
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