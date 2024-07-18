import tkinter as tk
from tkinter import messagebox
from db import connect_to_db

def open_login_window(root):
    login_info = {"login": None}

    def authenticate():
        login = entry_login.get()
        password = entry_password.get()

        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM utilisateurs WHERE login=%s AND password=%s", (login, password))
        result = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        if result > 0:
            login_info["login"] = login
            login_window.destroy()
        else:
            messagebox.showerror("Erreur", "Login ou mot de passe incorrect")

    login_window = tk.Toplevel(root)
    login_window.title("Login")

    tk.Label(login_window, text="Login").grid(row=0, column=0)
    entry_login = tk.Entry(login_window)
    entry_login.grid(row=0, column=1)

    tk.Label(login_window, text="Mot de passe").grid(row=1, column=0)
    entry_password = tk.Entry(login_window, show='*')
    entry_password.grid(row=1, column=1)

    btn_login = tk.Button(login_window, text="Se connecter", command=authenticate)
    btn_login.grid(row=2, columnspan=2)

    root.wait_window(login_window)
    return login_info["login"]
