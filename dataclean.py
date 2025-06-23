import pandas as pd
import re

# Load the Excel file
file_path = 'Bangladeshi/bdjobs_data.xlsx'  # Replace with your file path
data = pd.read_excel(file_path)

# 1. Delete Empty Fields (rows with NaN values in the 'Skills' column)
data_cleaned = data.dropna(subset=['Skills'])

# 2. Remove Rows with Bangla Text in "Job Title" Column Only
# Define a function to detect Bangla text in a string
def contains_bangla(text):
    # Check if any character in the text belongs to the Bengali Unicode range
    return bool(re.search('[\u0980-\u09FF]', str(text)))

# Filter out rows where the "Job Title" column contains Bangla text
data_cleaned = data_cleaned[~data_cleaned['Job Title'].apply(contains_bangla)]

# Save the cleaned data to a new Excel file
cleaned_file_name = 'cleaned_data.xlsx'
data_cleaned.to_excel(cleaned_file_name, index=False)

# Display a sample of the cleaned data
print(data_cleaned.head())
