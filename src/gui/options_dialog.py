import tkinter as tk
from tkinter import ttk
import webbrowser


def open_options_dialog(root, categories, visible_categories, use_in_calc, design_settings, update_callback):
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

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<Enter>", lambda event: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda event: canvas.unbind_all("<MouseWheel>"))

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scrollable_frame.bind("<Configure>", on_frame_configure)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        local_visibility = {cat: tk.BooleanVar(value=visible_categories[cat].get()) for cat in categories}
        local_calc = {cat: tk.BooleanVar(value=use_in_calc[cat].get()) for cat in categories}
        local_calc_widget = {}

        unselect_all_btn = ttk.Button(scrollable_frame, text="Unselect All", command=lambda: unselect_all())
        unselect_all_btn.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        header_cat = ttk.Label(scrollable_frame, text="Category")
        header_calc = ttk.Label(scrollable_frame, text="Use in calculation")
        header_cat.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        header_calc.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        def on_visibility_change(cat, calc_cb):
            if not local_visibility[cat].get():
                local_calc[cat].set(False)
                calc_cb.config(state="disabled")
            else:
                calc_cb.config(state="normal")

        def unselect_all():
            for cat in categories:
                local_visibility[cat].set(False)
                local_calc[cat].set(False)

        row_index = 2
        for cat in categories:
            vis_cb = ttk.Checkbutton(scrollable_frame, text=cat, variable=local_visibility[cat])
            vis_cb.grid(row=row_index, column=0, padx=10, pady=3, sticky="w")
            calc_cb = ttk.Checkbutton(scrollable_frame, variable=local_calc[cat])
            calc_cb.grid(row=row_index, column=1, padx=10, pady=3, sticky="w")
            if not local_visibility[cat].get():
                calc_cb.config(state="disabled")
            local_visibility[cat].trace_add("write",
                                            lambda *args, cat=cat, calc_cb=calc_cb: on_visibility_change(cat, calc_cb))
            local_calc_widget[cat] = calc_cb
            row_index += 1

        bottom_frame = ttk.Frame(content_frame)
        bottom_frame.pack(side="bottom", fill="x", pady=5)

        def save_options():
            for cat in categories:
                visible_categories[cat].set(local_visibility[cat].get())
                use_in_calc[cat].set(local_calc[cat].get())
            update_callback()
            options_dialog.destroy()

        def reset_options():
            for cat in categories:
                local_visibility[cat].set(True)
                local_calc[cat].set(True)

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
        credits_var = tk.BooleanVar(value=design_settings.get("credits", False))
        review_label = ttk.Label(settings_frame, text="Review Heading Size:")
        review_label.grid(row=0, column=0, sticky="w", pady=5, padx=5)
        review_spin = ttk.Spinbox(settings_frame, from_=1, to=6, textvariable=review_heading_var, width=5)
        review_spin.grid(row=0, column=1, sticky="w", pady=5, padx=5)
        category_label = ttk.Label(settings_frame, text="Category Heading Size:")
        category_label.grid(row=1, column=0, sticky="w", pady=5, padx=5)
        category_spin = ttk.Spinbox(settings_frame, from_=1, to=6, textvariable=category_heading_var, width=5)
        category_spin.grid(row=1, column=1, sticky="w", pady=5, padx=5)
        credits_check = ttk.Checkbutton(settings_frame, text="Include Credits ( would be awesome! <3 )",
                                        variable=credits_var)
        credits_check.grid(row=2, column=0, columnspan=2, sticky="w", pady=5, padx=5)
        bottom_frame = ttk.Frame(content_frame)
        bottom_frame.pack(side="bottom", fill="x", pady=5)

        def save_design_settings():
            design_settings["review_heading"] = review_heading_var.get()
            design_settings["category_heading"] = category_heading_var.get()
            design_settings["credits"] = credits_var.get()
            update_callback()
            options_dialog.destroy()

        def reset_design_settings():
            review_heading_var.set(1)
            category_heading_var.set(3)
            credits_var.set(False)

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
