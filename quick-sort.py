import time
import random
from tkinter import *
import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'

root = Tk()
root.title('Sorting Algorithm Visualisation')
root.maxsize(900, 600)
root.config(bg='black')

data = []

def drawData(data, colorArray):
    canvas.delete("all")
    c_height = 380
    c_width = 600
    y_position = 150 # Keep circles in the middle of the canvas
    offset = 30
    spacing = 10

    # Calculate the circle diameter dynamically based on data size and available width
    total_width = c_width - 2 * offset - spacing * (len(data) - 1)
    circle_diameter = total_width / len(data) - spacing  # Adjusted diameter

    # Calculate the total width occupied by circles
    total_circle_width = len(data) * (circle_diameter + spacing) - spacing
    offset = (c_width - total_circle_width) / 2  # Adjusted offset for centering

    for i in range(len(data)):
        # Calculate circle coordinates for a horizontal line
        x = i * (circle_diameter + spacing) + offset
        y = y_position

        canvas.create_oval(x, y, x + circle_diameter, y + circle_diameter, fill=colorArray[i])
        canvas.create_text(x + circle_diameter // 2, y + circle_diameter // 2, anchor=CENTER, text=str(data[i]))

    root.update_idletasks()


def Generate():
    global data

    minVal = int(minEntry.get())
    maxVal = int(maxEntry.get())
    size = int(sizeEntry.get())

    data = []
    for _ in range(size):
        data.append(random.randrange(minVal, maxVal + 1))

    drawData(data, ['red' for x in range(len(data))])


def partition(data, head, tail, drawData, timeTick):
    border = head
    pivot = data[tail]

    drawData(data, getColorArray(len(data), head, tail, border, border))
    time.sleep(timeTick)

    for j in range(head, tail):
        if data[j] < pivot:
            drawData(data, getColorArray(len(data), head, tail, border, j, True))
            time.sleep(timeTick)

            data[border], data[j] = data[j], data[border]
            border += 1

        drawData(data, getColorArray(len(data), head, tail, border, j))
        time.sleep(timeTick)

    # swap pivot with border value
    drawData(data, getColorArray(len(data), head, tail, border, tail, True))
    time.sleep(timeTick)

    data[border], data[tail] = data[tail], data[border]

    return border


def quick_sort(data, head, tail, drawData, timeTick):
    if head < tail:
        partitionIdx = partition(data, head, tail, drawData, timeTick)

        # LEFT PARTITION
        quick_sort(data, head, partitionIdx - 1, drawData, timeTick)

        # RIGHT PARTITION
        quick_sort(data, partitionIdx + 1, tail, drawData, timeTick)


def getColorArray(dataLen, head, tail, border, currIdx, isSwaping=False):
    colorArray = []
    for i in range(dataLen):
        # base coloring
        if i >= head and i <= tail:
            colorArray.append('gray')
        else:
            colorArray.append('white')

        if i == tail:
            colorArray[i] = 'blue'
        elif i == border:
            colorArray[i] = 'red'
        elif i == currIdx:
            colorArray[i] = 'yellow'

        if isSwaping:
            if i == border or i == currIdx:
                colorArray[i] = 'green'

    return colorArray

def StartAlgorithm():
    global data
    if not data: return

    quick_sort(data, 0, len(data) - 1, drawData, speedScale.get())
    drawData(data, ['green' for x in range(len(data))])

# frame / base lauout
UI_frame = Frame(root, width=600, height=200, bg='grey')
UI_frame.grid(row=0, column=0, padx=10, pady=5 , sticky="nsew")

canvas = Canvas(root, width=600, height=380, bg='white')
canvas.grid(row=1, column=0, padx=10, pady=5 , sticky="nsew")

speedScale = Scale(UI_frame, from_=0.1, to=5.0, length=200, digits=2, resolution=0.2, orient=HORIZONTAL,
                   label="Select Speed [s]")
speedScale.grid(row=0, column=2, padx=5, pady=5)
speedScale.set(1.0)

sizeEntry = Scale(UI_frame, from_=3, to=25, resolution=1, orient=HORIZONTAL, label="Data Size")
sizeEntry.grid(row=1, column=0, padx=5, pady=5)

minEntry = Scale(UI_frame, from_=0, to=10, resolution=1, orient=HORIZONTAL, label="Min Value")
minEntry.grid(row=1, column=1, padx=5, pady=5)

maxEntry = Scale(UI_frame, from_=10, to=100, resolution=1, orient=HORIZONTAL, label="Max Value")
maxEntry.grid(row=1, column=2, padx=5, pady=5)

UI_frame.config(bg='lightgrey')
Button(UI_frame, text="Generate", command=Generate, bg='white', fg='black').grid(row=1, column=3, padx=5, pady=5)
Button(UI_frame, text="Start", command=StartAlgorithm, bg='red', fg='black').grid(row=0, column=3, padx=5, pady=5)

root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

root.mainloop()
