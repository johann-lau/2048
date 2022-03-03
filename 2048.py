from enum import Enum
import random

class Direction(Enum):
  W = UP = 1
  D = RIGHT = 2
  S = DOWN = 3
  A = LEFT = 4


class Game2048:
  def __init__(self):
    self.score = 0 # Incremented at line 45
    self.grid = [[None, None, None, None],
                 [None, None, None, None],
                 [None, None, None, None],
                 [None, None, None, None]]
    self.spawn_random() # Two random tiles at initialization
    self.spawn_random()

  def pretty_print(self): # Returns a beautified string for monospace printing.
    flattened_grid = [j for i in self.grid for j in i if j != None]
    box_length = len(str(max(flattened_grid))) # String length of maximum value in self.grid
    box_length = max(box_length, 4) # At least 4
    desc = f"Score: {self.score}\n"
    for i in self.grid:
      desc += "|".join([f"{j: ^{box_length}}" if j else " " * box_length for j in i]) + "\n"
    return desc[:-1]

  def spawn_random(self): # Adds a random tile 2 or 4.
    new = random.choice([2, 4])
    empties = [[i, j] for i in range(0, 4) for j in range(0, 4) if not self.grid[i][j]]
    chosen = random.choice(empties)
    self.grid[chosen[0]][chosen[1]] = new
  
  def input_left(self): # Handles input to the left. Other directions are done through reflection.
    for i in range(4): # Let's say self.grid[0] is [4, None, 4, 8]
      for j in range(3): # Loop through first three items [4, None, 4]
        if self.grid[i][j]:
          righters = list(filter(lambda x: x, self.grid[i][(j+1):])) # Values to the right excluding Nones
          if righters:
            dir_r = righters[0] # First value directly to the right excluding Nones
            if self.grid[i][j] == dir_r:
              self.grid[i][j] *= 2 # After all iterations should give [8, None, 4, 8]
              self.score += self.grid[i][j]
              self.grid[i][righters.index(dir_r) + j + 1] = None # Index of dir_r in i: righters.index(dir_r) + j + 1
              # After all iterations should give [8, None, None, 8]
      self.grid[i] = list(filter(lambda x: x, self.grid[i])) # Remove Nones
      self.grid[i].extend([None] * (4 - len(self.grid[i])))
  
  def twod_flip(self):
    # ORIGINAL             AFTER
    # a | b | c | d        a | e | i | m
    # e | f | g | h        b | f | j | n
    # i | j | k | l        c | g | k | o
    # m | n | o | p        d | h | l | p
    new_grid = []
    for j in range(4): # Note that this is iterating through the x-axis
      new_grid.append([self.grid[i][j] for i in range(4)])
    self.grid = new_grid

  def input(self, direction): # Handle user inputs
    if direction == Direction.LEFT:
      self.input_left()
    elif direction == Direction.RIGHT:
      for i in range(4):
        self.grid[i].reverse()
      self.input_left()
      for i in range(4):
        self.grid[i].reverse()
    else:
      self.twod_flip()
      if direction == Direction.DOWN:
        for i in range(4):
          self.grid[i].reverse()
      self.input_left()
      if direction == Direction.DOWN:
        for i in range(4):
          self.grid[i].reverse()
      self.twod_flip()
    game.spawn_random()


game = Game2048()
inp = ""
print(game.pretty_print() + "\n\n")
inp = input("Direction (WASD, or Q to quit): ").lower()
while inp != "q":
  if inp in ['w', 'a', 's', 'd']:
    game.input(eval(f"Direction.{inp.upper()}"))
    print(game.pretty_print())
  inp = input("Direction (WASD, or Q to quit): ").lower()
