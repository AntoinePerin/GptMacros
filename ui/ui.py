import tkinter as tk
from tkinter import ttk, messagebox
from macros.Macros import run_macro_1, run_macro_2

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GptMacros")
        self.root.resizable(False, False)
        self.set_window_size()
        self.create_tabs()
        self.active_label = None
        self.active_button = None
        self.modifiers = []

    def set_window_size(self):
        lgt = 400
        wdt = 300

        # Taille maximale de la fenêtre
        self.root.maxsize(lgt, wdt)  # Largeur max x Hauteur max
        # Taille minimale de la fenêtre (optionnel)
        self.root.minsize(lgt, wdt)   # Largeur min x Hauteur min

    def create_tabs(self):
        tab_control = ttk.Notebook(self.root)

        tab1 = ttk.Frame(tab_control)
        tab2 = ttk.Frame(tab_control)

        tab_control.add(tab1, text='Macros')
        tab_control.add(tab2, text='À propos')

        # Créer la liste de key bindings avec boutons dans le premier onglet
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
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_columnconfigure(1, weight=0)
            frame.grid_columnconfigure(2, weight=0)

            desc_label = ttk.Label(frame, text=macro_label, anchor='w', wraplength=150)
            desc_label.grid(row=i, column=0, sticky='w', padx=(0, 5))

            key_label = ttk.Label(frame, text=key, width=15, font=('Helvetica', 10, 'bold'), anchor='w')
            key_label.grid(row=i, column=1, padx=(0, 5))

            button = ttk.Button(frame, text="Modifier")
            button.grid(row=i, column=2, padx=5, sticky='e')
            button.config(command=lambda l=key_label, b=button: self.capture_key_combination(l, b))

            self.key_bindings.append(key_label)
            self.labels.append(desc_label)

    def capture_key_combination(self, label, button):
        if self.active_label is not None:
            messagebox.showerror("Erreur", "Vous ne pouvez modifier qu'une ligne à la fois.")
            return

        self.active_label = label
        self.active_button = button
        self.modifiers = []
        label.config(text="Appuyer sur une touche...", width=30)
        button.config(state='disabled')
        self.root.bind('<KeyPress>', self.record_key_combination)
        self.root.bind('<KeyRelease>', self.record_key_combination)

    def record_key_combination(self, event):
        if event.type == '2':  # KeyPress
            combination = self.get_combination(event)
            if combination:
                self.modifiers.append(combination)
        elif event.type == '3':  # KeyRelease
            if self.active_label:
                self.active_label.config(text='+'.join(self.modifiers))
                self.active_button.config(state='normal')
                self.active_label = None
                self.active_button = None
                self.root.unbind('<KeyPress>')
                self.root.unbind('<KeyRelease>')

    def get_combination(self, event):
        keysym = event.keysym
        state = event.state
        modifiers = []
        if state & 0x4:  # Control
            modifiers.append('Ctrl')
        if state & 0x1:  # Shift
            modifiers.append('Shift')
        if state & 0x20000:  # Alt
            modifiers.append('Alt')

        # Ajoute la touche principale à la liste des modificateurs si elle n'est pas un modificateur
        if keysym not in ['Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R', 'Meta_L', 'Meta_R']:
            modifiers.append(keysym)

        return '+'.join(modifiers) if modifiers else None

    def run(self):
        self.root.mainloop()