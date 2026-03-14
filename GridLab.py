import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import time
import sys
import os


# -------- resource path (works for exe) --------
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# -------- set application icon --------
def set_icon(window):
    icon_path = resource_path("icon.ico")
    img = Image.open(icon_path)
    icon = ImageTk.PhotoImage(img)
    window.iconphoto(True, icon)


# -------- save grid image --------
def save_image(grid_width, grid_height, grid_state):

    cell_size = 40
    width = grid_width * cell_size
    height = grid_height * cell_size

    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    for row in range(grid_height):
        for col in range(grid_width):

            if grid_state[row][col]:

                x0 = col * cell_size
                y0 = row * cell_size
                x1 = x0 + cell_size
                y1 = y0 + cell_size

                draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255, 255))

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"grid_image_{timestamp}.png"

    image.save(filename)
    print(f"Image saved as {filename}")


# -------- main dimension window --------
def main():

    def get_dimensions():

        try:
            grid_width = int(width_entry.get())
            grid_height = int(height_entry.get())

            if grid_width <= 0 or grid_height <= 0:
                raise ValueError

            dimensions_window.destroy()
            start_main_window(grid_width, grid_height)

        except ValueError:
            error_label.config(text="Please enter valid positive integers.")

    dimensions_window = tk.Tk()
    dimensions_window.title("Grid Dimensions")
    set_icon(dimensions_window)

    tk.Label(dimensions_window,
             text="Enter Grid Dimensions",
             font=("Arial", 14)).pack(pady=10)

    input_frame = tk.Frame(dimensions_window)
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="Width:").grid(row=0, column=0, padx=5)

    width_entry = tk.Entry(input_frame)
    width_entry.grid(row=0, column=1, padx=5)

    tk.Label(input_frame, text="Height:").grid(row=1, column=0, padx=5)

    height_entry = tk.Entry(input_frame)
    height_entry.grid(row=1, column=1, padx=5)

    error_label = tk.Label(dimensions_window, text="", fg="red")
    error_label.pack()

    submit_button = tk.Button(dimensions_window,
                              text="Submit",
                              command=get_dimensions)

    submit_button.pack(pady=10)

    dimensions_window.mainloop()


# -------- main grid window --------
def start_main_window(grid_width, grid_height):

    grid_state = [[False] * grid_width for _ in range(grid_height)]

    root = tk.Tk()
    root.title("GridLab")
    set_icon(root)

    canvas_frame = tk.Frame(root)
    canvas_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(canvas_frame, bg="gray")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    h_scroll = tk.Scrollbar(canvas_frame,
                            orient=tk.HORIZONTAL,
                            command=canvas.xview)

    h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

    v_scroll = tk.Scrollbar(canvas_frame,
                            orient=tk.VERTICAL,
                            command=canvas.yview)

    v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(xscrollcommand=h_scroll.set,
                     yscrollcommand=v_scroll.set)

    cell_size = 40
    canvas_width = grid_width * cell_size
    canvas_height = grid_height * cell_size

    canvas.config(scrollregion=(0, 0, canvas_width, canvas_height))

    rect_ids = [[None for _ in range(grid_width)]
                for _ in range(grid_height)]

    for i in range(grid_height):

        for j in range(grid_width):

            x0 = j * cell_size
            y0 = i * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size

            rect_ids[i][j] = canvas.create_rectangle(
                x0, y0, x1, y1,
                outline="white",
                fill="black"
            )

    # toggle cell color
    def toggle_cell(event):

        col = int(canvas.canvasx(event.x) // cell_size)
        row = int(canvas.canvasy(event.y) // cell_size)

        if 0 <= row < grid_height and 0 <= col < grid_width:

            grid_state[row][col] = not grid_state[row][col]

            color = "white" if grid_state[row][col] else "black"

            canvas.itemconfig(rect_ids[row][col], fill=color)

    canvas.bind("<Button-1>", toggle_cell)

    # save button
    def save_and_exit():
        save_image(grid_width, grid_height, grid_state)
        root.destroy()

    save_button = tk.Button(root,
                            text="Save Image",
                            command=save_and_exit)

    save_button.pack()

    root.mainloop()


# -------- start program --------
if __name__ == "__main__":
    main()