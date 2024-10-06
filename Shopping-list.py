import tkinter as tk
from tkinter import messagebox
import json
import os

class ShoppingListApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Shopping List")
        self.master.configure(bg="pink")

        self.shopping_list = {}
        self.filename = "shopping_list.json"
        self.load_list()

        # Create the GUI components
        self.create_widgets()

    def create_widgets(self):
        # Header
        label_logo = tk.Label(self.master, text="SHOPPING LIST", font=("Helvetica", 24, "bold"), bg="#e6ffe6", fg="#006600")
        label_logo.pack(pady=10)

        # Input Frame
        frame = tk.Frame(self.master, bg="#007FFF")
        frame.pack(padx=10, pady=10, fill='both', expand=True)

        tk.Label(frame, text="Item:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_item = tk.Entry(frame, font=("Arial", 12))
        self.entry_item.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Amount:", bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_amount = tk.Entry(frame, font=("Arial", 12))
        self.entry_amount.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Price ($):", bg="#f0f0f0", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_price = tk.Entry(frame, font=("Arial", 12))
        self.entry_price.grid(row=2, column=1, padx=5, pady=5)

        # Action Buttons
        buttons = [
            ("Add Item", self.add_item),
            ("Edit Item", self.edit_item),
            ("Remove Item", self.remove_item),
            ("Display List", self.display_list),
            ("Calculate Total Cost", self.calculate_total),
            ("Clear List", self.clear_list),
        ]

        for i, (text, command) in enumerate(buttons):
            button = tk.Button(frame, text=text, font=("Arial", 12), command=command)
            button.grid(row=3+i, column=0, columnspan=2, padx=5, pady=5, sticky="we")

        # Listbox with ScrollBar
        self.listbox_frame = tk.Frame(frame)
        self.listbox_frame.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.listbox = tk.Listbox(self.listbox_frame, font=("Arial", 12), height=8)
        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(self.listbox_frame)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        # Confirm on close
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_list(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.shopping_list = json.load(f)

    def save_list(self):
        with open(self.filename, 'w') as f:
            json.dump(self.shopping_list, f)

    def display_list(self):
        self.listbox.delete(0, tk.END)
        for item, details in self.shopping_list.items():
            amount, price = details
            self.listbox.insert(tk.END, f"- {item} (Amount: {amount}, Price: ${price:.2f})")

    def add_item(self):
        item = self.entry_item.get().strip()
        amount = self.entry_amount.get().strip()
        price = self.entry_price.get().strip()
        
        if not item or not amount or not price:
            messagebox.showerror("Error", "Please enter item, amount, and price.")
            return

        try:
            amount = int(amount)
            price = float(price)
            if amount < 0 or price < 0:
                raise ValueError("Negative values are not allowed.")
            
            if item in self.shopping_list:
                self.shopping_list[item][0] += amount  # Update amount
            else:
                self.shopping_list[item] = [amount, price]  # Store amount and price

            self.entry_item.delete(0, tk.END)
            self.entry_amount.delete(0, tk.END)
            self.entry_price.delete(0, tk.END)
            self.display_list()
            self.save_list()
            messagebox.showinfo("Success", f"{amount} {item}(s) at ${price:.2f} each have been added to your shopping list.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def remove_item(self):
        item = self.entry_item.get().strip()
        if item in self.shopping_list:
            del self.shopping_list[item]
            self.entry_item.delete(0, tk.END)
            self.display_list()
            self.save_list()
            messagebox.showinfo("Success", f"{item} has been removed from your shopping list.")
        else:
            messagebox.showerror("Error", f"{item} is not in your shopping list.")

    def edit_item(self):
        item = self.entry_item.get().strip()
        new_amount = self.entry_amount.get().strip()
        
        if not item or not new_amount:
            messagebox.showerror("Error", "Please enter both item and new amount.")
            return

        try:
            new_amount = int(new_amount)
            if new_amount < 0:
                raise ValueError("Negative values are not allowed.")
            if item in self.shopping_list:
                self.shopping_list[item][0] = new_amount  # Update the item's amount
                self.entry_item.delete(0, tk.END)
                self.entry_amount.delete(0, tk.END)
                self.display_list()
                self.save_list()
                messagebox.showinfo("Success", f"The amount of {item} has been updated to {new_amount}.")
            else:
                messagebox.showerror("Error", f"{item} is not in your shopping list.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def clear_list(self):
        self.shopping_list.clear()
        self.display_list()
        self.save_list()
        messagebox.showinfo("Success", "All items have been cleared from your shopping list.")

    def calculate_total(self):
        total = sum(amount * price for amount, price in self.shopping_list.values())
        messagebox.showinfo("Total Cost", f"Total cost of items in the shopping list: ${total:.2f}")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.master.destroy()

# Main function
def main():
    root = tk.Tk()
    app = ShoppingListApp(root)
    root.mainloop()

# Run the main function
if __name__ == "__main__":
    main()
