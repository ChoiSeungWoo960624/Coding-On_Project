import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Tkinter 창 생성
root = tk.Tk()
root.title("Tkinter 그래프 예제")

# Matplotlib 그래프 생성
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
ax.plot([1, 2, 3, 4, 5], [10, 20, 25, 30, 40], marker="o")
ax.set_title("간단한 라인 그래프")

# Tkinter에서 Matplotlib 그래프 삽입
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack()

root.mainloop()
