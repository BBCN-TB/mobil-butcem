import flet as ft
import os

def main(page: ft.Page):
    page.title = "Akıllı Bütçe Yönetimi"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#f2f2f7"

    # --- VERİLER ---
    guncel_brut = 80622.0  #
    zam_orani = 0.1860      #
    maas_geliri = 79000.0   #
    gumus_geliri = 12000.0  #
    
    # Kredi Kartları ve Harç Borcu
    kartlar = {"H": 2795, "V": 15700, "Y": 10370, "Q": 3123, "G": 23700}
    harc_ucreti = 52000.0   #

    # --- FONKSİYONLAR ---
    def ozet_view():
        toplam_borc = sum(kartlar.values()) + harc_ucreti
        return ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Text("Toplam Aylık Gelir", color="white70"),
                    ft.Text(f"₺ {maas_geliri + gumus_geliri:,.2f}", size=30, weight="bold", color="white"),
                ]),
                bgcolor="blue", padding=20, border_radius=15
            ),
            ft.Text("Kritik Borç Bilgisi", size=18, weight="bold"),
            ft.ListTile(leading=ft.Icon("school"), title=ft.Text("Harç Ücreti"), trailing=ft.Text(f"₺ {harc_ucreti:,.0f}")),
            ft.ListTile(leading=ft.Icon("credit_card"), title=ft.Text("Toplam Kart Borcu"), trailing=ft.Text(f"₺ {sum(kartlar.values()):,.0f}"))
        ], scroll=ft.ScrollMode.AUTO)

    def gelir_view():
        # Kamu personeli Ocak ayı zamlı maaş hesabı
        # Yeni Brüt = 80.622 * 1.1860
        yeni_maas = guncel_brut * (1 + zam_orani)
        return ft.Column([
            ft.Text("Maaş Analizi (Ocak 2026)", size=20, weight="bold"),
            ft.Card(content=ft.Container(padding=15, content=ft.Column([
                ft.Text(f"Güncel Brüt: ₺ {guncel_brut:,.2f}"),
                ft.Text(f"Zam Oranı: % {zam_orani*100:.2f}"),
                ft.Divider(),
                ft.Text(f"Tahmini Yeni Brüt: ₺ {yeni_maas:,.2f}", weight="bold", color="green")
            ])))
        ])

    def borc_view():
        rows = []
        for kart, miktar in kartlar.items():
            rows.append(ft.ListTile(
                leading=ft.CircleAvatar(content=ft.Text(kart), bgcolor="orange"),
                title=ft.Text(f"{kart} Kredi Kartı"),
                trailing=ft.Text(f"₺ {miktar:,.2f}", weight="bold")
            ))
        return ft.Column([ft.Text("Kredi Kartı Detayları", size=20, weight="bold")] + rows)

    # Sekme Yönetimi
    content_area = ft.Container(content=ozet_view(), padding=10, expand=True)

    def tab_change(e):
        idx = e.control.selected_index
        if idx == 0: content_area.content = ozet_view()
        elif idx == 1: content_area.content = gelir_view()
        elif idx == 2: content_area.content = borc_view()
        page.update()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon="home", label="Özet"),
            ft.NavigationDestination(icon="trending_up", label="Gelir"),
            ft.NavigationDestination(icon="payments", label="Borçlar"),
        ],
        on_change=tab_change
    )

    page.add(
        ft.Container(content=ft.Text("Bütçe Yönetimi", size=22, weight="bold"), alignment=ft.Alignment(0, 0), padding=10),
        content_area
    )

# Render Port Ayarı
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")
