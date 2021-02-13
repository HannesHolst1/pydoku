import copy

# can solve 3x3, 9x9, 16x16 
block_size = 3
grid_numbers = range(1, 10)

def ReturnBlockOfCoordinates(x, y):
    """
    Returns the block in which the coordinates are located.
    """
    block_x = int(x / block_size)
    block_y = int(y / block_size)

    if block_x == block_size:
        block_x = block_x - 1

    if block_y == block_size:
        block_y = block_y - 1

    return (block_x, block_y)

def get_x_axis_elements(all_x_axis_elements):
    x_axis = set()
    x_axis.update(element for element in all_x_axis_elements if element != 0)
    return x_axis

def get_y_axis_elements(grid, which_y_axis):
    y_axis = set()
    for x in range(0, len(grid)):
        if grid[x][which_y_axis] != 0:
            y_axis.add(grid[x][which_y_axis])
    return y_axis

def ExactCover(grid, x, y):
    """
    Calculates the Exact Cover for an element in the grid and returns all possible numbers.
    """
    x_axis = get_x_axis_elements(grid[x])
    
    y_axis = get_y_axis_elements(grid, y)
    
    BlockOfCoordinates = ReturnBlockOfCoordinates(x, y) 

    block = set()
    steps = int(len(grid)**0.5)
    for i in range(0, len(grid), steps):
        for j in range(0, len(grid), steps):
            CurrentBlock = ReturnBlockOfCoordinates(i, j)
            if  CurrentBlock == BlockOfCoordinates:
                # not happy here
                block.update(element for element in grid[i][j:j+block_size] if element != 0)
                block.update(element for element in grid[i+1][j:j+block_size] if element != 0)
                block.update(element for element in grid[i+2][j:j+block_size] if element != 0)

    numbers_used_for_coordinates = set()
    numbers_used_for_coordinates.update(x_axis)
    numbers_used_for_coordinates.update(y_axis)
    numbers_used_for_coordinates.update(block)

    possible_answers = set()
    for possible_answer in grid_numbers:
        if not possible_answer in numbers_used_for_coordinates:
            possible_answers.add(possible_answer)

    return possible_answers

def is_grid_solved(grid):
    continue_processing = [0 in x for x in grid]
    return not any(continue_processing)

def solve(grid):
    """
    Solves the given Sudoku grid using recursion.
    """

    if is_grid_solved(grid):
        return grid

    new_grid = copy.deepcopy(grid)

    for x_element in range(len(new_grid)):
        for y_element in range(len(new_grid[x_element])):
            if new_grid[x_element][y_element] == 0:
                answers = ExactCover(new_grid, x_element, y_element)
                for answer in answers:
                    new_grid[x_element][y_element] = answer
                    new_grid = solve(new_grid)
                    if not is_grid_solved(new_grid):
                        new_grid[x_element][y_element] = 0
                    else:
                        break
                return new_grid

    return new_grid