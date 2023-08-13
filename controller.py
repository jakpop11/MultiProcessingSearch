import os
from tkinter import filedialog

import file_service
from search import Search
from benchmark import Benchmark


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
        self.view.load_text(self.model.text)

    def load_output(self, info):
        self.view.load_output(info)

    def search(self):
        pattern = self.view.get_search_entry()
        if pattern == "":
            return

        self.view.on_search_start()
        # algorytm szukajacy
        self.model.search = Search(self.model.text, pattern)
        self.model.search.multiprocess_search((os.cpu_count() + 1)//2)

        # wyswietlenie indeksow w oknie output
        self.load_output(f"Wrzorzec znaleziony na pozycji:\n{str(self.model.search.get_results())}")

        self.view.on_search_finished(self.model.search.get_results(), self.model.search.plen)

    def benchmark_search(self):
        pattern = self.view.get_search_entry()
        if pattern == "":
            return

        self.view.on_search_start()
        # algorytm szukajacy
        self.model.search = Search(self.model.text, pattern)
        benchmark = Benchmark(self.model.search)
        benchmark.run()

        # zapis danych do pliku
        tmp = f"\nWyniki dla {self.model.search.tlen:_} znakow:\n\n"
        for p, time in benchmark.times.items():
            tmp += f"{p}: {time}\n"
        file_service.append_file_with_str("Logs.txt", tmp)

        # wyswietlenie indeksow w oknie output
        self.load_output(f"Wrzorzec znaleziony na pozycji:\n{str(self.model.search.get_results())}")

        self.view.on_search_finished(self.model.search.get_results(), self.model.search.plen)
