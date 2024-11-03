import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os

columns = ['№', 'Производитель', 'Модель', 'Цвет', 'Коробка передач', 'Привод', 'Тип двигателя', 'Заведена/Не заведена', 'Двери открыты/Закрыты']

def showdata():
    try:
        with open('data_source.txt', 'r', encoding='utf-8') as file:
            data = file.readlines()
        r = []
        for i in data:
            if i.strip():
                s = [x for x in i.strip().split("/")]
                r.append(s)
        return r
    except FileNotFoundError:
        return []

def find_num(): #номер машинки
    data = showdata()
    number = 0
    for row in data:
        num1 = int(row[0])
        if num1 > number:
            number = num1
    return number

def delete_car():
    selected_item = main_tree.selection()[0]
    if selected_item:
        selected_values = main_tree.item(selected_item)['values']
        try:
            car_number = int(selected_values[0]) #номер машинки
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат номера машины.")
            return

        if messagebox.askyesno("Подтверждение удаления", f"Вы действительно хотите удалить машину №{car_number}?"):
            try:
                with open('data_source.txt', 'r+', encoding='utf-8') as file:
                    d = file.readlines()
                    rdata = []
                    for i in d:
                        s = [x for x in i.strip().split("/")]
                        if int(s[0]) != car_number:
                            rdata.append(s)
                    for i in range(len(rdata)):
                        rdata[i][0] = str(i + 1)
                    s = ["/".join(x) for x in rdata]
                    file.seek(0)
                    file.truncate(0)
                    for i in s:
                        file.write(str(i) + '\n')
                update_main_table()
                main_tree.selection_set(())
                delete_button['state'] = tk.DISABLED
                edit_button['state'] = tk.DISABLED
            except FileNotFoundError:
                messagebox.showerror("Ошибка", "Файл data_source.txt не найден.")

