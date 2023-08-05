import os
import tkinter as tk
from tkinter import filedialog

import file_service
from search import Search


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
