# Compare cut_summary with compiled_data
def compare_cut_summary(compiled_data, cut_summary):
    missing_cuts = {}
    
    for stud, cuts in compiled_data.items():
        if stud not in cut_summary:
            missing_cuts[stud] = "Entire stud missing in cut summary"
            continue
        
        for length, quantity in cuts:
            if length not in cut_summary[stud]:
                if stud not in missing_cuts:
                    missing_cuts[stud] = []
                missing_cuts[stud].append((length, quantity, "Cut missing"))
            elif cut_summary[stud][length] < quantity:
                if stud not in missing_cuts:
                    missing_cuts[stud] = []
                missing_cuts[stud].append((length, quantity, f"Missing {quantity - cut_summary[stud][length]} pieces"))

    # Print the results
    if missing_cuts:
        print("\nMissing Cuts or Quantities:")
        for stud, issues in missing_cuts.items():
            if isinstance(issues, str):
                print(f"{stud}: {issues}")
            else:
                for length, quantity, issue in issues:
                    print(f"{stud}: Length {length}, Quantity {quantity} - {issue}")
    else:
        print("No cuts or quantities are missing from the cut summary.")

    return missing_cuts



