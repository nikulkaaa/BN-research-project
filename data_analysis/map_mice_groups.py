import pandas as pd

# File paths (replace with actual file names)
filtered_file = "BN-research-project/data/object_exploration.csv"  # The test-only CSV
mapping_file = "BN-research-project/data_analysis/mice_groups.csv"  # The file containing sex, sleep, and cycle info
output_file = "BN-research-project/data/full_explorations.csv"  # Output file with new columns added

# Load the filtered test trials CSV
df_filtered = pd.read_csv(filtered_file)

# Load the mapping CSV
df_mapping = pd.read_csv(mapping_file)

# Rename 'Group_SD' to 'Sleep' for consistency
df_mapping = df_mapping.rename(columns={"Group_SD": "Sleep"})

# Extract the mouse identifier (second word) from 'Video Name'
df_filtered["Mouse"] = df_filtered["Video Name"].str.split().str[1]

# Convert both 'Mouse' columns to lowercase to avoid case mismatches
df_filtered["Mouse"] = df_filtered["Mouse"].str.lower()
df_mapping["Mouse"] = df_mapping["Mouse"].str.lower()

# Merge the dataframes on the 'Mouse' column
df_merged = pd.merge(df_filtered, df_mapping[["Mouse", "Sex", "Sleep", "cycle"]], on="Mouse", how="left")

# Rename 'cycle' to 'Cycle'
df_merged = df_merged.rename(columns={"cycle": "Cycle"})

# Reorder columns to place 'Sex', 'Sleep', and 'Cycle' right after 'Video Name'
cols = ["Video Name", "Sex", "Sleep", "Cycle"] + [col for col in df_merged.columns if col not in ["Video Name", "Sex", "Sleep", "Cycle", "Mouse"]]
df_merged = df_merged[cols]

# Save the annotated DataFrame
df_merged.to_csv(output_file, index=False)

print(f"Annotated CSV saved as {output_file}")
