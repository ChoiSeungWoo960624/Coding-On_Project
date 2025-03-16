import tkinter as tk

def open_new_window():
    new_window = tk.Toplevel(root)
    new_window.title("추가 창")
    new_label = tk.Label(new_window, text="추가 창입니다.")
    new_label.pack()
    
root = tk.Tk()
root.title("기본 창")

label = tk.Label(root, text="기본 창입니다.")
label.pack()

button = tk.Button(root, text="추가 창 열기", command=open_new_window)
button.pack()
 
root.mainloop()

'''
앞창이 꺼지면 뒷창도꺼짐
'''