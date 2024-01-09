import ctypes
import psutil

HEDEF_ADRES = "0087C2F4"
ISLEM_ADI = "mb_warband.exe"

def islem_id_al(procces_adi):
    for islem in psutil.process_iter(['pid', 'name']):
        if islem.info['name'] == procces_adi:
            return islem.info['pid']
    return None

def bellek_degeri_oku(islem_id, adress):
    process_handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, islem_id)
    buffer = ctypes.c_int()
    ctypes.windll.kernel32.ReadProcessMemory(process_handle, int(adress, 16), ctypes.byref(buffer), ctypes.sizeof(buffer), None)
    ctypes.windll.kernel32.CloseHandle(process_handle)
    return buffer.value

def bellek_degeri_yaz(islem_id, adress, yeni_deger):
    process_handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, islem_id)
    ctypes.windll.kernel32.WriteProcessMemory(process_handle, int(adress, 16), ctypes.byref(ctypes.c_int(yeni_deger)), 4, None)
    ctypes.windll.kernel32.CloseHandle(process_handle)

def main():
    while True:
        kullanici_girisi = input("Yeni değeri girin (0: 'Hile aktif', 1: 'Hile pasif', q: çıkış): ")
        
        if kullanici_girisi.lower() == "q":
            break
        
        if kullanici_girisi not in ["0", "1"]:
            print("Geçersiz giriş. 0 veya 1 girin.")
            continue

        yeni_deger = int(kullanici_girisi)
        yeni_deger_metin = "Aktif" if yeni_deger == 0 else "Pasif"
        
        islem_id = islem_id_al(ISLEM_ADI)
        
        if islem_id is not None:
            hedef_adress = HEDEF_ADRES

            eski_deger = bellek_degeri_oku(islem_id, hedef_adress)
            print("Eski Değer:", eski_deger)

            bellek_degeri_yaz(islem_id, hedef_adress, yeni_deger)
            print("Yeni Değer:", yeni_deger)
            print("Durum:", yeni_deger_metin)
        else:
            print("Hedef işlem bulunamadı.")

if __name__ == "__main__":
    main()
