from blacksheep import *
print(f"all possible jumps:\n{LEGAL_JUMPS}")
print(f"number of jumps: {len(LEGAL_JUMPS)}")

# black, whites = 0, [1]
# black, whites = 0, [1, 7]

#challenge 1
#black, whites = 8, [6, 9, 12]

#challenge 7
black, whites = 6, [4, 5, 8, 9, 10]

print(solve_puzzle_rec(black, whites))