import tkinter as tk
from tkinter import messagebox, simpledialog


class DailyBudgetTracker:
    def __init__(self, budget):
        self.budget = budget
        self.expenses = []
        self.category_totals = {}

    def add_expense(self, amount, category):
        self.expenses.append({"amount": amount, "category": category})

        if category in self.category_totals:
            self.category_totals[category] += amount
        else:
            self.category_totals[category] = amount

    def total_expenses(self):
        return sum(expense["amount"] for expense in self.expenses)

    def remaining_budget(self):
        return self.budget - self.total_expenses()

    def budget_status(self):
        total = self.total_expenses()
        if total > self.budget:
            overspend = total - self.budget
            return f"⚠️ Budget Alert! Exceeded by ${overspend:.2f}"
        else:
            remaining = self.budget - total
            return f"✅ Budget OK. Remaining: ${remaining:.2f}"


class DailyBudgetTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Budget Tracker with Budget Alerts")
        self.root.geometry("500x500")

        self.tracker = None

        self.setup_budget_screen()

    def setup_budget_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = tk.Label(self.root, text="🤑 Daily Budget Tracker 🚨", font=("Arial", 18, "bold"))
        title.pack(pady=20)

        tk.Label(self.root, text="Enter your monthly budget:").pack(pady=10)

        self.budget_entry = tk.Entry(self.root, width=20)
        self.budget_entry.pack(pady=5)

        start_button = tk.Button(self.root, text="Start Tracker", command=self.start_tracker)
        start_button.pack(pady=20)

    def start_tracker(self):
        try:
            budget = float(self.budget_entry.get())
            self.tracker = DailyBudgetTracker(budget)
            self.setup_main_screen()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the budget.")

    def setup_main_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        title = tk.Label(self.root, text="Daily Budget Tracker Dashboard", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        self.status_label = tk.Label(self.root, text=self.tracker.budget_status(), font=("Arial", 12))
        self.status_label.pack(pady=10)

        add_button = tk.Button(self.root, text="➕ Add Expense", width=20, command=self.add_expense_gui)
        add_button.pack(pady=5)

        view_button = tk.Button(self.root, text="📜 View Expenses", width=20, command=self.view_expenses_gui)
        view_button.pack(pady=5)

        summary_button = tk.Button(self.root, text="📊 View Summary", width=20, command=self.view_summary_gui)
        summary_button.pack(pady=5)

        exit_button = tk.Button(self.root, text="❌ Exit", width=20, command=self.root.quit)
        exit_button.pack(pady=20)

        self.output_text = tk.Text(self.root, height=12, width=55)
        self.output_text.pack(pady=10)

    def add_expense_gui(self):
        try:
            amount = simpledialog.askfloat("Add Expense", "Enter amount:")
            if amount is None:
                return

            category = simpledialog.askstring("Add Expense", "Enter category (Food, Rent, Gas, etc.):")
            if category is None or category.strip() == "":
                return

            category = category.strip().title()
            self.tracker.add_expense(amount, category)
            self.status_label.config(text=self.tracker.budget_status())
            messagebox.showinfo("Success", f"Added ${amount:.2f} to {category}.")
        except ValueError:
            messagebox.showerror("Error", "Invalid expense amount.")

    def view_expenses_gui(self):
        self.output_text.delete("1.0", tk.END)

        if not self.tracker.expenses:
            self.output_text.insert(tk.END, "No expenses recorded.\n")
            return

        self.output_text.insert(tk.END, "--- All Expenses ---\n")
        for idx, expense in enumerate(self.tracker.expenses, 1):
            self.output_text.insert(
                tk.END,
                f"{idx}. Category: {expense['category']}, Amount: ${expense['amount']:.2f}\n"
            )

    def view_summary_gui(self):
        self.output_text.delete("1.0", tk.END)

        total_expenses = self.tracker.total_expenses()
        remaining = self.tracker.remaining_budget()

        self.output_text.insert(tk.END, "--- Budget Summary ---\n")
        self.output_text.insert(tk.END, f"Total Budget: ${self.tracker.budget:.2f}\n")
        self.output_text.insert(tk.END, f"Total Spent: ${total_expenses:.2f}\n")
        self.output_text.insert(tk.END, f"Remaining: ${remaining:.2f}\n\n")

        self.output_text.insert(tk.END, "--- Category Breakdown ---\n")
        if not self.tracker.category_totals:
            self.output_text.insert(tk.END, "No category expenses yet.\n")
        else:
            for category, total in self.tracker.category_totals.items():
                self.output_text.insert(tk.END, f"{category}: ${total:.2f}\n")

        self.output_text.insert(tk.END, "\n--------------------------\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = DailyBudgetTrackerGUI(root)
    root.mainloop()




