import tkinter as tk
from tkinter import messagebox

IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17,  9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
] # Начальная перестановка (64 бита)

PC1 = [
    57, 49, 41, 33, 25, 17,  9,
     1, 58, 50, 42, 34, 26, 18,
    10,  2, 59, 51, 43, 35, 27,
    19, 11,  3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
     7, 62, 54, 46, 38, 30, 22,
    14,  6, 61, 53, 45, 37, 29,
    21, 13,  5, 28, 20, 12,  4
] # Сжатие ключа 64 -> 56 бит

SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1] # Сдвиги C и D по раундам

PC2 = [
    14, 17, 11, 24,  1,  5,
     3, 28, 15,  6, 21, 10,
    23, 19, 12,  4, 26,  8,
    16,  7, 27, 20, 13,  2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
] # Сжатие ключа 56 -> 48 бит

E = [
    32,  1,  2,  3,  4,  5,
     4,  5,  6,  7,  8,  9,
     8,  9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32,  1
] # Расширение R с 32 -> 48 бит

S_BOXES = [
    # S1
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    # S2
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    # S3
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    # S4
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    # S5
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    # S6
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    # S7
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    # S8
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
] # 8 S-боксов для замены 6 бит -> 4 бита

P = [
    16,  7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26,  5, 18, 31, 10,
     2,  8, 24, 14, 32, 27,  3,  9,
    19, 13, 30,  6, 22, 11,  4, 25
] # Перестановка после S-боксов

FP = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41,  9, 49, 17, 57, 25
]

def permute(bits, table):
    result = []
    for i in table:
        result.append(bits[i - 1])
    return result


def left_shift(bits, n):
    n = n % len(bits)
    return bits[n:] + bits[:n]

def des_encrypt_block(text_bytes, key_bytes):
    """Шифрует один блок 8 байт. Возвращает hex-строку 16 символов."""
    # Дополняем до 8 байт
    data = b'\x00' * (8 - len(text_bytes)) + text_bytes
    key = b'\x00' * (8 - len(key_bytes)) + key_bytes

    # Превращаем в биты
    data_bits = []
    for byte in data:
        data_bits.extend([int(b) for b in format(byte, '08b')])

    key_bits = []
    for byte in key:
        key_bits.extend([int(b) for b in format(byte, '08b')])

    # Начальная перестановка
    data_after_ip = permute(data_bits, IP)

    # Готовим ключи раундов
    key_pc1 = permute(key_bits, PC1)
    C = key_pc1[:28]
    D = key_pc1[28:]

    keys = []
    for round_num in range(16):
        shift = SHIFTS[round_num]
        C = left_shift(C, shift)
        D = left_shift(D, shift)
        CD = C + D
        K = permute(CD, PC2)
        keys.append(K)

    # 16 раундов
    L = data_after_ip[:32]
    R = data_after_ip[32:]

    for round_num in range(16):
        K = keys[round_num]

        R_expanded = permute(R, E)
        xor_result = [a ^ b for a, b in zip(R_expanded, K)]
        bits_48 = ''.join(str(b) for b in xor_result)

        s_output = []
        for i in range(0, 48, 6):
            group = bits_48[i:i+6]
            box_num = i // 6 + 1
            row = int(group[0] + group[5], 2)
            col = int(group[1:5], 2)
            value = S_BOXES[box_num - 1][row][col]
            s_output.append(value)

        s_output_str = ''.join(format(v, '04b') for v in s_output)
        s_output_bits = [int(b) for b in s_output_str]
        f_result = permute(s_output_bits, P)

        R_new = [a ^ b for a, b in zip(L, f_result)]
        L, R = R, R_new

    # Финальная перестановка
    final_block = R + L
    encrypted_bits = permute(final_block, FP)

    # Превращаем в hex
    encrypted_str = ''.join(str(b) for b in encrypted_bits)
    encrypted_hex = ''
    for i in range(0, 64, 4):
        nibble = encrypted_str[i:i+4]
        encrypted_hex += format(int(nibble, 2), 'x')

    return encrypted_hex

