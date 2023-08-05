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