def change_car():
    selected_item = main_tree.selection()[0]
    if selected_item:
        selected_values = main_tree.item(selected_item)['values']
        try:
            car_number = int(selected_values[0])
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат номера машины.")
            return

        def save_changes():
            try:
                vvod_fabric = producer_var.get()
                vvod_model = model_var.get()
                vvod_color = color_var.get()
                vvod_transmission = transmission_var.get()
                vvod_drive = drive_var.get()
                vvod_engine = engine_type_var.get()
                vvod_started = started_var.get()
                vvod_open = open_var.get()
                with open('data_source.txt', 'r+', encoding='utf-8') as file:
                    d = file.readlines()
                    rdata = []
                    for i in d:
                        s = [x for x in i.strip().split("/")]
                        if int(s[0]) == car_number:
                            s[1] = vvod_fabric
                            s[2] = vvod_model
                            s[3] = vvod_color
                            s[4] = vvod_transmission
                            s[5] = vvod_drive
                            s[6] = vvod_engine
                            s[7] = vvod_started
                            s[8] = vvod_open
                        rdata.append(s)
                    s = ["/".join(x) for x in rdata]
                    file.seek(0)
                    file.truncate(0)
                    for i in s:
                        file.write(str(i) + '\n')
                update_main_table()
                edit_window.destroy()
            except FileNotFoundError:
                messagebox.showerror("Ошибка", "Файл data_source.txt не найден.")

        data = showdata()
        for i in range(len(data)):
            if int(data[i][0]) == car_number:
                car_data = data[i]
                break

        edit_window = tk.Toplevel(root)
        edit_window.title(f"Редактирование машины №{car_number}")

        # Центрирование окна
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = edit_window.winfo_reqwidth()
        window_height = edit_window.winfo_reqheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        edit_window.geometry(f"+{x}+{y}")

        # Производитель
        producer_label = tk.Label(edit_window, text="Производитель:")
        producer_label.grid(row=0, column=0, padx=5, pady=5)
        global producer_var
        producer_var = tk.StringVar(edit_window)
        producer_var.set(car_data[1])
        global producer_listbox
        producer_listbox = ttk.Combobox(edit_window, textvariable=producer_var, values=get_producers(), state="readonly")
        producer_listbox.grid(row=1, column=0, padx=5, pady=5)
        producer_listbox.bind("<<ComboboxSelected>>", lambda event: update_model_listbox2(producer_var.get(), model_listbox))

        # Модель
        model_label = tk.Label(edit_window, text="Модель:")
        model_label.grid(row=0, column=1, padx=5, pady=5)
        global model_var
        model_var = tk.StringVar(edit_window)
        model_var.set(car_data[2])
        global model_listbox
        model_listbox = ttk.Combobox(edit_window, textvariable=model_var, values=get_models_by_producer(producer_var.get()), state="readonly")
        model_listbox.grid(row=1, column=1, padx=5, pady=5)

        # Цвет
        color_label = tk.Label(edit_window, text="Цвет:")
        color_label.grid(row=2, column=0, padx=5, pady=5)
        global color_var
        color_var = tk.StringVar(edit_window)
        color_var.set(car_data[3])
        color_listbox = ttk.Combobox(edit_window, textvariable=color_var, values=get_colors(), state="readonly")
        color_listbox.grid(row=3, column=0, padx=5, pady=5)

        # Коробка передач
        transmission_label = tk.Label(edit_window, text="Коробка передач:")
        transmission_label.grid(row=2, column=1, padx=5, pady=5)
        global transmission_var
        transmission_var = tk.StringVar(edit_window)
        transmission_var.set(car_data[4])
        transmission_listbox = ttk.Combobox(edit_window, textvariable=transmission_var, values=["Автоматическая", "Механическая", "Роботизировання", "Вариатор"], state="readonly")
        transmission_listbox.grid(row=3, column=1, padx=5, pady=5)

        # Привод
        drive_label = tk.Label(edit_window, text="Привод:")
        drive_label.grid(row=4, column=0, padx=5, pady=5)
        global drive_var
        drive_var = tk.StringVar(edit_window)
        drive_var.set(car_data[5])
        drive_listbox = ttk.Combobox(edit_window, textvariable=drive_var, values=["Задний", "Передний", "Полный"], state="readonly")
        drive_listbox.grid(row=5, column=0, padx=5, pady=5)

        # Тип двигателя
        engine_type_label = tk.Label(edit_window, text="Тип двигателя:")
        engine_type_label.grid(row=4, column=1, padx=5, pady=5)
        global engine_type_var
        engine_type_var = tk.StringVar(edit_window)
        engine_type_var.set(car_data[6])
        engine_type_listbox = ttk.Combobox(edit_window, textvariable=engine_type_var, values=["Бензиновый", "Дизельный", "Инжекторный", "Роторный", "Гибридный"], state="readonly")
        engine_type_listbox.grid(row=5, column=1, padx=5, pady=5)

        # Заведена/Не заведена
        started_label = tk.Label(edit_window, text="Заведена/Не заведена:")
        started_label.grid(row=6, column=0, padx=5, pady=5)
        global started_var
        started_var = tk.StringVar(edit_window)
        started_var.set(car_data[7])
        started_listbox = ttk.Combobox(edit_window, textvariable=started_var, values=["Заведена", "Не заведена"], state="readonly")
        started_listbox.grid(row=7, column=0, padx=5, pady=5)

        # Открыта/Закрыта
        open_label = tk.Label(edit_window, text="Открыта/Закрыта:")
        open_label.grid(row=6, column=1, padx=5, pady=5)
        global open_var
        open_var = tk.StringVar(edit_window)
        open_var.set(car_data[8])
        open_listbox = ttk.Combobox(edit_window, textvariable=open_var, values=["Открыта", "Закрыта"], state="readonly")
        open_listbox.grid(row=7, column=1, padx=5, pady=5)

        save_button = tk.Button(edit_window, text="Сохранить", command=save_changes)
        save_button.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

