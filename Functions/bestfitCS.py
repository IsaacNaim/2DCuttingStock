import itertools

# Function to extract the standard length from the stud name
def extract_standard_length(name):
    # Split by 'x' and take the last element, then multiply by 12
    length = int(name.split('x')[-1]) * 12
    return length

# Implement the cutting stock algorithm
def cutting_stock(cuts_dict):
    results = {}
    waste_percentages = {}
    
    for stud, cuts in cuts_dict.items():
        standard_length = extract_standard_length(stud)
        results[stud] = []
        total_waste = 0
        total_combinations = 0
        
        # Flatten the cuts into individual pieces
        flat_cuts = []
        for length, quantity in cuts:
            flat_cuts.extend([length] * quantity)
        
        # Sort cuts by length in descending order for better fitting
        flat_cuts.sort(reverse=True)
        
        while flat_cuts:
            remaining_length = standard_length
            used_cuts = []
            
            # Try to fit as many cuts as possible into the standard length
            for cut in flat_cuts[:]:
                if cut <= remaining_length:
                    used_cuts.append(cut)
                    remaining_length -= cut
                    flat_cuts.remove(cut)
            
            # Record the cuts made and the remaining waste
            results[stud].append((used_cuts, remaining_length))
            total_waste += remaining_length
            total_combinations += 1
        
        # After processing, ensure all quantities were fulfilled
        unused_cuts = flat_cuts
        if unused_cuts:
            print(f"Warning: Some cuts were not used for {stud}: {unused_cuts}")
            # Implement a best-fit algorithm to handle these unused cuts
            
            # Example of handling unused cuts with additional studs
            additional_studs = []
            while unused_cuts:
                remaining_length = standard_length
                used_cuts = []
                
                for cut in unused_cuts[:]:
                    if cut <= remaining_length:
                        used_cuts.append(cut)
                        remaining_length -= cut
                        unused_cuts.remove(cut)
                
                additional_studs.append((used_cuts, remaining_length))
                total_waste += remaining_length
                total_combinations += 1
            
            results[stud].extend(additional_studs)
        
        # Calculate the waste percentage for this stud type
        total_material_used = total_combinations * standard_length
        waste_percentage = (total_waste / total_material_used) * 100
        waste_percentages[stud] = waste_percentage
    
    return results, waste_percentages


