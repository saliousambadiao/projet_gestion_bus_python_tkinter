import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from db import connect_to_db

def open_driver_management():
    driver_window = tk.Toplevel()
    driver_window.title("Gestion des Chauffeurs")

    def add_driver():
        nom = entry_nom.get()
        prenom = entry_prenom.get()
        telephone = entry_telephone.get()
        age = entry_age.get()
        type_permis = combobox_type_permis.get()

        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO chauffeurs (nom, prenom, telephone, age, type_permis) VALUES (%s, %s, %s, %s, %s)",
                           (nom, prenom, telephone, age, type_permis))
            conn.commit()
            messagebox.showinfo("Succès", "Chauffeur ajouté avec succès")
            refresh_driver_list()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout du chauffeur : {str(e)}")
        finally:
            cursor.close()
            conn.close()

    def modify_driver():
        selected_driver = driver_listbox.curselection()
        if not selected_driver:
            messagebox.showerror("Erreur", "Veuillez sélectionner un chauffeur à modifier")
            return
        
        driver_index = selected_driver[0]
        driver_id = drivers[driver_index][0]

        new_nom = simpledialog.askstring("Modifier Chauffeur", "Nouveau nom:", initialvalue=drivers[driver_index][1])
        new_prenom = simpledialog.askstring("Modifier Chauffeur", "Nouveau prénom:", initialvalue=drivers[driver_index][2])
        new_telephone = simpledialog.askstring("Modifier Chauffeur", "Nouveau téléphone:", initialvalue=drivers[driver_index][3])
        new_age = simpledialog.askstring("Modifier Chauffeur", "Nouvel âge:", initialvalue=drivers[driver_index][4])
        new_type_permis = simpledialog.askstring("Modifier Chauffeur", "Nouveau type de permis:", initialvalue=drivers[driver_index][5])

        if not all([new_nom, new_prenom, new_telephone, new_age, new_type_permis]):
            messagebox.showerror("Erreur", "Toutes les informations doivent être renseignées")
            return

        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE chauffeurs SET nom=%s, prenom=%s, telephone=%s, age=%s, type_permis=%s WHERE id=%s",
                           (new_nom, new_prenom, new_telephone, new_age, new_type_permis, driver_id))
            conn.commit()
            messagebox.showinfo("Succès", "Chauffeur modifié avec succès")
            refresh_driver_list()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la mise à jour du chauffeur : {str(e)}")
        finally:
            cursor.close()
            conn.close()

    def delete_driver():
        selected_driver = driver_listbox.curselection()
        if not selected_driver:
            messagebox.showerror("Erreur", "Veuillez sélectionner un chauffeur à supprimer")
            return
        
        driver_index = selected_driver[0]
        driver_id = drivers[driver_index][0]

        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM chauffeurs WHERE id=%s", (driver_id,))
            conn.commit()
            messagebox.showinfo("Succès", "Chauffeur supprimé avec succès")
            refresh_driver_list()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression du chauffeur : {str(e)}")
        finally:
            cursor.close()
            conn.close()

    def refresh_driver_list():
        global drivers
        drivers = []
        driver_listbox.delete(0, tk.END)

        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nom, prenom, telephone, age, type_permis FROM chauffeurs")
        drivers = cursor.fetchall()
        for driver in drivers:
            driver_listbox.insert(tk.END, f"{driver[2]} {driver[1]} - {driver[4]} ans - {driver[3]} - {driver[5]}")
        cursor.close()
        conn.close()

    tk.Label(driver_window, text="Nom").grid(row=0, column=0, padx=10, pady=5)
    entry_nom = tk.Entry(driver_window)
    entry_nom.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(driver_window, text="Prénom").grid(row=1, column=0, padx=10, pady=5)
    entry_prenom = tk.Entry(driver_window)
    entry_prenom.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(driver_window, text="Téléphone").grid(row=2, column=0, padx=10, pady=5)
    entry_telephone = tk.Entry(driver_window)
    entry_telephone.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(driver_window, text="Âge").grid(row=3, column=0, padx=10, pady=5)
    entry_age = tk.Entry(driver_window)
    entry_age.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(driver_window, text="Type de permis").grid(row=4, column=0, padx=10, pady=5)
    combobox_type_permis = ttk.Combobox(driver_window, values=["Permis A", "Permis B"])
    combobox_type_permis.grid(row=4, column=1, padx=10, pady=5)

    btn_add_driver = tk.Button(driver_window, text="Ajouter", command=add_driver)
    btn_add_driver.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    btn_modify_driver = tk.Button(driver_window, text="Modifier", command=modify_driver)
    btn_modify_driver.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    btn_delete_driver = tk.Button(driver_window, text="Supprimer", command=delete_driver)
    btn_delete_driver.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    driver_listbox = tk.Listbox(driver_window, width=100)
    driver_listbox.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

    refresh_driver_list()
