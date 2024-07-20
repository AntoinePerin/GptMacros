import tkinter as tk
from tkinter import ttk, messagebox
from pynput import keyboard
import threading

class App:
    def __init__(self):

        #Listener, touches préssées
        self.pressed_vks = set()
        
        #combinaison enregistrées
        self.key_bindings = set()
        self.labels = set()

        #dico combinaison foncton
        self.combinations = {
            "Correcteur d'orthographe": (frozenset([keyboard.Key.shift, keyboard.KeyCode(vk=65)]), self.function_1),  # shift + a
            "Traduction en Anglais": (frozenset([keyboard.Key.shift, keyboard.KeyCode(vk=66)]), self.function_2),    # shift + b
        }

        # interface utilisateur
        self.initUi()
        
        # Démarrer le listener pour les frappes de touches dans un thread séparé
        self.listener_thread = threading.Thread(target=self.start_listener)
        self.listener_thread.start()

        # Créer un événement pour signaler l'arrêt du listener
        self.stop_event = threading.Event()

        # Assurer l'arrêt propre du thread à la fermeture de l'application
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)


    #___________________________UI_____________________________________

    def initUi(self):
        # interface utilisateur
        self.root = tk.Tk()
        self.root.title("GptMacros")
        self.set_window_size()
        self.create_tabs()

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

        self.render_tab_1(tab1)
        self.render_tab_2(tab2)

        tab_control.pack(expand=1, fill='both')

    def render_tab_1(self, parent):
        self.create_key_bindings(parent)
        
    def render_tab_2(self, parent):
        label = ttk.Label(parent, text='Cette application exécute des macros clavier.')
        label.pack(pady=10)
        label2 = ttk.Label(parent, text='Développé par Antoine Périn (et ChatGpt <3).')
        label2.pack(pady=10)

    def create_key_bindings(self, parent):

        frame = ttk.Frame(parent)
        frame.pack(pady=5, padx=10, fill='x')

        # Configurer les colonnes pour l'alignement
        frame.columnconfigure(0, weight=1, uniform="a")  
        frame.columnconfigure(1, weight=1, uniform="a")  
        frame.columnconfigure(2, weight=0)

        # Créer des labels non modifiables avec labels fixes
        for i,(label, (combination, _)) in enumerate(self.combinations.items()):

            desc_label = ttk.Label(frame, text=label, anchor='w', wraplength=200, justify='left')
            desc_label.grid(row=i, column=0, padx=(0, 5), sticky='w')

            key_label = ttk.Label(frame, text=self.get_combination_str(combination), font=('Helvetica', 10, 'bold'), anchor='w')
            key_label.grid(row=i, column=1, padx=(0, 5), sticky='w')

            button = ttk.Button(frame, text="Modifier")
            button.grid(row=i, column=2, padx=5, sticky='w')
            #button.config(command=lambda l=key_label, b=button: self.capture_key_combination(l, b))

            # self.key_bindings.append(key_label)
            # self.labels.append(desc_label)
            

    def get_combination_str(self, combination):
        # Convertir la combinaison de touches en une chaîne lisible
        keys = []
        for key in combination:
            if isinstance(key, keyboard.Key):
                keys.append(key.name)
            else:
                keys.append(chr(key.vk))
        return "+".join(keys)

    #_________________________________Listener___________________________________


    def function_1(self):
        print('Executed function_1')

    def function_2(self):
        print('Executed function_2')

    def get_vk(self, key):
        return key.vk if hasattr(key, 'vk') else key.value.vk
    
    def on_press(self,key):
        vk = self.get_vk(key)  # Get the key's vk
        self.pressed_vks.add(vk)  # Add it to the set of currently pressed keys
        for combination in self.combination_to_function:  # Loop through each combination
            if self.is_combination_pressed(combination):  # Check if all keys in the combination are pressed
                self.combination_to_function[combination]()  # If so, execute the function
    
    def on_release(self, key):
        vk = self.get_vk(key)  # Get the key's vk
        self.pressed_vks.remove(vk)  # Remove it from the set of currently pressed keys

    def is_combination_pressed(self,combination):
        return all([self.get_vk(key) in self.pressed_vks for key in combination])

    def start_listener(self):
        # Configurer et démarrer le listener
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            self.stop_event.wait()  # Attendre que l'événement d'arrêt soit déclenché
            listener.stop()  # Arrêter le listener proprement

    def on_close(self):
        # Méthode appelée lors de la fermeture de la fenêtre
        self.stop_event.set()  # Arrêter le listener
        self.listener_thread.join()  # Attendre que le thread du listener se termine
        self.root.destroy()  # Détruire la fenêtre Tkinter

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()