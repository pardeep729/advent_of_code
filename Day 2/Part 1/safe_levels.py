import pandas as pd

def check_direction_of_change(a, b):
    if a - b > 0:
        direction = '+' # Increasing
    elif a - b < 0 :
        direction = '-' # Decreasing
    else:
        direction = None

    return direction

def calculate_safe_reports_with_problem_dampner(rows: list):
    total_safe_reports = 0
    for i in rows:
        max_reports_versions = len(i)+1 # Max number of report versions possible
        safe_reports = max_reports_versions # Start with all report versions being safe

        # Iterate over all versions of the report (All version where omitting 1 level each time + full version)
        for k in range(max_reports_versions):
            report_iteration = [e for idx, e in enumerate(i) if idx != k]

            safe_report = 1 # Start with this version of report being safe
            # Iterate over all pairs of adjacent numbers
            for j in range(len(report_iteration)-1):
                curr_num = int(report_iteration[j])
                next_num = int(report_iteration[j+1])

                # For first 2 values, check direction of change
                if j == 0:
                    report_direction = check_direction_of_change(curr_num, next_num)
                    if report_direction is None:
                        safe_report = 0 # Adjacent levels must differ by at least 1 

                # Check if current pair direction not same as first
                current_direction = check_direction_of_change(curr_num, next_num)
                if report_direction != current_direction:
                    safe_report = 0 # Direction of change is not consistent

                # Check if value is less than 1 or greater than 3
                diff = abs(curr_num - next_num) 
                if diff < 1 or diff > 3:
                    safe_report = 0 # Change too large
                
            safe_reports -= 1 if safe_report == 0 else 0 # Remove report from max report versions safe counter if not safe 
        
        total_safe_reports += 1 if safe_reports > 0 else 0 # Consider the report safe is at least 1 version safe

    return total_safe_reports


# Example
with open('../example.txt', 'r') as f:
    example_rows = [line.strip().split() for line in f]

print("Example:", calculate_safe_reports_with_problem_dampner(example_rows))

# Input
with open('../input.txt', 'r') as f:
    input_rows = [line.strip().split() for line in f]

print("Input:", calculate_safe_reports_with_problem_dampner(input_rows))