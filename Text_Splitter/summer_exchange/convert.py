# Define the input and output file paths
import re

# Define the input and output file paths
input_file_path = 'summer_exchange_info.txt'
output_file_path = 'output.txt'

# Read the input file
with open(input_file_path, 'r') as input_file:
    text = input_file.read()

# Reduce consecutive spaces to a single space
text = re.sub('\s+', ' ', text)

# Write the modified text to the output file
with open(output_file_path, 'w') as output_file:
    output_file.write(text)