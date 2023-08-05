import tkinter as tk

from model import Model
from view import View
from controller import Controller


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
