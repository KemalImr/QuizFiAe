import tkinter as tk
from tkinter import messagebox
import json
import random

# Fragen aus JSON-Datei laden
def load_questions(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        messagebox.showerror("Error", f"Fehler beim Laden der Datei {filename}: {e}")
        return []

# Fragen aus beiden JSON-Dateien mischen
def load_mixed_questions(files):
    all_questions = []
    for file in files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                all_questions.extend(json.load(f))
        except Exception as e:
            messagebox.showerror("Error", f"Fehler beim Laden der Datei {file}: {e}")
            return []
    random.shuffle(all_questions)
    return all_questions

class QuizApp:
    def __init__(self, root, questions):
        self.root = root
        self.root.title("Quiz Game")
        self.center_window(600, 300)

        self.score = 0
        self.question_index = 0
        self.questions = questions

        self.question_label = tk.Label(root, text="", wraplength=450)
        self.question_label.pack(pady=20)

        self.var = tk.IntVar()
        self.choices = []
        for i in range(4):
            rb = tk.Radiobutton(root, text="", variable=self.var, value=i)
            rb.pack(anchor="w")
            self.choices.append(rb)

        self.submit_button = tk.Button(root, text="Submit", command=self.check_answer)
        self.submit_button.pack(pady=20)

        self.show_question()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def show_question(self):
        if self.question_index < len(self.questions):
            q = self.questions[self.question_index]
            self.question_label.config(text=q["question"])

            # Update Radiobuttons based on the number of choices
            for i, choice in enumerate(q["choices"]):
                if i < len(self.choices):
                    self.choices[i].config(text=choice, state=tk.NORMAL)
                else:
                    rb = tk.Radiobutton(self.root, text=choice, variable=self.var, value=i)
                    rb.pack(anchor="w")
                    self.choices.append(rb)

            for i in range(len(q["choices"]), len(self.choices)):
                self.choices[i].config(state=tk.DISABLED)

            self.var.set(-1)
        else:
            self.show_result()

    def check_answer(self):
        selected = self.var.get()
        if selected == -1:
            messagebox.showwarning("Warning", "Please select an answer")
            return

        q = self.questions[self.question_index]
        if selected == q["answer"]:
            explanation = "\n".join(q["explanation"])
            messagebox.showinfo("Richtig", f"Deine Antwort ist richtig!\n{explanation}")
            self.score += 1
        else:
            explanation = "\n".join(q["explanation"])
            messagebox.showinfo("Falsch", f"Deine Antwort ist falsch.\n\nErklärung:\n{explanation}")

        self.question_index += 1
        self.show_question()

    def show_result(self):
        messagebox.showinfo("Result", f"Your score is: {self.score} out of {len(self.questions)}")
        self.root.destroy()

def select_question_pool():
    def start_quiz(selection):
        if selection == "Projekt Management":
            questions = load_questions("questionsProjektManagement.json")
        elif selection == "Wirtschaft":
            questions = load_questions("questionsWirtschaft.json")
        elif selection == "UML":
            questions = load_questions("questionsUML.json")
        elif selection == "Programmierung":
            questions = load_questions("questionsProgrammierung.json")
        else:
            questions = load_mixed_questions([
                "questionsProjektManagement.json",
                "questionsWirtschaft.json",
                "questionsUML.json",
                "questionsProgrammierung.json"
            ])
        
        quiz_window = tk.Toplevel(root)
        app = QuizApp(quiz_window, questions)
        root.withdraw()
    
    selection_window = tk.Toplevel(root)
    selection_window.title("Select Question Pool")
    center_window(selection_window, 400, 200)

    tk.Label(selection_window, text="Wählen Sie den Fragen-Pool:").grid(row=0, column=0, columnspan=2, pady=20)

    tk.Button(selection_window, text="Projekt Management", command=lambda: start_quiz("Projekt Management")).grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    tk.Button(selection_window, text="Wirtschaft", command=lambda: start_quiz("Wirtschaft")).grid(row=1, column=1, padx=10, pady=10, sticky="ew")
    tk.Button(selection_window, text="UML", command=lambda: start_quiz("UML")).grid(row=2, column=0, padx=10, pady=10, sticky="ew")
    tk.Button(selection_window, text="Programmierung", command=lambda: start_quiz("Programmierung")).grid(row=2, column=1, padx=10, pady=10, sticky="ew")
    tk.Button(selection_window, text="Mix aus allen", command=lambda: start_quiz("Mix aus allen")).grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

    for i in range(2):
        selection_window.grid_columnconfigure(i, weight=1)

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    select_question_pool()
    root.mainloop()
