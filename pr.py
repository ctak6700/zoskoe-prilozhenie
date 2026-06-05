import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import json
import os

DATA_FILE = "exams_library.json"


class ExamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Трекер Экзаменов")
        self.root.geometry("650x550")

        self.exams = []
        self.load_data()

        self.setup_ui()
        self.update_listbox()

    def setup_ui(self):
        input_frame = ttk.LabelFrame(self.root, text="Ввод данных", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(input_frame, text="Предмет:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.subject_entry = ttk.Entry(input_frame, width=30)
        self.subject_entry.grid(row=0, column=1, pady=2)

        ttk.Label(input_frame, text="Преподаватель:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.teacher_entry = ttk.Entry(input_frame, width=30)
        self.teacher_entry.grid(row=1, column=1, pady=2)

        ttk.Label(input_frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.date_entry = ttk.Entry(input_frame, width=30)
        self.date_entry.grid(row=2, column=1, pady=2)

        self.cheat_var = tk.BooleanVar()
        self.cheat_check = ttk.Checkbutton(input_frame, text="Можно списать?", variable=self.cheat_var)
        self.cheat_check.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=2)

        ttk.Label(input_frame, text="Шкала Лебедевой (0-100%):").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.strictness_scale = tk.Scale(input_frame, from_=0, to=100, orient=tk.HORIZONTAL)
        self.strictness_scale.grid(row=4, column=1, sticky=tk.W + tk.E, pady=2)

        add_btn = ttk.Button(input_frame, text="Добавить в библиотеку", command=self.add_exam)
        add_btn.grid(row=5, column=0, columnspan=2, pady=10)

        list_frame = ttk.LabelFrame(self.root, text="Библиотека (выбери предмет)", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.listbox = tk.Listbox(list_frame, height=6)
        self.listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.listbox.bind('<<ListboxSelect>>', self.show_details)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        output_frame = ttk.LabelFrame(self.root, text="Че имеем", padding=10)
        output_frame.pack(fill=tk.X, padx=10, pady=5)

        self.result_label = ttk.Label(output_frame, text="Нажми и увидь",
                                      justify=tk.LEFT)
        self.result_label.pack(anchor=tk.W)

    def add_exam(self):
        subject = self.subject_entry.get().strip()
        teacher = self.teacher_entry.get().strip()
        date_str = self.date_entry.get().strip()
        can_cheat = self.cheat_var.get()
        strictness = self.strictness_scale.get()

        if not subject or not teacher or not date_str:
            messagebox.showwarning("Ошибка", "Error!")
            return

        try:
            datetime.datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError:
            messagebox.showerror("Ошибка даты", "Используйте формат ДД.ММ.ГГГГ (например, 01.01.2026)")
            return

        exam_data = {
            "subject": subject,
            "teacher": teacher,
            "date": date_str,
            "can_cheat": can_cheat,
            "strictness": strictness
        }

        self.exams.append(exam_data)
        self.save_data()
        self.update_listbox()

        self.subject_entry.delete(0, tk.END)
        self.teacher_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.cheat_var.set(False)
        self.strictness_scale.set(0)

        messagebox.showinfo("Найс", "Данные в библиотеку!")

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for exam in self.exams:
            self.listbox.insert(tk.END, f"{exam['subject']} ({exam['date']}) - {exam['teacher']}")

    def show_details(self, event):
        selection = self.listbox.curselection()
        if not selection:
            return

        index = selection[0]
        exam = self.exams[index]

        today = datetime.date.today()
        exam_date = datetime.datetime.strptime(exam["date"], "%d.%m.%Y").date()
        days_left = (exam_date - today).days

        cheat_text = "Да" if exam["can_cheat"] else "Нет"

        if days_left < 0:
            time_status = f"Экзамен прошел {abs(days_left)} дней назад."
            advice = "Ну шо, как оно?"
        elif days_left == 0:
            time_status = "Прикинь, экз сегодня"
            advice = "Тут поможет только молитва и ягер."
        else:
            time_status = f"Дней до экзамена: {days_left}"

            if exam["strictness"] > 80 and not exam["can_cheat"]:
                advice = "Сама лебедева принимает, тебе не выжить."
            elif days_left < 3 and exam["strictness"] > 50:
                advice = "Ну пора бы и начать готовится."
            elif exam["can_cheat"] and exam["strictness"] < 40:
                advice = "Кемарни, а там когда нибудь и до билетов дойдешь."
            else:
                advice = "Думай только о мираже."

        result_text = (
            f"Предмет: {exam['subject']}\n"
            f"Преподаватель: {exam['teacher']} (Злость: {exam['strictness']}%)\n"
            f"Возможность списать: {cheat_text}\n"
            f"-----------------------------------\n"
            f"{time_status}\n"
            f"Вердикт: {advice}"
        )
        self.result_label.config(text=result_text)

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.exams, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                try:
                    self.exams = json.load(f)
                except json.JSONDecodeError:
                    self.exams = []


if __name__ == "__main__":
    root = tk.Tk()
    app = ExamApp(root)
    root.mainloop()
