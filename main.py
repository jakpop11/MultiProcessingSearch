import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
import os

import file_service
from search import Search


class Model:
    """
    Obsluguje przplyw danych
    oraz dzialanie algorytmow
    """
    def __init__(self):
        self.filepath = "Krzyzacy_full.txt"
        self.text = ""
        self.search = None
        self.line_indexes = []

    def generate_file(self, chars_quantity: int):
        """
        Generuje plik zawierajacy podana liczbe znakow
        :param chars_quantity: min. 1_000
        :return:
        """
        filepath = f"{chars_quantity:_}_chars.txt"
        data = ""

        # pomija istniejacy plik
        if file_service.is_file(filepath):
            return

        print("Generating long file")
        print(f"{chars_quantity:_}")

        # line with 1000 chars
        for i in range(499):
            data = data + f"{i % 10}a"
        data = data + 'g\n'

        # x lines
        for i in range(chars_quantity // 1000):
            print(i)
            file_service.append_file_with_str(filepath, data)

        print("Finished")


class View(ttk.Frame):
    """
    Definiuje i obsluguje interfejs aplikacji
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=1, padx=5, pady=2)

        # setup widgets
        self.__create_widgets()

        # setup controller
        self.controller = None

    def set_controller(self, controller):
        """
        Przypisuje kontroler do widoku
        :param controller:
        :return:
        """
        self.controller = controller

    def __create_widgets(self):

        # Menu Bar
        menu_f = ttk.Frame(self)
        menu_f.pack(fill="x")

        self.open_file_btn = ttk.Button(menu_f, text="Open File", command=self.__open_btn_command)
        self.open_file_btn.pack(side="left")
        self.generate_files_btn = ttk.Button(menu_f, text="Generate Files", command=self.__generate_btn_command)
        self.generate_files_btn.pack(side="left")

        # TEST convert string index to tkinter text index
        self.convert_btn = ttk.Button(menu_f, text="Convert indexes", command=self.__convert_btn_command)
        self.convert_btn.pack(side="left")

        # Search
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x")

        self.entry = ttk.Entry(search_frame)
        self.entry.pack(side="left", fill="x", expand=True)
        self.search_btn = ttk.Button(search_frame, text="Search", command=self.__search_btn_command)
        self.search_btn.pack()

        # Content
        content_frame = ttk.Frame(self)
        content_frame.pack(fill="both", expand=True, pady=4)

        # Text
        self.text_box = scrolledtext.ScrolledText(content_frame, wrap="word")
        self.text_box.pack(fill="both", expand=True, pady=2)
        self.text_box.config(state="disabled")

        # Output panel
        output_lable = ttk.Label(content_frame, text="Output:")
        output_lable.pack(fill="x")

        self.output = scrolledtext.ScrolledText(content_frame, wrap="word", padx=2, height=16, borderwidth=2, background="#e0e0e0")
        self.output.pack(fill="x")
        self.output.config(state="disabled")

    def __load_text(self):
        self.controller.load_text()

    def __open_btn_command(self):
        self.controller.open_file()

    def __generate_btn_command(self):
        self.controller.generate_files()

    def __search_btn_command(self):
        self.controller.search()

    def __convert_btn_command(self):
        self.controller.convert_indexes()


class Controller:
    """
    Kontroluje komunikacje pomiedzy widokiem a dzialaniem aplikacji
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # setup view
        self.load_text()

    def open_file(self):
        try:
            filepath = filedialog.askopenfilename()
        except Exception:
            print("Error during opening file")
            filepath = "PanTadeusz.txt"

        # if not canceled
        if filepath != "":
            self.model.filepath = filepath
            self.load_text()

    def generate_files(self):
        for quantity in [100_000, 10_000_000, 1_000_000_000]:
            self.model.generate_file(quantity)

    def load_text(self):
        text = file_service.read_file_to_str(self.model.filepath)
        self.model.text = text
        self.view.text_box.configure(state=tk.NORMAL)
        # clear text_box
        self.view.text_box.delete(1.0, "end")
        self.view.text_box.insert("insert", text)
        self.view.text_box.configure(state="disable")

        # calculate new line indexes
        self.model.line_indexes.clear()
        for i, ch in enumerate(self.model.text):
            if ch == '\n':
                self.model.line_indexes.append(i)

        # set text tag
        self.view.text_box.tag_configure("pattern", background="yellow")

    def load_output(self, info):
        self.view.output.configure(state=tk.NORMAL)
        # clear text_box
        self.view.output.delete(1.0, "end")
        self.view.output.insert("insert", info)
        self.view.output.configure(state="disable")

    def convert_indexes(self):
        self.load_output(f"New line char on index:\n{str(self.model.line_indexes)}")

        for index in self.model.search.get_results():
            text_index, end_index = self._convert_index(index, self.model.search.plen)

            # highlight text
            self.view.text_box.tag_add("pattern", text_index, end_index)

    def _convert_index(self, index, length) -> (str, str):
        line_indexes = self.model.line_indexes

        for i in range(len(line_indexes)):
            l_index = line_indexes[i]

            if index < l_index:
                result = f"{i+1}.{index - line_indexes[i-1]-1}"
                end = f"{i+1}.{index - line_indexes[i-1]-1 + length}"
                # print(f"{index} < [{i}]{l_index} -> {result}")
                # print(f"{index+length} < [{i}]{l_index} -> {end}")
                return (result, end)

    def search(self):
        pattern = self.view.entry.get()
        if pattern == "":
            return

        self.view.search_btn.configure(state="disable")
        # algorytm szukajacy
        self.model.search = Search(self.model.text, pattern)
        self.model.search.multiprocess_search((os.cpu_count() + 1)//2)

        # self.model.search.multiprocess_test()
        times = self.model.search.get_times()
        print("Times:")
        print(times)

        self.model.search.generate_plots()

        # zapis danych do pliku
        tmp = f"\nWyniki dla {self.model.search.tlen:_} znakow:\n\n"
        for p, time in times.items():
            tmp += f"{p}: {time}\n"
        file_service.append_file_with_str("Logs.txt", tmp)

        # wyswietlenie indeksow w oknie output
        self.load_output(f"Wrzorzec znaleziony na pozycji:\n{str(self.model.search.get_results())}")

        self.view.search_btn.configure(state="normal")


class App(tk.Tk):
    """
    Definiuje bazowe okno z modulu tkinter
    oraz laczy elementy wzorca MVC
    """

    def __init__(self):
        super().__init__()

        self.title("Multiprocessing Search")
        self.geometry("800x540")

        # Model
        model = Model()

        # View
        view = View(self)

        # Controller
        controller = Controller(model, view)
        view.set_controller(controller)


if __name__ == "__main__":
    app = App()
    app.mainloop()
