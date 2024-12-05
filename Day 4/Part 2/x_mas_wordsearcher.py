import re

pattern = "MAS"

def no_of_occurences_of_pattern_in_string(pattern, word):
    matches = [m.start() for m in re.finditer(pattern, word)] # Look in forward direction
    matches += [m.start() for m in re.finditer(pattern, word[::-1])] # Look in reverse direction
    return len(matches)

def x_mas_wordsearcher(pattern, grid_rows):
    total_occurences = 0

    rows = len(grid_rows)
    cols = len(grid_rows[0][0])
    for r in range(rows - len(pattern) + 1):
        for c in range(cols - len(pattern) + 1):
            # Generate each 3x3 grid in the wider grid
            mini_grid = [
                [grid_rows[r][0][c],   grid_rows[r][0][c+1],   grid_rows[r][0][c+2]  ],
                [grid_rows[r+1][0][c], grid_rows[r+1][0][c+1], grid_rows[r+1][0][c+2]],
                [grid_rows[r+2][0][c], grid_rows[r+2][0][c+1], grid_rows[r+2][0][c+2]]
            ]

            # Define each max diagonal
            ld = ''.join([mini_grid[0][0], mini_grid[1][1], mini_grid[2][2]])
            rd = ''.join([mini_grid[0][2], mini_grid[1][1], mini_grid[2][0]])

            # Count occurences of X-MAS
            total_occurences += 1 if no_of_occurences_of_pattern_in_string(pattern, ld) == 1 and no_of_occurences_of_pattern_in_string(pattern, rd) == 1 else 0

    return total_occurences

# Example
with open('../example.txt', 'r') as f:
    example_rows = [line.strip().split() for line in f]

print("Example:", x_mas_wordsearcher(pattern, example_rows))

# Actual input
with open('../input.txt', 'r') as f:
    input_rows = [line.strip().split() for line in f]

print("Actual input:", x_mas_wordsearcher(pattern, input_rows))