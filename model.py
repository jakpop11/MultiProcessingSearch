import file_service


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
