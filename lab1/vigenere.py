import tkinter as tk

alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

def encrypt():
    text = entry_input.get().lower()
    key = entry_key.get().lower()

    result = ""
    key_index = 0
    for char in text:
        if char in alphabet:
            index = alphabet.index(char)
            shift = alphabet.index(key[key_index])
            new_index = (index + shift) % len(alphabet)
            result += alphabet[new_index]

            key_index = (key_index + 1) % len(key)
        else:
            result += char

    entry_output.delete(0, tk.END)
    entry_output.insert(0, result)

def decrypt():
    text = entry_cipher.get().lower()
    key = entry_key.get().lower()

    result = ""
    key_index = 0
    for char in text:
        if char in alphabet:
            index = alphabet.index(char)
            shift = alphabet.index(key[key_index])
            new_index = (index - shift) % len(alphabet)
            result += alphabet[new_index]

            key_index = (key_index + 1) % len(key)
        else:
            result += char

    entry_output.delete(0, tk.END)
    entry_output.insert(0, result)

root = tk.Tk()
root.title("Шифрование")
root.geometry("500x300")

tk.Label(root, text="Исходный текст:").pack(pady=5)
entry_input = tk.Entry(root, width=60)
entry_input.pack()

tk.Label(root, text="Ключ(сдвиг):").pack(pady=5)
entry_key = tk.Entry(root, width=60)
entry_key.pack()

tk.Label(root, text="Зашифрованный текст:").pack(pady=5)
entry_cipher = tk.Entry(root, width=60)
entry_cipher.pack()

tk.Label(root, text="Результат:").pack(pady=5)
entry_output = tk.Entry(root, width=60)
entry_output.pack()

frame = tk.Frame(root)
frame.pack(pady=15)

tk.Button(frame, text="Шифровать", command=encrypt).grid(row=0, column=0, padx=10)
tk.Button(frame, text="Расшифровать", command=decrypt).grid(row=0, column=1, padx=10)

root.mainloop()