def des_decrypt_block(hex_text, key_bytes):
    """Расшифровывает один блок. Возвращает байты."""
    key = b'\x00' * (8 - len(key_bytes)) + key_bytes

    # Превращаем hex в биты
    enc_bits = []
    for c in hex_text:
        enc_bits.extend([int(b) for b in format(int(c, 16), '04b')])

    # Ключ
    key_bits = []
    for byte in key:
        key_bits.extend([int(b) for b in format(byte, '08b')])

    key_pc1 = permute(key_bits, PC1)
    C = key_pc1[:28]
    D = key_pc1[28:]

    keys = []
    for round_num in range(16):
        shift = SHIFTS[round_num]
        C = left_shift(C, shift)
        D = left_shift(D, shift)
        CD = C + D
        K = permute(CD, PC2)
        keys.append(K)

    # Начальная перестановка
    data_after_ip = permute(enc_bits, IP)

    L = data_after_ip[:32]
    R = data_after_ip[32:]

    # 16 раундов с ключами в обратном порядке
    for round_num in range(16):
        K = keys[15 - round_num]

        R_expanded = permute(R, E)
        xor_result = [a ^ b for a, b in zip(R_expanded, K)]
        bits_48 = ''.join(str(b) for b in xor_result)

        s_output = []
        for i in range(0, 48, 6):
            group = bits_48[i:i+6]
            box_num = i // 6 + 1
            row = int(group[0] + group[5], 2)
            col = int(group[1:5], 2)
            value = S_BOXES[box_num - 1][row][col]
            s_output.append(value)

        s_output_str = ''.join(format(v, '04b') for v in s_output)
        s_output_bits = [int(b) for b in s_output_str]
        f_result = permute(s_output_bits, P)

        R_new = [a ^ b for a, b in zip(L, f_result)]
        L, R = R, R_new

    # Финальная перестановка
    final_block = R + L
    decrypted_bits = permute(final_block, FP)

    # Превращаем в байты
    dec_str = ''.join(str(b) for b in decrypted_bits)
    decrypted_bytes = []
    for i in range(0, 64, 8):
        byte = int(dec_str[i:i+8], 2)
        decrypted_bytes.append(byte)

    return bytes(decrypted_bytes)

def on_encrypt():
    text = input_text.get("1.0", tk.END).rstrip("\n")
    key = key_encrypt.get()
    
    if not text:
        messagebox.showerror("Ошибка", "Введите текст")
        return
    if not key:
        messagebox.showerror("Ошибка", "Введите ключ для шифрования")
        return
    if len(key) > 100:
        messagebox.showerror("Ошибка", "Ключ не длиннее 100 символов")
        return
    
    # Кодируем текст и ключ в байты cp1251
    text_bytes = text.encode("cp1251")
    key_bytes = key.encode("cp1251")
    
    # Разбиваем текст на блоки по 8 байт
    blocks = []
    for i in range(0, len(text_bytes), 8):
        block = text_bytes[i:i+8]
        blocks.append(block)
    
    # Шифруем каждый блок
    result = ""
    for block in blocks:
        result += des_encrypt_block(block, key_bytes)
    
    # Выводим в поле
    input_text.delete("1.0", tk.END)
    input_text.insert("1.0", result)

def on_decrypt():
    text = input_text.get("1.0", tk.END).rstrip("\n")
    key = key_decrypt.get()
    
    if not text:
        messagebox.showerror("Ошибка", "Введите зашифрованный текст")
        return
    if not key:
        messagebox.showerror("Ошибка", "Введите ключ для дешифрования")
        return
    if len(key) > 100:
        messagebox.showerror("Ошибка", "Ключ не длиннее 100 символов")
        return
    
    # Кодируем ключ в байты
    key_bytes = key.encode("cp1251")
    
    # Разбиваем hex на блоки по 16 символов (8 байт = 16 hex)
    blocks = []
    for i in range(0, len(text), 16):
        block = text[i:i+16]
        blocks.append(block)
    
    # Расшифровываем каждый блок
    result_bytes = b""
    for block in blocks:
        decrypted = des_decrypt_block(block, key_bytes)
        result_bytes += decrypted
    
    # Убираем нулевые байты спереди
    result_bytes = result_bytes.lstrip(b'\x00')
    
    # Превращаем в строку
    try:
        result = result_bytes.decode("cp1251")
    except:
        result = "(ошибка декодирования)"
    
    # Выводим в поле
    input_text.delete("1.0", tk.END)
    input_text.insert("1.0", result)

root = tk.Tk()
root.title("DES")
root.geometry("600x600")

tk.Label(root, text="Текст:").pack(anchor="w", padx=10, pady=(10, 0))

input_text = tk.Text(root, height=5, font=("Consolas", 11))
input_text.pack(fill="x", padx=10, pady=5)

tk.Label(root, text="Ключ для шифрования:").pack(anchor="w", padx=10, pady=(10, 0))

key_encrypt = tk.Entry(root, font=("Consolas", 11))
key_encrypt.pack(fill="x", padx=10, pady=5)

tk.Label(root, text="Ключ для дешифрования:").pack(anchor="w", padx=10, pady=(10, 0))

key_decrypt = tk.Entry(root, font=("Consolas", 11))
key_decrypt.pack(fill="x", padx=10, pady=5)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Шифровать", width=15, command=on_encrypt).pack(side="left", padx=10)
tk.Button(btn_frame, text="Расшифровать", width=15, command=on_decrypt).pack(side="left", padx=10)

root.mainloop()