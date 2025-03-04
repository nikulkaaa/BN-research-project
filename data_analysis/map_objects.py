import pandas as pd

# Load the first dataset (exploration times)
file1 = "BN-research-project/data/exploration_with_object_estimation.csv"  # Replace with actual filename
df1 = pd.read_csv(file1)

# Load the second dataset (moved/non-moved mapping)
file2 = "BN-research-project/data_analysis/mapping_objects.csv"  # Replace with actual filename
df2 = pd.read_csv(file2)

# Merge the datasets on 'video_name' and 'roi_name'
merged_df = df1.merge(df2, on=['video_name', 'roi_name'], how='left')

# Save the merged dataset
output_file = "BN-research-project/data/object_exploration.csv"
merged_df.to_csv(output_file, index=False)

print(f"Merged data saved to {output_file}")