def add_car():
    def save_car():
        try:
            vvod_fabric = producer_var.get()
            vvod_model = model_var.get()
            vvod_color = color_var.get()
            vvod_transmission = transmission_var.get()
            vvod_drive = drive_var.get()
            vvod_engine = engine_type_var.get()
            vvod_started = started_var.get()
            vvod_open = open_var.get()
            num = find_num() + 1
            car_string = f'{num}/{vvod_fabric}/{vvod_model}/{vvod_color}/{vvod_transmission}/{vvod_drive}/{vvod_engine}/{vvod_started}/{vvod_open}'
            with open('data_source.txt', 'a', encoding='utf-8') as file:
                file.write(car_string + '\n')
            update_main_table()
            add_window.destroy()
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл data_source.txt не найден.")

    add_window = tk.Toplevel(root)
    add_window.title("Добавить машину")

    # Центрирование окна
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = add_window.winfo_reqwidth()
    window_height = add_window.winfo_reqheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    add_window.geometry(f"+{x}+{y}")

    # Производитель
    producer_label = tk.Label(add_window, text="Производитель:")
    producer_label.grid(row=0, column=0, padx=5, pady=5)
    global producer_var
    producer_var = tk.StringVar(add_window)
    global producer_listbox
    producer_listbox = ttk.Combobox(add_window, textvariable=producer_var, values=get_producers(), state="readonly")
    producer_listbox.grid(row=1, column=0, padx=5, pady=5)
    producer_listbox.bind("<<ComboboxSelected>>", lambda event: update_model_listbox2(producer_var.get(), model_listbox))

    # Модель
    model_label = tk.Label(add_window, text="Модель:")
    model_label.grid(row=0, column=1, padx=5, pady=5)
    global model_var
    model_var = tk.StringVar(add_window)
    global model_listbox
    model_listbox = ttk.Combobox(add_window, textvariable=model_var, values=[], state="readonly")  # Initialize with empty values
    model_listbox.grid(row=1, column=1, padx=5, pady=5)

    # Цвет
    color_label = tk.Label(add_window, text="Цвет:")
    color_label.grid(row=2, column=0, padx=5, pady=5)
    global color_var
    color_var = tk.StringVar(add_window)
    color_listbox = ttk.Combobox(add_window, textvariable=color_var, values=get_colors(), state="readonly")
    color_listbox.grid(row=3, column=0, padx=5, pady=5)

    # Коробка передач
    transmission_label = tk.Label(add_window, text="Коробка передач:")
    transmission_label.grid(row=2, column=1, padx=5, pady=5)
    global transmission_var
    transmission_var = tk.StringVar(add_window)
    transmission_listbox = ttk.Combobox(add_window, textvariable=transmission_var, values=["Автомат", "Механика", "Робот", "Вариатор"], state="readonly")
    transmission_listbox.grid(row=3, column=1, padx=5, pady=5)

    # Привод
    drive_label = tk.Label(add_window, text="Привод:")
    drive_label.grid(row=4, column=0, padx=5, pady=5)
    global drive_var
    drive_var = tk.StringVar(add_window)
    drive_listbox = ttk.Combobox(add_window, textvariable=drive_var, values=["Задний", "Передний", "Полный"], state="readonly")
    drive_listbox.grid(row=5, column=0, padx=5, pady=5)

    # Тип двигателя
    engine_type_label = tk.Label(add_window, text="Тип двигателя:")
    engine_type_label.grid(row=4, column=1, padx=5, pady=5)
    global engine_type_var
    engine_type_var = tk.StringVar(add_window)
    engine_type_listbox = ttk.Combobox(add_window, textvariable=engine_type_var, values=["Бензиновый", "Дизельный", "Инжекторный", "Роторный", "Гибридный"], state="readonly")
    engine_type_listbox.grid(row=5, column=1, padx=5, pady=5)

    # Заведена/Не заведена
    started_label = tk.Label(add_window, text="Заведена/Не заведена:")
    started_label.grid(row=6, column=0, padx=15, pady=15)
    global started_var
    started_var = tk.StringVar(add_window)
    started_listbox = ttk.Combobox(add_window, textvariable=started_var, values=["Заведена", "Не заведена"], state="readonly")
    started_listbox.grid(row=7, column=0, padx=15, pady=15)

    # Открыта/Закрыта
    open_label = tk.Label(add_window, text="Открыта/Закрыта:")
    open_label.grid(row=6, column=1, padx=15, pady=15)
    global open_var
    open_var = tk.StringVar(add_window)
    open_listbox = ttk.Combobox(add_window, textvariable=open_var, values=["Открыта", "Закрыта"], state="readonly")
    open_listbox.grid(row=7, column=1, padx=15, pady=15)

    save_button = tk.Button(add_window, text="Сохранить", command=save_car)
    save_button.grid(row=8, column=0, columnspan=2, padx=15, pady=15)

