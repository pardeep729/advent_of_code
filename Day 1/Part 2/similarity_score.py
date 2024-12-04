import pandas as pd

def calculate_similarity_score(left_list, right_list):
    total_similarity_score = 0
    for i in left_list:
        similarity_score = i * right_list.count(i)
        total_similarity_score += similarity_score

    return total_similarity_score

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

print("Example:", calculate_similarity_score(left_list, right_list))

# Actual input
df = pd.read_csv('../input.txt', delimiter='   ', header=None, engine='python')
left_list = df[0].to_list()
right_list = df[1].to_list()

print("Actual input:", calculate_similarity_score(left_list, right_list))