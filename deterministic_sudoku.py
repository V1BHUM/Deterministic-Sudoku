import random

class Sudoku:
    def __init__(self):
        self.grid = [['-']*9 for _ in range(9)]
        self.possible = dict()
        for x in range(9):
            for y in range(9):
                self.possible[(y,x)] = set(list(range(1,10)))
        
        self.possible_check = []
        self.possible_check.extend([('row', i) for i in range(9)])
        self.possible_check.extend([('col', i) for i in range(9)])
        self.possible_check.extend([('block', i, j) for i in range(3) for j in range(3)])


    def add_num(self, y, x, val):
        for Y, X in self.get_row(y):
            self.possible[(Y, X)].discard(val)
        for Y, X in self.get_column(x):
            self.possible[(Y, X)].discard(val)
        for Y, X in self.get_block(y//3, x//3):
            self.possible[(Y, X)].discard(val)      
        self.possible[y,x] = set()
        self.grid[y][x] = val


    def find_something(self):
        random.shuffle(self.possible_check)
        for check in self.possible_check:
            kind = check[0]
            if kind == 'row':
                made = dict({i:[] for i in range(1, 10)})
                for Y, X in self.get_row(check[1]):
                    for val in self.possible[(Y, X)]:
                        made[val].append((Y, X))
                for key, val in made.items():
                    if(len(val) == 1):
                        return ('row', check[1], val[0], key)
                    
            elif kind == 'col':
                made = dict({i:[] for i in range(1, 10)})
                for Y, X in self.get_column(check[1]):
                    for val in self.possible[(Y, X)]:
                        made[val].append((Y, X))
                for key, val in made.items():
                    if(len(val) == 1):
                        return ('col', check[1], val[0], key)
            
            else:
                made = dict({i:[] for i in range(1, 10)})
                for Y, X in self.get_block(check[1], check[2]):
                    for val in self.possible[(Y, X)]:
                        made[val].append((Y, X))
                for key, val in made.items():
                    if(len(val) == 1):
                        return ('block', (check[1], check[2]), val[0], key)    

        return None 


    def input_grid(self, grid_list):
        if len(grid_list) != 9:
            print("Invalid input! Grid should contain exactly 9 rows.")
            return
        
        for i, row_str in enumerate(grid_list):
            if len(row_str) != 9:
                print(f"Invalid input in row {i+1}! Row should contain exactly 9 characters.")
                return
            for j, cell in enumerate(row_str):
                if(cell != '-'):
                    self.add_num(i, j, int(cell))

    def solve(self):
        tick = self.find_something()
        if tick is None:
            print('Halting')
            return None
        print('\n\n')
        print(tick)
        y,x = tick[2]
        self.add_num(y, x, tick[3])
        self.print_grid()
        return tick

    def print_grid(self):
        print("Sudoku Grid:")
        for row in self.grid:
            print(" ".join(str(cell) for cell in row))

    def get_val(self, idx):
        return self.grid[idx[0]][idx[1]]

    def get_row(self, row_num):
        return [(row_num, i) for i in range(9)]

    def get_column(self, col_num):
        return [(i, col_num) for i in range(9)]

    def get_block(self, row_num, col_num):
        start_row = (row_num) * 3
        start_col = (col_num) * 3
        blocks = []
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                blocks.append((i, j))
        return blocks

if __name__ == "__main__":
    sudoku = Sudoku()
    grid_input = [
        "-75--8-21",
        "6---9----",
        "8----2--6",
        "---1-----",
        "-27----5-",
        "-----59-4",
        "-----9---",
        "-8-31----",
        "3-4---6-8"
    ]
    sudoku.input_grid(grid_input)
    sudoku.print_grid()
    
    sudoku.solve()
