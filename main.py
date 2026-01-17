import flet as ft
import os

def main(page: ft.Page):
    # --- 1. AYARLAR ---
    page.title = "Cüzdan 2026"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#111111" 
    page.padding = 0
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    # --- 2. SABİT VERİLER (Başlangıç Durumu) ---
    maas = 79000
    gumus = 12000
    sabit_borclar = 52000 + 2795 + 15700 + 10370 + 3123 + 23700 # Harç + Kartlar
    
    # Değişkenler (Harcama eklendikçe değişecek)
    toplam_gelir = maas + gumus
    toplam_gider = sabit_borclar
    
    # --- 3. UI ELEMANLARI (Referanslar) ---
    # Bu elemanları burada tanımlıyoruz ki fonksiyonlar içinden erişebilelim
    txt_kalan = ft.Text(f"₺ {toplam_gelir - toplam_gider:,.0f}", size=36, weight="bold", color="white")
    txt_gider = ft.Text(f"- ₺ {toplam_gider:,.0f}", color="white", weight="bold")
    
    input_ad = ft.TextField(label="Harcama Adı", height=40, text_size=14, bgcolor="white", border_radius=10, expand=True)
    input_tutar = ft.TextField(label="Tutar", height=40, text_size=14, bgcolor="white", border_radius=10, width=100, keyboard_type=ft.KeyboardType.NUMBER)
    
    # Eklenen harcamaların listeleneceği kutu
    harcama_listesi = ft.Column(scroll=ft.ScrollMode.AUTO, height=200)

    # --- 4. FONKSİYONLAR ---
    
    def harcama_ekle(e):
        nonlocal toplam_gider # Dışarıdaki değişkeni güncellemek için
        
        # Boş giriş kontrolü
        if not input_ad.value or not input_tutar.value:
            return 
            
        try:
            tutar = float(input_tutar.value)
        except ValueError:
            return # Sayı girilmezse işlem yapma

        # 1. Gideri Artır
        toplam_gider += tutar
        
        # 2. Ekranı Güncelle (Rakamlar)
        kalan = toplam_gelir - toplam_gider
        txt_kalan.value = f"₺ {kalan:,.0f}"
        txt_kalan.color = "#76FF03" if kalan > 0 else "#FF1744" # Eksiye düşerse kırmızı olsun
        txt_gider.value = f"- ₺ {toplam_gider:,.0f}"

        # 3. Listeye Yeni Satır Ekle
        yeni_satir = ft.Container(
            padding=10, bgcolor="white", border_radius=8, margin=ft.margin.only(bottom=5),
            content=ft.Row([
                ft.Row([
                    ft.Icon(ft.icons.SHOPPING_BAG, size=16, color="grey"),
                    ft.Text(input_ad.value, weight="bold", color="black"),
                ]),
                ft.Text(f"-{tutar:.0f} TL", color="red", weight="bold")
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )
        harcama_listesi.controls.insert(0, yeni_satir) # En üste ekle

        # 4. Kutuları Temizle
        input_ad.value = ""
        input_tutar.value = ""
        
        page.update()

    # --- 5. SAYFA TASARIMLARI ---

    # Mavi Kart (Bakiye Göstergesi)
    bakiye_karti = ft.Container(
        padding=20, bgcolor="#2962FF", border_radius=20,
        content=ft.Column([
            ft.Text("Kalan Nakit", color="white70"),
            txt_kalan,
            ft.Divider(color="white24"),
            ft.Row([
                ft.Column([ft.Text("Gelir", color="white70", size=10), ft.Text(f"₺ {toplam_gelir:,.0f}", color="white", weight="bold")]),
                ft.Column([ft.Text("Gider", color="white70", size=10), txt_gider]),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ])
    )

    # Giriş Alanı (Yeni Harcama Ekleme)
    giris_alani = ft.Container(
        padding=10, bgcolor="#e3f2fd", border_radius=15,
        content=ft.Column([
            ft.Text("Hızlı Harcama Ekle", size=12, color="blue", weight="bold"),
            ft.Row([input_ad, input_tutar]),
            ft.ElevatedButton("Listeye Ekle", color="white", bgcolor="blue", width=300, on_click=harcama_ekle)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

    # Ana Sayfa Birleşimi
    ozet_view = ft.Column([
        ft.Text("OCAK 2026", size=24, weight="bold", color="black"),
        ft.Container(height=10),
        bakiye_karti,
        ft.Container(height=15),
        giris_alani,
        ft.Container(height=15),
        ft.Text("Son Hareketler", size=16, weight="bold", color="grey"),
        harcama_listesi
    ])

    # Diğer Sayfalar (Salt Okunur Bilgiler)
    gelir_view = ft.Column([
        ft.Text("GELİRLER", size=24, weight="bold", color="black"),
        ft.Container(height=20),
        ft.ListTile(leading=ft.Icon(ft.icons.MONEY), title=ft.Text("Maaş"), trailing=ft.Text(f"{maas} TL")),
        ft.ListTile(leading=ft.Icon(ft.icons.STAR), title=ft.Text("Gümüş"), trailing=ft.Text(f"{gumus} TL")),
    ])

    borc_view = ft.Column([
        ft.Text("SABİT BORÇLAR", size=24, weight="bold", color="black"),
        ft.Container(height=20),
        ft.ListTile(leading=ft.Icon(ft.icons.SCHOOL, color="red"), title=ft.Text("Harç"), trailing=ft.Text("52.000 TL")),
        ft.ListTile(leading=ft.Icon(ft.icons.CREDIT_CARD, color="red"), title=ft.Text("Kartlar Toplam"), trailing=ft.Text(f"{sabit_borclar-52000} TL")),
    ])

    # --- 6. ÇERÇEVE VE MENÜ ---
    
    icerik_kutusu = ft.Container(content=ozet_view, expand=True, padding=20)

    def sayfa_degis(e, hedef):
        if hedef == "ozet": icerik_kutusu.content = ozet_view
        if hedef == "gelir": icerik_kutusu.content = gelir_view
        if hedef == "borc": icerik_kutusu.content = borc_view
        page.update()

    telefon = ft.Container(
        width=390, height=844, bgcolor="#f2f2f7", border_radius=30,
        alignment=ft.Alignment(0,0), clip_behavior=ft.ClipBehavior.HARD_EDGE,
        content=ft.Column([
            ft.Container(height=40),
            icerik_kutusu,
            ft.NavigationBar(
                selected_index=0,
                on_change=lambda e: sayfa_degis(e, "ozet" if e.control.selected_index==0 else ("gelir" if e.control.selected_index==1 else "borc")),
                destinations=[
                    ft.NavigationDestination(icon=ft.icons.HOME, label="Özet"),
                    ft.NavigationDestination(icon=ft.icons.TRENDING_UP, label="Gelir"),
                    ft.NavigationDestination(icon=ft.icons.Money_OFF, label="Borç"),
                ]
            )
        ])
    )
    
    page.add(telefon)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")