def update_main_table(): #обновление содержимого дерева
    data = showdata()
    main_tree.delete(*main_tree.get_children())
    for row in data:
        main_tree.insert("", tk.END, values=row)

def select_car(event): #выбор элементов
    selected_items = main_tree.selection()
    if selected_items:
        edit_button['state'] = tk.NORMAL
        delete_button['state'] = tk.NORMAL

def clear_selection(event=None): #отмена текущего выбора
    main_tree.selection_set(())
    edit_button['state'] = tk.DISABLED
    delete_button['state'] = tk.DISABLED

def find_car(): #поиск машинки по критериям
    def search_car():
        global search_tree  #добавляем глобальную переменную search_tree
        data = showdata()
        found_cars = []
        for row in data:
            if (
                    (not producer_var.get() or row[1] == producer_var.get())
                    and (not model_var.get() or row[2] == model_var.get())
                    and (not color_var.get() or row[3] == color_var.get())
                    and (not transmission_var.get() or row[4] == transmission_var.get())
                    and (not drive_var.get() or row[5] == drive_var.get())
                    and (not engine_var.get() or row[6] == engine_var.get())
                    and (not started_var.get() or row[7] == started_var.get())
                    and (not open_var.get() or row[8] == open_var.get())
            ):
                found_cars.append(row)

        if found_cars:
            search_tree.delete(*search_tree.get_children())
            for row in found_cars:
                search_tree.insert("", tk.END, values=row)
        else:
            messagebox.showinfo("Результат поиска", "Машины с заданными параметрами не найдены")

    def clear_filters(): #очистить фильтры
        producer_var.set('')
        model_var.set('')
        color_var.set('')
        transmission_var.set('')
        drive_var.set('')
        engine_var.set('')
        started_var.set('')
        open_var.set('')
        # Обновляем список моделей после очистки фильтров
        update_model_listbox(producer_var.get(), model_listbox)
        search_car() # Обновить таблицу после очистки

    search_window = tk.Toplevel(root)
    search_window.title("Поиск машины")

    # Центрирование окна
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = search_window.winfo_reqwidth()
    window_height = search_window.winfo_reqheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    search_window.geometry(f"+{x}+{y}")

    # Создаем переменные для хранения значений из полей ввода
    number_var = tk.StringVar()
    producer_var = tk.StringVar()
    model_var = tk.StringVar()
    color_var = tk.StringVar()
    transmission_var = tk.StringVar()
    drive_var = tk.StringVar()
    engine_var = tk.StringVar()
    started_var = tk.StringVar()
    open_var = tk.StringVar()

    # Создаем поля ввода и метки
    # Убрали номер
    producer_label = tk.Label(search_window, text="Производитель:")
    producer_label.grid(row=0, column=0, padx=5, pady=5)
    global producer_listbox
    producer_listbox = ttk.Combobox(search_window, textvariable=producer_var, values=get_producers(), state="readonly")
    producer_listbox.grid(row=1, column=0, padx=5, pady=5)
    producer_listbox.bind("<<ComboboxSelected>>", lambda event: update_model_listbox(producer_var.get(), model_listbox))

    # Модель
    model_label = tk.Label(search_window, text="Модель:")
    model_label.grid(row=0, column=1, padx=5, pady=5)
    global model_listbox
    model_listbox = ttk.Combobox(search_window, textvariable=model_var, values=[], state="readonly")
    model_listbox.grid(row=1, column=1, padx=5, pady=5)
    producer_listbox.bind("<<ComboboxSelected>>", lambda event: update_model_listbox2(producer_var.get(), model_listbox))

    # Цвет
    color_label = tk.Label(search_window, text="Цвет:")
    color_label.grid(row=2, column=0, padx=5, pady=5)
    global color_listbox
    color_listbox = ttk.Combobox(search_window, textvariable=color_var, values=get_colors(), state="readonly")
    color_listbox.grid(row=3, column=0, padx=5, pady=5)

    # Коробка передач
    transmission_label = tk.Label(search_window, text="Коробка передач:")
    transmission_label.grid(row=2, column=1, padx=5, pady=5)
    global transmission_listbox
    transmission_listbox = ttk.Combobox(search_window, textvariable=transmission_var, values=["Автомат", "Механика", "Робот", "Вариатор"], state="readonly")
    transmission_listbox.grid(row=3, column=1, padx=5, pady=5)

    # Привод
    drive_label = tk.Label(search_window, text="Привод:")
    drive_label.grid(row=4, column=0, padx=5, pady=5)
    global drive_listbox
    drive_listbox = ttk.Combobox(search_window, textvariable=drive_var, values=["Задний", "Передний", "Полный"], state="readonly")
    drive_listbox.grid(row=5, column=0, padx=5, pady=5)

    # Тип двигателя
    engine_type_label = tk.Label(search_window, text="Тип двигателя:")
    engine_type_label.grid(row=4, column=1, padx=5, pady=5)
    global engine_type_listbox
    engine_type_listbox = ttk.Combobox(search_window, textvariable=engine_var, values=["Бензиновый", "Дизельный", "Инжекторный", "Роторный", "Гибридный"], state="readonly")
    engine_type_listbox.grid(row=5, column=1, padx=5, pady=5)

    # Заведена/Не заведена
    started_label = tk.Label(search_window, text="Заведена/Не заведена:")
    started_label.grid(row=6, column=0, padx=5, pady=5)
    global started_listbox
    started_listbox = ttk.Combobox(search_window, textvariable=started_var, values=["Заведена", "Не заведена"], state="readonly")
    started_listbox.grid(row=7, column=0, padx=5, pady=5)

    # Открыта/Закрыта
    open_label = tk.Label(search_window, text="Открыта/Закрыта:")
    open_label.grid(row=6, column=1, padx=5, pady=5)
    global open_listbox
    open_listbox = ttk.Combobox(search_window, textvariable=open_var, values=["Открыта", "Закрыта"], state="readonly")
    open_listbox.grid(row=7, column=1, padx=5, pady=5)

    search_button = tk.Button(search_window, text="Найти", command=search_car)
    search_button.grid(row=8, column=0, padx=5, pady=5)

    clear_button = tk.Button(search_window, text="Очистить фильтры", command=clear_filters)
    clear_button.grid(row=8, column=1, padx=5, pady=5)

    # Таблица в отдельном окне
    search_tree_frame = tk.Frame(search_window)
    search_tree_frame.grid(row=9, column=0, columnspan=2, padx=5, pady=5)  # Используем grid

    global search_tree  # Объявляем search_tree как глобальную переменную
    search_tree = ttk.Treeview(search_tree_frame, columns=columns, show='headings')
    search_tree.column(columns[0], width=30)
    search_tree.column(columns[1], width=150)
    search_tree.column(columns[3], width=180)
    search_tree.column(columns[4], width=180)
    search_tree.column(columns[5], width=110)
    search_tree.column(columns[6], width=120)
    search_tree.column(columns[7], width=150)
    for i, col in enumerate(columns):
        search_tree.heading(col, text=col)
    search_tree.pack(side="left", fill="both", expand=True)

    search_window.update_idletasks()  # Обновление геометрии окна поиска
    search_window.geometry(f"+{x-550}+{y-300}")  # Установка размера и позиции окна поиска


