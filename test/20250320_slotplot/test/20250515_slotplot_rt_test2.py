import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

root = tk.Tk()
root.title("Matplotlib 动画嵌入 Tkinter")

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = ax.plot([], [], 'r-')

def init():
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1, 1)
    return ln,

def update(frame):
    xdata.append(frame)
    ydata.append(np.sin(frame))
    ln.set_data(xdata, ydata)
    return ln,

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

ani = animation.FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                              init_func=init, blit=True, interval=50)
# ani = animation.FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
#                               blit=True, interval=50)

root.mainloop()
