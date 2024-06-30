import tkinter as tk
from tkinter import ttk, messagebox
from macros.Macros import run_macro_1, run_macro_2
import json
import os
from pynput import keyboard
import threading

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GptMacros")
        self.root.resizable(False, False)
        self.set_window_size()
        self.create_tabs()
        self.active_label = None
        self.active_button = None
        self.modifiers = set()
        self.keys = set()
        self.bindings = []

        # Charger les données depuis le fichier JSON
        self.load_key_bindings()

        # Démarrer le listener pour les frappes de touches dans un thread séparé
        self.listener_thread = threading.Thread(target=self.start_listener)
        self.listener_thread.start()

    def set_window_size(self):
        lgt = 400
        wdt = 300
        self.root.maxsize(lgt, wdt)  
        self.root.minsize(lgt, wdt)   

    def create_tabs(self):
        tab_control = ttk.Notebook(self.root)

        tab1 = ttk.Frame(tab_control)
        tab2 = ttk.Frame(tab_control)

        tab_control.add(tab1, text='Macros')
        tab_control.add(tab2, text='À propos')

        self.create_key_bindings(tab1)

        label1 = ttk.Label(tab1, text='Cliquez sur le bouton pour exécuter la macro 1.')
        label1.pack(pady=10)
        button1 = ttk.Button(tab1, text='Exécuter Macro 1', command=run_macro_1)
        button1.pack(pady=10)

        label2 = ttk.Label(tab2, text='Cette application exécute des macros clavier.')
        label2.pack(pady=10)
        label3 = ttk.Label(tab2, text='Développé par Antoine Périn (et ChatGpt <3).')
        label3.pack(pady=10)

        tab_control.pack(expand=1, fill='both')

    def create_key_bindings(self, parent):
        self.key_bindings = []
        self.labels = []

        # Labels des fonctionnalités
        label_Macro = ["Correcteur d'orthographe : ", "Traduction en Anglais : "]

        # Exemple de données initiales pour les touches
        data = ["A", "B"]

        # Créer des labels non modifiables avec labels fixes
        for i, (macro_label, key) in enumerate(zip(label_Macro, data)):
            frame = ttk.Frame(parent)
            frame.pack(pady=5, padx=10, fill='x')

            # Configurer les colonnes pour l'alignement
            frame.columnconfigure(0, weight=1, uniform="a")  
            frame.columnconfigure(1, weight=1, uniform="a")  
            frame.columnconfigure(2, weight=0)  

            desc_label = ttk.Label(frame, text=macro_label, anchor='w', wraplength=200, justify='left')
            desc_label.grid(row=i, column=0, padx=(0, 5), sticky='w')

            key_label = ttk.Label(frame, text=key, font=('Helvetica', 10, 'bold'), anchor='w')
            key_label.grid(row=i, column=1, padx=(0, 5), sticky='w')

            button = ttk.Button(frame, text="Modifier")
            button.grid(row=i, column=2, padx=5, sticky='w')
            button.config(command=lambda l=key_label, b=button: self.capture_key_combination(l, b))

            self.key_bindings.append(key_label)
            self.labels.append(desc_label)

    def capture_key_combination(self, label, button):
        if self.active_label is not None:
            messagebox.showerror("Erreur", "Vous ne pouvez modifier qu'une ligne à la fois.")
            return

        self.active_label = label
        self.active_button = button
        self.modifiers.clear()
        self.keys.clear()
        label.config(text="Appuyer sur une touche...", wraplength=200)
        button.config(state='disabled')
        self.root.bind('<KeyPress>', self.record_key_combination)
        self.root.bind('<KeyRelease>', self.record_key_release)

    def record_key_combination(self, event):
        keysym = event.keysym
        if keysym in {'Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R', 'Meta_L', 'Meta_R'}:
            self.modifiers.add(keysym)
        else:
            self.keys.add(keysym)

    def record_key_release(self, event):
        # Mise à jour de la combinaison lors du relâchement des touches
        combination = self.get_combination()
        if self.active_label:
            self.active_label.config(text=combination)
            self.active_button.config(state='normal')
            self.active_label = None
            self.active_button = None
            self.root.unbind('<KeyPress>')
            self.root.unbind('<KeyRelease>')

            # Sauvegarder la combinaison dans un fichier JSON
            self.save_key_bindings()

    def get_combination(self):
        # Ordre des modificateurs
        order = {'Control_L': 'Ctrl', 'Control_R': 'Ctrl', 'Shift_L': 'Shift', 'Shift_R': 'Shift',
                 'Alt_L': 'Alt', 'Alt_R': 'Alt', 'Meta_L': 'Meta', 'Meta_R': 'Meta'}

        # Convertir les modificateurs en liste triée
        sorted_modifiers = [order[key] for key in sorted(self.modifiers) if key in order]
        # Ajouter les touches principales
        main_keys = sorted(self.keys)
        
        return '+'.join(sorted_modifiers + main_keys)

    def save_key_bindings(self):
        bindings = {i: label.cget('text') for i, label in enumerate(self.key_bindings)}
        with open('bindings.json', 'w') as f:
            json.dump(bindings, f)

    def load_key_bindings(self):
        if os.path.exists('bindings.json'):
            with open('bindings.json', 'r') as f:
                bindings = json.load(f)
                for i, key_label in enumerate(self.key_bindings):
                    if str(i) in bindings:
                        key_label.config(text=bindings[str(i)])

    def on_press(self, key):
        try:
            # Afficher la touche pressée si elle a une représentation de caractère
            print(f'Key pressed: {key.char}')
        except AttributeError:
            # Pour les touches spéciales comme Shift, Ctrl, etc.
            print(f'Special key pressed: {key}')

    def on_release(self, key):
        # Optionnel: ajouter des actions lors du relâchement de la touche
        if key == keyboard.Key.esc:
            # Arrêter le listener si la touche 'esc' est pressée
            return False

    def start_listener(self):
        # Configurer et démarrer le listener
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def run(self):
        self.root.mainloop()

# Lancer l'application
if __name__ == "__main__":
    app = App()
    app.run()
