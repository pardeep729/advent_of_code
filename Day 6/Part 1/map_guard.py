guard_directions_order = ['^', '>', 'v', '<']

guard_directions_trajectory_mapping = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1)  
}

def calculate_trajectory(guard_direction):
    """ 
    Given guards direction (represented by ^, <, > or v), calculate the trajectory, to be used in moving position across the rows and indexes of list
    """

    return guard_directions_trajectory_mapping.get(guard_direction, (0,0))

def out_of_bounds(grid_max_r, grid_max_c, new_r_pos, new_c_pos):
    """
    Given max r and c of a grid and the next trajectory, return True if player about to go out of bounds, or False otherwise
    """

    if (
        (new_r_pos < 0) or
        (new_r_pos >= grid_max_r) or
        (new_c_pos < 0) or
        (new_c_pos >= grid_max_c)
    ):
        return True
    else:
        return False
    
def calculate_new_map(lab_map):
    # Convert to matrix
    lab_map_grid = [list(i) for i in lab_map.splitlines()]
    # Store max shape too
    grid_max_r = len(lab_map_grid)
    grid_max_c = len(lab_map_grid[0])

    # Find starting index of guard and direction
    guard_direction = None
    guard_pos = (None, None)
    for r_idx, r in enumerate(lab_map_grid):
        if guard_direction == None and guard_pos == (None, None):
            for d, _ in guard_directions_trajectory_mapping.items():
                if d in r:
                    guard_direction = d
                    guard_pos = (r_idx, r.index(d)) 
                    break
        else:
            break

    # Evaluate grid while guard still in map
    is_guard_in_map = True
    while is_guard_in_map:
        # Store current row and col position, as well as current trajectory
        guard_r_pos, guard_c_pos = guard_pos
        trajectory = calculate_trajectory(guard_direction)
        trajectory_r, trajectory_c = trajectory

        # Mark current grid as visited 'X'
        lab_map_grid[guard_r_pos][guard_c_pos] = 'X'

        # Mark possible next position if head same direction (to check)
        new_r_pos = guard_r_pos + trajectory_r
        new_c_pos = guard_c_pos + trajectory_c

        # Calculate if next position would put guard outside map, end it there
        if out_of_bounds(grid_max_r, grid_max_c, new_r_pos, new_c_pos):
            is_guard_in_map = False
            break

        # Check if next position is an obstacle
        if lab_map_grid[new_r_pos][new_c_pos] == '#':
            guard_direction_idx = guard_directions_order.index(guard_direction)
            new_guard_direction_idx = (guard_direction_idx + 1) % 4 # If at last position, then set back to 0 (loop around)
            guard_direction = guard_directions_order[new_guard_direction_idx]
        else:
            new_guard_pos = (new_r_pos, new_c_pos)
            guard_pos = new_guard_pos
            lab_map_grid[new_r_pos][new_c_pos] = guard_direction

    # Generate new lab_map (string)
    new_lab_map = '\n'.join([''.join(r) for r in lab_map_grid])

    # Count the 'X's
    return new_lab_map.count('X')

# Example
with open('../example_map.txt', 'r') as f:
    lab_map = f.read()

print(calculate_new_map(lab_map))

# Actual Input
with open('../input_map.txt', 'r') as f:
    lab_map = f.read()

print(calculate_new_map(lab_map))

