# gui/options_dialog.py
import tkinter as tk
from tkinter import ttk
import webbrowser


def open_options_dialog(root, categories, visible_categories, design_settings, update_callback):
    """
    Opens the options dialog with three buttons:
      - Categories: Opens the category selection view.
      - Design settings: Allows the user to select heading sizes for review and categories.
      - Help: Opens the GitHub issues URL.
    After saving changes, update_callback() is called to update the GUI.
    """
    options_dialog = tk.Toplevel(root)
    options_dialog.title("Options")
    options_dialog.geometry("400x500")

    # Top frame for the three buttons
    button_frame = ttk.Frame(options_dialog)
    button_frame.pack(side="top", fill="x", pady=5)

    # Content frame for displaying different settings views
    content_frame = ttk.Frame(options_dialog)
    content_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    def load_categories():
        # Clear current content in the content_frame
        for widget in content_frame.winfo_children():
            widget.destroy()

        # Create a scrollable frame for category selection
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

        # Bind mousewheel events to enable scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<Enter>", lambda event: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda event: canvas.unbind_all("<MouseWheel>"))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Create local visibility variables for each category
        local_visibility = {cat: tk.BooleanVar(value=visible_categories[cat].get()) for cat in categories}

        def unselect_all():
            for var in local_visibility.values():
                var.set(False)

        unselect_all_btn = ttk.Button(scrollable_frame, text="Unselect All", command=unselect_all)
        unselect_all_btn.pack(padx=10, pady=10, anchor="w")

        # Create checkboxes for each category
        for cat in categories:
            cb = ttk.Checkbutton(scrollable_frame, text=cat, variable=local_visibility[cat])
            cb.pack(anchor="w", padx=10, pady=3)

        # Bottom frame for Save and Reset buttons
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
        # Clear current content in the content_frame
        for widget in content_frame.winfo_children():
            widget.destroy()

        # Create a frame for design settings
        settings_frame = ttk.Frame(content_frame)
        settings_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # Variables for design settings (heading sizes)
        review_heading_var = tk.IntVar(value=design_settings.get("review_heading", 1))
        category_heading_var = tk.IntVar(value=design_settings.get("category_heading", 3))

        # Label and Spinbox for Review Heading Size
        review_label = ttk.Label(settings_frame, text="Review Heading Size:")
        review_label.grid(row=0, column=0, sticky="w", pady=5, padx=5)
        review_spin = ttk.Spinbox(settings_frame, from_=1, to=6, textvariable=review_heading_var, width=5)
        review_spin.grid(row=0, column=1, sticky="w", pady=5, padx=5)

        # Label and Spinbox for Category Heading Size
        category_label = ttk.Label(settings_frame, text="Category Heading Size:")
        category_label.grid(row=1, column=0, sticky="w", pady=5, padx=5)
        category_spin = ttk.Spinbox(settings_frame, from_=1, to=6, textvariable=category_heading_var, width=5)
        category_spin.grid(row=1, column=1, sticky="w", pady=5, padx=5)

        # Bottom frame for Save and Reset buttons
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
        # Open the GitHub issues URL in the default web browser
        url = "https://github.com/DameonJWendtland/steam-review/issues"
        webbrowser.open(url)

    # Top buttons for switching between views
    btn_categories = ttk.Button(button_frame, text="Categories", command=load_categories)
    btn_design = ttk.Button(button_frame, text="Design settings", command=load_design_settings)
    btn_help = ttk.Button(button_frame, text="Help 🔗", command=open_help)

    btn_categories.pack(side="left", expand=True, fill="x", padx=5)
    btn_design.pack(side="left", expand=True, fill="x", padx=5)
    btn_help.pack(side="left", expand=True, fill="x", padx=5)

    # Load default view (Categories)
    load_categories()
