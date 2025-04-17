import pygame


class ClearLine:
    def __init__(self, grid):
        self.grid = grid

    def check_and_clear(self):
        # Check and clear full rows
        for row in range(len(self.grid)):
            if all(self.grid[row]):  # If all cells in the row are filled
                # print(f"Clearing row {row}")
                self.clear_row(row)

        # Check and clear full columns
        for col in range(len(self.grid[0])):
            if all(self.grid[row][col] for row in range(len(self.grid))):  # If all cells in the column are filled
                # print(f"Clearing column {col}")
                self.clear_column(col)

        # Debugging: Print the grid state after clearing
        # print("Grid state after clearing:")
        # for row in self.grid:
        #     print(row)

    def clear_row(self, row):
        # Clear the row by setting all cells to 0
        self.grid[row] = [0] * len(self.grid[row])

    def clear_column(self, col):
        # Clear the column by setting all cells to 0
        for row in range(len(self.grid)):
            self.grid[row][col] = 0