def get_producers(): #добавление производителей машинок, моделей
    try:
        with open('data_proizvod.txt', 'r', encoding='utf-8') as file:
            producers = file.readlines()
        return [p.strip() for p in producers]
    except FileNotFoundError:
        messagebox.showerror("Ошибка", "Файл data_proizvod.txt не найден.")
        return []
def update_model_listbox2(producer, model_listbox):
    model_listbox['values'] = get_models_by_producer(producer)
    model_listbox.current(0)
def get_models_by_producer(producer):
    try:
        with open('data_marka.txt', 'r', encoding='utf-8') as file:
            data = file.readlines()
        models = []
        for line in data:
            parts = line.strip().split('/')
            if parts[0] == producer:
                models.extend(parts[1:])
        return models
    except FileNotFoundError:
        messagebox.showerror("Ошибка", "Файл data_marka.txt не найден.")
        return []

def get_colors(): #добавление цветов из txt
    try:
        with open('data_color.txt', 'r', encoding='utf-8') as file:
            colors = file.readlines()
        return [c.strip() for c in colors]
    except FileNotFoundError:
        messagebox.showerror("Ошибка", "Файл data_color.txt не найден.")
        return []
def update_model_listbox(producer, model_listbox):
    model_listbox['values'] = get_models_by_producer(producer)
    model_listbox.current(0)

