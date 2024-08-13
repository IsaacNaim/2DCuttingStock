import os
import pandas as pd
from Functions.BOMv1excelfiilesparse import compile_final_data
from Functions.GilmoreGomoryCSAlgorithm import ggcutting_stock_algorithm
from Functions.pywraplpCSAlgorithm import or_cuttingstock
from Functions.bestfitCS import cutting_stock
from Functions. missingcutcheck import compare_cut_summary
# Define the path to the input files directory
input_files_dir = 'InputFiles'
file_paths = [os.path.join(input_files_dir, file) for file in os.listdir(input_files_dir) if file.endswith('.xlsx') and not file.startswith('~$')]
print(f"Found files: {file_paths}")
# Compile the final data from all BOM files (including post-processing)
compiled_data = compile_final_data(file_paths)
print(compiled_data)
#results = ggcutting_stock_algorithm(compiled_data )
# Run the algorithm
# Run the algorithm
final_results, waste_percentages, cut_summary = cutting_stock(compiled_data)

# Print the results
for stud, cuts in final_results.items():
    print(f"Results for {stud}:")
    for cut, waste in cuts:
        print(f"   Cut combination: {cut}, Waste: {waste} inches")
    print()

# Print the waste percentages
print("\nFinal Waste Percentages:")
for stud, waste_percentage in waste_percentages.items():
    print(f"{stud}: {waste_percentage:.2f}%")

# Print the cut summary
print("\nSummary of Cuts Used:")
for stud, summary in cut_summary.items():
    print(f"{stud}: {summary}")

# Get the missing cuts and quantities
missing_cuts = compare_cut_summary(compiled_data, cut_summary)


# Convert dictionaries to DataFrames for Excel export
def dict_to_df(dictionary):
    return pd.DataFrame.from_dict(dictionary, orient='index')

# Prepare data for export
final_results_df = pd.concat({k: pd.DataFrame(v, columns=['Cut Combination', 'Waste']) for k, v in final_results.items()}, axis=0)
final_results_df.index.names = ['Stud', 'Combination']

waste_percentages_df = dict_to_df(waste_percentages)
waste_percentages_df.columns = ['Waste Percentage']

cut_summary_df = pd.concat({k: pd.Series(v) for k, v in cut_summary.items()}, axis=1).T
cut_summary_df.index.name = 'Stud'

# Define the output file path
output_folder = os.path.join(os.getcwd(), 'OutputFiles')
output_file = os.path.join(output_folder, 'cutting_stock_results.xlsx')
if missing_cuts:
    missing_cuts_df = pd.concat({k: pd.DataFrame(v, columns=['Length', 'Quantity', 'Issue']) for k, v in missing_cuts.items() if isinstance(v, list)}, axis=0)
    missing_cuts_df.index.names = ['Stud', 'Issue Index']
    with pd.ExcelWriter(output_file) as writer:
        final_results_df.to_excel(writer, sheet_name='Final Results')
        waste_percentages_df.to_excel(writer, sheet_name='Waste Percentages')
        cut_summary_df.to_excel(writer, sheet_name='Cut Summary')
        missing_cuts_df.to_excel(writer, sheet_name='Missing Cuts')
else:
    with pd.ExcelWriter(output_file) as writer:
        final_results_df.to_excel(writer, sheet_name='Final Results')
        waste_percentages_df.to_excel(writer, sheet_name='Waste Percentages')



