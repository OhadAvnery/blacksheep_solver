'''
THE BOARD:

0-1-2
-3-4-
5-6-7
-8-9-
A-B-C (10-11-12)

13 crates in total.
Represented by a list of chars, l, where l[i] is: 
X (nothing) / B (black) / W (white).
'''

import functools
import logging

# uncomment this line if you want to see nasty debug notes
# logging.basicConfig(level=logging.DEBUG)


# GRID_ROWS[a] = (i,j)-
# means the indexes at row a are i to j, INCLUSIVE.
GRID_ROWS = [(0,2), (3,4), (5,7), (8,9), (10,12)]

def list_to_grid(lst):
	'''
	given a list l of length 13, return a corresponding 5-row grid (matrix).
	'''

	# sublist_bounds[a] = (i,j)-
	# means the indexes at row a are i to j, INCLUSIVE.
	sublist_bounds = [(0,2), (3,4), (5,7), (8,9), (10,12)]
	return [lst[slice(i,j+1)] for (i,j) in sublist_bounds]


def grid_to_list(grid):
	'''
	given a grid, return a corresponding 12-elements list.
	'''
	return list(functools.reduce(lambda x,y: x+y, grid))

def calculate_index_dicts():
	grid_to_list_index = {}
	'''
	returns (grid_to_list_index, list_to_grid_index).
	The first one- a dict with elements of the form (i,j):d,
	where d is the list index corresponding to the grid indexes (i,j).
	The second one- the exact converse.
	'''

	for row_num, (start, end) in enumerate(GRID_ROWS):
		for j in range(start, end + 1):
			grid_to_list_index[(row_num, j - start)] = j

	list_to_grid_index = {val:key for key,val in grid_to_list_index.items()}  
	return grid_to_list_index, list_to_grid_index 

grid_to_list_index, list_to_grid_index = calculate_index_dicts()



def calculate_legal_jumps():
	'''
	returns a dict whose elements have the form : 
	(i,j):k,
	where i can jump over j to k.
	'''

	'''
	there are 8 possible directions to jump in,
	as seen in this diagram:
	123
	8X4
	765
	we'll manually construct the dict in directions 1-4.
	For 5-8, we'll simply reverse the jumps.
	'''

	# at first, jumps_1_to_4 will have elements of the form:
	# (p1,p2):p3,
	# where p_i are given in grid coordinates.
	jumps_1_to_4 = dict()


	# 1,3 - 'main cases'
	for i in [2, 4]:
		# 1
		for j in [1,2]:
			jumps_1_to_4[( (i,j), (i-1,j-1) )] = (i-2,j-1)

		# 3
		for j in [0,1]:
			jumps_1_to_4[( (i,j), (i-1,j) )] = (i-2,j+1)
		
	# 1,3 - special cases
	jumps_1_to_4.update({
		((3,0), (2,1)) : (1,1),
		((3,1), (2,1)) : (1,0)
		})
	
	# 2
	jumps_1_to_4.update({
		((4,j), (2,j)) : (0,j) for j in range(3)
		})

	# 4
	jumps_1_to_4.update({
		((i,0), (i,1)) : (i,2) for i in [0,2,4]
		})

	all_jumps = dict()
	for (p1, p2), p3 in jumps_1_to_4.items():
		i1 = grid_to_list_index[p1]
		i2 = grid_to_list_index[p2]
		i3 = grid_to_list_index[p3]
		all_jumps.update({(i1,i2):i3, (i3,i2):i1})

	return all_jumps

LEGAL_JUMPS = calculate_legal_jumps()

def solve_puzzle_rec(black, whites):
	'''
	params: 
	black - an index 0<=i<=12 for the black ball,
	whites- list of indexes for the white balls.
	if the puzzle has a solution, 
	return the list of necessary jumps (in order).
	Else, return None.
	'''

	# base case- no white balls, no moves are needed
	if not whites:
		logging.debug(f"black: {black}, whites: {whites}, result: []")
		return []

	# for all pairs (p1,p2) such that p2 is white,
	# check if p1 can jump over p3.
	# if so, simulate that move, and do the recursion.
	balls = whites + [black]
	for p1 in balls:
		for p2 in whites:
			if (p1, p2) not in LEGAL_JUMPS:
				continue
			p3 = LEGAL_JUMPS[(p1, p2)]
			# we can't jump to an existing ball!
			if p3 in balls: 
				continue

			# remove the ball from p2
			temp_whites = whites.copy()
			temp_whites.remove(p2)

			
			if p1 == black:
				temp_black = p3
			else:  #black doesn't change
				temp_black = black
				temp_whites.remove(p1)
				temp_whites.append(p3)

			temp_solution = solve_puzzle_rec(temp_black, temp_whites)
			if temp_solution is None:
				continue

			solution = [(p1,p2,p3)] + temp_solution
			logging.debug(f"black: {black}, whites: {whites}, sol: {solution}")
			return solution

	logging.debug(f"black: {black}, whites: {whites}, sol: None")
	return None
