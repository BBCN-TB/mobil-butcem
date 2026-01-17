import flet as ft
import os

def main(page: ft.Page):
    # --- 1. AYARLAR ---
    page.title = "Cüzdan 2026"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#111111" 
    page.padding = 0
    
    # HİZALAMA (Shortcuts kullanmadık, manuel yaptık)
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    # --- 2. VERİLER ---
    maas = 79000
    gumus = 12000
    borclar = 52000 + 2795 + 15700 + 10370 + 3123 + 23700
    gelir = maas + gumus
    kalan = gelir - borclar

    # --- 3. YARDIMCI FONKSİYONLAR ---
    
    # HATA ÇÖZÜMÜ BURADA:
    # 'name=' kelimesini sildik. Doğrudan 'ikon_kodu' gönderiyoruz.
    def kart_yap(baslik, tutar, renk):
        return ft.Container(
            padding=15, bgcolor="white", border_radius=10, margin=ft.margin.only(bottom=5),
            content=ft.Row([
                ft.Text(baslik, color="black", weight="bold"),
                ft.Text(f"{tutar} TL", color=renk, weight="bold")
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )

    # ÖZET SAYFASI
    ozet_sayfasi = ft.Column([
        ft.Text("OCAK 2026", size=30, weight="bold", color="black"),
        ft.Container(height=20),
        ft.Container(
            padding=20, bgcolor="blue", border_radius=15,
            content=ft.Column([
                ft.Text("Kalan Nakit", color="white"),
                ft.Text(f"{kalan} TL", size=40, weight="bold", color="white")
            ])
        ),
        ft.Container(height=20),
        kart_yap("Toplam Gelir", gelir, "green"),
        kart_yap("Toplam Gider", borclar, "red"),
    ])

    # GELİR SAYFASI
    gelir_sayfasi = ft.Column([
        ft.Text("GELİRLER", size=30, weight="bold", color="black"),
        ft.Container(height=20),
        kart_yap("Maaş", maas, "blue"),
        kart_yap("Gümüş", gumus, "orange"),
        ft.Container(height=10),
        ft.Text("Not: Zam oranı %18.60", color="grey")
    ])

    # BORÇ SAYFASI
    borc_sayfasi = ft.Column([
        ft.Text("BORÇLAR", size=30, weight="bold", color="black"),
        ft.Container(height=20),
        kart_yap("Harç", 52000, "red"),
        kart_yap("Kredi Kartları", borclar - 52000, "red"),
    ])

    # --- 4. ANA YAPI ---
    
    icerik_alani = ft.Container(content=ozet_sayfasi, expand=True, padding=20)

    def sayfa_degis(e, hedef):
        if hedef == "ozet": icerik_alani.content = ozet_sayfasi
        if hedef == "gelir": icerik_alani.content = gelir_sayfasi
        if hedef == "borc": icerik_alani.content = borc_sayfasi
        page.update()

    # SANAL TELEFON ÇERÇEVESİ
    telefon = ft.Container(
        width=390, height=844, 
        bgcolor="#f2f2f7", 
        border_radius=30,
        
        # HATA ÇÖZÜMÜ: 'alignment.center' YOK.
        alignment=ft.Alignment(0, 0),
        
        content=ft.Column([
            ft.Container(height=40), # Çentik
            icerik_alani,
            
            # ALT MENÜ (Basit Butonlar)
            ft.Container(
                bgcolor="white", height=80,
                content=ft.Row([
                    # HATA ÇÖZÜMÜ: Icon(name="home") yerine Icon("home")
                    ft.IconButton(icon="home", icon_color="blue", on_click=lambda e: sayfa_degis(e, "ozet")),
                    ft.IconButton(icon="trending_up", icon_color="blue", on_click=lambda e: sayfa_degis(e, "gelir")),
                    ft.IconButton(icon="credit_card", icon_color="blue", on_click=lambda e: sayfa_degis(e, "borc")),
                ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)
            )
        ])
    )
    
    page.add(telefon)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")
