import flet as ft
import os

def main(page: ft.Page):
    # --- AYARLAR ---
    page.title = "Cüzdan 2026"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#111111" 
    page.padding = 0
    # ESKİ SÜRÜM UYUMLU HİZALAMA (Shortcuts yok)
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    # --- VERİLER ---
    guncel_brut = 80622.0
    zam_orani = 0.1860
    maas_geliri = 79000.0
    gumus_geliri = 12000.0
    kartlar = {"H": 2795, "V": 15700, "Y": 10370, "Q": 3123, "G": 23700}
    harc_ucreti = 52000.0

    # --- HESAPLAMALAR ---
    toplam_gelir = maas_geliri + gumus_geliri
    toplam_borc = sum(kartlar.values()) + harc_ucreti
    kalan = toplam_gelir - toplam_borc
    yeni_maas = guncel_brut * (1 + zam_orani)

    # --- İÇERİK PARÇALARI ---
    
    # 1. ÖZET SAYFASI
    ozet_icerik = ft.Column([
        ft.Text("OCAK 2026", size=24, weight="bold", color="black"),
        ft.Container(height=10),
        ft.Container(
            padding=20, bgcolor="blue", border_radius=15,
            content=ft.Column([
                ft.Text("Kalan Nakit", color="white"),
                ft.Text(f"{kalan:,.0f} TL", size=30, weight="bold", color="white")
            ])
        ),
        ft.Container(height=20),
        ft.Text("Gelirler: " + f"{toplam_gelir:,.0f} TL", color="green", weight="bold"),
        ft.Text("Giderler: " + f"{toplam_borc:,.0f} TL", color="red", weight="bold"),
    ])

    # 2. MAAŞ SAYFASI
    maas_icerik = ft.Column([
        ft.Text("MAAŞ ANALİZİ", size=24, weight="bold", color="black"),
        ft.Container(height=20),
        ft.Container(
            padding=15, bgcolor="white", border_radius=10,
            content=ft.Column([
                ft.Text(f"Eski Brüt: {guncel_brut}", color="black"),
                ft.Text(f"Zam Oranı: %18.60", color="black"),
                ft.Divider(),
                ft.Text(f"YENİ BRÜT: {yeni_maas:,.2f} TL", color="green", weight="bold"),
            ])
        )
    ])

    # 3. BORÇ SAYFASI
    borc_icerik = ft.Column([
        ft.Text("BORÇ LİSTESİ", size=24, weight="bold", color="black"),
        ft.Container(height=10),
        ft.Text(f"Harç: {harc_ucreti} TL", color="red"),
        ft.Text(f"Kredi Kartları: {sum(kartlar.values())} TL", color="red"),
    ])

    # --- ANA YAPI ---
    ekran_kutusu = ft.Container(content=ozet_icerik, padding=20, expand=True)

    def menu_tikla(e, sayfa_no):
        if sayfa_no == 1: ekran_kutusu.content = ozet_icerik
        if sayfa_no == 2: ekran_kutusu.content = maas_icerik
        if sayfa_no == 3: ekran_kutusu.content = borc_icerik
        page.update()

    # SANAL TELEFON (Koordinat sistemi ile ortalama - Hata vermez)
    telefon = ft.Container(
        width=390, height=844, bgcolor="#f2f2f7", border_radius=30,
        # İŞTE ÇÖZÜM: alignment.center YERİNE Alignment(0,0)
        alignment=ft.Alignment(0, 0), 
        content=ft.Column([
            ft.Container(height=40), # Çentik
            ekran_kutusu,
            # BASİT BUTON MENÜSÜ
            ft.Container(
                height=70, bgcolor="white",
                content=ft.Row([
                    ft.ElevatedButton("Özet", on_click=lambda e: menu_tikla(e, 1)),
                    ft.ElevatedButton("Maaş", on_click=lambda e: menu_tikla(e, 2)),
                    ft.ElevatedButton("Borç", on_click=lambda e: menu_tikla(e, 3)),
                ], alignment=ft.MainAxisAlignment.CENTER)
            )
        ])
    )

    page.add(telefon)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")
