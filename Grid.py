import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageDraw
import time

def save_image(grid_width, grid_height, grid_state):
    cell_size = 40  # Size of each cell in pixels
    width = grid_width * cell_size
    height = grid_height * cell_size

    # Create an image with a transparent background
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Draw white squares for the clicked cells
    for row in range(grid_height):
        for col in range(grid_width):
            if grid_state[row][col]:
                x0 = col * cell_size
                y0 = row * cell_size
                x1 = x0 + cell_size
                y1 = y0 + cell_size
                draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255, 255))

    # Generate a unique filename using the current timestamp
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"grid_image_{timestamp}.png"

    # Save the image
    image.save(filename)
    print(f"Image saved as {filename}")

def main():
    # Get the grid dimensions from the user
    root = tk.Tk()
    root.withdraw()
    grid_width = simpledialog.askinteger("Input", "Enter the number of squares in width:", minvalue=1)
    grid_height = simpledialog.askinteger("Input", "Enter the number of squares in height:", minvalue=1)

    if not grid_width or not grid_height:
        return

    # Initialize grid state
    grid_state = [[False] * grid_width for _ in range(grid_height)]

    # Main window
    root = tk.Tk()
    root.title("Grid Color Picker")

    # Create scrollable canvas
    canvas_frame = tk.Frame(root)
    canvas_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(canvas_frame, bg="gray")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add scrollbars
    h_scroll = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
    h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
    v_scroll = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
    v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

    # Define scrollable region
    cell_size = 40
    canvas_width = grid_width * cell_size
    canvas_height = grid_height * cell_size
    canvas.config(scrollregion=(0, 0, canvas_width, canvas_height))

    # Draw the grid
    rect_ids = [[None for _ in range(grid_width)] for _ in range(grid_height)]
    for i in range(grid_height):
        for j in range(grid_width):
            x0 = j * cell_size
            y0 = i * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size
            rect_ids[i][j] = canvas.create_rectangle(x0, y0, x1, y1, outline="white", fill="black")

    # Toggle cell state on click
    def toggle_cell(event):
        col = int(canvas.canvasx(event.x) // cell_size)
        row = int(canvas.canvasy(event.y) // cell_size)

        if 0 <= row < grid_height and 0 <= col < grid_width:
            grid_state[row][col] = not grid_state[row][col]
            color = "white" if grid_state[row][col] else "black"
            canvas.itemconfig(rect_ids[row][col], fill=color)

    canvas.bind("<Button-1>", toggle_cell)

    # Save button
    def save_and_exit():
        save_image(grid_width, grid_height, grid_state)
        root.destroy()

    save_button = tk.Button(root, text="Save Image", command=save_and_exit)
    save_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
