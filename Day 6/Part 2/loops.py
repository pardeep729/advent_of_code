import copy

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

def calculate_loops(lab_map):
    # Convert to matrix
    lab_map_grid_base = [list(i) for i in lab_map.splitlines()]
    # Store max shape too
    grid_max_r = len(lab_map_grid_base)
    grid_max_c = len(lab_map_grid_base[0])

    # Calculate the max total iterations (for tracking run)
    max_iterations = grid_max_r * grid_max_c
    print(max_iterations)
    iteration_count = 0  # Initialize the counter

    total_loops = 0 # Total number of loop recorded

    # Loop over all positions as the possible "O" position
    for o_pos_r_idx, grid_row in enumerate(lab_map_grid_base):
        for o_pos_c_idx, _ in enumerate(grid_row):
            # Iteration counter
            iteration_count += 1  # Increment the counter

            # Start with fresh copy of base map
            lab_map_grid = copy.deepcopy(lab_map_grid_base) # TODO: This is causing memory issues (stop after 420/16,900), optimise

            # Only evaluate if that position is empty (so can replace with "O")
            if lab_map_grid[o_pos_r_idx][o_pos_c_idx] == '.':

                lab_map_grid[o_pos_r_idx][o_pos_c_idx] = 'O' 
                repeat_pos = (None, None) # Keep track of square to side of the O obstacle. If we visit twice, it's a loop
                is_loop = False # Keep track of if the current iteration is a loop

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
                temp_counter = 0
                while (is_guard_in_map and not is_loop):
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
                    # print(grid_max_r, grid_max_c, new_r_pos, new_c_pos)
                    if out_of_bounds(grid_max_r, grid_max_c, new_r_pos, new_c_pos):
                        is_guard_in_map = False
                        break

                    # Check if next position is an obstacle
                    if lab_map_grid[new_r_pos][new_c_pos] in ('#', 'O'):
                        guard_direction_idx = guard_directions_order.index(guard_direction)
                        new_guard_direction_idx = (guard_direction_idx + 1) % 4 # If at last position, then set back to 0 (loop around)
                        guard_direction = guard_directions_order[new_guard_direction_idx]

                        # If it's specifically a 'O', note the current position (unless we've already visited it, in which case we've found a loop)
                        if lab_map_grid[new_r_pos][new_c_pos] == 'O':
                            if repeat_pos == (None, None):
                                repeat_pos = (guard_r_pos, guard_c_pos)
                            else:  
                                is_loop = True
                    else:
                        new_guard_pos = (new_r_pos, new_c_pos)
                        guard_pos = new_guard_pos
                        lab_map_grid[new_r_pos][new_c_pos] = guard_direction

                    temp_counter+=1

                # Generate new lab_map (string)
                new_lab_map = '\n'.join([''.join(r) for r in lab_map_grid])

                if is_loop:
                    total_loops += 1

            # print(f"Iteration {iteration_count}/{max_iterations}: Processing cell ({o_pos_r_idx}, {o_pos_c_idx})")
            print(f"Iteration {iteration_count}/{max_iterations}")


    # Return total loops
    return total_loops

# Example
with open('../example_map.txt', 'r') as f:
    lab_map = f.read()

print(calculate_loops(lab_map))

# Actual Input
with open('../input_map.txt', 'r') as f:
    lab_map = f.read()

print(calculate_loops(lab_map))

