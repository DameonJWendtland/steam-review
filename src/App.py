import tkinter as tk
from tkinter import ttk, filedialog, messagebox

categories = {
    "Graphics": [
        "You forget what reality is",
        "Beautiful",
        "Good",
        "Decent",
        "Bad",
        "Don’t look too long at it",
        "MS-DOS"
    ],
    "Gameplay": [
        "Very good",
        "Good",
        "It's just gameplay",
        "Mehh",
        "Watch paint dry instead",
        "Just don't"
    ],
    "Audio": [
        "Eargasm",
        "Very good",
        "Good",
        "Not too bad",
        "Bad",
        "I'm now deaf"
    ],
    "Audience": [
        "Everyone",
        "Kids",
        "Teens",
        "Adults",
        "Grandma"
    ],
    "PC Requirements": [
        "Check if you can run paint",
        "Potato",
        "Decent",
        "Fast",
        "Rich boi",
        "Ask NASA if they have a spare computer"
    ],
    "Game Size": [
        "Floppy Disk",
        "Old Fashioned",
        "Workable",
        "Big",
        "Will eat 15% of your 1TB hard drive",
        "You will want an entire hard drive to hold it",
        "You will need to invest in a black hole to hold all the data"
    ],
    "Difficulty": [
        "Just press 'W'",
        "Easy",
        "Easy to learn / Hard to master",
        "Significant brain usage",
        "Difficult",
        "Dark Souls"
    ],
    "Grind": [
        "Nothing to grind",
        "Only if u care about leaderboards/ranks",
        "Isn't necessary to progress",
        "Average grind level",
        "Too much grind",
        "You'll need a second life for grinding"
    ],
    "Story": [
        "No Story",
        "Some lore",
        "Average",
        "Good",
        "Lovely",
        "It'll replace your life"
    ],
    "Game Time": [
        "Long enough for a cup of coffee",
        "Short",
        "Average",
        "Long",
        "To infinity and beyond"
    ],
    "Price": [
        "It's free!",
        "Worth the price",
        "If it's on sale",
        "If u have some spare money left",
        "Not recommended",
        "You could also just burn your money"
    ],
    "Bugs": [
        "Never heard of",
        "Minor bugs",
        "Can get annoying",
        "ARK: Survival Evolved",
        "The game itself is a big terrarium for bugs"
    ],
    "Controls": [
        "Perfect",
        "Needs improvement",
        "Frustrating"
    ],
    "Multiplayer": [
        "Top",
        "Good",
        "Connection issues",
        "Missing completely"
    ],
    "Replayability": [
        "Unlimited",
        "Playable multiple times",
        "One-time only"
    ],
    "Innovation / Originality": [
        "Groundbreaking",
        "Refreshing",
        "Repetitive"
    ],
    "Atmosphere / Immersion": [
        "Fully immersive",
        "Exciting",
        "Superficial"
    ],
    "Support / Community": [
        "Helpful",
        "Neutral",
        "Frustrating"
    ]
}

root = tk.Tk()
root.title("Steam Review Generator")
root.geometry("800x600")
root.resizable(True, True)

selected_options = {}
audience_vars = {}
audience_widgets = {}

def update_audience_checkbuttons():
    everyone_selected = audience_vars["Everyone"].get()
    for option, widget in audience_widgets.items():
        if option != "Everyone":
            if everyone_selected:
                widget.config(state="disabled")
                audience_vars[option].set(False)
            else:
                widget.config(state="normal")
    if not everyone_selected:
        for option in categories["Audience"]:
            if option != "Everyone" and audience_vars[option].get():
                audience_widgets["Everyone"].config(state="disabled")
                break
        else:
            audience_widgets["Everyone"].config(state="normal")

notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

for cat, options in categories.items():
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=cat)
    if cat == "Audience":
        audience_vars = {option: tk.BooleanVar(value=False) for option in options}
        audience_widgets = {}
        for i, option in enumerate(options):
            cb = ttk.Checkbutton(frame, text=option, variable=audience_vars[option],
                                 command=update_audience_checkbuttons)
            cb.grid(row=i, column=0, sticky="w", padx=10, pady=2)
            audience_widgets[option] = cb
    else:
        var = tk.StringVar(value="")
        selected_options[cat] = var
        for i, option in enumerate(options):
            rb = ttk.Radiobutton(frame, text=option, variable=var, value=option)
            rb.grid(row=i, column=0, sticky="w", padx=10, pady=2)

rating_frame = ttk.LabelFrame(root, text="Rating")
rating_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
rating_var = tk.IntVar(value=5)
rating_scale = tk.Scale(rating_frame, from_=1, to=10, orient="horizontal", variable=rating_var)
rating_scale.pack(padx=10, pady=5, fill="x")

output_frame = ttk.Frame(root)
output_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

output_text = tk.Text(output_frame, wrap="word")
output_text.grid(row=0, column=0, sticky="nsew")
scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=output_text.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
output_text.config(yscrollcommand=scrollbar.set)

root.columnconfigure(0, weight=1)
root.rowconfigure(2, weight=1)
output_frame.columnconfigure(0, weight=1)
output_frame.rowconfigure(0, weight=1)

def generate_review():
    review_lines = []
    rating = rating_var.get()
    header = f"[h1]{rating} / 10[/h1]"
    review_lines.append(header)
    review_lines.append("")
    for cat, options in categories.items():
        review_lines.append(f"[h3]{cat}[/h3]")
        if cat == "Audience":
            for option in options:
                marker = "☑" if audience_vars[option].get() else "☐"
                review_lines.append(f"{marker} {option}")
        else:
            selected = selected_options[cat].get()
            for option in options:
                marker = "☑" if option == selected else "☐"
                review_lines.append(f"{marker} {option}")
        review_lines.append("")
    review_lines.append(header)
    review_text = "\n".join(review_lines)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, review_text)

def save_as_txt():
    review_text = output_text.get("1.0", tk.END).strip()
    if not review_text:
        messagebox.showwarning("Warning", "No review available! Please generate a review first.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                                             title="Save review as TXT")
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(review_text)
            messagebox.showinfo("Success", "Review saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save the file:\n{e}")

def copy_review():
    review_text = output_text.get("1.0", tk.END).strip()
    if not review_text:
        messagebox.showwarning("Warning", "No review available! Please generate a review first.")
        return
    root.clipboard_clear()
    root.clipboard_append(review_text)
    messagebox.showinfo("Success", "Review copied to clipboard!")

button_frame = ttk.Frame(root)
button_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
button_frame.columnconfigure((0, 1, 2), weight=1)

generate_button = ttk.Button(button_frame, text="Generate Review", command=generate_review)
generate_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

save_button = ttk.Button(button_frame, text="Save as TXT", command=save_as_txt)
save_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

copy_button = ttk.Button(button_frame, text="Copy Review", command=copy_review)
copy_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

root.mainloop()
