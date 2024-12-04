import pandas as pd

def location_distance(left_list, right_list):
    total_diff = 0
    for l, r in zip(sorted(left_list), sorted(right_list)):
        diff = abs(l - r)
        total_diff += diff

    return total_diff

# Example
left_list = [
    3,   
    4,   
    2,   
    1,   
    3,   
    3 
]

right_list = [
    4,
    3,
    5,
    3,
    9,
    3
]

print("Example:", location_distance(left_list, right_list))

# Actual input
df = pd.read_csv('../input.txt', delimiter='   ', header=None, engine='python')
left_list = df[0].to_list()
right_list = df[1].to_list()

print("Actual input:", location_distance(left_list, right_list))