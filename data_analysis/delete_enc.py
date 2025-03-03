import pandas as pd

# Load the CSV file
input_file = "BN-research-project/data/exploration_results.csv"  # Replace with your actual file name
output_file = "BN-research-project/data/filtered_explorations.csv"  # Output file with only test rows

# Read the CSV file
df = pd.read_csv(input_file)

# Filter rows where 'Video Name' contains 'Test'
filtered_df = df[df["Video Name"].str.contains("Test", case=False, na=False)]

# Save the filtered DataFrame to a new CSV file
filtered_df.to_csv(output_file, index=False)

print(f"Filtered CSV saved as {output_file}")