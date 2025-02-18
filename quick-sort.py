import time
import random
import tkinter as tk
import os

if os.name == 'posix':  # macOS fix
    os.environ['TK_SILENCE_DEPRECATION'] = '1'

# Initialize window
root = tk.Tk()
root.title('Sorting Algorithm Visualization')
root.geometry('800x600')
root.config(bg='black')

data = []  # Data list

# Canvas for drawing
canvas = tk.Canvas(root, width=700, height=400, bg='white')
canvas.pack(pady=20)

def drawData(data, colorArray):
    """ Function to draw circles for visualization """
    canvas.delete("all")
    c_width = 700
    y_position = 150  # Keep circles in the middle of the canvas
    spacing = 10

    # Dynamically adjust circle size
    max_size = min(40, (c_width - spacing * len(data)) // len(data))
    max_size = max(20, max_size)  # Keep a minimum size

    offset = (c_width - (len(data) * (max_size + spacing))) // 2

    for i in range(len(data)):
        x = i * (max_size + spacing) + offset
        y = y_position
        canvas.create_oval(x, y, x + max_size, y + max_size, fill=colorArray[i])
        canvas.create_text(x + max_size // 2, y + max_size // 2, text=str(data[i]), font=("Helvetica", 10), fill='black')

    root.update_idletasks()

def generate_data():
    """ Generate random numbers for sorting """
    global data
    try:
        min_val = int(minEntry.get())
        max_val = int(maxEntry.get())
        size = int(sizeEntry.get())
        if min_val >= max_val or size < 3:
            raise ValueError

        data = [random.randint(min_val, max_val) for _ in range(size)]
        drawData(data, ['red' for _ in range(len(data))])
    except ValueError:
        error_label.config(text="Invalid Input! Check Min, Max, and Size values.", fg="red")

def partition(data, low, high):
    """ Partition function for QuickSort """
    pivot = data[high]
    i = low - 1
    for j in range(low, high):
        if data[j] < pivot:
            i += 1
            data[i], data[j] = data[j], data[i]
            drawData(data, getColorArray(len(data), low, high, i, j, True))
            root.after(speedScale.get())  # Non-blocking delay
    data[i+1], data[high] = data[high], data[i+1]
    drawData(data, getColorArray(len(data), low, high, i+1, high, True))
    root.after(speedScale.get())
    return i+1

def quick_sort(data, low, high):
    """ Recursive QuickSort """
    if low < high:
        pi = partition(data, low, high)
        quick_sort(data, low, pi - 1)
        quick_sort(data, pi + 1, high)

def getColorArray(dataLen, low, high, border, currIdx, isSwapping=False):
    """ Get color array for sorting animation """
    colorArray = ['gray' if low <= i <= high else 'white' for i in range(dataLen)]
    colorArray[high] = 'blue'
    colorArray[border] = 'red'
    colorArray[currIdx] = 'yellow'
    if isSwapping:
        colorArray[border] = colorArray[currIdx] = 'green'
    return colorArray

def start_algorithm():
    """ Start QuickSort Algorithm """
    global data
    if not data:
        return
    quick_sort(data, 0, len(data) - 1)
    drawData(data, ['green' for _ in range(len(data))])

# UI Elements
control_frame = tk.Frame(root, bg='grey')
control_frame.pack(pady=5)

speedScale = tk.Scale(control_frame, from_=10, to=500, length=200, digits=2, resolution=10, orient=tk.HORIZONTAL, label="Time (ms)")
speedScale.set(100)
speedScale.grid(row=0, column=1, padx=5, pady=5)

sizeEntry = tk.Scale(control_frame, from_=3, to=25, resolution=1, orient=tk.HORIZONTAL, label="Data Size")
sizeEntry.set(10)
sizeEntry.grid(row=1, column=0, padx=5, pady=5)

minEntry = tk.Scale(control_frame, from_=0, to=50, resolution=1, orient=tk.HORIZONTAL, label="Min Value")
minEntry.set(1)
minEntry.grid(row=1, column=1, padx=5, pady=5)

maxEntry = tk.Scale(control_frame, from_=10, to=100, resolution=1, orient=tk.HORIZONTAL, label="Max Value")
maxEntry.set(50)
maxEntry.grid(row=1, column=2, padx=5, pady=5)

tk.Button(control_frame, text="Generate", command=generate_data, bg='white', fg='black').grid(row=1, column=3, padx=5, pady=5)
tk.Button(control_frame, text="Start", command=start_algorithm, bg='white', fg='black').grid(row=0, column=3, padx=5, pady=5)

error_label = tk.Label(root, text="", bg='black')
error_label.pack()

root.mainloop()
