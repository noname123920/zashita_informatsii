import tkinter as tk


def crc32(data: bytes) -> int:
    crc = 0xFFFFFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xEDB88320
            else:
                crc >>= 1
    return crc ^ 0xFFFFFFFF


def calculate():
    text = entry.get()
    if not text:
        result_label.config(text="Введите текст!")
        return
    h = crc32(text.encode('cp1251'))
    result_label.config(text=f"CRC-32: {h:08X}")


root = tk.Tk()
root.title("CRC-32")
root.geometry("400x200")

tk.Label(root, text="Введите текст:").pack(pady=5)
entry = tk.Entry(root, width=40)
entry.pack(pady=5)

tk.Button(root, text="Вычислить", command=calculate).pack(pady=10)

result_label = tk.Label(root, text="CRC-32: —", font=("Courier", 14))
result_label.pack(pady=10)

root.mainloop()