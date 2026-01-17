import flet as ft
import os

def main(page: ft.Page):
    # --- 1. EKRAN AYARLARI (Bilgisayarda Telefon Gibi Görünsün) ---
    page.title = "Cüzdanım 2026"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = "#262626"  # Bilgisayar arka planı koyu gri
    page.padding = 0
    page.window_width = 390
    page.window_height = 844

    # --- 2. VERİLER ---
    guncel_brut = 80622.0
    zam_orani = 0.1860
    maas_geliri = 79000.0
    gumus_geliri = 12000.0
    kartlar = {"H": 2795, "V": 15700, "Y": 10370, "Q": 3123, "G": 23700}
    harc_ucreti = 52000.0

    # --- 3. YARDIMCI FONKSİYONLAR ---
    
    # Listeler için şık satır tasarımı
    def satir_olustur(ikon_adi, baslik, tutar, yazi_rengi="black"):
        return ft.Container(
            padding=15,
            bgcolor="white",
            border_radius=12,
            margin=ft.margin.only(bottom=8),
            content=ft.Row([
                ft.Row([
                    ft.Icon(name=ikon_adi, color="black54"),
                    ft.Text(baslik, size=14, weight="bold", color="#333333"),
                ]),
                ft.Text(f"₺ {tutar:,.0f}", size=14, weight="bold", color=yazi_rengi)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )

    # --- 4. EKRAN İÇERİKLERİ ---
    
    def get_ozet_view():
        toplam_gelir = maas_geliri + gumus_geliri
        toplam_borc = sum(kartlar.values()) + harc_ucreti
        kalan = toplam_gelir - toplam_borc
        
        return ft.Column([
            ft.Text("Ocak 2026 Durumu", size=24, weight="bold", color="black"),
            ft.Container(height=10),
            # Mavi Bilgi Kartı
            ft.Container(
                bgcolor="#2962FF", # Koyu Mavi
                padding=20,
                border_radius=20,
                content=ft.Column([
                    ft.Text("Toplam Gelir", color="white70", size=12),
                    ft.Text(f"₺ {toplam_gelir:,.0f}", size=34, weight="bold", color="white"),
                    ft.Divider(color="white24"),
                    ft.Row([
                        ft.Column([
                            ft.Text("Giderler", color="white70", size=12),
                            ft.Text(f"- ₺ {toplam_borc:,.0f}", color="white", weight="bold"),
                        ]),
                        ft.Column([
                            ft.Text("Kalan Nakit", color="white70", size=12),
                            ft.Text(f"₺ {kalan:,.0f}", color="#76FF03" if kalan > 0 else "#FF1744", weight="bold"),
                        ], alignment=ft.MainAxisAlignment.END),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ])
            ),
            ft.Container(height=25),
            ft.Text("Ödemeler", size=16, weight="bold", color="grey"),
            satir_olustur("school", "Harç Ödemesi", harc_ucreti, "red"),
            satir_olustur("credit_card", "Kart Borçları", sum(kartlar.values()), "red"),
        ], scroll=ft.ScrollMode.HIDDEN)

    def get_maas_view():
        yeni_brut = guncel_brut * (1 + zam_orani)
        return ft.Column([
            ft.Text("Gelir Analizi", size=24, weight="bold", color="black"),
            ft.Container(height=15),
            ft.Container(
                padding=20, bgcolor="white", border_radius=15,
                content=ft.Column([
                    ft.Text("Kamu Personeli Maaş", weight="bold", color="black"),
                    ft.Divider(),
                    ft.Row([ft.Text("Mevcut Brüt:", color="black"), ft.Text(f"₺ {guncel_brut:,.0f}", color="black")] , alignment="spaceBetween"),
                    ft.Row([ft.Text("Zam Oranı:", color="black"), ft.Text(f"% {zam_orani*100:.1f}", color="black")], alignment="spaceBetween"),
                    ft.Divider(),
                    ft.Row([ft.Text("Yeni Brüt:", color="green", weight="bold"), ft.Text(f"₺ {yeni_brut:,.0f}", color="green", weight="bold")], alignment="spaceBetween"),
                ])
            ),
            ft.Container(height=10),
            satir_olustur("star", "Gümüş Yatırımı", gumus_geliri, "#FBC02D")
        ])

    def get_borc_view():
        liste = [ft.Text("Borç Detayları", size=24, weight="bold", color="black"), ft.Container(height=15)]
        for k, v in kartlar.items():
            liste.append(satir_olustur("credit_card", f"{k} Kartı", v, "#D32F2F"))
        return ft.Column(liste, scroll=ft.ScrollMode.HIDDEN)

    # --- 5. ANA YAPI (MENÜ VE ÇERÇEVE) ---

    icerik_kutusu = ft.Container(content=get_ozet_view(), expand=True, padding=25)

    # ÖZEL BUTON YAPISI (Tab veya NavigationBar kullanmadık - Hata vermez)
    def menubutton(ikon_adi, yazi, index_no):
        return ft.Container(
            content=ft.Column([
                ft.Icon(name=ikon_adi, color="#2962FF", size=28),
                ft.Text(yazi, size=11, color="#2962FF")
            ], spacing=2, alignment=ft.MainAxisAlignment.CENTER),
            padding=10,
            on_click=lambda e: sayfa_degis(index_no), # Tıklama özelliği
            border_radius=10,
            ink=True # Dokunma efekti
        )

    def sayfa_degis(index):
        if index == 0: icerik_kutusu.content = get_ozet_view()
        elif index == 1: icerik_kutusu.content = get_maas_view()
        elif index == 2: icerik_kutusu.content = get_borc_view()
        page.update()

    # TELEFON ÇERÇEVESİ
    telefon_ekrani = ft.Container(
        width=390,
        height=844,
        bgcolor="#f2f2f7", # Telefonun içi (Açık Gri)
        border_radius=35,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        content=ft.Column([
            # Çentik Boşluğu
            ft.Container(height=40, width=390, bgcolor="#f2f2f7"),
            
            # İçerik Alanı
            icerik_kutusu,
            
            # Alt Menü Çubuğu
            ft.Container(
                bgcolor="white",
                height=85,
                padding=ft.padding.only(bottom=15, top=5),
                shadow=ft.BoxShadow(blur_radius=20, color="black12"),
                content=ft.Row([
                    menubutton("home", "Özet", 0),
                    menubutton("trending_up", "Gelir", 1),
                    menubutton("credit_card", "Borçlar", 2),
                ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)
            )
        ], spacing=0)
    )

    page.add(telefon_ekrani)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")
