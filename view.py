import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext


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

        self.__line_indexes = []

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
        # Later change to benchmark multiprocessing
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

    def load_text(self, text: str):
        self.text_box.configure(state=tk.NORMAL)
        # clear text_box
        self.text_box.delete(1.0, "end")
        self.text_box.insert("insert", text)
        self.text_box.configure(state="disabled")

        # calculate new line indexes
        self.__line_indexes.clear()
        for i, ch in enumerate(text):
            if ch == '\n':
                self.__line_indexes.append(i)

    def load_output(self, text: str):
        self.output.configure(state=tk.NORMAL)
        # clear text_box
        self.output.delete(1.0, "end")
        self.output.insert("insert", text)
        self.output.configure(state="disabled")

    def get_search_entry(self) -> str:
        return self.entry.get()

    def on_search_start(self):
        self.search_btn.configure(state="disable")

    def on_search_finished(self, indexes: list, pattern_length: int):
        self.search_btn.configure(state="normal")
        self._highlight_patterns(indexes, pattern_length)

    def _highlight_patterns(self, indexes: list, pattern_length: int):
        self.text_box.tag_delete("pattern")

        # set text tag
        self.text_box.tag_configure("pattern", background="yellow")

        for index in indexes:
            text_index, end_index = self.__convert_index(index, pattern_length)

            # highlight text
            self.text_box.tag_add("pattern", text_index, end_index)

    def __convert_index(self, index: int, length: int) -> (str, str):
        # TODO: decrease time complexity by starting for loop from previous line index
        for i, l_index in enumerate(self.__line_indexes):
            # continue until in line with pattern
            if index >= l_index:
                continue

            relative_index = index - self.__line_indexes[i-1] - 1
            start = f"{i+1}.{relative_index}"
            end = f"{i+1}.{relative_index + length}"

            return start, end

    def __open_btn_command(self):
        self.controller.open_file()

    def __generate_btn_command(self):
        self.controller.generate_files()

    def __search_btn_command(self):
        self.controller.search()

    def __convert_btn_command(self):
        self.controller.convert_indexes()
