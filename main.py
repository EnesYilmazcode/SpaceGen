import tkinter as tk
import random

matrix = [[1 for _ in range(50)] for _ in range(50)]

root = tk.Tk()
root.title("SpaceGen")

canvas = tk.Canvas(root, width=500, height=500, bg='white')
canvas.pack()

cell_size = 10

rectangles = {}

for row in range(50):
    for col in range(50):
        x1 = col * cell_size
        y1 = row * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size
        
        rect_id = canvas.create_rectangle(x1, y1, x2, y2, fill='white')
        rectangles[(row, col)] = rect_id

# Track if mouse is being held down
is_dragging = False

def paint_cell(row, col):
    """Set a cell to 0 (black)"""
    if 0 <= row < 50 and 0 <= col < 50:
        if matrix[row][col] == 1:  # Only paint if it's currently white
            matrix[row][col] = 0
            rect_id = rectangles[(row, col)]
            canvas.itemconfig(rect_id, fill='black')

def on_click(event):
    global is_dragging
    is_dragging = True
    
    col = event.x // cell_size
    row = event.y // cell_size
    
    if 0 <= row < 100 and 0 <= col < 100:
        matrix[row][col] = 1 - matrix[row][col]
        
        new_color = 'white' if matrix[row][col] == 1 else 'black'
        rect_id = rectangles[(row, col)]
        canvas.itemconfig(rect_id, fill=new_color)
        
        print(f"Cell [{row}][{col}] = {matrix[row][col]}")

def on_drag(event):
    """Paint cells while dragging"""
    if is_dragging:
        col = event.x // cell_size
        row = event.y // cell_size
        paint_cell(row, col)

def on_release(event):
    """Stop dragging"""
    global is_dragging
    is_dragging = False

def on_key_r(event):
    """Initialize random noise for cave generation (45% walls)"""
    wall_chance = 0.45

    for row in range(50):
        for col in range(50):
            if random.random() < wall_chance:
                matrix[row][col] = 0
                canvas.itemconfig(rectangles[(row, col)], fill='black')
            else:
                matrix[row][col] = 1
                canvas.itemconfig(rectangles[(row, col)], fill='white')

    print("Random noise generated (45% walls)")

def on_key_c(event):
    """Clear all - reset everything to 1 (white)"""
    for row in range(50):
        for col in range(50):
            matrix[row][col] = 1
            rect_id = rectangles[(row, col)]
            canvas.itemconfig(rect_id, fill='white')
    
    print("Grid cleared - all cells reset to 1")



def smooth_once():
    """Run one smoothing pass, returns True if any cells changed"""
    global matrix
    new_matrix = [[0 for _ in range(50)] for _ in range(50)]
    changed = False

    for row in range(50):
        for col in range(50):
            wall_count = 0
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 2):
                    if 0 <= i < 50 and 0 <= j < 50:
                        if matrix[i][j] == 0:
                            wall_count += 1
                    else:
                        wall_count += 1

            if wall_count >= 5:
                new_matrix[row][col] = 0
            else:
                new_matrix[row][col] = 1

            if new_matrix[row][col] != matrix[row][col]:
                changed = True

    matrix = new_matrix
    return changed


def smooth(event):
    """Smooths until stable or max iterations reached"""
    max_iterations = 50

    for i in range(max_iterations):
        changed = smooth_once()
        if not changed:
            print(f"Stabilized after {i + 1} iterations")
            break
    else:
        print(f"Stopped after {max_iterations} iterations")

    # Update display
    for row in range(50):
        for col in range(50):
            color = 'white' if matrix[row][col] == 1 else 'black'
            canvas.itemconfig(rectangles[(row, col)], fill=color)

canvas.bind("<Button-1>", on_click)
canvas.bind("<B1-Motion>", on_drag)
canvas.bind("<ButtonRelease-1>", on_release)
root.bind("r", on_key_r)
root.bind("c", on_key_c)
root.bind("s", smooth)

root.mainloop()
