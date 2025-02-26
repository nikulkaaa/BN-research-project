import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib
import glob

matplotlib.use('Agg')

from functions_for_DLC_analysis import get_bodyparts, create_rois, get_exploration_time

st.title("DLC Exploration Time Analysis")

# Upload video_data.csv file
video_data_file = st.file_uploader("Upload your video_data.csv file. If you don't have it yet, run set_ratios.ipynb first.", type=["csv"])

if video_data_file is not None:
    video_data = pd.read_csv(video_data_file)
    st.write("### Uploaded Video Data:")
    st.dataframe(video_data)

    # Get body parts and ROI names from user input
    bpt_plus_names = [name.strip() for name in st.text_area("Body parts to track (comma-separated)", "nose").split(',')]
    bpt_minus_names = [name.strip() for name in st.text_area("Body parts to subtract (comma-separated)", "left-front-paw, right-front-paw").split(',')]
    rois_names = [name.strip() for name in st.text_area("ROI names (comma-separated)", "non-moved object, moved object").split(',')]

    boundary_size_distance = st.number_input("Boundary size distance (cm)", value=1)
    fps = st.number_input("Frames per second (fps)", value=25.0)

    # Manually input the folder path
    folder_path = st.text_input("Enter the folder path containing the .h5 files")

    if folder_path:
        # Save in session state
        st.session_state.folder_path = folder_path
        st.success(f"Folder manually set: {folder_path}")

        # Ensure the folder exists
        if not os.path.exists(folder_path):
            st.error("The specified folder does not exist. Please enter a valid path.")
        else:
            # Get a list of all .h5 files in the folder
            h5_files = glob.glob(os.path.join(folder_path, "*.h5"))

            if not h5_files:  # If no .h5 files are found
                st.error("No .h5 files found in the selected folder. Please select a folder containing valid .h5 files.")
            else:
                # Proceed with analysis
                results = []
                video_names = video_data['videoname']
                cm_to_pixel_ratios = [float(i) for i in video_data['cm_to_pixel_ratio']]
                DLCscorer = 'DLC_resnet50_BN research projectFeb3shuffle1_54500'

                for video, ratio in zip(video_names, cm_to_pixel_ratios):
                    st.write(f"### Processing Video: {video}")
                    h5_file_path = os.path.join(folder_path, f"{video}{DLCscorer}.h5")

                    if not os.path.exists(h5_file_path):
                        st.error(f"File not found: {h5_file_path}")
                        continue

                    try:
                        df = pd.read_hdf(h5_file_path)
                        rois = create_rois(df=df, DLCscorer=DLCscorer, distance=boundary_size_distance, names=rois_names, cm_to_pixel_ratio=ratio)
                        rois_substracting = create_rois(df=df, DLCscorer=DLCscorer, distance=0, names=rois_names, cm_to_pixel_ratio=ratio)
                        bpt_plus = get_bodyparts(df=df, DLCscorer=DLCscorer, fps=fps, bpt_names=bpt_plus_names)
                        bpt_minus = get_bodyparts(df=df, DLCscorer=DLCscorer, fps=fps, bpt_names=bpt_minus_names)

                        explorationn = get_exploration_time(rois, rois_substracting, bpt_plus, bpt_minus, fps)

                        for exp in explorationn:
                            results.append({
                                "Video Name": video,
                                "ROI Name": exp.get("name"),
                                "Exploration Time (s)": exp.get("exploration time"),
                                "cm_to_pixel_ratio": ratio
                            })

                            st.write(f"Total Exploration Time for {exp.get('name')}: {exp.get('exploration time')}s")

                    except Exception as e:
                        st.error(f"Error processing {video}: {str(e)}")

                # Display results in a DataFrame
                if results:
                    results_df = pd.DataFrame(results)
                    st.dataframe(results_df)

                    # Let the user specify a filename for the CSV download
                    # Ensure custom filename is stored in session state
                    if "custom_filename" not in st.session_state:
                        st.session_state["custom_filename"] = "exploration_results"

                    # Create an input box for filename
                    custom_filename = st.text_input("Enter a filename for the results (without extension)", value=st.session_state["custom_filename"]).strip()

                    # Only update session state if the input is different
                    if custom_filename and custom_filename != st.session_state["custom_filename"]:
                        st.session_state["custom_filename"] = custom_filename

                    # Ensure filename has .csv extension
                    final_filename = f"{st.session_state['custom_filename']}.csv"

                    # Convert results to CSV
                    csv = results_df.to_csv(index=False).encode("utf-8")

                    # Display the download button
                    st.download_button(
                        label="Download Results as CSV",
                        data=csv,
                        file_name=final_filename,
                        mime="text/csv"
                    )

                    # Debugging: Show what filename is being used
                    st.write(f"Saving file as: {final_filename}")

