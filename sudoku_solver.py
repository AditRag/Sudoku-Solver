import tkinter as tk
from tkinter import messagebox

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🧩 Sudoku Solver: Problem ➡ Solution")
        self.root.configure(bg="#DDEEFF")

        self.input_entries = [[None for _ in range(9)] for _ in range(9)]
        self.output_entries = [[None for _ in range(9)] for _ in range(9)]

        self.build_gui()

    def build_gui(self):
        main_frame = tk.Frame(self.root, bg="#DDEEFF")
        main_frame.pack(padx=20, pady=20)

        # Problem grid
        left_frame = tk.Frame(main_frame, bg="#DDEEFF")
        left_frame.grid(row=0, column=0)
        tk.Label(left_frame, text="Problem", font=('Helvetica', 14, 'bold'), bg="#DDEEFF").pack()
        self.create_grid(left_frame, self.input_entries)

        # Arrow label
        tk.Label(main_frame, text="➡", font=("Helvetica", 30, "bold"), bg="#DDEEFF").grid(row=0, column=1, padx=15)

        # Solution grid
        right_frame = tk.Frame(main_frame, bg="#DDEEFF")
        right_frame.grid(row=0, column=2)
        tk.Label(right_frame, text="Solution", font=('Helvetica', 14, 'bold'), bg="#DDEEFF").pack()
        self.create_grid(right_frame, self.output_entries, readonly=True)

        # Solve button
        button_frame = tk.Frame(self.root, bg="#DDEEFF")
        button_frame.pack(pady=15)
        solve_btn = tk.Button(button_frame, text="Solve", font=('Helvetica', 14, 'bold'), bg="#4CAF50", fg="white",
                              padx=20, pady=5, command=self.solve)
        solve_btn.pack()

    def create_grid(self, parent, entry_matrix, readonly=False):
        grid_frame = tk.Frame(parent, bg="black")
        grid_frame.pack(pady=10)

        for i in range(9):
            for j in range(9):
                e = tk.Entry(grid_frame, width=2, font=('Helvetica', 20), justify='center', relief='flat')
                if readonly:
                    e.config(state='disabled', disabledbackground="#F0F0F0", disabledforeground="black")
                padx = (1, 1)
                pady = (1, 1)
                if j in [0, 3, 6]:
                    padx = (4, 1)
                if i in [0, 3, 6]:
                    pady = (4, 1)
                e.grid(row=i, column=j, padx=padx, pady=pady, ipady=5)
                entry_matrix[i][j] = e

    def get_input_grid(self):
        grid = []
        for row in self.input_entries:
            current_row = []
            for cell in row:
                val = cell.get()
                current_row.append(int(val) if val.isdigit() else 0)
            grid.append(current_row)
        return grid

    def set_output_grid(self, grid):
        for i in range(9):
            for j in range(9):
                cell = self.output_entries[i][j]
                cell.config(state="normal")
                cell.delete(0, tk.END)
                if grid[i][j] != 0:
                    cell.insert(0, str(grid[i][j]))
                cell.config(state="disabled")

    def is_valid(self, grid, row, col, num):
        for x in range(9):
            if grid[row][x] == num or grid[x][col] == num:
                return False
        startRow, startCol = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if grid[startRow + i][startCol + j] == num:
                    return False
        return True

    def solve_sudoku(self, grid, row=0, col=0):
        if row == 9:
            return True
        if col == 9:
            return self.solve_sudoku(grid, row + 1, 0)
        if grid[row][col] != 0:
            return self.solve_sudoku(grid, row, col + 1)

        for num in range(1, 10):
            if self.is_valid(grid, row, col, num):
                grid[row][col] = num
                if self.solve_sudoku(grid, row, col + 1):
                    return True
                grid[row][col] = 0
        return False

    def solve(self):
        grid = self.get_input_grid()
        if self.solve_sudoku(grid):
            self.set_output_grid(grid)
        else:
            messagebox.showerror("Error", "No solution exists for the given Sudoku.")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
