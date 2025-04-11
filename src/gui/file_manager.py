from tkinter import filedialog, messagebox


def save_review(root, review_text):
    if not review_text:
        messagebox.showwarning("Warning", "No review available! Please generate a review first.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(review_text)
            messagebox.showinfo("Success", "Review saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save the file:\n{e}")


def copy_review(root, review_text):
    if not review_text:
        messagebox.showwarning("Warning", "No review available! Please generate a review first.")
        return
    root.clipboard_clear()
    root.clipboard_append(review_text)
    messagebox.showinfo("Success", "Review copied to clipboard!")
