# Import the pandas library for handling CSV file operations
import pandas as pd

# Define a function that joins multiple CSV files into one
def join():
    # List of output file paths (relative paths for different CSV files to be merged)
    outputPaths = [
        "test-text-output-1.csv",
        "test-text-output-2.csv",
        "test-text-output-3.csv",
    ]

    # Store the number of files to be concatenated (for potential use or logging)
    cnt = len(outputPaths)

    # Define the folder path where all the output files are stored
    outputFolderPath = "./dataset/"

    # Create an empty DataFrame that will hold the concatenated data
    df = pd.DataFrame()

    # Iterate through each file path in the outputPaths list
    for outputPath in outputPaths:
        # Create the full path for each CSV file by combining the folder path and file name
        tempPath = outputFolderPath + outputPath
        print(tempPath)  # Print the path being processed (for debugging or progress tracking)

        # Read the current CSV file into a temporary DataFrame
        tempDf = pd.read_csv(tempPath)

        # Concatenate the temporary DataFrame to the main DataFrame 'df'
        df = pd.concat([df, tempDf])

    # Save the final concatenated DataFrame as a new CSV file
    df.to_csv("./final_test_output.csv", index=False)  # Exclude the index from the saved file

# Call the join function to execute the script
join()
