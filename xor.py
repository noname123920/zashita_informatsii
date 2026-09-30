import tkinter as tk
from tkinter import messagebox

def encrypt(text, key):
    result = []
    prev = 0
    for i, ch in enumerate(text):
        k = key[i % len(key)]
        c = ord(ch) ^ ord(k) ^ prev
        c = ((c << 3) | (c >> 29)) & 0xFFFFFFFF
        result.append(c)
        prev = c
    return result

def decrypt(codes, key):
    result = []
    prev = 0
    for i, c_enc in enumerate(codes):
        k = key[i % len(key)]
        c = ((c_enc >> 3) | (c_enc << 29)) & 0xFFFFFFFF
        m = c ^ ord(k) ^ prev
        result.append(chr(m))
        prev = c_enc
    return result

def on_encrypt():
    text = input_text.get("1.0", tk.END).rstrip("\n")
    key = key_encrypt.get()
    if not key:
        messagebox.showerror("Ошибка", "Введите ключ для шифрования")
        return
    if len(key) > 100:
        messagebox.showerror("Ошибка", "Ключ не должен быть длиннее 100 символов")
        return
    result = encrypt(text, key)
    dec_result = " ".join(str(n) for n in result)
    input_text.delete("1.0", tk.END)
    input_text.insert("1.0", dec_result)

def on_decrypt():
    text = input_text.get("1.0", tk.END).rstrip("\n")
    key = key_decrypt.get()
    if not key:
        messagebox.showerror("Ошибка", "Введите ключ для дешифрования")
        return
    if len(key) > 100:
        messagebox.showerror("Ошибка", "Ключ не должен быть длиннее 100 символов")
        return
    codes = [int(x) for x in text.split()]
    result = decrypt(codes, key)
    dec_result = "".join(result)
    input_text.delete("1.0", tk.END)
    input_text.insert("1.0", dec_result)

root = tk.Tk()

tk.Label(root, text="Текст (исходный / зашифрованный):").pack(anchor="w", padx=10, pady=(10, 0))

input_text = tk.Text(root, height=7, font=("Consolas", 11))
input_text.pack(fill="both", expand=True, padx=10, pady=5)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Шифровать", command=on_encrypt).pack(side="left", padx=10)
tk.Button(btn_frame, text="Расшифровать", command=on_decrypt).pack(side="left", padx=10)

tk.Label(root, text="Ключ для шифрования:").pack(anchor="w", padx=10, pady=(10, 0))

key_encrypt = tk.Entry(root, font=("Consolas", 11))
key_encrypt.pack(fill="x", padx=10, pady=2)

tk.Label(root, text="Ключ для дешифрования:").pack(anchor="w", padx=10, pady=(10, 0))

key_decrypt = tk.Entry(root, font=("Consolas", 11))
key_decrypt.pack(fill="x", padx=10, pady=2)

root.mainloop()