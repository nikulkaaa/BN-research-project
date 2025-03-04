import pandas as pd

def process_csv(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Group by unique identifiers and calculate Index as moved / (non-moved + moved)
    def calculate_index(group):
        moved = group.loc[group["ROI Name"] == "moved", "Exloration Time (s)"].sum()
        total = group["Exloration Time (s)"].sum()
        return moved / total if total > 0 else 0
    
    df_grouped = df.groupby(["Video Name", "Sex", "Sleep", "Cycle"]).apply(calculate_index).reset_index(name="Index")
    
    # Save to new CSV file
    df_grouped.to_csv(output_file, index=False)
    print(f"Processed file saved as: {output_file}")

# Example usage
input_csv = "BN-research-project/data/full_explorations.csv"  # Change this to your actual filename
output_csv = "BN-research-project/data/clean_explorations.csv"
process_csv(input_csv, output_csv)

