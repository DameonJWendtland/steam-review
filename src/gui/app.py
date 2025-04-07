# gui/app.py
import tkinter as tk
from tkinter import ttk, messagebox
from src.categories import categories
from src.gui.tabs import CategoryTabs
from src.gui.review_generator import generate_review_text
from src.gui.file_manager import save_review, copy_review
from src.gui.options_dialog import open_options_dialog
from src.gui.rating_calculator import calculate_recommended_rating


class SteamReviewGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.categories = categories
        self.visible_categories = {cat: tk.BooleanVar(value=True) for cat in self.categories}
        self.design_settings = {"review_heading": 1, "category_heading": 3}

        self.notebook = ttk.Notebook(root)
        self.notebook.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.tabs = CategoryTabs(self.notebook, self.categories, self.visible_categories)

        self.create_rating_frame()
        self.create_output_frame()
        self.create_button_frame()

        root.columnconfigure(0, weight=1)
        root.rowconfigure(2, weight=1)

    def create_rating_frame(self):
        self.rating_frame = ttk.LabelFrame(self.root, text="Rating")
        self.rating_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.rating_var = tk.IntVar(value=5)
        self.rating_scale = tk.Scale(self.rating_frame, from_=1, to=10, orient="horizontal", variable=self.rating_var)
        self.rating_scale.pack(padx=10, pady=5, fill="x")

    def create_output_frame(self):
        self.output_frame = ttk.Frame(self.root)
        self.output_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.output_text = tk.Text(self.output_frame, wrap="word")
        self.output_text.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(self.output_frame, orient="vertical", command=self.output_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.output_text.config(yscrollcommand=scrollbar.set)
        self.output_frame.columnconfigure(0, weight=1)
        self.output_frame.rowconfigure(0, weight=1)

    def create_button_frame(self):
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.button_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)

        ttk.Button(self.button_frame, text="Generate Review", command=self.generate_review).grid(row=0, column=0,
                                                                                                 padx=5, pady=5,
                                                                                                 sticky="ew")
        ttk.Button(self.button_frame, text="Save as TXT", command=self.save_as_txt).grid(row=0, column=1, padx=5,
                                                                                         pady=5, sticky="ew")
        ttk.Button(self.button_frame, text="Copy Review", command=self.copy_review).grid(row=0, column=2, padx=5,
                                                                                         pady=5, sticky="ew")
        ttk.Button(self.button_frame, text="Options", command=self.open_options).grid(row=0, column=3, padx=5, pady=5,
                                                                                      sticky="ew")
        ttk.Button(self.button_frame, text="Recommend Rating", command=self.show_recommended_rating).grid(row=0,
                                                                                                          column=4,
                                                                                                          padx=5,
                                                                                                          pady=5,
                                                                                                          sticky="ew")

    def generate_review(self):
        review_text = generate_review_text(
            rating=self.rating_var.get(),
            categories=self.categories,
            visible_categories=self.visible_categories,
            selected_options=self.tabs.selected_options,
            audience_vars=self.tabs.audience_vars,
            design_settings=self.design_settings
        )
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, review_text)

    def save_as_txt(self):
        review_text = self.output_text.get("1.0", tk.END).strip()
        save_review(self.root, review_text)

    def copy_review(self):
        review_text = self.output_text.get("1.0", tk.END).strip()
        copy_review(self.root, review_text)

    def open_options(self):
        open_options_dialog(self.root, self.categories, self.visible_categories, self.design_settings, self.update_tabs)

    def update_tabs(self):
        self.tabs.update_category_visibility()

    def show_recommended_rating(self):
        recommended = calculate_recommended_rating(
            self.categories,
            self.visible_categories,
            self.tabs.selected_options,
            self.tabs.audience_vars
        )

        dialog = tk.Toplevel(self.root)
        dialog.title("Recommended Rating")
        dialog.geometry("300x150")

        label = ttk.Label(dialog, text=f"Recommended rating:\n{recommended} / 10", font=("Arial", 14))
        label.pack(pady=20)

        button_frame = ttk.Frame(dialog)
        button_frame.pack(side="bottom", fill="x", pady=10, padx=10)

        def on_cancel():
            dialog.destroy()

        def on_apply():
            self.rating_var.set(recommended)
            dialog.destroy()

        cancel_button = ttk.Button(button_frame, text="Cancel", command=on_cancel)
        apply_button = ttk.Button(button_frame, text="Apply", command=on_apply)

        cancel_button.pack(side="left", expand=True, fill="x", padx=(0, 5))
        apply_button.pack(side="right", expand=True, fill="x", padx=(5, 0))
