import psutil

HEDEF_ADRES = "0x0087C2F4"
ISLEM_ADI = "mb_warband"

def islem_id_al(procces_adi):
    for islem in psutil.process_iter(['pid', 'name']):
        if islem.info['name'] == procces_adi:
            return islem.info['pid']
    return None

def bellek_degeri_oku(islem_id, adress):
    try:
        with open(f"/proc/{islem_id}/mem", 'rb', 0) as f:
            f.seek(int(adress, 16))
            return int.from_bytes(f.read(4), byteorder='little')
    except Exception as e:
        print(f"Hata: {e}")
        return None

def bellek_degeri_yaz(islem_id, adress, yeni_deger):
    try:
        with open(f"/proc/{islem_id}/mem", 'wb', 0) as f:
            f.seek(int(adress, 16))
            f.write((yeni_deger).to_bytes(4, byteorder='little'))
    except Exception as e:
        print(f"Hata: {e}")

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
