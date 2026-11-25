import subprocess
import platform
import getpass
import os
import sys


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


def get_hash(text: str) -> str:
    return f"{crc32(text.encode('utf-8')):08X}"


def get_system_info() -> str:
    if platform.system() == "Darwin":
        cmd = "ioreg -l | grep IOPlatformSerialNumber"
        raw = subprocess.check_output(cmd, shell=True)
        serial = raw.decode("utf-8").split("=")[-1].strip().strip('"')
    else:
        cmd = "wmic baseboard get serialnumber"
        raw = subprocess.check_output(cmd, shell=True)
        serial = raw.decode("utf-8").split("\n")[1].strip()

    arch = platform.machine()
    os_name = platform.system()
    os_ver = platform.release()
    host = platform.node()
    user = getpass.getuser()

    return f"{serial}|{arch}|{os_name}|{os_ver}|{host}|{user}"


def main():
    info = get_system_info()
    current = get_hash(info)

    if not os.path.exists("license.key"):
        with open("license.key", "w") as f:
            f.write(current)
        print("Установка завершена. Лицензия создана.")
        print("Хеш:", current)
        return

    with open("license.key") as f:
        saved = f.read().strip()

    if saved == current:
        print("Лицензия действительна. Программа работает.")
    else:
        print("НЕЛЕГАЛЬНОЕ ИСПОЛЬЗОВАНИЕ! Программа заблокирована.")
        sys.exit(1)


if __name__ == "__main__":
    main()