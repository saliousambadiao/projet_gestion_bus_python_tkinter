import tkinter as tk
from tkinter import messagebox, simpledialog
from db import connect_to_db
import mysql.connector

def open_user_management():
    user_window = tk.Toplevel()
    user_window.title("Gestion des Utilisateurs")

    # Function to fetch users from database and display them
    def fetch_users():
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nom, prenom, telephone, email, login FROM utilisateurs")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return users

    def add_user():
        nom = entry_nom.get()
        prenom = entry_prenom.get()
        telephone = entry_telephone.get()
        email = entry_email.get()
        login = entry_login.get()
        mot_de_passe = entry_mot_de_passe.get()

        conn = connect_to_db()
        cursor = conn.cursor()

        try:
            # Vérifier si le login existe déjà
            cursor.execute("SELECT COUNT(*) FROM utilisateurs WHERE login = %s", (login,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Erreur", "Ce login existe déjà")
                return

            cursor.execute("INSERT INTO utilisateurs (nom, prenom, telephone, email, login, password) VALUES (%s, %s, %s, %s, %s, %s)",
                           (nom, prenom, telephone, email, login, mot_de_passe))
            conn.commit()
            messagebox.showinfo("Succès", "Utilisateur ajouté avec succès")
            refresh_user_list()
        except mysql.connector.errors.IntegrityError as e:
            messagebox.showerror("Erreur", str(e))
        finally:
            cursor.close()
            conn.close()

    def delete_user():
        login = entry_login_delete.get()
        password = entry_password_delete.get()

        conn = connect_to_db()
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM utilisateurs WHERE login = %s AND password = %s", (login, password))
            if cursor.rowcount == 0:
                messagebox.showerror("Erreur", "Utilisateur non trouvé ou mot de passe incorrect")
            else:
                conn.commit()
                messagebox.showinfo("Succès", "Utilisateur supprimé avec succès")
                refresh_user_list()
        except mysql.connector.errors.IntegrityError as e:
            messagebox.showerror("Erreur", str(e))
        finally:
            cursor.close()
            conn.close()
    def modify_user():
        selected_user = user_listbox.curselection()
        if not selected_user:
            messagebox.showerror("Erreur", "Veuillez sélectionner un utilisateur à modifier")
            return
        
        index = selected_user[0]
        user_data = fetch_users()[index]
        user_id = user_data[0]
        
        # Demander les nouvelles informations
        new_nom = simpledialog.askstring("Modifier Utilisateur", "Nouveau nom:", initialvalue=user_data[1])
        new_prenom = simpledialog.askstring("Modifier Utilisateur", "Nouveau prénom:", initialvalue=user_data[2])
        new_telephone = simpledialog.askstring("Modifier Utilisateur", "Nouveau téléphone:", initialvalue=user_data[3])
        new_email = simpledialog.askstring("Modifier Utilisateur", "Nouvel email:", initialvalue=user_data[4])
        new_login = simpledialog.askstring("Modifier Utilisateur", "Nouveau login:", initialvalue=user_data[5])
        new_password = simpledialog.askstring("Modifier Utilisateur", "Nouveau mot de passe:", show='*')

        if not all([new_nom, new_prenom, new_telephone, new_email, new_login, new_password]):
            messagebox.showerror("Erreur", "Toutes les informations doivent être renseignées")
            return

        conn = connect_to_db()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE utilisateurs
                SET nom = %s, prenom = %s, telephone = %s, email = %s, login = %s, password = %s
                WHERE id = %s
            """, (new_nom, new_prenom, new_telephone, new_email, new_login, new_password, user_id))
            conn.commit()
            messagebox.showinfo("Succès", "Utilisateur modifié avec succès")
            refresh_user_list()
        except mysql.connector.errors.IntegrityError as e:
            messagebox.showerror("Erreur", str(e))
        finally:
            cursor.close()
            conn.close()

    def refresh_user_list():
        user_listbox.delete(0, tk.END)
        users = fetch_users()
        for user in users:
            user_listbox.insert(tk.END, f"{user[2]} {user[1]} - {user[4]} - {user[3]}")

    # Labels and Entries for user input
    tk.Label(user_window, text="Nom").grid(row=0, column=0, padx=10, pady=5)
    entry_nom = tk.Entry(user_window)
    entry_nom.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(user_window, text="Prénom").grid(row=1, column=0, padx=10, pady=5)
    entry_prenom = tk.Entry(user_window)
    entry_prenom.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(user_window, text="Téléphone").grid(row=2, column=0, padx=10, pady=5)
    entry_telephone = tk.Entry(user_window)
    entry_telephone.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(user_window, text="Email").grid(row=3, column=0, padx=10, pady=5)
    entry_email = tk.Entry(user_window)
    entry_email.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(user_window, text="Login").grid(row=4, column=0, padx=10, pady=5)
    entry_login = tk.Entry(user_window)
    entry_login.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(user_window, text="Mot de passe").grid(row=5, column=0, padx=10, pady=5)
    entry_mot_de_passe = tk.Entry(user_window)
    entry_mot_de_passe.grid(row=5, column=1, padx=10, pady=5)

    # Button to add user
    btn_add_user = tk.Button(user_window, text="Ajouter", command=add_user)
    btn_add_user.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    # Listbox to display users
    user_listbox = tk.Listbox(user_window, width=100)
    user_listbox.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    # Fetch users initially and display in the listbox
    refresh_user_list()

    # Button to refresh user list
    btn_refresh = tk.Button(user_window, text="Actualiser", command=refresh_user_list)
    btn_refresh.grid(row=8, column=0, padx=10, pady=10)
    
    # Entry for deleting user
    tk.Label(user_window, text="Login de l'utilisateur à supprimer").grid(row=9, column=0, padx=10, pady=5)
    entry_login_delete = tk.Entry(user_window)
    entry_login_delete.grid(row=9, column=1, padx=10, pady=5)

    tk.Label(user_window, text="Mot de passe de l'utilisateur à supprimer").grid(row=10, column=0, padx=10, pady=5)
    entry_password_delete = tk.Entry(user_window, show="*")
    entry_password_delete.grid(row=10, column=1, padx=10, pady=5)

    # Button to delete user
    btn_delete_user = tk.Button(user_window, text="Supprimer", command=delete_user)
    btn_delete_user.grid(row=11, column=0, columnspan=2, padx=10, pady=10)

    # Button to modify user
    btn_modify_user = tk.Button(user_window, text="Modifier", command=modify_user)
    btn_modify_user.grid(row=12, column=0, columnspan=2, padx=10, pady=10)

  
