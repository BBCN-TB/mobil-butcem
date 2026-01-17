import flet as ft
import os

def main(page: ft.Page):
    # --- AYARLAR ---
    page.title = "Cüzdan 2026"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#111111"  # Bilgisayar ekranı siyah
    page.padding = 0
    # Artık bu komutlar hata vermeyecek çünkü requirements.txt'yi güncelledik
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    # --- VERİLER ---
    maas = 79000
    gumus = 12000
    borclar = 52000 + 2795 + 15700 + 10370 + 3123 + 23700
    gelir = maas + gumus
    kalan = gelir - borclar

    # --- YARDIMCI FONKSİYON ---
    def kart_olustur(ikon, baslik, tutar, renk):
        return ft.Container(
            padding=15, bgcolor="white", border_radius=12, margin=ft.margin.only(bottom=8),
            content=ft.Row([
                ft.Row([
                    ft.Icon(ikon, color="black54"), # Artık ikonları rahatça kullanabiliriz
                    ft.Text(baslik, color="#333333", weight="bold"),
                ]),
                ft.Text(f"{tutar:,.0f} TL", color=renk, weight="bold")
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )

    # --- SAYFA İÇERİKLERİ ---
    
    # 1. ÖZET
    ozet_view = ft.Column([
        ft.Text("OCAK 2026", size=26, weight="bold", color="black"),
        ft.Container(height=10),
        ft.Container(
            padding=20, bgcolor="blue", border_radius=20,
            content=ft.Column([
                ft.Text("Kalan Nakit", color="white70"),
                ft.Text(f"₺ {kalan:,.0f}", size=36, weight="bold", color="white")
            ])
        ),
        ft.Container(height=20),
        kart_olustur(ft.icons.TRENDING_UP, "Toplam Gelir", gelir, "green"),
        kart_olustur(ft.icons.TRENDING_DOWN, "Toplam Gider", borclar, "red"),
    ])

    # 2. GELİR
    gelir_view = ft.Column([
        ft.Text("GELİRLER", size=26, weight="bold", color="black"),
        ft.Container(height=20),
        kart_olustur(ft.icons.MONEY, "Maaş", maas, "blue"),
        kart_olustur(ft.icons.STAR, "Gümüş", gumus, "orange"),
        ft.Container(padding=10, content=ft.Text("Not: Zam oranı %18.60", color="grey"))
    ])

    # 3. BORÇ
    borc_view = ft.Column([
        ft.Text("BORÇLAR", size=26, weight="bold", color="black"),
        ft.Container(height=20),
        kart_olustur(ft.icons.SCHOOL, "Harç", 52000, "red"),
        kart_olustur(ft.icons.CREDIT_CARD, "Kredi Kartları", borclar - 52000, "red"),
    ])

    # --- ANA YAPI ---
    icerik_kutusu = ft.Container(content=ozet_view, expand=True, padding=25)

    def sayfa_degis(e, hedef):
        if hedef == 0: icerik_kutusu.content = ozet_view
        if hedef == 1: icerik_kutusu.content = gelir_view
        if hedef == 2: icerik_kutusu.content = borc_view
        page.update()

    # SANAL TELEFON
    telefon = ft.Container(
        width=390, height=844, bgcolor="#f2f2f7", border_radius=35,
        alignment=ft.alignment.center, # requirements.txt güncellendiği için bu artık çalışır!
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        content=ft.Column([
            ft.Container(height=40), # Çentik
            icerik_kutusu,
            # ALT MENÜ
            ft.NavigationBar(
                selected_index=0,
                on_change=lambda e: sayfa_degis(e, e.control.selected_index),
                destinations=[
                    ft.NavigationDestination(icon=ft.icons.HOME, label="Özet"),
                    ft.NavigationDestination(icon=ft.icons.TRENDING_UP, label="Gelir"),
                    ft.NavigationDestination(icon=ft.icons.CREDIT_CARD, label="Borç"),
                ]
            )
        ])
    )
    
    page.add(telefon)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")
