import flet as ft
import os

def main(page: ft.Page):
    # --- SAYFA AYARLARI ---
    page.title = "Bütçe 2026"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#f2f2f7"
    page.padding = 0
    page.spacing = 0

    # --- KİŞİSEL VERİLER ---
    guncel_brut = 80622.0
    zam_orani = 0.1860
    maas_geliri = 79000.0
    gumus_geliri = 12000.0
    kartlar = {"H": 2795, "V": 15700, "Y": 10370, "Q": 3123, "G": 23700}
    harc_ucreti = 52000.0

    # --- 1. ÖZET EKRANI ---
    def get_ozet_view():
        toplam_gelir = maas_geliri + gumus_geliri
        toplam_borc = sum(kartlar.values()) + harc_ucreti
        kalan = toplam_gelir - toplam_borc

        return ft.Column([
            ft.Container(height=10),
            ft.Text("Ocak 2026 Durumu", size=24, weight="bold", color="black"),
            ft.Container(
                bgcolor="blue",
                padding=20,
                border_radius=20,
                content=ft.Column([
                    ft.Text("Toplam Gelir", color="white70"),
                    ft.Text(f"₺ {toplam_gelir:,.0f}", size=28, weight="bold", color="white"),
                    ft.Divider(color="white24"),
                    ft.Row([
                        ft.Column([
                            ft.Text("Giderler", color="white70", size=12),
                            ft.Text(f"- ₺ {toplam_borc:,.0f}", color="white", weight="bold"),
                        ]),
                        ft.Column([
                            ft.Text("Kalan Nakit", color="white70", size=12),
                            ft.Text(f"₺ {kalan:,.0f}", color="orange" if kalan < 0 else "lightgreen", weight="bold"),
                        ], alignment=ft.MainAxisAlignment.END),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ])
            ),
            ft.Divider(color="transparent", height=20),
            ft.Text("Kritik Ödemeler", size=16, weight="bold", color="grey"),
            ft.ListTile(leading=ft.Icon("school", color="red"), title=ft.Text("Harç Ödemesi"), trailing=ft.Text(f"₺ {harc_ucreti:,.0f}")),
            ft.ListTile(leading=ft.Icon("credit_card", color="orange"), title=ft.Text("Kart Borçları"), trailing=ft.Text(f"₺ {sum(kartlar.values()):,.0f}")),
        ], scroll=ft.ScrollMode.AUTO)

    # --- 2. MAAŞ EKRANI ---
    def get_maas_view():
        yeni_brut = guncel_brut * (1 + zam_orani)
        return ft.Column([
            ft.Container(height=10),
            ft.Text("Maaş Analizi", size=24, weight="bold", color="black"),
            ft.Card(
                color="white",
                elevation=2,
                content=ft.Container(
                    padding=20,
                    content=ft.Column([
                        ft.Text("Kamu Personeli Maaş", weight="bold", size=16),
                        ft.Divider(),
                        ft.Row([ft.Text("Mevcut Brüt:"), ft.Text(f"₺ {guncel_brut:,.2f}")] , alignment="spaceBetween"),
                        ft.Row([ft.Text("Zam Oranı:"), ft.Text(f"% {zam_orani*100:.2f}")], alignment="spaceBetween"),
                        ft.Divider(),
                        ft.Row([ft.Text("Yeni Brüt:", color="green", weight="bold"), ft.Text(f"₺ {yeni_brut:,.2f}", color="green", weight="bold")], alignment="spaceBetween"),
                    ])
                )
            ),
            ft.ListTile(leading=ft.Icon("star", color="yellow"), title=ft.Text("Gümüş Getirisi"), trailing=ft.Text(f"₺ {gumus_geliri:,.0f}")),
        ])

    # --- 3. BORÇ EKRANI ---
    def get_borc_view():
        borc_listesi = []
        for kart, miktar in kartlar.items():
            borc_listesi.append(
                ft.ListTile(
                    leading=ft.CircleAvatar(content=ft.Text(kart), bgcolor="red", color="white"),
                    title=ft.Text(f"{kart} Kartı"),
                    trailing=ft.Text(f"₺ {miktar:,.0f}", weight="bold", color="red")
                )
            )
        return ft.Column([
            ft.Container(height=10),
            ft.Text("Borç Detayları", size=24, weight="bold", color="black"),
            ft.Column(borc_listesi),
        ], scroll=ft.ScrollMode.AUTO)

    # --- MENÜ SİSTEMİ (Hatasız Yöntem) ---
    icerik_alani = ft.Container(content=get_ozet_view(), padding=20, expand=True)

    def sayfa_degistir(e, sayfa_no):
        if sayfa_no == 0:
            icerik_alani.content = get_ozet_view()
        elif sayfa_no == 1:
            icerik_alani.content = get_maas_view()
        elif sayfa_no == 2:
            icerik_alani.content = get_borc_view()
        page.update()

    # Özel Alt Menü (Built-in NavigationBar yerine bunu kullanıyoruz)
    # Bu yöntem "AttributeError" verme ihtimalini ortadan kaldırır.
    ozel_alt_menu = ft.Container(
        bgcolor="white",
        padding=10,
        border_radius=ft.border_radius.only(top_left=20, top_right=20),
        shadow=ft.BoxShadow(blur_radius=10, color="grey"),
        content=ft.Row([
            ft.IconButton(icon="home", icon_size=30, icon_color="blue", on_click=lambda e: sayfa_degistir(e, 0)),
            ft.IconButton(icon="trending_up", icon_size=30, icon_color="blue", on_click=lambda e: sayfa_degistir(e, 1)),
            ft.IconButton(icon="credit_card", icon_size=30, icon_color="blue", on_click=lambda e: sayfa_degistir(e, 2)),
        ], alignment=ft.MainAxisAlignment.SPACE_AROUND)
    )

    page.add(
        ft.Column([
            icerik_alani,   # Üstte İçerik
            ozel_alt_menu   # Altta Menü
        ], expand=True)
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")
