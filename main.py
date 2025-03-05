import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
import json
import google.generativeai as genai

genai.configure(api_key="API-KEY")

# Load and save functions
def load_dictionary(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_dictionary(dictionary, filename):
    with open(filename, 'w') as file:
        json.dump(dictionary, file, indent=4)

def generate_ai_summary(word, meaning):
    prompt = (
        f"Create a short summary for the word '{word}' with its meaning '{meaning}'. "
        f"Provide 2 example sentences using the word in different contexts."
    )
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating summary: {e}"


def add_word():
    word = simpledialog.askstring("Add Word", "Enter the word:")
    if word:
        if word in dictionary:
            messagebox.showinfo("Info", "Word already exists.")
        else:
            meaning = simpledialog.askstring("Add Meaning", f"Enter the meaning of '{word}':")
            if meaning:
                dictionary[word] = {"meaning": meaning}
                messagebox.showinfo("Success", f"'{word}' added successfully!")

def delete_word():
    word = simpledialog.askstring("Delete Word", "Enter the word to delete:")
    if word in dictionary:
        del dictionary[word]
        messagebox.showinfo("Success", f"'{word}' deleted successfully!")
    else:
        messagebox.showerror("Error", "Word not found.")

def update_word():
    word = simpledialog.askstring("Update Word", "Enter the word to update:")
    if word in dictionary:
        choice = simpledialog.askstring("Choice", "Update (word/meaning)?")
        if choice == "word":
            new_word = simpledialog.askstring("New Word", "Enter the new word:")
            dictionary[new_word] = dictionary.pop(word)
            messagebox.showinfo("Updated", f"Word updated to '{new_word}'.")
        elif choice == "meaning":
            new_meaning = simpledialog.askstring("New Meaning", "Enter the new meaning:")
            dictionary[word]["meaning"] = new_meaning
            messagebox.showinfo("Updated", f"Meaning of '{word}' updated.")
    else:
        messagebox.showerror("Error", "Word not found.")

def show_dictionary():
    display_window = tk.Toplevel(root)
    display_window.title("Dictionary Words")
    display_window.configure(bg="#f0f8ff")

    text_area = scrolledtext.ScrolledText(display_window, width=80, height=25, font=("Consolas", 12), wrap=tk.WORD)
    text_area.pack(padx=20, pady=20)

    for word, details in dictionary.items():
        if "summary" not in details:
            details["summary"] = generate_ai_summary(word, details["meaning"])
        text_area.insert(tk.END, f"Word: {word}\nMeaning: {details['meaning']}\nAI Summary:\n{details['summary']}\n{'-'*70}\n")

def save_and_exit():
    save_dictionary(dictionary, filename)
    messagebox.showinfo("Saved", "Dictionary saved successfully!")
    root.destroy()


root = tk.Tk()
root.title("WordCraft AI")
root.configure(bg="#eaf6fd")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 500
window_height = 500
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

container = tk.Frame(root, bg="#dbe9f4", padx=30, pady=30, relief=tk.RIDGE, bd=2)
container.place(relx=0.5, rely=0.5, anchor="center")

title_label = tk.Label(container, text="WordCraft AI", font=("Poppins", 20, "bold"), bg="#dbe9f4")
title_label.pack(pady=(0, 20))

button_style = {"width": 25, "height": 2, "font": ("Helvetica", 12)}

buttons = [
    ("Add Word", add_word),
    ("Delete Word", delete_word),
    ("Update Word or Meaning", update_word),
    ("Show All Words", show_dictionary),
    ("Save Dictionary", save_and_exit)
]

for text, command in buttons:
    btn = tk.Button(container, text=text, command=command, **button_style)
    btn.pack(pady=5)

filename = "english_dictionary.json"
dictionary = load_dictionary(filename)

root.mainloop()