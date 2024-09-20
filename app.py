# Import necessary components from langchain_core and langchain_ollama for handling prompts and models
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

# Optional imports that are currently commented out but can be used for alternative models or environment setup
# from langchain_groq import ChatGroq
import re  # Regular expressions for pattern matching in text
import pandas as pd  # For data manipulation using DataFrames
import numpy as np  # For numerical operations (currently unused but often useful in data processing)
# from dotenv import load_dotenv  # For loading environment variables from a .env file (commented out)

# Define a function that processes the context and entity name, and extracts numerical and unit information
def findAndFromContext(context, entityName):
    # Template string to be used in the prompt, which includes placeholders for context and question.
    # The prompt format ensures that the answer should include both a numerical value and a unit, matching specific formats.
    template = """
        Context: {context}
        Question: {question}

        Context contains the text extracted from an image. Use the given context to give answer to the question asked. Answer should be in the format: --numerical_value--, --unit--. For example, if the answer is 5 grams, then the answer should be written as: --5.0--, --gram--.
        "unit" should be written as it is one of the following: gram, cup, milligram, kilogram, ounce, gallon, volt, watt, pound, millilitre, foot, ton, decilitre, inch, litre, microgram, centimetre, quart, horsepower, kilowatt, hour, gigabyte, millimetre, pint, centilitre, metre, carat, nits

        Answer:
    """

    # Creating a ChatPromptTemplate using the above template string
    prompt = ChatPromptTemplate.from_template(template)

    # Initialize the ChatOllama model to process the input context and generate an answer.
    # The model used is 'gemma2:2b', but other models can be substituted (commented out alternatives).
    model = ChatOllama(model="gemma2:2b", temperature=0.5)  # Temperature controls the creativity of responses.

    # Combine the prompt and model into a chain where the prompt is fed into the model.
    chain = prompt | model

    # Construct a question specific to the entity (e.g., "Numerical value as floating integer of <entityName>")
    question = f"Numerical value as floating integer of {entityName}."

    # Invoke the chain with the provided context and generated question.
    # The result contains the model's response based on the input.
    result = chain.invoke({"context": context, "question": question})
    print(result.content)  # Print the model's response for debugging or inspection.

    # Use regular expressions to extract the numerical value and unit from the result, based on the expected format.
    matches = re.findall(r'\-\-(.*?)\-\-', result.content)
    print(matches)  # Print the extracted matches for debugging.

    # If two matches (number and unit) are found, return them combined as a string.
    if len(matches) == 2:
        return matches[0] + " " + matches[1]
    else:
        return ""  # Return an empty string if the required format is not found.


# Load CSV data into a pandas DataFrame for processing
df1 = pd.read_csv('./dataset/test-text-input-3.csv')
outputPath = './dataset/test-text-output-3.csv'

# Create a copy of the DataFrame to avoid modifying the original data.
# Initialize a new column to store the extracted answers (entity values).
df = df1.copy()  # Change the slice if needed
df['ans_entity_val'] = ""  # Initialize the new column

# Loop through each row in the DataFrame
for i in range(len(df)):
    entityName = df['entity_name'][i]  # Get the entity name from the current row
    context = df['extracted_text'][i]  # Get the extracted context (text) from the current row

    # Call the function 'findAndFromContext' to process the context and extract the numerical value and unit.
    ans = findAndFromContext(context, entityName)

    # Safely update the DataFrame with the extracted answer for the current row using .loc[].
    df.loc[i, 'ans_entity_val'] = ans

    # Save the updated DataFrame every 10 iterations to avoid losing progress.
    if (i + 1) % 10 == 0:
        print(f"Saving progress at iteration {i+1}")
        df10 = df[['index', 'ans_entity_val']]  # Select the columns to save
        df10.to_csv(outputPath, index=False)  # Save the partial results to CSV

# After processing all rows, save the final DataFrame to the CSV file.
df10 = df[['index', 'ans_entity_val']]  # Select the columns to save
df10.to_csv(outputPath, index=False)  # Save the final result to the output CSV
