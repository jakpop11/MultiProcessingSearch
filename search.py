import time
import multiprocessing


class Search:
    def __init__(self, text: str, pattern: str):
        self.text = text
        self.pattern = pattern

        self.tlen = len(text)
        self.plen = len(pattern)

        self.pattern_indexes = []

        # lista znakow wystepujacych we wzorcu
        # TODO: Convert to set {} ?
        self.p_chars = []

        for ch in insert_sort(list(pattern)):
            # czy znaku nie ma na liscie
            if binary_search(self.p_chars, ch) == -1:
                self.p_chars.append(ch)

        # # slownik czasow wzgledem liczby procesorow
        # self.times = {}

    def get_results(self) -> list:
        """
        Zwraca liste indeksow
        :return:
        """
        tmp = list(self.pattern_indexes)
        # sortownie ?
        # if len(tmp) != 0:
        #     return insert_sort(tmp)
        # else:
        #     return []
        return tmp

    def _search_loop(self, lo: int, hi: int):
        i = self.plen - 1 + lo
        j = self.plen - 1

        while i < hi + self.plen - 1 and i < self.tlen:

            if self.text[i] == self.pattern[j]:
                if j == 0:
                    # wzorzec znaleziony
                    self.pattern_indexes.append(i)
                    # print(f"Process: {p}, index:[{i}]")

                    # przesuniecie wskaznikow do kolejnej pozycji
                    i += self.plen
                    j = self.plen - 1
                    continue

                # "przesuniecie" sprawdzenia znakow o 1 w lewo
                i -= 1
                j -= 1

            else:
                # czy znak znajduje sie we wzorze
                if binary_search(self.p_chars, self.text[i]) != -1:
                    # "przesuniecie" wzorca o 1 w prawo
                    i += 1 + self.plen - j - 1
                    j = self.plen - 1
                else:
                    # "przesuniecie" o dlugosc wzorca w prawo
                    i += self.plen
                    j = self.plen - 1

    def multiprocess_search(self, total_processes_number: int) -> (int, float):
        manager = multiprocessing.Manager()

        # lista indeksow rozpoczynajacych wzorzec
        self.pattern_indexes = manager.list()
        print(f"\nmax proc: {total_processes_number}")

        r = self.tlen % total_processes_number
        shift = self.tlen // total_processes_number

        lo = 0
        hi = 0

        # tworzenie procesow
        processes = []
        for p in range(total_processes_number):
            if p < r:
                lo = hi
                hi = lo + shift + 1
            else:
                lo = hi
                hi = lo + shift

            # print(f"lo: {lo}, hi:{hi}")
            process = multiprocessing.Process(target=self._search_loop, args=(lo, hi))
            processes.append(process)

        # rozpoczecie pomiaru czasu
        start_time = time.perf_counter()

        # uruchomienie procesow rownolegle
        for p in processes:
            p.start()
        # zakonczenie pracy rownoleglej
        for p in processes:
            p.join()

        # zakonczenie pomiaru czasu
        finish_time = time.perf_counter()
        return total_processes_number, (finish_time - start_time)


def binary_search(data: list, find_ch: str) -> int:
    """
    Zwraca indeks szukanego znaku z listy
    lub '-1' jesli takiego nie znaleziono
    :param data:
    :param find_ch:
    :return:
    """

    # indeksy poczatku i konca rozpatrywanej czesci tablicy
    lo = 0
    hi = len(data) - 1
    # liczba wykonanych iteracji
    i = 0

    while lo <= hi:
        # Wyznacza indeks srodka listy
        mid = int(lo + ((hi - lo) / 2))
        i = i + 1

        if data[mid] < find_ch:
            lo = mid + 1
        elif find_ch < data[mid]:
            hi = mid - 1
        else:
            return mid

    # nie znaleziono znaku
    return -1


def insert_sort(data: list) -> list:
    """
    Zwraca posortowana liste
    :param data:
    :return:
    """

    result = data.copy()

    # Sortowanie
    for j in range(1, len(result)):
        i = j
        while i > 0 and result[i - 1] > result[i]:
            # zamiana wartosci
            tmp = result[i]
            result[i] = result[i - 1]
            result[i - 1] = tmp

            # iteracja w tyl
            i = i - 1
    return result
