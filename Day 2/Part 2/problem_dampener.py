import pandas as pd

def check_direction_of_change(a, b):
    if a - b > 0:
        direction = '+' # Increasing
    elif a - b < 0 :
        direction = '-' # Decreasing
    else:
        direction = None

    return direction

def calculate_safe_reports(rows: list):
    safe_reports = 0
    for i in rows:
        safe_report = 1 # Store report result (true by default)

        # Iterate over all pairs of adjacent numbers
        for j in range(len(i)-1):
            curr_num = int(i[j])
            next_num = int(i[j+1])

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
            
        safe_reports += safe_report

    return safe_reports


# Example
with open('../example.txt', 'r') as f:
    example_rows = [line.strip().split() for line in f]

print("Example:", calculate_safe_reports(example_rows))

# Input
with open('../input.txt', 'r') as f:
    input_rows = [line.strip().split() for line in f]

print("Input:", calculate_safe_reports(input_rows))