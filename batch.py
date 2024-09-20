# Import the pandas library for handling data operations
import pandas as pd

# Define the main function where the dataset will be split into smaller CSV files
def main():
    # Read the input CSV file into a pandas DataFrame
    df1 = pd.read_csv("./dataset/test_text_final.csv")
    
    # Make a copy of the DataFrame to avoid modifying the original
    df = df1.copy()
    
    # Reset the index of the DataFrame to ensure it's sequential, without keeping the old index
    df.reset_index(drop=True, inplace=True)

    # Get the total number of rows in the DataFrame
    rows = len(df)
    
    # Calculate how many full batches of 10,000 rows can be made using integer division
    batches = rows // 10000

    # Loop through the range of batches and include the last partial batch (if any) by adding 1
    for i in range(batches + 1):
        startInd = i * 10000  # Starting index for the current batch
        endInd = (i + 1) * 10000  # Ending index for the current batch
        
        # Slice the DataFrame to create a batch with rows from startInd to endInd
        batch_df = df[startInd:endInd]
        
        # Save the batch as a CSV file using an f-string to dynamically generate the filename.
        # The index is excluded because it's not needed in the output CSV file.
        batch_df.to_csv(f"./dataset/test-text-input-{i+1}.csv", index=False)

# Call the main function to execute the script
main()
