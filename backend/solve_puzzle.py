import copy

# can solve 3x3, 9x9, 16x16 
block_size = 3
grid_numbers = range(1, 10)
no_of_runs = 0

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
    # if not any(continue_processing): # check if any 0 are remaining

    #     for x_row in range(len(grid)): # check if
    #         x_valid = len(get_x_axis_elements(grid[x_row])) == block_size**2
    
    #     if x_valid:
    #         for y_row in range(len(grid)):
    #             y_valid = len(get_y_axis_elements(grid, y_row)) == block_size**2
    # else:
    #     x_valid = False
    #     y_valid = False

    # return x_valid & y_valid
    return not any(continue_processing)

def solve(grid):
    """
    Solves the given Sudoku grid using recursion.
    """
    global no_of_runs

    if is_grid_solved(grid):
        return grid

    new_grid = copy.deepcopy(grid)
    no_of_runs = no_of_runs + 1

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

# easy_grid = [[0,0,0,2,0,0,7,5,3],
#              [6,0,0,8,0,5,0,4,0],
#              [0,0,0,1,0,0,9,0,0],
#              [8,9,7,0,0,0,0,0,5],
#              [0,5,0,9,1,3,0,8,0],
#              [1,0,0,0,0,0,6,2,9],
#              [0,0,2,0,0,9,0,0,0],
#              [0,6,0,4,0,7,0,0,2],
#              [5,7,4,0,0,1,0,0,0]]

# medium_grid = [[1,0,0,0,3,8,0,0,6],
#                [0,3,0,7,0,9,0,0,0],
#                [0,8,6,0,0,0,0,3,7],
#                [0,0,0,0,7,0,3,0,0],
#                [0,4,0,0,8,0,0,2,0],
#                [0,0,8,0,9,0,0,0,0],
#                [6,9,0,0,0,0,7,4,0],
#                [0,0,0,6,0,2,0,9,0],
#                [2,0,0,9,4,0,0,0,1]]

# difficult_grid =    [[9,0,0,0,0,1,0,0,4],
#                      [7,4,3,0,0,0,0,0,0],
#                      [0,6,0,2,9,0,0,0,0],
#                      [0,0,0,0,0,9,0,8,0],
#                      [0,0,8,0,7,0,5,0,0],
#                      [0,3,0,5,0,0,0,0,0],
#                      [0,0,0,0,6,2,0,4,0],
#                      [0,0,0,0,0,0,8,7,6],
#                      [5,0,0,4,0,0,0,0,9]]

# most_hardest_grid = [[8,0,0,0,0,0,0,0,0],
#                      [0,0,3,6,0,0,0,0,0],
#                      [0,7,0,0,9,0,2,0,0],
#                      [0,5,0,0,0,7,0,0,0],
#                      [0,0,0,0,4,5,7,0,0],
#                      [0,0,0,1,0,0,0,3,0],
#                      [0,0,1,0,0,0,0,6,8],
#                      [0,0,8,5,0,0,0,1,0],
#                      [0,9,0,0,0,0,4,0,0]]


# grid_solved = solve(easy_grid)
# print("Easy Sudoku, No of steps {}".format(no_of_runs))
# for line in grid_solved:
#     print(line)

# no_of_runs = 0
# grid_solved = solve(medium_grid)
# print("Medium Sudoku, No of steps {}".format(no_of_runs))
# for line in grid_solved:
#     print(line)

# no_of_runs = 0
# grid_solved = solve(difficult_grid)
# print("Difficult Sudoku, No of steps {}".format(no_of_runs))
# for line in grid_solved:
#     print(line)

# no_of_runs = 0
# grid_solved = solve(most_hardest_grid)
# print("World's hardest Sudoku, No of steps {}".format(no_of_runs))
# for line in grid_solved:
#     print(line)