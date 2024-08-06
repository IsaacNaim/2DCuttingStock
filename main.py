import os
import pandas as pd
from Functions.BOMv1excelfiilesparse import compile_final_data
from Functions.GilmoreGomoryCSAlgorithm import ggcutting_stock_algorithm

# Define the path to the input files directory
input_files_dir = 'InputFiles'
file_paths = [os.path.join(input_files_dir, file) for file in os.listdir(input_files_dir) if file.endswith('.xlsx') and not file.startswith('~$')]
print(f"Found files: {file_paths}")
# Compile the final data from all BOM files (including post-processing)
compiled_data = compile_final_data(file_paths)
print(compiled_data)
results = ggcutting_stock_algorithm(compiled_data)
# Display the results
for key, value in results.items():
    print(f"Results for {key}:")
    for roll in value:
        print(f"  Roll: {roll}")
    print()
