import os
import matplotlib.pyplot as plt

from search import Search


class Benchmark:
    def __init__(self, search: Search):
        self.search = search

        # slownik czasow wzgledem liczby procesorow
        self.times = {}

    def run(self):
        self._start()
        self._generate_plots()

    def _generate_plots(self):
        fig = plt.figure(figsize=(10, 5))
        plt.bar(self.times.keys(), self.times.values(), color="orange", width=0.4)

        plt.xlabel("Liczba procesow")
        plt.ylabel("Czas [s]")
        plt.title(f"Porownanie czasow wykonywania algorytmu wzgledem ilosci procesow dla {self.search.tlen:_} znakow")
        # zapis wykresu do pliku
        plt.savefig(f"{self.search.tlen:_}_chars_plt.jpg")
        plt.show()

    def _start(self):
        """
        Kolejno uruchamia wyszukiwanie wykorzystujac rosnaca liczbe procesow
        :return:
        """
        for max_processes in range(1, os.cpu_count() + 1):
            _, score_time = self.search.multiprocess_search(max_processes)
            self.times[max_processes] = score_time
