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
