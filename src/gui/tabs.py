import tkinter as tk
from tkinter import ttk

class CategoryTabs:
    def __init__(self, notebook, categories, visible_categories):
        self.notebook = notebook
        self.categories = categories
        self.visible_categories = visible_categories
        self.frames = {}
        self.selected_options = {}
        self.audience_vars = {}
        self.audience_widgets = {}
        self.create_tabs()
    def create_tabs(self):
        for cat, options in self.categories.items():
            self.create_category_tab(cat, options)
            if self.visible_categories[cat].get():
                self.notebook.add(self.frames[cat], text=cat)
    def create_category_tab(self, cat, options):
        frame = ttk.Frame(self.notebook)
        self.frames[cat] = frame
        if cat == "Audience":
            self.audience_vars = {option: tk.BooleanVar(value=False) for option in options}
            self.audience_widgets = {}
            for i, option in enumerate(options):
                cb = ttk.Checkbutton(frame, text=option, variable=self.audience_vars[option], command=self.update_audience_checkbuttons)
                cb.grid(row=i, column=0, sticky="w", padx=10, pady=2)
                self.audience_widgets[option] = cb
        else:
            var = tk.StringVar(value="")
            self.selected_options[cat] = var
            for i, option in enumerate(options):
                rb = ttk.Radiobutton(frame, text=option, variable=var, value=option)
                rb.grid(row=i, column=0, sticky="w", padx=10, pady=2)
    def update_audience_checkbuttons(self):
        everyone_selected = self.audience_vars["Everyone"].get()
        for option, widget in self.audience_widgets.items():
            if option != "Everyone":
                widget.config(state="disabled" if everyone_selected else "normal")
                if everyone_selected:
                    self.audience_vars[option].set(False)
        if not everyone_selected:
            for option in self.categories["Audience"]:
                if option != "Everyone" and self.audience_vars[option].get():
                    self.audience_widgets["Everyone"].config(state="disabled")
                    break
            else:
                self.audience_widgets["Everyone"].config(state="normal")
    def update_category_visibility(self):
        current_tabs = self.notebook.tabs()
        for cat, frame in self.frames.items():
            if self.visible_categories[cat].get() and str(frame) not in current_tabs:
                self.notebook.add(frame, text=cat)
            elif not self.visible_categories[cat].get() and str(frame) in current_tabs:
                self.notebook.forget(frame)
