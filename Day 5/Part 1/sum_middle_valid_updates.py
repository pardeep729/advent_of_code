import pandas as pd

def sum_middle_valid_updates(updates_rel_fp, rules_rel_fp):
    """
    Given relative filepath to the updates and the rules files, calculate the sum of the middle values of updates that are valid (based on the rules given)
    """
    # Load updates
    with open(updates_rel_fp, 'r') as file:
        updates = file.read()

    # Split content into list of lists
    updates_list = [line.split(',') for line in updates.strip().split('\n')]

    # Converting the string values to integers
    updates_list = [[int(value) for value in line] for line in updates_list]

    # Load rules into dataframe
    rules_df = pd.read_csv(rules_rel_fp, delimiter='|', header=None, names=["First", "After"])

    total_middle_vals = 0 # Keep track of total sum of middle values of valid updates 
    # Evaluate each update
    for u in updates_list:
        # Only look at relevant rules
        related_rules_df = rules_df[rules_df["First"].isin(u) & rules_df["After"].isin(u)] 

        # Put pos of each value in each rule in table (or None if doesn't exist)
        related_rules_df = related_rules_df.copy() # Fix warning with DFs
        for c in ["First", "After"]:
            related_rules_df.loc[:, f"{c} Pos"] = rules_df[c].apply(lambda x: u.index(x) if x in u else None) 
        
        # Evaluate if any rules broken
        update_valid = (related_rules_df["First Pos"] < related_rules_df["After Pos"]).all() # True if all rules fine, False if at least 1 rule broken
        if update_valid:
            middle_pos = int((len(u)-1)/2) # Get middle position
            total_middle_vals += u[middle_pos]# Add to running total

    return total_middle_vals

# Example
print(sum_middle_valid_updates('../example_updates.txt', '../example_rules.txt'))

# Real input
print(sum_middle_valid_updates('../input_updates.txt', '../input_rules.txt'))