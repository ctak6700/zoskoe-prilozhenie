import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

#библиотека для расписания
SCHEDULE = {
    "1": {
        "Понедельник": [
            ("10:40 - 12:10", "пара", "Садовая 54, Лаб. 5"),
            ("10:40 - 12:10", "пара", "Садовая 54, Лаб. 5")
        ],
        "Вторник": [
            ("12:50 - 14:20", "Программирование (Python, Структуры данных)", "Точка кипения"),
            ("14:30 - 16:00", "Линейная алгебра", "Садовая 54, ауд. 404")
        ]
    },
    "2": {
        "Понедельник": [
            ("09:00 - 10:30", "Аналитическая геометрия", "ауд. 201"),
            ("10:40 - 12:10", "Инженерная графика", "ауд. 202")
        ],
        "Среда": [
            ("10:40 - 12:10", "Физика (Кинематика)", "Лаб. 2")
        ]
    },
    "3": {
        "Четверг": [
            ("09:00 - 10:30", "Графический дизайн", "Студия 1"),
            ("10:40 - 12:10", "Типографика", "Студия 2")
        ]
    },
    "4": {
        "Пятница": [
            ("12:50 - 14:20", "Физика (Электродинамика)", "Лаб. 6"),
            ("14:30 - 16:00", "Компьютерное зрение (OpenCV)", "Точка кипения")
        ]
    }
}

#дни
DAYS_OF_WEEK = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]

def show_schedule():
    group = group_combo.get()
    day = day_combo.get()

    if not group or not day:
        messagebox.showwarning("Ошибка", "Пожалуйста, выберите группу и день недели.")
        return

    # текстовая строка где писать
    text_output.config(state=tk.NORMAL)
    text_output.delete(1.0, tk.END)

    # выводит расписание
    group_data = SCHEDULE.get(group, {})
    day_schedule = group_data.get(day, [])

    # прочее инфо
    if not day_schedule:
        text_output.insert(tk.END, f"Для группы {group} на {day} пар нет.\n")
    else:
        text_output.insert(tk.END, f"--- Расписание: Группа {group} | {day} ---\n\n")
        for time, subject, room in day_schedule:
            text_output.insert(tk.END, f" Время: {time}\n")
            text_output.insert(tk.END, f" Пара: {subject}\n")
            text_output.insert(tk.END, f" Кабинет: {room}\n")
            text_output.insert(tk.END, "-"*45 + "\n")

    # чет блокирует
    text_output.config(state=tk.DISABLED)

# основное окно
root = tk.Tk()
root.title("Расписание занятий")
root.geometry("450x450")
root.resizable(False, False)

# фрейм контроль без него баглаг
frame_controls = tk.Frame(root, pady=10)
frame_controls.pack()

#выбор группы
tk.Label(frame_controls, text="Выберите группу:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
group_combo = ttk.Combobox(frame_controls, values=["1", "2", "3", "4"], state="readonly", width=15)
group_combo.grid(row=0, column=1, padx=5, pady=5)

#выбор дня
tk.Label(frame_controls, text="Выберите день недели:", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
day_combo = ttk.Combobox(frame_controls, values=DAYS_OF_WEEK, state="readonly", width=15)
day_combo.grid(row=1, column=1, padx=5, pady=5)

# кнопка
btn_show = tk.Button(root, text="Показать расписание", command=show_schedule, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
btn_show.pack(pady=10)

# эта фигня выводит текст
text_output = tk.Text(root, height=16, width=52, font=("Consolas", 10), state=tk.DISABLED, bg="#f9f9f9", wrap=tk.WORD)
text_output.pack(padx=10, pady=5)

root.mainloop()