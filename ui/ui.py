import tkinter as tk
from tkinter import ttk, messagebox
from macros.Macros import run_macro_1, run_macro_2

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GptMaccros")
        self.root.resizable(False, False)
        self.set_window_size()
        self.create_tabs()

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
        tab3 = ttk.Frame(tab_control)

        tab_control.add(tab1, text='Macro 1')
        tab_control.add(tab2, text='Macro 2')
        tab_control.add(tab3, text='À propos')

        # Créer la liste de text box avec boutons dans le premier onglet
        self.create_text_boxes_with_buttons(tab1)

        label1 = ttk.Label(tab1, text='Cliquez sur le bouton pour exécuter la macro 1.')
        label1.pack(pady=10)
        button1 = ttk.Button(tab1, text='Exécuter Macro 1', command=run_macro_1)
        button1.pack(pady=10)

        label2 = ttk.Label(tab2, text='Cliquez sur le bouton pour exécuter la macro 2.')
        label2.pack(pady=10)
        button2 = ttk.Button(tab2, text='Exécuter Macro 2', command=run_macro_2)
        button2.pack(pady=10)

        label3 = ttk.Label(tab3, text='Cette application exécute des macros clavier.')
        label3.pack(pady=10)
        label4 = ttk.Label(tab3, text='Développé par [Votre Nom].')
        label4.pack(pady=10)

        tab_control.pack(expand=1, fill='both')

    def create_text_boxes_with_buttons(self, parent):
        self.text_boxes = []
        self.labels = []
        
        # Exemple de données initiales pour les text boxes
        data = ["Texte 1", "Texte 2", "Texte 3"]

        # Créer des zones de texte non modifiables avec labels fixes
        for i, text in enumerate(data):
            frame = ttk.Frame(parent)
            frame.pack(pady=5, padx=10, fill='x')

            label = ttk.Label(frame, text=f"Label {i+1}", width=10, anchor='w')
            label.pack(side='left')

            text_box = tk.Text(frame, height=2, width=30, wrap='word')
            text_box.insert('1.0', text)
            text_box.configure(state='disabled')  # Zone de texte non modifiable
            text_box.pack(side='left')

            self.text_boxes.append(text_box)
            self.labels.append(label)
        
        # Bouton Modifier
        self.edit_button = ttk.Button(parent, text="Modifier", command=self.enable_editing)
        self.edit_button.pack(pady=10, padx=10, side='left')

        # Bouton Enregistrer
        self.save_button = ttk.Button(parent, text="Enregistrer", command=self.save_text_boxes, state='disabled')
        self.save_button.pack(pady=10, padx=10, side='left')

    def enable_editing(self):
        # Activer la modification des zones de texte
        for text_box in self.text_boxes:
            text_box.configure(state='normal')
        # Activer le bouton Enregistrer
        self.save_button.configure(state='normal')
        # Désactiver le bouton Modifier
        self.edit_button.configure(state='disabled')

    def save_text_boxes(self):
        # Sauvegarder les valeurs des zones de texte
        for i, text_box in enumerate(self.text_boxes):
            content = text_box.get('1.0', 'end-1c')
            print(f"Texte {i+1} sauvegardé : {content}")
        
        # Réinitialiser les boutons
        for text_box in self.text_boxes:
            text_box.configure(state='disabled')
        self.edit_button.configure(state='normal')
        self.save_button.configure(state='disabled')

    def run(self):
        self.root.mainloop()
