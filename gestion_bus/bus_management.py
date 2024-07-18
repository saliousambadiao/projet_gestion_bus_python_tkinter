import tkinter as tk
from tkinter import messagebox, simpledialog
from db import connect_to_db
import mysql.connector

def open_bus_management():
    bus_window = tk.Toplevel()
    bus_window.title("Gestion des Bus")

    # Function to fetch buses from database and display them
    def fetch_buses():
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, couleur, marque, numero FROM bus")
        buses = cursor.fetchall()
        cursor.close()
        conn.close()
        return buses

    def add_bus():
        couleur = entry_couleur.get()
        marque = entry_marque.get()
        numero = entry_numero.get()

        conn = connect_to_db()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO bus (couleur, marque, numero) VALUES (%s, %s, %s)",
                           (couleur, marque, numero))
            conn.commit()
            messagebox.showinfo("Succès", "Bus ajouté avec succès")
            refresh_bus_list()
        except mysql.connector.errors.IntegrityError as e:
            messagebox.showerror("Erreur", str(e))
        finally:
            cursor.close()
            conn.close()

    def delete_bus():
        numero = entry_numero_delete.get()

        conn = connect_to_db()
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM bus WHERE numero = %s", (numero,))
            if cursor.rowcount == 0:
                messagebox.showerror("Erreur", "Bus non trouvé")
            else:
                conn.commit()
                messagebox.showinfo("Succès", "Bus supprimé avec succès")
                refresh_bus_list()
        except mysql.connector.errors.IntegrityError as e:
            messagebox.showerror("Erreur", str(e))
        finally:
            cursor.close()
            conn.close()

    def modify_bus():
        selected_bus = bus_listbox.curselection()
        if not selected_bus:
            messagebox.showerror("Erreur", "Veuillez sélectionner un bus à modifier")
            return

        index = selected_bus[0]
        bus_data = fetch_buses()[index]
        bus_id = bus_data[0]

        new_couleur = simpledialog.askstring("Modifier Bus", "Nouvelle couleur:", initialvalue=bus_data[1])
        new_marque = simpledialog.askstring("Modifier Bus", "Nouvelle marque:", initialvalue=bus_data[2])
        new_numero = simpledialog.askstring("Modifier Bus", "Nouveau numéro:", initialvalue=bus_data[3])

        if not all([new_couleur, new_marque, new_numero]):
            messagebox.showerror("Erreur", "Toutes les informations doivent être renseignées")
            return

        conn = connect_to_db()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE bus
                SET couleur = %s, marque = %s, numero = %s
                WHERE id = %s
            """, (new_couleur, new_marque, new_numero, bus_id))
            conn.commit()
            messagebox.showinfo("Succès", "Bus modifié avec succès")
            refresh_bus_list()
        except mysql.connector.errors.IntegrityError as e:
            messagebox.showerror("Erreur", str(e))
        finally:
            cursor.close()
            conn.close()

    def refresh_bus_list():
        bus_listbox.delete(0, tk.END)
        buses = fetch_buses()
        for bus in buses:
            bus_listbox.insert(tk.END, f"{bus[3]} - {bus[2]} - {bus[1]}")

    # Labels and Entries for bus input
    tk.Label(bus_window, text="Couleur").grid(row=0, column=0, padx=10, pady=5)
    entry_couleur = tk.Entry(bus_window)
    entry_couleur.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(bus_window, text="Marque").grid(row=1, column=0, padx=10, pady=5)
    entry_marque = tk.Entry(bus_window)
    entry_marque.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(bus_window, text="Numéro").grid(row=2, column=0, padx=10, pady=5)
    entry_numero = tk.Entry(bus_window)
    entry_numero.grid(row=2, column=1, padx=10, pady=5)

    # Button to add bus
    btn_add_bus = tk.Button(bus_window, text="Ajouter", command=add_bus)
    btn_add_bus.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # Listbox to display buses
    bus_listbox = tk.Listbox(bus_window, width=100)
    bus_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    # Fetch buses initially and display in the listbox
    refresh_bus_list()
    
    # Entry for deleting bus
    tk.Label(bus_window, text="Numéro du bus à supprimer").grid(row=6, column=0, padx=10, pady=5)
    entry_numero_delete = tk.Entry(bus_window)
    entry_numero_delete.grid(row=6, column=1, padx=10, pady=5)

    # Button to delete bus
    btn_delete_bus = tk.Button(bus_window, text="Supprimer", command=delete_bus)
    btn_delete_bus.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    # Button to modify bus
    btn_modify_bus = tk.Button(bus_window, text="Modifier", command=modify_bus)
    btn_modify_bus.grid(row=8, column=0, columnspan=2, padx=10, pady=10)
