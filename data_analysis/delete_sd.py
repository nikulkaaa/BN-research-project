import pandas as pd

# File path (replace with your file name)
input_file = "BN-research-project/data/nika_data.csv"  # The file with added 'Sex', 'Sleep', and 'Cycle' columns
output_file = "BN-research-project/data/jesse_data.csv"  # Output file without SD groups

# Load the data
df = pd.read_csv(input_file)

# Remove rows where 'Sleep' is 'SD'
df_filtered = df[df["Sleep"] != "SD"]

# Save the filtered file
df_filtered.to_csv(output_file, index=False)

print(f"Filtered file saved as {output_file}")