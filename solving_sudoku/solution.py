assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    un_solved_values = [box for box in values.keys() if len(values[box]) == 2]
    for box in un_solved_values:
        digit = values[box]
        naked_twins = []
        naked_twins_peers = []
        naked_twins.append(box)
        # Find naked twins
        for peer in peers[box]:
            if len(values[peer]) == 2:
                if(values[peer] == digit):
                    twin_peer = peer
                    peers_inter = set(peers[box]).intersection(peers[twin_peer])
                    for peer in peers_inter:#peers[box]:
                        if(peer not in [box, twin_peer]):
                            if(len(values[peer]) > 1):
                                #replace digits
                                replaced = False
                                for dig in digit:
                                    if(dig in values[peer]):
                                        values[peer] = values[peer].replace(dig,'')
                                        replaced = True
                                if(replaced == True):
                                    zzz = 1

        naked_twins = list(set(naked_twins))
    return values  
    
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]        


def diag(A, B):
    "Cross product of elements in A and elements in B."
    #print(A,B)

    #print(boxes)

    startrow = rows.index(A)
    startcol = int(B)

    postrows = rows[startrow:10]
    prerows = rows[0:startrow]

    postcols = cols[startcol:10]
    precols = cols[0:startcol]

    dict1 = [k + v for k,v in zip(prerows, postcols[::-1]) ]

    dict2 =  [k + v for k,v in zip(postrows[::-1], precols) ]

    dict3 = [k + v for k,v in zip(prerows[::-1], precols[::-1][1: len(prerows) +1]) ]

    dict4 = [k + v for k,v in zip(postrows[1:len(postcols) + 1], postcols)]

    return dict1 + dict2 + dict3 + dict4


rows = 'ABCDEFGHI'
cols = '123456789'


boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(r, c) for r in ('ABC','DEF','GHI') for c in ('123','456','789')]
diag_ascending = [[str(r)+str(10- int(c)) for (r,c) in zip(rows,cols)]]
diag_descending = [[r+c for (r,c) in zip(rows,cols)]]
unitlist = row_units + column_units + square_units + diag_ascending + diag_descending

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
  

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """

    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    retval = dict(zip(boxes, chars))


    return retval

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    retval = search( reduce_puzzle( only_choice( eliminate(grid_values(grid)) ) )) 

    return retval




if __name__ == '__main__':

    #display(only_choice(eliminate(grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'))))    


    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    #display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        print('Error')
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
