import tkinter as tk
from pynput import keyboard
import threading

class App:
    def __init__(self):
        # interface utilisateur
        self.root = tk.Tk()

        #Listener, touches préssées
        self.pressed_vks = set()
        
        # Démarrer le listener pour les frappes de touches dans un thread séparé
        self.listener_thread = threading.Thread(target=self.start_listener)
        self.listener_thread.start()

        # Créer un événement pour signaler l'arrêt du listener
        self.stop_event = threading.Event()

        # Assurer l'arrêt propre du thread à la fermeture de l'application
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Create a mapping of keys to function (use frozenset as sets/lists are not hashable - so they can't be used as keys)
        # Note the missing `()` after function_1 and function_2 as want to pass the function, not the return value of the function
        self.combination_to_function = {
            frozenset([keyboard.Key.shift, keyboard.KeyCode(vk=65)]): self.function_1,  # shift + a
            frozenset([keyboard.Key.shift, keyboard.KeyCode(vk=66)]): self.function_2,  # shift + b
        }

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