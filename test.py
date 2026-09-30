def encrypt(text, key):
    prev = 0
    for i, ch in enumerate(text):
        k = key[i % len(key)]
        xor = ord(ch) ^ ord(k) ^ prev
        shifted = ((xor << 3) | (xor >> 29)) & 0xFFFFFFFF
        print(f"i={i} ch={ch} ord={ord(ch)} k={k} ord(k)={ord(k)} prev={prev} xor={xor} shifted={shifted}")
        prev = shifted


encrypt("ПРИВЕТ", "key")

# def decrypt(codes, key):
#     result = []
#     for i, c in enumerate(codes):
#         k = key[i % len(key)]
#         result.append(chr(c ^ ord(k)))
#     return result

# text = "ПРИВЕТ"
# key = "key"

# enc = encrypt(text, key)
# dec = decrypt(enc, key)

# print("Зашифровано:", enc)
# print("Расшифровано:", "".join(dec))
# print(type(dec))