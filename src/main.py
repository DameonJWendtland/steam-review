# main.py
import tkinter as tk
from gui.app import SteamReviewGeneratorApp


def main():
    root = tk.Tk()
    root.title("Steam Review Generator")
    root.geometry("800x600")
    root.resizable(True, True)
    root.iconbitmap("../icons/checkliste.ico")

    app = SteamReviewGeneratorApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
