import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
import time


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


encryption_folder = "C:\\Users\\Grace Lewis\\fortishare\\Encryption_Decryption"
# decryption_folder = "C:\\Users\\Grace Lewis\\fortishare\\Decrypted_Files"
decryption_folder = "C:\\Users\\Grace Lewis\\Desktop\\reciever"
encrypted_files_folder = "C:\\Users\\Grace Lewis\\fortishare\\Encryption_Decryption\\Encrypted_Files"
random_code = "123"  

class EncryptionHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_name = os.path.basename(event.src_path)
            logger.info(f"File {file_name} has been added to Encryption_Decryption folder.")
            self.encrypt_file(event.src_path)  # Pass the file path to encrypt_file

    def encrypt_file(self, file_path):  # Add file_path as an argument
        """Encrypts a file using the encryption.py script."""
        encryption_script = "C:\\Users\\Grace Lewis\\fortishare\\Encryption_Decryption\\encryption.py"
        file_name = os.path.basename(file_path)
      

        try:
            # Run the encryption script
            process = subprocess.Popen(["python", encryption_script, file_path, random_code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Wait for the process to finish
            process.wait()

            if process.returncode == 0:
                logger.info(f"File {file_name} encrypted successfully.")
                
        except Exception as e:
            logger.error(f"Error encrypting file {file_name}: {e}")

class DecryptionHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_name = os.path.basename(event.src_path)
            logger.info(f"File {file_name} has been added to Decrypted_Files folder.")
            self.decrypt_file(event.src_path)  # Pass the file path to decrypt_file

    def decrypt_file(self, file_path):  # Add file_path as an argument
        """Decrypts a file using the decryption.py script."""
        decryption_script = "C:\\Users\\Grace Lewis\\fortishare\\Encryption_Decryption\\decryption.py"
        file_name = os.path.basename(file_path)

        try:
            # Run the decryption script
            process = subprocess.Popen(["python", decryption_script, file_path, random_code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            process.wait()

            if process.returncode == 0:
                logger.info(f"File {file_name} decrypted successfully.")

        except Exception as e:
            logger.error(f"Error decrypting file {file_name}: {e}")

if __name__ == '__main__':
    encryption_handler = EncryptionHandler()
    decryption_handler = DecryptionHandler()
    
    observer = Observer()
    observer.schedule(encryption_handler, encryption_folder, recursive=True)
    observer.schedule(decryption_handler, decryption_folder, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("Observer Stopped")
    observer.join()
