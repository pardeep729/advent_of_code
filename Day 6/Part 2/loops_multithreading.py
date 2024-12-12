from concurrent.futures import ThreadPoolExecutor
import copy

guard_directions_order = ['^', '>', 'v', '<']
guard_directions_trajectory_mapping = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1)
}

def calculate_trajectory(guard_direction):
    """Calculate the trajectory for the given guard direction."""
    return guard_directions_trajectory_mapping.get(guard_direction, (0, 0))

def out_of_bounds(grid_max_r, grid_max_c, new_r_pos, new_c_pos):
    """Check if the position is out of bounds."""
    return new_r_pos < 0 or new_r_pos >= grid_max_r or new_c_pos < 0 or new_c_pos >= grid_max_c

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

    return new_lab_map

def process_obstacle_placement(o_pos, lab_map_grid_base, guard_direction_starting, guard_pos_starting, grid_max_r, grid_max_c, iteration):
    """Process a single obstacle placement to determine if it results in a loop."""
    o_pos_r_idx, o_pos_c_idx = o_pos
    guard_pos = guard_pos_starting
    guard_direction = guard_direction_starting

    for 
    lab_map_grid = copy.deepcopy(lab_map_grid_base)

    if lab_map_grid[o_pos_r_idx][o_pos_c_idx] != '.':
        print(f"Iteration {iteration} done: Position {o_pos} skipped (not empty).")
        return 0  # Skip invalid placements

    lab_map_grid[o_pos_r_idx][o_pos_c_idx] = 'O'
    repeat_pos = (None, None)
    is_loop = False
    is_guard_in_map = True

    while is_guard_in_map and not is_loop:
        guard_r_pos, guard_c_pos = guard_pos
        trajectory_r, trajectory_c = calculate_trajectory(guard_direction)
        new_r_pos, new_c_pos = guard_r_pos + trajectory_r, guard_c_pos + trajectory_c

        if out_of_bounds(grid_max_r, grid_max_c, new_r_pos, new_c_pos):
            is_guard_in_map = False
            break

        if lab_map_grid[new_r_pos][new_c_pos] in ('#', 'O'):
            guard_direction_idx = guard_directions_order.index(guard_direction)
            guard_direction = guard_directions_order[(guard_direction_idx + 1) % 4]

            if lab_map_grid[new_r_pos][new_c_pos] == 'O':
                if repeat_pos == (None, None):
                    repeat_pos = (guard_r_pos, guard_c_pos)
                else:
                    is_loop = True
        else:
            guard_pos = (new_r_pos, new_c_pos)
            lab_map_grid[new_r_pos][new_c_pos] = guard_direction

    print(f"Iteration {iteration} done: Position {o_pos}, Loop Detected: {is_loop}")
    return 1 if is_loop else 0

def calculate_loops_multithreaded(lab_map, visited_lab_map):
    """Calculate loops using multithreading."""
    lab_map_grid_base = [list(i) for i in lab_map.splitlines()]
    visited_lab_map_grid = [list(i) for i in visited_lab_map.splitlines()]
    grid_max_r, grid_max_c = len(lab_map_grid_base), len(lab_map_grid_base[0])

    guard_direction_starting, guard_pos_starting = None, (None, None)
    for r_idx, r in enumerate(lab_map_grid_base):
        if guard_direction_starting is None and guard_pos_starting == (None, None):
            for d in guard_directions_order:
                if d in r:
                    guard_direction_starting = d
                    guard_pos_starting = (r_idx, r.index(d))
                    break
        if guard_direction_starting:
            break

    x_coords = [(r, c) for r, row in enumerate(visited_lab_map_grid) for c, cell in enumerate(row) if cell == 'X']
    filtered_coords = [coord for coord in x_coords if coord != guard_pos_starting]

    with ThreadPoolExecutor() as executor:
        # Submit tasks for multithreading with an iteration counter
        futures = {
            executor.submit(
                process_obstacle_placement,
                coord,
                lab_map_grid_base,
                guard_direction_starting,
                guard_pos_starting,
                grid_max_r,
                grid_max_c,
                iteration
            ): iteration
            for iteration, coord in enumerate(filtered_coords, start=1)
        }
        total_loops = sum(f.result() for f in futures)  # Aggregate results

    return total_loops

# Example Usage
with open('../example_map.txt', 'r') as f:
    lab_map = f.read()

marked_lab_map = calculate_new_map(lab_map)
print(calculate_loops_multithreaded(lab_map, marked_lab_map))

# Actual Input
with open('../input_map.txt', 'r') as f:
    lab_map = f.read()

marked_lab_map = calculate_new_map(lab_map)
print(calculate_loops_multithreaded(lab_map, marked_lab_map))
