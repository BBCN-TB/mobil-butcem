import flet as ft
import os

def main(page: ft.Page):
    # --- AYARLAR ---
    page.title = "Cüzdan 2026"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#111111" # Bilgisayar ekranı siyah olsun
    page.padding = 0
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    # --- VERİLER ---
    maas = 79000
    gumus = 12000
    borclar = 52000 + 2795 + 15700 + 10370 + 3123 + 23700
    gelir = maas + gumus
    kalan = gelir - borclar

    # --- İÇERİK PARÇALARI ---
    def kart_olustur(baslik, tutar, renk):
        return ft.Container(
            padding=15, bgcolor="white", border_radius=10, margin=ft.margin.only(bottom=5),
            content=ft.Row([
                ft.Text(baslik, color="black", weight="bold"),
                ft.Text(f"{tutar} TL", color=renk, weight="bold")
            ], alignment="spaceBetween")
        )

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
        kart_olustur("Toplam Gelir", gelir, "green"),
        kart_olustur("Toplam Gider", borclar, "red"),
    ])

    gelir_sayfasi = ft.Column([
        ft.Text("GELİRLER", size=30, weight="bold", color="black"),
        ft.Container(height=20),
        kart_olustur("Maaş", maas, "blue"),
        kart_olustur("Gümüş", gumus, "orange"),
        ft.Container(padding=10, content=ft.Text("Maaş zammı %18.60 olarak hesaplandı.", color="grey"))
    ])

    # --- ANA KUTU VE BUTONLAR ---
    icerik = ft.Container(content=ozet_sayfasi, expand=True, padding=20)

    def degis(e, sayfa):
        if sayfa == "ozet": icerik.content = ozet_sayfasi
        if sayfa == "gelir": icerik.content = gelir_sayfasi
        page.update()

    # TELEFON GÖRÜNÜMÜ
    telefon = ft.Container(
        width=390, height=844, bgcolor="#f2f2f7", border_radius=30,
        alignment=ft.alignment.center,
        content=ft.Column([
            ft.Container(height=40), # Çentik boşluğu
            icerik,
            ft.Container( # Basit Buton Menüsü
                bgcolor="white", height=80,
                content=ft.Row([
                    ft.ElevatedButton("Özet", on_click=lambda e: degis(e, "ozet")),
                    ft.ElevatedButton("Gelir", on_click=lambda e: degis(e, "gelir")),
                ], alignment="center")
            )
        ])
    )
    
    page.add(telefon)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")
