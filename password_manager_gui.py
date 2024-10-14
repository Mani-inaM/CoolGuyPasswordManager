import tkinter as tk
from tkinter import messagebox
from password_manager import PasswordManager


class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager Login")
        self.root.geometry("400x250")

        self.pm = PasswordManager()

        label_master_password = tk.Label(self.root, text="Master Password")
        label_master_password.pack(pady=10)
        self.entry_master_password = tk.Entry(self.root, show="*", width=50)
        self.entry_master_password.pack()

        button_login = tk.Button(self.root, text="Login", command=self.login)
        button_login.pack(pady=10)

        button_add_user = tk.Button(self.root, text="Add User", command=self.open_add_user_window)
        button_add_user.pack(pady=10)

    def login(self):
        master_password = self.entry_master_password.get()

        if master_password:
            if self.pm.verify_master_password(master_password):
                self.open_services_window(master_password)
            else:
                messagebox.showwarning("Login Failed", "Incorrect Master Password.")
        else:
            messagebox.showwarning("Input Error", "Please enter the master password.")

    def open_services_window(self, master_password):
        services = self.pm.retrieve_all_services(master_password)

        if services is None:
            messagebox.showwarning("Error", "Invalid master password.")
            return

        services_window = tk.Toplevel(self.root)
        services_window.title("Stored Services")
        services_window.geometry("600x400")

        label_services = tk.Label(services_window, text="Stored Services", font=("Arial", 14))
        label_services.pack(pady=10)

        # Scrollable list for services
        service_frame = tk.Frame(services_window)
        service_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(service_frame)
        scrollbar = tk.Scrollbar(service_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add each service to the scrollable list
        for service, credentials in services.items():
            username, password = credentials
            service_label = tk.Label(scrollable_frame, text=f"Service: {service}")
            service_label.pack()

            username_label = tk.Label(scrollable_frame, text=f"Username: {username}")
            username_label.pack()

            password_var = tk.StringVar(value="*" * len(password))

            password_label = tk.Label(scrollable_frame, textvariable=password_var)
            password_label.pack()

            # Reveal/Hide password toggle function
            def reveal_password(pw=password, var=password_var):
                if var.get() == "*" * len(pw):
                    var.set(pw)
                else:
                    var.set("*" * len(pw))

            reveal_button = tk.Button(scrollable_frame, text="Reveal Password", command=lambda pw=password: reveal_password(pw))
            reveal_button.pack()

            # Copy password to clipboard function
            def copy_password(pw=password):
                self.root.clipboard_clear()
                self.root.clipboard_append(pw)
                messagebox.showinfo("Copied", f"Password for {service} copied to clipboard.")

            copy_button = tk.Button(scrollable_frame, text="Copy Password", command=lambda pw=password: copy_password(pw))
            copy_button.pack()

            tk.Label(scrollable_frame, text="").pack()  # Empty line separator

        # Add Service button
        button_add_service = tk.Button(services_window, text="Add Service", command=lambda: self.open_add_service_window(master_password))
        button_add_service.pack(pady=10)

    def open_add_service_window(self, master_password):
        add_service_window = tk.Toplevel(self.root)
        add_service_window.title("Add New Service")
        add_service_window.geometry("400x300")

        label_service = tk.Label(add_service_window, text="Service Name")
        label_service.pack(pady=5)
        entry_service = tk.Entry(add_service_window, width=50)
        entry_service.pack(pady=5)

        label_username = tk.Label(add_service_window, text="Username")
        label_username.pack(pady=5)
        entry_username = tk.Entry(add_service_window, width=50)
        entry_username.pack(pady=5)

        label_password = tk.Label(add_service_window, text="Password")
        label_password.pack(pady=5)
        entry_password = tk.Entry(add_service_window, show="*", width=50)
        entry_password.pack(pady=5)

        # Generate Password button
        def generate_password():
            generated_password = self.pm.helper.generate_password()
            entry_password.delete(0, tk.END)
            entry_password.insert(0, generated_password)

        button_generate_password = tk.Button(add_service_window, text="Generate Password", command=generate_password)
        button_generate_password.pack(pady=5)

        def add_service():
            service = entry_service.get()
            username = entry_username.get()
            password = entry_password.get()

            if service and username and password:
                master_password = self.entry_master_password.get()  # Fetch the master password from the login
                self.pm.store_password(master_password, service, username, password)
                messagebox.showinfo("Success", "New service added successfully!")
                add_service_window.destroy()
            else:
                messagebox.showwarning("Input Error", "Please fill all fields.")

        button_add = tk.Button(add_service_window, text="Add Service", command=add_service)
        button_add.pack(pady=20)

    def open_add_user_window(self):
        add_user_window = tk.Toplevel(self.root)
        add_user_window.title("Add New User")
        add_user_window.geometry("400x300")

        label_create_master_password = tk.Label(add_user_window, text="Create Master Password")
        label_create_master_password.pack(pady=10)
        entry_new_master_password = tk.Entry(add_user_window, show="*", width=50)
        entry_new_master_password.pack()

        label_confirm_master_password = tk.Label(add_user_window, text="Confirm Master Password")
        label_confirm_master_password.pack(pady=10)
        entry_confirm_master_password = tk.Entry(add_user_window, show="*", width=50)
        entry_confirm_master_password.pack()

        def create_user():
            new_password = entry_new_master_password.get()
            confirm_password = entry_confirm_master_password.get()

            if new_password and confirm_password:
                if new_password == confirm_password:
                    self.pm.create_user(new_password)
                    messagebox.showinfo("Success", "New user created successfully!")
                    add_user_window.destroy()
                else:
                    messagebox.showwarning("Error", "Passwords do not match.")
            else:
                messagebox.showwarning("Input Error", "Please fill all fields.")

        button_create_user = tk.Button(add_user_window, text="Create User", command=create_user)
        button_create_user.pack(pady=20)


# Start the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()
