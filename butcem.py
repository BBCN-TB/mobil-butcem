import flet as ft
import os

def main(page: ft.Page):
    # --- SAYFA AYARLARI ---
    page.title = "Bütçe 2026"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#f2f2f7" # iOS Gri Arka Plan
    page.padding = 0
    page.spacing = 0

    # --- KİŞİSEL VERİLER (Ocak 2026) ---
    guncel_brut = 80622.0
    zam_orani = 0.1860
    
    # Gelirler
    maas_geliri = 79000.0
    gumus_geliri = 12000.0
    
    # Borçlar (H, V, Y, Q, G Kartları ve Harç)
    kartlar = {"H": 2795, "V": 15700, "Y": 10370, "Q": 3123, "G": 23700}
    harc_ucreti = 52000.0

    # --- GÖRÜNÜM 1: ÖZET EKRANI ---
    def get_ozet_view():
        toplam_gelir = maas_geliri + gumus_geliri
        toplam_borc = sum(kartlar.values()) + harc_ucreti
        kalan = toplam_gelir - toplam_borc

        return ft.Container(
            padding=20,
            content=ft.Column([
                ft.Container(height=20), # Üst boşluk
                ft.Text("Ocak 2026 Durumu", size=24, weight="bold", color="black"),
                
                # Mavi Kart (Net Durum)
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
                ft.Divider(height=30, color="transparent"),
                ft.Text("Hızlı Bakış", size=16, weight="bold", color="grey"),
                ft.ListTile(leading=ft.Icon("school", color="red"), title=ft.Text("Harç Ödemesi"), trailing=ft.Text(f"₺ {harc_ucreti:,.0f}")),
                ft.ListTile(leading=ft.Icon("credit_card", color="orange"), title=ft.Text("Kart Borçları"), trailing=ft.Text(f"₺ {sum(kartlar.values()):,.0f}")),
            ], scroll=ft.ScrollMode.AUTO)
        )

    # --- GÖRÜNÜM 2: MAAŞ HESAPLAMA ---
    def get_maas_view():
        yeni_brut = guncel_brut * (1 + zam_orani)
        return ft.Container(
            padding=20,
            content=ft.Column([
                ft.Container(height=20),
                ft.Text("Maaş Analizi", size=24, weight="bold", color="black"),
                ft.Card(
                    color="white",
                    elevation=5,
                    content=ft.Container(
                        padding=20,
                        content=ft.Column([
                            ft.Text("Kamu Personeli Maaş", weight="bold", size=16),
                            ft.Divider(),
                            ft.Row([ft.Text("Mevcut Brüt:"), ft.Text(f"₺ {guncel_brut:,.2f}")] , alignment="spaceBetween"),
                            ft.Row([ft.Text("Zam Oranı:"), ft.Text(f"% {zam_orani*100:.2f}")], alignment="spaceBetween"),
                            ft.Divider(),
                            ft.Row([ft.Text("Tahmini Yeni Brüt:", color="green", weight="bold"), ft.Text(f"₺ {yeni_brut:,.2f}", color="green", weight="bold")], alignment="spaceBetween"),
                        ])
                    )
                ),
                ft.Container(height=20),
                ft.Text("Ek Gelirler", size=16, weight="bold", color="grey"),
                ft.ListTile(leading=ft.Icon("star", color="yellow"), title=ft.Text("Gümüş Getirisi"), subtitle=ft.Text("Yatırım/Satış"), trailing=ft.Text(f"₺ {gumus_geliri:,.0f}")),
            ])
        )

    # --- GÖRÜNÜM 3: BORÇ DETAYLARI ---
    def get_borc_view():
        borc_listesi = []
        for kart, miktar in kartlar.items():
            borc_listesi.append(
                ft.ListTile(
                    leading=ft.CircleAvatar(content=ft.Text(kart), bgcolor="red"),
                    title=ft.Text(f"{kart} Kartı"),
                    trailing=ft.Text(f"₺ {miktar:,.0f}", weight="bold", color="red")
                )
            )
        
        return ft.Container(
            padding=20,
            content=ft.Column([
                ft.Container(height=20),
                ft.Text("Borç Detayları", size=24, weight="bold", color="black"),
                ft.Text("Kredi Kartları", size=16, weight="bold", color="grey"),
                ft.Column(borc_listesi),
                ft.Divider(),
                ft.ListTile(
                    leading=ft.Icon("warning", color="red"),
                    title=ft.Text("Harç Ücreti", weight="bold"),
                    subtitle=ft.Text("Tek seferlik ödeme"),
                    trailing=ft.Text(f"₺ {harc_ucreti:,.0f}", weight="bold", color="red")
                )
            ], scroll=ft.ScrollMode.AUTO)
        )

    # --- ANA YAPI VE MENÜ ---
    
    # İçeriğin değişeceği alan
    icerik_alani = ft.Container(content=get_ozet_view(), expand=True)

    def menuyu_degistir(e):
        secilen = e.control.selected_index
        if secilen == 0:
            icerik_alani.content = get_ozet_view()
        elif secilen == 1:
            icerik_alani.content = get_maas_view()
        elif secilen == 2:
            icerik_alani.content = get_borc_view()
        page.update()

    # Alt Menü (En güvenli yöntem)
    alt_menu = ft.NavigationBar(
        selected_index=0,
        on_change=menuyu_degistir,
        destinations=[
            ft.NavigationDestination(icon=ft.icons.HOME, label="Özet"),
            ft.NavigationDestination(icon=ft.icons.TRENDING_UP, label="Gelir"),
            ft.NavigationDestination(icon=ft.icons.CREDIT_CARD, label="Borçlar"),
        ]
    )

    page.add(icerik_alani, alt_menu)

# --- RENDER BAŞLATMA AYARI ---
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")
