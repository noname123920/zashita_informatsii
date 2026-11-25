import subprocess
import platform
import getpass
import sys


LICENSE_HASH = "8E2E233B"


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
    current = get_hash(get_system_info())
    if current == LICENSE_HASH:
        print("Лицензия действительна. Программа работает.")
    else:
        print("НЕЛЕГАЛЬНОЕ ИСПОЛЬЗОВАНИЕ! Программа заблокирована.")
        sys.exit(1)


if __name__ == "__main__":
    main()