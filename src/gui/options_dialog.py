# gui/options_dialog.py
import tkinter as tk
from tkinter import ttk


def open_options_dialog(root, categories, visible_categories, update_callback):
    options_dialog = tk.Toplevel(root)
    options_dialog.title("Category Options")
    options_dialog.geometry("300x450")

    top_frame = ttk.Frame(options_dialog)
    top_frame.pack(side="top", fill="both", expand=True)

    canvas = tk.Canvas(top_frame)
    scrollbar = ttk.Scrollbar(top_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_frame_configure)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    canvas.yview_moveto(0)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    local_visibility = {cat: tk.BooleanVar(value=visible_categories[cat].get()) for cat in categories}

    def unselect_all():
        for var in local_visibility.values():
            var.set(False)

    unselect_all_btn = ttk.Button(scrollable_frame, text="Unselect All", command=unselect_all)
    unselect_all_btn.pack(padx=10, pady=10, anchor="w")

    for cat in categories:
        cb = ttk.Checkbutton(scrollable_frame, text=cat, variable=local_visibility[cat])
        cb.pack(anchor="w", padx=10, pady=3)

    button_frame = ttk.Frame(options_dialog)
    button_frame.pack(side="bottom", fill="x", pady=5, padx=10)

    def save_options():
        for cat in categories:
            visible_categories[cat].set(local_visibility[cat].get())
        update_callback()
        options_dialog.destroy()

    def reset_options():
        for cat in categories:
            local_visibility[cat].set(True)

    save_button = ttk.Button(button_frame, text="Save", command=save_options)
    reset_button = ttk.Button(button_frame, text="Reset", command=reset_options)
    save_button.pack(side="left", expand=True, fill="x", padx=(0, 5))
    reset_button.pack(side="right", expand=True, fill="x", padx=(5, 0))
