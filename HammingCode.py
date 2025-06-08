import tkinter as tk
from tkinter import scrolledtext, messagebox
import random

# --- Hamming Kodlama Fonksiyonu ---
def hamming_kodu_olustur(veri):
    bitler = [int(b) for b in veri]
    uzunluk = len(veri)

    if uzunluk == 8:
        p1 = bitler[0] ^ bitler[1] ^ bitler[3] ^ bitler[4] ^ bitler[6]
        p2 = bitler[0] ^ bitler[2] ^ bitler[3] ^ bitler[5] ^ bitler[6]
        p4 = bitler[1] ^ bitler[2] ^ bitler[3] ^ bitler[7]
        p8 = bitler[4] ^ bitler[5] ^ bitler[6] ^ bitler[7]
        return f"{p1}{p2}{bitler[0]}{p4}{bitler[1]}{bitler[2]}{bitler[3]}{p8}{bitler[4]}{bitler[5]}{bitler[6]}{bitler[7]}"
    
    elif uzunluk == 16:
        ham_kod = [0] * 21
        data_positions = [2,4,5,6,8,9,10,12,13,14,16,17,18,19,20]
        for i, pos in enumerate(data_positions):
            ham_kod[pos] = bitler[i]
        ham_kod[0]  = ham_kod[2] ^ ham_kod[4] ^ ham_kod[6] ^ ham_kod[8] ^ ham_kod[10] ^ ham_kod[12] ^ ham_kod[14] ^ ham_kod[16] ^ ham_kod[18]
        ham_kod[1]  = ham_kod[2] ^ ham_kod[5] ^ ham_kod[6] ^ ham_kod[9] ^ ham_kod[10] ^ ham_kod[13] ^ ham_kod[14] ^ ham_kod[17] ^ ham_kod[18]
        ham_kod[3]  = ham_kod[4] ^ ham_kod[5] ^ ham_kod[6] ^ ham_kod[11] ^ ham_kod[12] ^ ham_kod[13] ^ ham_kod[14] ^ ham_kod[19] ^ ham_kod[20]
        ham_kod[7]  = ham_kod[8] ^ ham_kod[9] ^ ham_kod[10] ^ ham_kod[11] ^ ham_kod[12] ^ ham_kod[13] ^ ham_kod[14]
        ham_kod[15] = ham_kod[16] ^ ham_kod[17] ^ ham_kod[18] ^ ham_kod[19] ^ ham_kod[20]
        return ''.join(str(b) for b in ham_kod)

    elif uzunluk == 32:
        ham_kod = [0] * 38
        data_positions = [i for i in range(38) if i not in [0,1,3,7,15,31]]
        for i, pos in enumerate(data_positions):
            ham_kod[pos] = bitler[i]
        for p in [0,1,3,7,15,31]:
            kontrol = 0
            for i in range(1, 39):
                if i & (p + 1):
                    kontrol ^= ham_kod[i-1]
            ham_kod[p] = kontrol
        return ''.join(str(b) for b in ham_kod)

    else:
        return None

# --- Hata Düzeltme Fonksiyonu ---
def hata_duzelt(kod):
    bitler = [int(b) for b in kod]
    uzunluk = len(bitler)

    if uzunluk == 7:
        p1 = bitler[0] ^ bitler[2] ^ bitler[4] ^ bitler[6]
        p2 = bitler[1] ^ bitler[2] ^ bitler[5] ^ bitler[6]
        p4 = bitler[3] ^ bitler[4] ^ bitler[5] ^ bitler[6]
        pozisyon = p1 * 1 + p2 * 2 + p4 * 4

    elif uzunluk == 12:
        p1 = bitler[0] ^ bitler[2] ^ bitler[4] ^ bitler[6] ^ bitler[8] ^ bitler[10]
        p2 = bitler[1] ^ bitler[2] ^ bitler[5] ^ bitler[6] ^ bitler[9] ^ bitler[10]
        p4 = bitler[3] ^ bitler[4] ^ bitler[5] ^ bitler[6] ^ bitler[11]
        p8 = bitler[7] ^ bitler[8] ^ bitler[9] ^ bitler[10] ^ bitler[11]
        pozisyon = p1 * 1 + p2 * 2 + p4 * 4 + p8 * 8

    elif uzunluk == 21:
        p1 = bitler[0] ^ bitler[2] ^ bitler[4] ^ bitler[6] ^ bitler[8] ^ bitler[10] ^ bitler[12] ^ bitler[14] ^ bitler[16] ^ bitler[18]
        p2 = bitler[1] ^ bitler[2] ^ bitler[5] ^ bitler[6] ^ bitler[9] ^ bitler[10] ^ bitler[13] ^ bitler[14] ^ bitler[17] ^ bitler[18]
        p4 = bitler[3] ^ bitler[4] ^ bitler[5] ^ bitler[6] ^ bitler[11] ^ bitler[12] ^ bitler[13] ^ bitler[14] ^ bitler[19] ^ bitler[20]
        p8 = bitler[7] ^ bitler[8] ^ bitler[9] ^ bitler[10] ^ bitler[11] ^ bitler[12] ^ bitler[13] ^ bitler[14]
        p16 = bitler[15] ^ bitler[16] ^ bitler[17] ^ bitler[18] ^ bitler[19] ^ bitler[20]
        pozisyon = p1*1 + p2*2 + p4*4 + p8*8 + p16*16

    elif uzunluk == 38:
        pozisyon = 0
        for p in [0,1,3,7,15,31]:
            kontrol = 0
            for i in range(1, 39):
                if i & (p + 1):
                    kontrol ^= bitler[i-1]
            if kontrol:
                pozisyon += p + 1

    else:
        return kod, None

    if 0 < pozisyon <= len(bitler):
        bitler[pozisyon - 1] ^= 1

    return ''.join(str(b) for b in bitler), pozisyon

