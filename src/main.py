import os
import tkinter as tk
from gui.app import SteamReviewGeneratorApp

def main():
    root = tk.Tk()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_dir, "icons", "checkliste.ico")
    root.iconbitmap(icon_path)
    root.title("Steam Review Generator")
    root.geometry("800x600")
    root.resizable(True, True)
    app = SteamReviewGeneratorApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
