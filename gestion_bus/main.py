import tkinter as tk
from db import connect_to_db
from login import open_login_window
from user_management import open_user_management
from receiver_management import open_receiver_management
from bus_management import open_bus_management
from driver_management import open_driver_management

def main():
    root = tk.Tk()
    root.title("Système de Gestion des Bus au Sénégal")
    root.geometry("400x400")

    # Vérification des identifiants de connexion
    user_login = open_login_window(root)
    if not user_login:
        return

    def open_management_window(title, open_function):
        def wrapper():
            management_window = tk.Toplevel()
            management_window.title(title)
            open_function(management_window)
        return wrapper

    def logout():
        root.destroy()
        main()

    # Display the login of the connected user
    tk.Label(root, text=f"Connecté en tant que : {user_login}").pack(pady=10)

    btn_user_management = tk.Button(root, text="Gestion des Utilisateurs", command=open_user_management)
    btn_user_management.pack(pady=10)

    btn_receiver_management = tk.Button(root, text="Gestion des Receveurs", command=open_receiver_management)
    btn_receiver_management.pack(pady=10)

    btn_driver_management = tk.Button(root, text="Gestion des Chauffeurs", command=open_driver_management)
    btn_driver_management.pack(pady=10)

    btn_bus_management = tk.Button(root, text="Gestion des Bus", command=open_bus_management)
    btn_bus_management.pack(pady=10)

    btn_logout = tk.Button(root, text="Déconnexion", command=logout)
    btn_logout.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