# --- Bit Görselleştirme ---
def hamming_kodu_gorsel_goster(canvas, kod, hatali_poz=None):
    canvas.delete("all")
    canvas.config(scrollregion=(0, 0, len(kod)*35 + 50, 60))
    x_start = 10
    for i, bit in enumerate(kod):
        renk = "lightblue"
        if i in [0,1,3,7,15,31]:
            renk = "lightgreen"
        if hatali_poz is not None and i == hatali_poz - 1:
            renk = "red"
        canvas.create_rectangle(x_start, 10, x_start+30, 40, fill=renk)
        canvas.create_text(x_start+15, 25, text=bit, font=("Consolas", 12))
        canvas.create_text(x_start+15, 50, text=str(i+1), font=("Arial", 8))
        x_start += 35

# --- GUI ---
pencere = tk.Tk()
pencere.title("Hamming SEC-DED Simülatörü")
pencere.geometry("1000x600")
pencere.configure(bg="#e8f0fe")

etiket = tk.Label(pencere, text="8, 16 veya 32 bitlik 0-1 verisi giriniz:", bg="#e8f0fe", font=("Arial", 12))
etiket.pack(pady=5)

veri_giris = tk.Entry(pencere, width=50, font=("Consolas", 14))
veri_giris.pack(pady=5)

buton_kutusu = tk.Frame(pencere, bg="#e8f0fe")
buton_kutusu.pack(pady=10)

tk.Button(buton_kutusu, text="Hamming Uygula", command=lambda: uygula_hamming(), bg="#4caf50", fg="white", font=("Arial", 12)).grid(row=0, column=0, padx=10)
tk.Button(buton_kutusu, text="Hata Oluştur", command=lambda: hata_olustur_gui(), bg="#f44336", fg="white", font=("Arial", 12)).grid(row=0, column=1, padx=10)
tk.Button(buton_kutusu, text="Düzelt", command=lambda: duzelt_gui(), bg="#2196f3", fg="white", font=("Arial", 12)).grid(row=0, column=2, padx=10)

sonuc_kutusu = scrolledtext.ScrolledText(pencere, width=100, height=6, font=("Consolas", 12), wrap=tk.WORD)
sonuc_kutusu.pack(pady=10)

canvas_frame = tk.Frame(pencere)
canvas_frame.pack(fill=tk.X, padx=10)

x_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

gorsel_canvas = tk.Canvas(canvas_frame, height=60, bg="white", xscrollcommand=x_scrollbar.set)
gorsel_canvas.pack(side=tk.TOP, fill=tk.X)

x_scrollbar.config(command=gorsel_canvas.xview)

son_hatali_kod = ""

def uygula_hamming():
    veri = veri_giris.get()
    if not veri.isdigit() or len(veri) not in [8, 16, 32]:
        messagebox.showerror("Hata", "Lütfen yalnızca 8, 16 veya 32 bitlik 0-1 verisi girin.")
        return
    kod = hamming_kodu_olustur(veri)
    if kod:
        sonuc_kutusu.delete(1.0, tk.END)
        sonuc_kutusu.insert(tk.END, f"Giriş Verisi:     {veri}\n")
        sonuc_kutusu.insert(tk.END, f"Hamming Kodu:     {kod}\n")
        hamming_kodu_gorsel_goster(gorsel_canvas, kod)

def hata_olustur_gui():
    global son_hatali_kod
    veri = veri_giris.get()
    kod = hamming_kodu_olustur(veri)
    if not kod:
        return
    liste_kod = list(kod)
    hata_index = random.randint(0, len(liste_kod) - 1)
    liste_kod[hata_index] = '0' if liste_kod[hata_index] == '1' else '1'
    hatali_kod = ''.join(liste_kod)
    son_hatali_kod = hatali_kod
    sonuc_kutusu.insert(tk.END, f"\nYapay Hatalı Kod: {hatali_kod}\n")
    sonuc_kutusu.insert(tk.END, f"Hatalı Bit Poz.:  {hata_index + 1}\n")
    hamming_kodu_gorsel_goster(gorsel_canvas, hatali_kod, hata_index + 1)

def duzelt_gui():
    global son_hatali_kod
    if not son_hatali_kod:
        messagebox.showwarning("Uyarı", "Önce bir hata oluşturmalısınız.")
        return
    duzeltilmis, pozisyon = hata_duzelt(son_hatali_kod)
    if pozisyon:
        sonuc_kutusu.insert(tk.END, f"Düzeltilmiş Kod:  {duzeltilmis}\n")
        sonuc_kutusu.insert(tk.END, f"Düzeltilen Bit:   {pozisyon}\n")
        hamming_kodu_gorsel_goster(gorsel_canvas, duzeltilmis)
    else:
        sonuc_kutusu.insert(tk.END, "Hata tespit edilemedi.\n")

pencere.mainloop()
