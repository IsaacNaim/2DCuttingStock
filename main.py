import os
import pandas as pd
from Functions.BOMv1excelfiilesparse import compile_final_data
from Functions.GilmoreGomoryCSAlgorithm import ggcutting_stock_algorithm
from Functions.pywraplpCSAlgorithm import or_cuttingstock
from Functions.bestfitCS import cutting_stock
# Define the path to the input files directory
input_files_dir = 'InputFiles'
file_paths = [os.path.join(input_files_dir, file) for file in os.listdir(input_files_dir) if file.endswith('.xlsx') and not file.startswith('~$')]
print(f"Found files: {file_paths}")
# Compile the final data from all BOM files (including post-processing)
compiled_data = compile_final_data(file_paths)
print(compiled_data)
#results = ggcutting_stock_algorithm(compiled_data )
# Run the algorithm
results, waste_percentages = cutting_stock(compiled_data)

# Print the results
for stud, cuts in results.items():
    print(f"Results for {stud}:")
    for cut, waste in cuts:
        print(f"   Cut combination: {cut}, Waste: {waste} inches")
    print()

# Print the waste percentages
print("\nFinal Waste Percentages:")
for stud, waste_percentage in waste_percentages.items():
    print(f"{stud}: {waste_percentage:.2f}%")




