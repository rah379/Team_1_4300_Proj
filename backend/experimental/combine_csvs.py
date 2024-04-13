import os
import pandas as pd


def concatenate_csv_files(folder_path, output_file):
    # Get a list of all CSV files in the folder
    csv_files = [file for file in os.listdir(
        folder_path) if file.endswith('.csv')]

    # Check if there are any CSV files in the folder
    if not csv_files:
        print("No CSV files found in the specified folder.")
        return

    # Read the first CSV file to get the header
    first_file_path = os.path.join(folder_path, csv_files[0])
    header = pd.read_csv(first_file_path, nrows=0).columns.tolist()

    # Initialize an empty DataFrame to store concatenated data
    concatenated_data = pd.DataFrame(columns=header)

    # Iterate through all CSV files and concatenate them
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        df = pd.read_csv(file_path)
        concatenated_data = pd.concat(
            [concatenated_data, df], ignore_index=True)

    # Write the concatenated data to a new CSV file
    concatenated_data.to_csv(output_file, index=False)
    print(f"Concatenated data saved to {output_file}")


# Example usage:
folder_path = './data'
output_file = 'concatenated_data.csv'
concatenate_csv_files(folder_path, output_file)
