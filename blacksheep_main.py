import logging
import sys
from blacksheep import *

# uncomment this line if you want to see nasty debug notes
#logging.basicConfig(level=logging.DEBUG)

def diagram_to_list(diagram):
	'''diagram-
	a string with 5 lines.
	'''
	diagram_lines = diagram.split('\n')
	grid = []
	for line in diagram_lines:
		line = line.replace(" ", "")
		if line:
			grid.append(line)
	return grid_to_list(grid)

def list_to_diagram(lst):
	diagram_lines = []
	grid = list_to_grid(lst)
	for grid_line in grid:
		line = " ".join(grid_line)
		if len(grid_line) == 2:
			line = " " + line
		diagram_lines.append(line)

	return "\n".join(diagram_lines)

def main():
	filename = sys.argv[1]
	with open(filename, 'r') as f:
		diagram = f.read()

	puzzle_list = diagram_to_list(diagram)
	logging.debug(puzzle_list)
	logging.debug(list_to_diagram(puzzle_list))

	black = puzzle_list.index('B')
	whites = [j for j in range(len(puzzle_list)) if puzzle_list[j] == 'W']
	sol_raw = solve_puzzle_rec(black, whites)
	#note to myself- can one change logging so it won't show debug notes from blacksheep.py?
	logging.debug(sol_raw)  
	if sol_raw is None:
		print("unsolvable puzzle!")
		exit(1)

	sol_diagrams = [diagram]
	temp_list = puzzle_list.copy()
	for (p1,p2,p3) in sol_raw:
		temp_list[p3] = temp_list[p1]
		temp_list[p1] = '.'
		temp_list[p2] = '.'
		sol_diagrams.append(list_to_diagram(temp_list))


	sol_data = "\n\n".join(sol_diagrams)

	sol_filename = filename + ".sol"
	with open(sol_filename, 'w') as f:
		f.write(sol_data)


if __name__ == '__main__':
	main() 



	
