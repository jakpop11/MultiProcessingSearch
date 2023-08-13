import os.path


def read_file_to_list(filepath, is_int: bool = False, sep: str = None) -> list:
    """
    Wczytuje dane z pliku do listy
    :param filepath:
    :param is_int:
    :param sep:
    :return:
    """
    file = open(filepath, 'r', encoding="utf-8")
    tmp_list = file.read().split(sep=sep)
    file.close()

    if is_int:
        # Parsuje elemanty listy na int
        table = []
        for n in tmp_list:
            table.append(int(n))
        return table

    return tmp_list


def read_file_to_str(filepath) -> str:
    """
    Wczytuje dane z pliku do string
    :param filepath:
    :return:
    """
    if filepath == '':
        return ''

    file = open(filepath, 'r', encoding="utf-8")
    tmp_str = file.read()
    file.close()

    return tmp_str


def write_to_file_from_list(filepath, data: list):
    """
    Zapisuje dane do pliku
    :param filepath:
    :param data:
    :return:
    """
    with open(filepath, 'w') as file:
        for element in data:
            file.write(f"{element}\n")


def append_file_with_str(filepath, data: str):
    """
    Dopisuje dane do pliku
    :param filepath:
    :param data:
    :return:
    """
    with open(filepath, 'a') as file:
        file.write(data)


def is_file(filepath) -> bool:
    """
    Zwraca czy pod dana sciezka istnieje juz plik
    :param filepath:
    :return:
    """
    return os.path.isfile(filepath)
