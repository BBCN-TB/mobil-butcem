import flet as ft
import os

def main(page: ft.Page):
    # --- 1. SAYFA AYARLARI (Masaüstünde Telefon Görünümü İçin) ---
    page.title = "Cüzdanım 2026"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = "#262626"  # Bilgisayarda açınca arka plan koyu olsun
    page.padding = 0

    # --- 2. VERİLER ---
    guncel_brut = 80622.0
    zam_orani = 0.1860
    maas_geliri = 79000.0
    gumus_geliri = 12000.0
    kartlar = {"H": 2795, "V": 15700, "Y": 10370, "Q": 3123, "G": 23700}
    harc_ucreti = 52000.0

    # --- 3. YARDIMCI GÖRÜNÜM PARÇALARI ---
    
    # Listeler için özel satır tasarımı (Kaymayı önler)
    def satir_olustur(ikon, baslik, tutar, renk="black"):
        return ft.Container(
            padding=10,
            bgcolor="white",
            border_radius=10,
            margin=ft.margin.only(bottom=5),
            content=ft.Row([
                ft.Row([
                    ft.Icon(ikon, color=renk),
                    ft.Text(baslik, size=14, weight="bold", color="#333333"),
                ]),
                ft.Text(f"₺ {tutar:,.0f}", size=14, weight="bold", color=renk)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )

    # --- 4. EKRANLAR (VIEWS) ---
    
    def get_ozet_view():
        toplam_gelir = maas_geliri + gumus_geliri
        toplam_borc = sum(kartlar.values()) + harc_ucreti
        kalan = toplam_gelir - toplam_borc
        
        return ft.Column([
            ft.Text("Ocak 2026 Durumu", size=22, weight="bold", color="black"),
            ft.Container(height=10),
            # Mavi Kart
            ft.Container(
                bgcolor="#2196F3", # Mavi
                padding=20,
                border_radius=20,
                content=ft.Column([
                    ft.Text("Toplam Gelir", color="white70", size=12),
                    ft.Text(f"₺ {toplam_gelir:,.0f}", size=32, weight="bold", color="white"),
                    ft.Divider(color="white24"),
                    ft.Row([
                        ft.Column([
                            ft.Text("Giderler", color="white70", size=12),
                            ft.Text(f"- ₺ {toplam_borc:,.0f}", color="white", weight="bold"),
                        ]),
                        ft.Column([
                            ft.Text("Kalan", color="white70", size=12),
                            ft.Text(f"₺ {kalan:,.0f}", color="#C6FF00" if kalan > 0 else "#FF5252", weight="bold"),
                        ], alignment=ft.MainAxisAlignment.END),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ])
            ),
            ft.Container(height=20),
            ft.Text("Ödemeler", size=16, weight="bold", color="grey"),
            satir_olustur("school", "Harç Ödemesi", harc_ucreti, "red"),
            satir_olustur("credit_card", "Kart Borçları", sum(kartlar.values()), "orange"),
        ], scroll=ft.ScrollMode.HIDDEN)

    def get_maas_view():
        yeni_brut = guncel_brut * (1 + zam_orani)
        return ft.Column([
            ft.Text("Gelir Analizi", size=22, weight="bold", color="black"),
            ft.Container(height=10),
            ft.Container(
                padding=15, bgcolor="white", border_radius=15,
                content=ft.Column([
                    ft.Text("Kamu Personeli Maaş", weight="bold"),
                    ft.Divider(),
                    ft.Row([ft.Text("Mevcut Brüt:"), ft.Text(f"₺ {guncel_brut:,.0f}")] , alignment="spaceBetween"),
                    ft.Row([ft.Text("Zam Oranı:"), ft.Text(f"% {zam_orani*100:.1f}")], alignment="spaceBetween"),
                    ft.Divider(),
                    ft.Row([ft.Text("Yeni Brüt:", color="green"), ft.Text(f"₺ {yeni_brut:,.0f}", color="green", weight="bold")], alignment="spaceBetween"),
                ])
            ),
            ft.Container(height=10),
            satir_olustur("star", "Gümüş Yatırımı", gumus_geliri, "#FBC02D")
        ])

    def get_borc_view():
        liste = [ft.Text("Borç Detayları", size=22, weight="bold", color="black"), ft.Container(height=10)]
        for k, v in kartlar.items():
            liste.append(satir_olustur("credit_card", f"{k} Kartı", v, "#D32F2F"))
        return ft.Column(liste, scroll=ft.ScrollMode.HIDDEN)

    # --- 5. MENÜ VE ÇERÇEVE YÖNETİMİ ---

    icerik_kutusu = ft.Container(content=get_ozet_view(), expand=True, padding=20)

    # HATA VERMEYEN GÜVENLİ MENÜ BUTONU
    def menubutton(ikon, text, index):
        return ft.Container(
            content=ft.Column([
                ft.Icon(ikon, color="#2196F3"),
                ft.Text(text, size=10, color="#2196F3")
            ], spacing=2, alignment=ft.MainAxisAlignment.CENTER),
            padding=10,
            on_click=lambda e: sayfa_degis(index),
            ink=True # Tıklama efekti
        )

    def sayfa_degis(index):
        if index == 0: icerik_kutusu.content = get_ozet_view()
        elif index == 1: icerik_kutusu.content = get_maas_view()
        elif index == 2: icerik_kutusu.content = get_borc_view()
        page.update()

    # --- 6. SANAL TELEFON ÇERÇEVESİ (EN ÖNEMLİ KISIM) ---
    telefon_cercevesi = ft.Container(
        width=390,  # iPhone Genişliği
        height=844, # iPhone Yüksekliği
        bgcolor="#f2f2f7", # iOS Gri Arka Plan
        border_radius=35,  # Telefon köşeleri
        clip_behavior=ft.ClipBehavior.HARD_EDGE, # Taşanları kes
        alignment=ft.alignment.center,
        content=ft.Column([
            # Üst Boşluk (Çentik Payı)
            ft.Container(height=40, width=390, bgcolor="#f2f2f7"),
            
            # Değişen İçerik Alanı
            icerik_kutusu,
            
            # Alt Menü Çubuğu
            ft.Container(
                bgcolor="white",
                height=80,
                padding=ft.padding.only(bottom=20),
                content=ft.Row([
                    menubutton("home", "Özet", 0),
                    menubutton("trending_up", "Gelir", 1),
                    menubutton("credit_card", "Borçlar", 2),
                ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)
            )
        ], spacing=0)
    )

    page.add(telefon_cercevesi)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")