def open_producers_window(): #управление списком производителей
    def save_producers():
        try:
            with open("data_proizvod.txt", "w", encoding='utf-8') as f:
                for item in producer_listbox.get(0, tk.END):
                    f.write(item + "\n")
            producers_window.destroy()
            messagebox.showinfo("Сохранение", "Производители успешно сохранены!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения: {e}")

    def add_item(listbox, var):
        new_item = entry.get()
        if new_item:
            listbox.insert(tk.END, new_item)
            var.set('')
            entry.delete(0, tk.END)

    def delete_item(listbox):
        selected_index = listbox.curselection()
        if selected_index:
            listbox.delete(selected_index[0])

    producers_window = tk.Toplevel(root)
    producers_window.title("Производители")

    # Центрирование окна
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = producers_window.winfo_reqwidth()
    window_height = producers_window.winfo_reqheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    producers_window.geometry(f"+{x}+{y}")

    # Список производителей
    producer_label = tk.Label(producers_window, text="Производитель:")
    producer_label.grid(row=0, column=0, columnspan=2)
    global producer_listbox
    producer_listbox = tk.Listbox(producers_window,width=40, height=15)
    producer_listbox.grid(row=1, column=0, columnspan=2)
    load_listbox("data_proizvod.txt", producer_listbox)
    # Поле ввода
    entry = tk.Entry(producers_window)
    entry.grid(row=2, column=0, columnspan=2,pady=5)
    var = tk.StringVar()
    entry['textvariable'] = var

    # Кнопки
    add_producer_button = tk.Button(producers_window, text="Добавить производителя", command=lambda: add_item(producer_listbox, var))
    add_producer_button.grid(row=3, column=0, padx=5, pady=5)
    delete_producer_button = tk.Button(producers_window, text="Удалить производителя", command=lambda: delete_item(producer_listbox))
    delete_producer_button.grid(row=3, column=1, padx=5, pady=5)

    # Кнопка сохранения
    save_button = tk.Button(producers_window, text="Сохранить", command=save_producers)
    save_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

def load_listbox(filename, listbox):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = file.readlines()
        listbox.delete(0, tk.END)  # Очищаем существующие элементы
        for i in data:
            listbox.insert(tk.END, i.strip())
    except FileNotFoundError:
        messagebox.showerror("Ошибка", f"Файл {filename} не найден.")
def load_listbox(filename, listbox):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = file.readlines()
        listbox.delete(0, tk.END)  # Очищаем существующие элементы
        for i in data:
            listbox.insert(tk.END, i.strip())
    except FileNotFoundError:
        messagebox.showerror("Ошибка", f"Файл {filename} не найден.")
def update_model_listbox2(producer, model_listbox):
    models = get_models_by_producer(producer)
    model_listbox['values'] = models  # Обновляем значения combobox
    model_listbox.current(0)
