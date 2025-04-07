import os
import tkinter as tk
from tkinter import ttk
import webbrowser

def open_options_dialog(root, categories, visible_categories, design_settings, update_callback):
    options_dialog = tk.Toplevel(root)
    options_dialog.title("Options")
    options_dialog.geometry("400x500")
    options_dialog.iconbitmap("C:/Users/micro/PycharmProjects/steam-review/src/icons/optionen.ico")

    button_frame = ttk.Frame(options_dialog)
    button_frame.pack(side="top", fill="x", pady=5)
    content_frame = ttk.Frame(options_dialog)
    content_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)
    def load_categories():
        for widget in content_frame.winfo_children():
            widget.destroy()
        top_frame = ttk.Frame(content_frame)
        top_frame.pack(side="top", fill="both", expand=True)
        canvas = tk.Canvas(top_frame)
        scrollbar = ttk.Scrollbar(top_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        scrollable_frame.bind("<Configure>", on_frame_configure)
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind("<Enter>", lambda event: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda event: canvas.unbind_all("<MouseWheel>"))
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        local_visibility = {cat: tk.BooleanVar(value=visible_categories[cat].get()) for cat in categories}
        def unselect_all():
            for var in local_visibility.values():
                var.set(False)
        unselect_all_btn = ttk.Button(scrollable_frame, text="Unselect All", command=unselect_all)
        unselect_all_btn.pack(padx=10, pady=10, anchor="w")
        for cat in categories:
            cb = ttk.Checkbutton(scrollable_frame, text=cat, variable=local_visibility[cat])
            cb.pack(anchor="w", padx=10, pady=3)
        bottom_frame = ttk.Frame(content_frame)
        bottom_frame.pack(side="bottom", fill="x", pady=5)
        def save_options():
            for cat in categories:
                visible_categories[cat].set(local_visibility[cat].get())
            update_callback()
            options_dialog.destroy()
        def reset_options():
            for cat in categories:
                local_visibility[cat].set(True)
        save_button = ttk.Button(bottom_frame, text="Save", command=save_options)
        reset_button = ttk.Button(bottom_frame, text="Reset", command=reset_options)
        save_button.pack(side="left", expand=True, fill="x", padx=(0, 5))
        reset_button.pack(side="right", expand=True, fill="x", padx=(5, 0))
    def load_design_settings():
        for widget in content_frame.winfo_children():
            widget.destroy()
        settings_frame = ttk.Frame(content_frame)
        settings_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        review_heading_var = tk.IntVar(value=design_settings.get("review_heading", 1))
        category_heading_var = tk.IntVar(value=design_settings.get("category_heading", 3))
        review_label = ttk.Label(settings_frame, text="Review Heading Size:")
        review_label.grid(row=0, column=0, sticky="w", pady=5, padx=5)
        review_spin = ttk.Spinbox(settings_frame, from_=1, to=6, textvariable=review_heading_var, width=5)
        review_spin.grid(row=0, column=1, sticky="w", pady=5, padx=5)
        category_label = ttk.Label(settings_frame, text="Category Heading Size:")
        category_label.grid(row=1, column=0, sticky="w", pady=5, padx=5)
        category_spin = ttk.Spinbox(settings_frame, from_=1, to=6, textvariable=category_heading_var, width=5)
        category_spin.grid(row=1, column=1, sticky="w", pady=5, padx=5)
        bottom_frame = ttk.Frame(content_frame)
        bottom_frame.pack(side="bottom", fill="x", pady=5)
        def save_design_settings():
            design_settings["review_heading"] = review_heading_var.get()
            design_settings["category_heading"] = category_heading_var.get()
            update_callback()
            options_dialog.destroy()
        def reset_design_settings():
            review_heading_var.set(1)
            category_heading_var.set(3)
        save_button = ttk.Button(bottom_frame, text="Save", command=save_design_settings)
        reset_button = ttk.Button(bottom_frame, text="Reset", command=reset_design_settings)
        save_button.pack(side="left", expand=True, fill="x", padx=(0, 5))
        reset_button.pack(side="right", expand=True, fill="x", padx=(5, 0))
    def open_help():
        url = "https://github.com/DameonJWendtland/steam-review/issues"
        webbrowser.open(url)
    btn_categories = ttk.Button(button_frame, text="Categories", command=load_categories)
    btn_design = ttk.Button(button_frame, text="Design settings", command=load_design_settings)
    btn_help = ttk.Button(button_frame, text="Help 🔗", command=open_help)
    btn_categories.pack(side="left", expand=True, fill="x", padx=5)
    btn_design.pack(side="left", expand=True, fill="x", padx=5)
    btn_help.pack(side="left", expand=True, fill="x", padx=5)
    load_categories()
