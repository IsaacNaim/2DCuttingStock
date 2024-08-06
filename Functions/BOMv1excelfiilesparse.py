import pandas as pd
import re
from collections import defaultdict, Counter

def parse_combination_string(combination_string):
    """Parses the combination string to extract numbers and their quantities."""
    pattern = re.compile(r'\d+\(([\d.]+)\)')
    return [float(match) for match in pattern.findall(combination_string)]

def find_combination_headers(df):
    """Finds all rows in the DataFrame containing the target column header."""
    headers = []
    target_column = 'Combination - Serial Number (LF actual inches) '
    for i, row in df.iterrows():
        if target_column in row.values:
            headers.append(i)
    return headers

def process_bom_file(file_path):
    """Processes a BOM Excel file and extracts the required data."""
    try:
        df = pd.read_excel(file_path, sheet_name='Stud - Wastage Calc', header=None, engine='openpyxl')
        headers = find_combination_headers(df)


        if not headers:
            print(f"No headers found in file: {file_path}")
            return {}

        data_sections = {}

        for header in headers:
            name_cell = df.iat[header, 0]
            section_name = str(name_cell).replace(' ', '').replace("'", "")
            start_row = header + 1

            # Collect data until the next header or the end of the DataFrame
            data = []
            for i in range(start_row, len(df)):
                if i in headers:  # Stop if we encounter another header
                    break
                if pd.notna(df.iat[i, 2]):
                    data.append(parse_combination_string(df.iat[i, 2]))

            if section_name not in data_sections:
                data_sections[section_name] = []
            data_sections[section_name].append(data)  # Append the new list of lists

        return data_sections

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return {}

def post_process_data(compiled_data):
    """Transforms each list of lists into a list of unique numbers and their occurrences."""
    processed_data = {}
    for section_name, lists in compiled_data.items():
        combined_counter = Counter()
        for sublist in lists:
            for item in sublist:  # Flatten the sublist
                combined_counter.update(item)
        processed_data[section_name] = [[num, count] for num, count in combined_counter.items()]
    return processed_data

def compile_final_data(file_paths):
    """Compiles the final numbers and their total quantities from all BOM files and post-processes them."""
    compiled_data = defaultdict(list)
    for file_path in file_paths:
        data_sections = process_bom_file(file_path)
        for section_name, data in data_sections.items():
            compiled_data[section_name].extend(data)
    post_processed_data = post_process_data(compiled_data)
    sortedppdata = change_order_of_dict(sort_compiled_data(post_processed_data))
    sortedppdata = adjust_stud_dict_values(sortedppdata)
    sortedppdata = rename_stud_dict_keys(sortedppdata)
    if sortedppdata:
        for section_name, data in sortedppdata.items():
            #print(f"Compiled Data for {section_name}:")
            for item in data:
                #print(f"{item[0]}: {item[1]}")
                continue
    # Save the processed data to an Excel file
        output_file = 'processed_input_data_bomv1.xlsx'
        save_to_excel(sortedppdata, output_file)
        print(f"Processed data saved to {output_file}")
    else:
        print("No data compiled.")
    return sortedppdata

def sort_compiled_data(compiled_data):
    """Sorts each list of lists by the first value in each sublist."""
    sorted_data = {}
    for section_name, data in compiled_data.items():
        sorted_data[section_name] = sorted(data, key=lambda x: x[0])
    return sorted_data

def save_to_excel(processed_data, output_file):
    """Saves the processed data to an Excel file with each list of lists in its own column."""
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        df = pd.DataFrame()
        for section_name, data in processed_data.items():
            # Create a DataFrame for the current section
            section_df = pd.DataFrame(data, columns=[section_name, 'Count'])
            # Append to the main DataFrame
            df = pd.concat([df, section_df], axis=1)

        # Write the DataFrame to an Excel sheet
        df.to_excel(writer, sheet_name='Processed Data', index=False)

def change_order_of_dict(compiled_data):
    # Sort the dictionary keys such that 'Stud2x4' keys come first
    sorted_keys = sorted(compiled_data.keys(), key=lambda x: (not x.startswith('Stud2x4'), x))
    # Create a DataFrame to hold the sorted lists
    new_dict = {}
    # Insert the sorted lists into the DataFrame
    for key in sorted_keys:
        new_dict[key] = compiled_data[key]
    return new_dict

def adjust_stud_dict_values(stud_dict):
    # Iterate through the dictionary
    for key in stud_dict:
        for sublist in stud_dict[key]:
            # Check if the key is 'Stud2x48Count' or 'Stud2x68Count' and the value is 96
            if key in ['Stud2x48Count', 'Stud2x68Count'] and sublist[0] == 96:
                sublist[0] *= 1000
            else:
                sublist[0] += 0.125  # Add 0.125 to the first item in the sublist
                sublist[0] *= 1000

    return stud_dict

def rename_stud_dict_keys(stud_dict):
    renamed_dict = {}
    for key in stud_dict:
        # Remove 'Count' from the key
        new_key = key.replace('Count', '')
        # Add 'x' after the number that comes after 'x4' or 'x6'
        if 'x4' in new_key:
            new_key = new_key.replace('x4', 'x4x')
        elif 'x6' in new_key:
            new_key = new_key.replace('x6', 'x6x')
        renamed_dict[new_key] = stud_dict[key]
    return renamed_dict