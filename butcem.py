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
    
    kartlar = {"H": 2795, "V": 15700, "Y": 10370, "Q": 3123, "G": 23700} #
    harc_ucreti = 52000.0   #

    # --- GÖRÜNÜM MODÜLLERİ ---
    def ozet_view():
        return ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Text("Toplam Aylık Gelir", color="white70"),
                    ft.Text(f"₺ {maas_geliri + gumus_geliri:,.2f}", size=30, weight="bold", color="white"),
                ]),
                bgcolor="blue", padding=20, border_radius=15
            ),
            ft.Text("Önemli Ödemeler", size=18, weight="bold"),
            ft.ListTile(leading=ft.Icon("school"), title=ft.Text("Harç Ücreti"), trailing=ft.Text(f"₺ {harc_ucreti:,.0f}")),
            ft.ListTile(leading=ft.Icon("credit_card"), title=ft.Text("Kredi Kartları"), trailing=ft.Text(f"₺ {sum(kartlar.values()):,.0f}"))
        ], scroll=ft.ScrollMode.AUTO)

    def gelir_view():
        yeni_maas = guncel_brut * (1 + zam_orani)
        return ft.Column([
            ft.Text("Maaş Analizi (2026 Ocak)", size=20, weight="bold"),
            ft.Card(content=ft.Container(padding=15, content=ft.Column([
                ft.Text(f"Güncel Brüt: ₺ {guncel_brut:,.2f}"),
                ft.Text(f"Zam Oranı: % {zam_orani*100:.2f}"),
                ft.Divider(),
                ft.Text(f"Yeni Brüt Tahmini: ₺ {yeni_maas:,.2f}", weight="bold", color="green")
            ])))
        ])

    def borc_view():
        rows = [ft.ListTile(title=ft.Text(f"{k} Kartı Borcu"), trailing=ft.Text(f"₺ {v:,.0f}")) for k, v in kartlar.items()]
        return ft.Column([ft.Text("Kart Borç Detayları", size=20, weight="bold")] + rows)

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
            ft.NavigationDestination(icon="trending_up", label="Maaş"),
            ft.NavigationDestination(icon="payments", label="Borçlar"),
        ],
        on_change=tab_change
    )

    page.add(content_area)

# --- RENDER İÇİN PORT VE HOST AYARI ---
if __name__ == "__main__":
    # Render'ın verdiği portu kullan, yoksa 8080 kullan
    port = int(os.getenv("PORT", 8080)) 
    ft.app(
        target=main, 
        view=ft.AppView.WEB_BROWSER, 
        port=port, 
        host="0.0.0.0" # Bu satır dış erişim için zorunludur
    )
