import re

pattern = "XMAS"

def no_of_occurences_of_pattern_in_string(pattern, word):
    matches = [m.start() for m in re.finditer(pattern, word)] # Look in forward direction
    matches += [m.start() for m in re.finditer(pattern, word[::-1])] # Look in reverse direction
    return len(matches)

def rotate_grid_45(grid, flip=True):
    """
    Rotate a grid of characters 45 degrees.
    """

    # Convert input to proper grid format (if single strings per row)
    grid = [list(row[0]) for row in grid]
    
    rows = len(grid)
    cols = len(grid[0])

    # Determine the range of keys based on `flip`
    if flip:
        # For i + j, keys range from 0 to rows + cols - 2
        diagonals = [[] for _ in range(rows + cols - 1)]
        for i in range(rows):
            for j in range(cols):
                key = i + j
                diagonals[key].append(grid[i][j])
    else:
        # For i - j, keys range from -(cols - 1) to (rows - 1)
        diagonals = {}
        for i in range(rows):
            for j in range(cols):
                key = i - j
                if key not in diagonals:
                    diagonals[key] = []
                diagonals[key].append(grid[i][j])
        diagonals = [diagonals[key] for key in sorted(diagonals.keys())]

    # Convert diagonals into strings
    rotated_grid = ["".join(diag) for diag in diagonals]

    return rotated_grid

def xmas_wordsearcher(pattern, rows):
    # Keep track of occurrences of word
    occurences = 0

    # Find all horizontal instances of word
    for i in rows:
        # print(i)
        occurences += no_of_occurences_of_pattern_in_string(pattern, i[0])

    # Find all vertical instances of word
    split_rows = [list(row[0]) for row in rows] # Split strings into lists of characters
    transposed = list(map(list, zip(*split_rows))) # Transpose using zip

    # Print the result
    for t in transposed:
        # print(''.join(t))
        occurences += no_of_occurences_of_pattern_in_string(pattern, ''.join(t))

    # Find all diagonal instances of word
    ## Left diagonal
    for ld in rotate_grid_45(rows, flip=True):
        occurences += no_of_occurences_of_pattern_in_string(pattern, ld)
    ## Right diagonal
    for rd in rotate_grid_45(rows, flip=False):
        occurences += no_of_occurences_of_pattern_in_string(pattern, rd)

    return occurences


# Example
with open('../example.txt', 'r') as f:
    example_rows = [line.strip().split() for line in f]

print("Example:", xmas_wordsearcher(pattern, example_rows))

# Actual input
with open('../input.txt', 'r') as f:
    input_rows = [line.strip().split() for line in f]

print("Actual input:", xmas_wordsearcher(pattern, input_rows))