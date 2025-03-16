import tkinter as tk

def on_button_click():
    label.config(text="전기전력확인하기")

# 메인 윈도우 설정
root = tk.Tk()
root.title("전기전력 확인용 UI")
root.geometry("620x480")

# 레이블
label = tk.Label(root, text="전기전력확인", font=("Arial", 16))
label.pack(pady=20)

# 프레임 
frame = tk.Frame(root)
frame.pack(pady=20)

# 최대 금액 입력
max_amount_label = tk.Label(frame, text="최대 금액", font=("Arial", 14))
max_amount_label.grid(row=0, column=0, padx=10, pady=5)
max_amount_entry = tk.Entry(frame, font=("Arial", 14))
max_amount_entry.grid(row=0, column=1, pady=5)

# 경고 금액 입력
warning_amount_label = tk.Label(frame, text="경고 금액", font=("Arial", 14))
warning_amount_label.grid(row=1, column=0, padx=10, pady=5)
warning_amount_entry = tk.Entry(frame, font=("Arial", 14))
warning_amount_entry.grid(row=1, column=1, pady=5)

# 메인 루프 실행
root.mainloop()