def open_models_window():
    def save_models():
        try:
            vvod_fabric = producer_listbox.get()  # Получаем выбранный производитель
            models = model_listbox.get(0, tk.END)  # Получаем все модели из listbox

            # Открываем файл для записи
            with open("data_marka.txt", "r+", encoding='utf-8') as f:
                lines = f.readlines()
                # Находим нужную строку по производителю
                for i, line in enumerate(lines):
                    if vvod_fabric in line:
                        # Заменяем модели в найденной строке
                        lines[i] = f"{vvod_fabric}/{'/'.join(models)}\n"
                        break
                else:
                    # Если строка не найдена, добавляем ее в конец файла
                    lines.append(f"{vvod_fabric}/{'/'.join(models)}\n")

                # Записываем обновленные данные в файл
                f.seek(0)
                f.truncate(0)
                f.writelines(lines)

            models_window.destroy()
            messagebox.showinfo("Сохранение", "Модели успешно сохранены!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения: {e}")

    def add_model():
        new_model = model_entry.get().strip()
        if new_model:
            model_listbox.insert(tk.END, new_model)
            model_entry.delete(0, tk.END)

    def delete_model():
        selected_index = model_listbox.curselection()
        if selected_index:
            model_listbox.delete(selected_index[0])

    models_window = tk.Toplevel(root)
    models_window.title("Модели")

    # Центрирование окна
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = models_window.winfo_reqwidth()
    window_height = models_window.winfo_reqheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    models_window.geometry(f"+{x}+{y}")

    # Выпадающий список производителей
    producer_label = tk.Label(models_window, text="Производитель:")
    producer_label.grid(row=0, column=0, padx=5, pady=5)
    global producer_listbox
    producer_listbox = ttk.Combobox(models_window, values=get_producers(), state="readonly")
    producer_listbox.grid(row=1, column=0, padx=5, pady=5)
    producer_listbox.bind("<<ComboboxSelected>>", lambda event: update_model_listbox(producer_listbox.get(), model_listbox))

    # Список моделей
    model_label = tk.Label(models_window, text="Модели:")
    model_label.grid(row=0, column=1, padx=5, pady=5)
    global model_listbox
    model_listbox = tk.Listbox(models_window, width=25, height=15)
    model_listbox.grid(row=1, column=1, padx=5, pady=5)

    # Поле ввода модели
    model_entry_label = tk.Label(models_window, text="Введите модель:")
    model_entry_label.grid(row=2, column=0,columnspan=2, padx=5, pady=5)
    global model_entry
    model_entry = tk.Entry(models_window)
    model_entry.grid(row=3, column=0,columnspan=2, padx=5, pady=5)

    # Кнопка добавить модель
    add_model_button = tk.Button(models_window, text="Добавить модель", command=add_model)
    add_model_button.grid(row=4, column=0,ipadx=20, padx=5, pady=5)

    # Кнопка удалить модель
    delete_model_button = tk.Button(models_window, text="Удалить модель", command=delete_model)
    delete_model_button.grid(row=4, column=1,ipadx=20, pady=5)

    # Кнопка сохранить
    save_button = tk.Button(models_window, text="Сохранить", command=save_models)
    save_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    # Начальное обновление списка моделей
    update_model_listbox(producer_listbox.get(), model_listbox)

