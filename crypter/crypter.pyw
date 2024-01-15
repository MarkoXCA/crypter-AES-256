import tkinter as tk
from tkinter import filedialog
from cryptography.fernet import Fernet
import os
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Définir le nom du fichier pour stocker les clés de chiffrement
KEY_FILE = "key/encryption_key.key"
BACKUP_FILE = "key/key_backup.txt"

# Couleurs du thème sombre
bg_color = "#094A2A"  # Couleur de fond
fg_color = "white"    # Couleur du texte
button_bg = "#094A2A" # Couleur de fond des boutons
button_fg = "#50B95C"   # Couleur du texte des boutons
border_color = "#094A2A"  # Couleur de la bordure

# Variables pour le déplacement de la fenêtre
mouse_x, mouse_y = 0, 0

# Font moderne
font = ("Helvetica", 12)

# Fonction pour chiffrer ou déchiffrer un fichier avec la clé globale
def process_file(encrypt=True):
    global global_key
    if not global_key:
        status_label.config(text="Veuillez définir une clé de chiffrement.", fg="red")
        return

    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            cipher_suite = Fernet(global_key)

            with open(file_path, 'rb') as f:
                data = f.read()

            if encrypt:
                encrypted_data = cipher_suite.encrypt(data)
                save_path = filedialog.asksaveasfilename(defaultextension=os.path.splitext(file_path)[-1])
                if save_path:
                    with open(save_path, 'wb') as f:
                        f.write(encrypted_data)
            else:
                decrypted_data = cipher_suite.decrypt(data)
                save_path = filedialog.asksaveasfilename(defaultextension=os.path.splitext(file_path)[-1])
                if save_path:
                    with open(save_path, 'wb') as f:
                        f.write(decrypted_data)
        except Exception as e:
            status_label.config(text=f"Erreur : {str(e)}", fg="red")

# Fonction pour définir la clé globale à partir d'un fichier ou demander à l'utilisateur
def set_key():
    global global_key
    if os.path.isfile(KEY_FILE):
        with open(KEY_FILE, 'rb') as key_file:
            global_key = key_file.readline().strip()
    else:
        key_input = input("Veuillez entrer la clé de chiffrement (base64) : ")
        global_key = key_input.encode()
        with open(KEY_FILE, 'wb') as key_file:
            key_file.write(global_key + b'\n')
    
    key_text.delete(1.0, tk.END)
    key_text.insert(tk.END, global_key.decode())
    status_label.config(text="Clé de chiffrement définie.", fg="#59D102")

# Fonction pour générer une nouvelle clé et écraser la première ligne du fichier
def generate_key():
    new_key = Fernet.generate_key()
    with open(KEY_FILE, 'r') as key_file:
        lines = key_file.readlines()
    
    with open(KEY_FILE, 'w') as key_file:
        key_file.write(new_key.decode() + '\n')
        key_file.writelines(lines[1:])
    
    key_text.delete(1.0, tk.END)
    key_text.insert(tk.END, new_key.decode())
    status_label.config(text="Nouvelle clé générée et écrite sur la première ligne du fichier.", fg="#59D102")

# Fonction pour sauvegarder toutes les clés dans un fichier de sauvegarde
def backup_keys():
    with open(KEY_FILE, 'r') as key_file:
        keys = key_file.readlines()
    
    with open(BACKUP_FILE, 'a') as backup_file:
        backup_file.writelines(keys)
        backup_file.write("\n\n")  # Séparateur entre les clés

    status_label.config(text=f"Toutes les clés ont été sauvegardées dans {BACKUP_FILE}.", fg="#59D102")

# Fonction pour fermer la fenêtre
def close_window():
    root.destroy()

# Gestionnaire d'événement pour le clic gauche de la souris
def on_mouse_press(event):
    global mouse_x, mouse_y
    mouse_x, mouse_y = event.x, event.y

# Gestionnaire d'événement pour le déplacement de la souris avec le clic gauche maintenu
def on_mouse_drag(event):
    x, y = event.x_root - mouse_x, event.y_root - mouse_y
    root.geometry(f"+{x}+{y}")

# Création de l'interface utilisateur
root = tk.Tk()
root.title("Outil de chiffrement/déchiffrement AES-256")
root.configure(bg=bg_color)
root.overrideredirect(True)  # Supprimer la barre de titre

# Associez les gestionnaires d'événements aux widgets pertinents
root.bind("<ButtonPress-1>", on_mouse_press)
root.bind("<B1-Motion>", on_mouse_drag)

# Charger une image depuis une URL
image_url = "https://cdn.discordapp.com/attachments/1153277328403726418/1196381886474354688/Ryuk-Couleur-Noir-Marque-Checkpoint.png?ex=65b76c75&is=65a4f775&hm=6c16238a5430f1e2869b20d4e69fb9ba464b8d7aede2665580d111e9905bb75e&"  # Remplacez l'URL par l'URL de votre image
response = requests.get(image_url)
image_data = BytesIO(response.content)
image = Image.open(image_data)
image_width, image_height = image.size

# Créez un widget Label pour afficher l'image en arrière-plan
photo = ImageTk.PhotoImage(image)
background_label = tk.Label(root, image=photo)
background_label.image = photo  # Gardez une référence à l'image pour éviter la suppression
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Remplit toute la fenêtre

close_button = tk.Button(root, text="Fermer", command=close_window, bg=button_bg, fg=button_fg, font=font)
close_button.pack(anchor=tk.NE)
# Personnalisation de la bordure
root.configure(highlightbackground=border_color, highlightcolor=border_color, highlightthickness=2)

set_key_button = tk.Button(root, text="Définir la clé", command=set_key, bg=button_bg, fg=button_fg, font=font)
set_key_button.pack()

generate_key_button = tk.Button(root, text="Générer une nouvelle clé", command=generate_key, bg=button_bg, fg=button_fg, font=font)
generate_key_button.pack()

backup_keys_button = tk.Button(root, text="Sauvegarder les clés", command=backup_keys, bg=button_bg, fg=button_fg, font=font)
backup_keys_button.pack()

global_key = None  # Initialisez la clé globale

encrypt_button = tk.Button(root, text="Chiffrer un fichier", command=lambda: process_file(encrypt=True), bg=button_bg, fg=button_fg, font=font)
decrypt_button = tk.Button(root, text="Déchiffrer un fichier", command=lambda: process_file(encrypt=False), bg=button_bg, fg=button_fg, font=font)

encrypt_button.pack(pady=10)
decrypt_button.pack(pady=10)

key_text = tk.Text(root, height=1, width=50, bg=bg_color, fg=fg_color, font=font)
key_text.pack()
key_text.insert(tk.END, global_key.decode() if global_key else "")

status_label = tk.Label(root, text="", fg="green", bg=bg_color, font=font)
status_label.pack()

# Ajoutez un bouton pour fermer la fenêtre

root.mainloop()
