import math
import tkinter as tk
from tkinter import messagebox

p = 1000000007
q = 1000000009
n = p * q
phi = (p - 1) * (q - 1)
e = 65537
d = pow(e, -1, phi)

def encrypt_text(text):
    b = text.encode("cp1251")
    m = int.from_bytes(b, "big")
    if m >= n:
        raise ValueError("Текст слишком длинный для этого ключа")
    c = pow(m, e, n)
    return c, len(b)


def decrypt_text(c, length):
    m = pow(c, d, n)
    return m.to_bytes(length, "big").decode("cp1251")

root = tk.Tk()

root.title("RSA — асимметричное шифрование")

root.geometry("600x450")

tk.Label(root, text="Текст (открытый или шифртекст):").pack(anchor="w", padx=10, pady=(10, 0))
txt_input = tk.Text(root, height=4, width=70)
txt_input.pack(padx=10, pady=5)

tk.Label(root, text="Ключ для шифрации (e, n):").pack(anchor="w", padx=10)
txt_pub = tk.Entry(root, width=70)
txt_pub.insert(0, f"({e}, {n})")
txt_pub.pack(padx=10, pady=5)

tk.Label(root, text="Ключ для дешифрации (d, n):").pack(anchor="w", padx=10)
txt_priv = tk.Entry(root, width=70)
txt_priv.insert(0, f"({d}, {n})")
txt_priv.pack(padx=10, pady=5)

tk.Label(root, text="Результат:").pack(anchor="w", padx=10)
txt_output = tk.Text(root, height=4, width=70)
txt_output.pack(padx=10, pady=5)

def on_encrypt():
    try:
        text = txt_input.get("1.0", "end").strip()
        c, length = encrypt_text(text)
        txt_output.delete("1.0", "end")
        txt_output.insert("1.0", f"{c}:{length}")
    except Exception as ex:
        messagebox.showerror("Ошибка шифрования", str(ex))


def on_decrypt():
    try:
        data = txt_input.get("1.0", "end").strip()
        c_str, length_str = data.split(":")
        text = decrypt_text(int(c_str), int(length_str))
        txt_output.delete("1.0", "end")
        txt_output.insert("1.0", text)
    except Exception as ex:
        messagebox.showerror("Ошибка дешифрования", str(ex))

tk.Button(root, text="Шифровать", width=15, command=on_encrypt).pack(side="left", padx=10, pady=10)
tk.Button(root, text="Расшифровать", width=15, command=on_decrypt).pack(side="left", padx=10, pady=10)

root.mainloop()