def open_colors_window():
    def save_colors():
        try:
            with open("data_color.txt", "w", encoding='utf-8') as f:
                for item in color_listbox.get(0, tk.END):
                    f.write(item + "\n")
            colors_window.destroy()
            messagebox.showinfo("Сохранение", "Цвета успешно сохранены!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения: {e}")

    def add_item(listbox, var):
        new_item = entry.get()
        if new_item:
            listbox.insert(tk.END, new_item)
            var.set('')
            entry.delete(0, tk.END)

    def delete_item(listbox):
        selected_index = listbox.curselection()
        if selected_index:
            listbox.delete(selected_index[0])

    colors_window = tk.Toplevel(root)
    colors_window.title("Цвета машин")

    # Центрирование окна
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = colors_window.winfo_reqwidth()
    window_height = colors_window.winfo_reqheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    colors_window.geometry(f"+{x}+{y}")

    # Список цветов
    color_label = tk.Label(colors_window, text="Цвет:")
    color_label.grid(row=0, column=0, columnspan=2)
    global color_listbox
    color_listbox = tk.Listbox(colors_window, width=40, height=15)
    color_listbox.grid(row=1, column=0, columnspan=2)
    load_listbox("data_color.txt", color_listbox)

    # Поле ввода
    entry = tk.Entry(colors_window)
    entry.grid(row=2, column=0, columnspan=2, pady=5)
    var = tk.StringVar()
    entry['textvariable'] = var

    # Кнопки
    add_color_button = tk.Button(colors_window, text="Добавить цвет", command=lambda: add_item(color_listbox, var))
    add_color_button.grid(row=3, column=0, padx=5, pady=5)
    delete_color_button = tk.Button(colors_window, text="Удалить цвет", command=lambda: delete_item(color_listbox))
    delete_color_button.grid(row=3, column=1, padx=5, pady=5)

    # Кнопка сохранения
    save_button = tk.Button(colors_window, text="Сохранить", command=save_colors)
    save_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

def update_model_listbox(producer, model_listbox):
    models = get_models_by_producer(producer)
    model_listbox.delete(0, tk.END)  # Очищаем существующие модели
    for model in models:
        model_listbox.insert(tk.END, model)

root = tk.Tk()
root.title("База данных машин")
root.geometry("1800x800")
main_frame = tk.Frame(root)
main_frame.pack(pady=20)

# Кнопки
add_button = tk.Button(main_frame, text="Добавить машину", command=add_car, width=15)
add_button.grid(row=0, column=0, padx=10)

delete_button = tk.Button(main_frame, text="Удалить машину", command=delete_car, state=tk.DISABLED, width=15)
delete_button.grid(row=0, column=1, padx=10)

edit_button = tk.Button(main_frame, text="Редактировать машину", command=change_car, state=tk.DISABLED, width=15)
edit_button.grid(row=0, column=2, padx=10)

find_button = tk.Button(main_frame, text="Найти машину", command=find_car, width=15)
find_button.grid(row=0, column=3, padx=10)

producers_button = tk.Button(main_frame, text="Производители", command=open_producers_window, width=20)
producers_button.grid(row=0, column=6, padx=10)

models_button = tk.Button(main_frame, text="Модели", command=open_models_window, width=15)
models_button.grid(row=0, column=7, padx=10)

colors_button = tk.Button(main_frame, text="Цвета", command=open_colors_window, width=15)
colors_button.grid(row=0, column=4, padx=10)

# Таблица
main_tree_frame = tk.Frame(root)
main_tree_frame.pack(fill="both", expand=True)  # Занимаем всё пространство в окне

# Создаем вертикальную полосу прокрутки
scrollbar = tk.Scrollbar(main_tree_frame, orient="vertical")
scrollbar.pack(side="right", fill="y")

global main_tree #отображение табл данных в граф инт
main_tree = ttk.Treeview(main_tree_frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
for i, col in enumerate(columns):
    main_tree.heading(col, text=col)
main_tree.pack(side="left", fill="both", expand=True)
main_tree.column(columns[0], width=30)
main_tree.column(columns[1], width=150)
main_tree.column(columns[2], width=150)
main_tree.column(columns[3], width=180)
main_tree.column(columns[4], width=150)
main_tree.column(columns[5], width=100)
for i, col in enumerate(columns):
    main_tree.heading(col, text=col,)
main_tree.pack(side="left", fill="both", expand=True)

# Связываем полосу прокрутки с Treeview
scrollbar.config(command=main_tree.yview)

# Обновление таблицы при запуске
update_main_table()

# Обработчик события выбора строки
main_tree.bind("<<TreeviewSelect>>", select_car)

# Обработчик события нажатия на кнопку мыши в таблице
main_tree.bind("<Button-1>", clear_selection)

root.mainloop()
