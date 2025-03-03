import pandas as pd

def process_csv(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Group by unique identifiers and calculate Index
    df_grouped = df.groupby(["Video Name", "Sex", "Sleep", "Cycle"]).apply(
        lambda x: (x["Exploration Time (s)"].iloc[0] / x["Exploration Time (s)"].sum())
    ).reset_index(name="Index")
    
    # Save to new CSV file
    df_grouped.to_csv(output_file, index=False)
    print(f"Processed file saved as: {output_file}")

# Example usage
input_csv = "BN-research-project/data/jesse_data.csv"  # Change this to your actual filename
output_csv = "BN-research-project/data/clean_jesse_data.csv"
process_csv(input_csv, output_csv)
