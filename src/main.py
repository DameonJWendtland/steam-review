import tkinter as tk
from gui.app import SteamReviewGeneratorApp


def main():
    root = tk.Tk()
    root.iconbitmap("C:/Users/micro/PycharmProjects/steam-review/src/icons/checkliste.ico")
    root.title("Steam Review Generator")
    root.geometry("800x600")
    root.resizable(True, True)
    app = SteamReviewGeneratorApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
