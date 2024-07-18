import tkinter as tk
from tkinter import messagebox, simpledialog
from db import connect_to_db

def open_receiver_management():
    receiver_window = tk.Toplevel()
    receiver_window.title("Gestion des Receveurs")

    def fetch_receivers():
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nom, prenom, telephone, age FROM receveurs")
        receivers = cursor.fetchall()
        cursor.close()
        conn.close()
        return receivers

    def add_receiver():
        nom = entry_nom.get()
        prenom = entry_prenom.get()
        telephone = entry_telephone.get()
        age = entry_age.get()

        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO receveurs (nom, prenom, telephone, age) VALUES (%s, %s, %s, %s)",
                       (nom, prenom, telephone, age))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Succès", "Receveur ajouté avec succès")
        refresh_receiver_list()

    def delete_receiver():
        selected_receiver = receiver_listbox.curselection()
        if not selected_receiver:
            messagebox.showerror("Erreur", "Veuillez sélectionner un receveur à supprimer")
            return
        
        index = selected_receiver[0]
        receiver_id = receiver_list[index][0]

        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM receveurs WHERE id = %s", (receiver_id,))
            conn.commit()
            messagebox.showinfo("Succès", "Receveur supprimé avec succès")
            refresh_receiver_list()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression du receveur : {str(e)}")
        finally:
            cursor.close()
            conn.close()

    def modify_receiver():
        selected_receiver = receiver_listbox.curselection()
        if not selected_receiver:
            messagebox.showerror("Erreur", "Veuillez sélectionner un receveur à modifier")
            return
        
        index = selected_receiver[0]
        receiver_data = receiver_list[index]
        receiver_id = receiver_data[0]
        
        # Demander les nouvelles informations
        new_nom = simpledialog.askstring("Modifier Receveur", "Nouveau nom:", initialvalue=receiver_data[1])
        new_prenom = simpledialog.askstring("Modifier Receveur", "Nouveau prénom:", initialvalue=receiver_data[2])
        new_telephone = simpledialog.askstring("Modifier Receveur", "Nouveau téléphone:", initialvalue=receiver_data[3])
        new_age = simpledialog.askstring("Modifier Receveur", "Nouvel âge:", initialvalue=receiver_data[4])

        if not all([new_nom, new_prenom, new_telephone, new_age]):
            messagebox.showerror("Erreur", "Toutes les informations doivent être renseignées")
            return

        conn = connect_to_db()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE receveurs
                SET nom = %s, prenom = %s, telephone = %s, age = %s
                WHERE id = %s
            """, (new_nom, new_prenom, new_telephone, new_age, receiver_id))
            conn.commit()
            messagebox.showinfo("Succès", "Receveur modifié avec succès")
            refresh_receiver_list()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la modification du receveur : {str(e)}")
        finally:
            cursor.close()
            conn.close()

    def refresh_receiver_list():
        receiver_listbox.delete(0, tk.END)
        global receiver_list
        receiver_list = fetch_receivers()
        for receiver in receiver_list:
            receiver_listbox.insert(tk.END, f"{receiver[1]} {receiver[2]} - {receiver[3]} - {receiver[4]} ans")

    # Labels and Entries for receiver input
    tk.Label(receiver_window, text="Nom").pack()
    entry_nom = tk.Entry(receiver_window)
    entry_nom.pack()

    tk.Label(receiver_window, text="Prénom").pack()
    entry_prenom = tk.Entry(receiver_window)
    entry_prenom.pack()

    tk.Label(receiver_window, text="Téléphone").pack()
    entry_telephone = tk.Entry(receiver_window)
    entry_telephone.pack()

    tk.Label(receiver_window, text="Âge").pack()
    entry_age = tk.Entry(receiver_window)
    entry_age.pack()

    # Button to add receiver
    btn_add_receiver = tk.Button(receiver_window, text="Ajouter", command=add_receiver)
    btn_add_receiver.pack()

    # Listbox to display receivers
    receiver_listbox = tk.Listbox(receiver_window, width=100)
    receiver_listbox.pack()

    # Fetch receivers initially and display in the listbox
    refresh_receiver_list()

    # Button to refresh receiver list
    btn_refresh_receivers = tk.Button(receiver_window, text="Actualiser", command=refresh_receiver_list)
    btn_refresh_receivers.pack()

    # Button to delete receiver
    btn_delete_receiver = tk.Button(receiver_window, text="Supprimer", command=delete_receiver)
    btn_delete_receiver.pack()

    # Button to modify receiver
    btn_modify_receiver = tk.Button(receiver_window, text="Modifier", command=modify_receiver)
    btn_modify_receiver.pack()

# Example usage (replace with actual database interaction)
# if __name__ == "__main__":
#     open_receiver_management()
