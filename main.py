import flet as ft
from datetime import datetime

def main(page: ft.Page):
    page.title = "Bütçem 2026"
    page.theme_mode = ft.ThemeMode.LIGHT
    # Mobil görünüm ayarları
    page.window_width = 400
    page.window_height = 800
    page.padding = 20
    
    # --- VERİ SAKLAMA ---
    # Uygulama açık kaldığı sürece verileri bu listede tutacağız
    transactions = []

    # --- KATEGORİ YAPISI ---
    categories_data = {
        "Gider": ["Kredi Kartı", "Kira", "Fatura", "Eğitim", "Mutfak", "Diğer"],
        "Gelir": ["Maaş", "Ek Gelir"],
        "Yatırım": ["Altın", "Döviz", "Borsa"]
    }

    # --- UI BİLEŞENLERİ ---
    
    # 1. Sayfa: Özet (Dashboard)
    summary_container = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    
    # 2. Sayfa: İşlem Ekleme Formu Elemanları
    type_dropdown = ft.Dropdown(
        label="İşlem Türü",
        options=[ft.dropdown.Option(k) for k in categories_data.keys()],
        on_change=lambda e: update_category_options(e.control.value),
        border_radius=10
    )
    
    category_dropdown = ft.Dropdown(label="Kategori", options=[], border_radius=10)
    amount_input = ft.TextField(label="Tutar (₺)", keyboard_type=ft.KeyboardType.NUMBER, border_radius=10)
    date_display = ft.Text(f"Tarih: {datetime.now().strftime('%d.%m.%Y')}", size=16, weight="bold")
    
    selected_date = datetime.now()

    # Tarih Seçici Fonksiyonu
    def on_date_change(e):
        nonlocal selected_date
        selected_date = e.control.value
        date_display.value = f"Tarih: {selected_date.strftime('%d.%m.%Y')}"
        page.update()

    date_picker = ft.DatePicker(
        on_change=on_date_change,
        first_date=datetime(2025, 1, 1),
        last_date=datetime(2030, 12, 31),
    )
    page.overlay.append(date_picker)

    # Tür seçilince kategorileri güncelleyen fonksiyon
    def update_category_options(t_type):
        category_dropdown.options = [ft.dropdown.Option(c) for c in categories_data[t_type]]
        category_dropdown.value = None
        page.update()

    # İşlem Kaydetme
    def save_transaction(e):
        if not amount_input.value or not type_dropdown.value or not category_dropdown.value:
            page.snack_bar = ft.SnackBar(ft.Text("Lütfen tüm alanları doldurun!"))
            page.snack_bar.open = True
            page.update()
            return
        
        new_transaction = {
            "id": datetime.now().timestamp(),
            "type": type_dropdown.value,
            "category": category_dropdown.value,
            "amount": float(amount_input.value),
            "date": selected_date.strftime("%d.%m.%Y")
        }
        transactions.append(new_transaction)
        
        # Formu sıfırla ve Özet'e dön
        amount_input.value = ""
        refresh_dashboard()
        page.navigation_bar.selected_index = 0
        switch_page(0)
        page.update()

    # İşlem Silme
    def delete_item(t_id):
        nonlocal transactions
        transactions = [t for t in transactions if t["id"] != t_id]
        refresh_dashboard()
        page.update()

    # Dashboard Yenileme
    def refresh_dashboard():
        summary_container.controls.clear()
        
        total_gelir = sum(t["amount"] for t in transactions if t["type"] == "Gelir")
        total_gider = sum(t["amount"] for t in transactions if t["type"] == "Gider")
        total_yatirim = sum(t["amount"] for t in transactions if t["type"] == "Yatırım")
        net_durum = total_gelir - total_gider
        
        # Mavi Özet Kartı
        summary_container.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("OCAK 2026", color="white", size=18, weight="bold"),
                    ft.Text("Kalan Nakit", color="white70"),
                    ft.Text(f"₺ {net_durum:,.2f}", size=32, color="white", weight="bold"),
                    ft.Row([
                        ft.Text(f"Gelir: ₺{total_gelir:,.0f}", color="white"),
                        ft.Text(f"Gider: ₺{total_gider:,.0f}", color="white"),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ]),
                bgcolor=ft.colors.BLUE_600,
                padding=20,
                border_radius=20,
                margin=ft.margin.only(bottom=20)
            )
        )
        
        summary_container.controls.append(ft.Text("Son Hareketler", size=20, weight="bold"))
        
        # İşlem Listesi
        for t in reversed(transactions):
            icon_color = ft.colors.GREEN if t["type"] == "Gelir" else ft.colors.RED if t["type"] == "Gider" else ft.colors.ORANGE
            summary_container.controls.append(
                ft.Card(
                    content=ft.ListTile(
                        leading=ft.Icon(ft.icons.PAYMENTS, color=icon_color),
                        title=ft.Text(f"{t['category']} - {t['amount']} ₺"),
                        subtitle=ft.Text(f"{t['date']} | {t['type']}"),
                        trailing=ft.IconButton(
                            icon=ft.icons.DELETE_OUTLINE,
                            icon_color=ft.colors.GREY_400,
                            on_click=lambda e, tid=t["id"]: delete_item(tid)
                        )
                    )
                )
            )

    # --- SAYFA YÖNETİMİ ---
    add_transaction_view = ft.Column([
        ft.Text("İşlem Ekle", size=28, weight="bold"),
        ft.Divider(),
        type_dropdown,
        category_dropdown,
        amount_input,
        ft.Container(
            content=ft.Row([
                ft.IconButton(icon=ft.icons.CALENDAR_MONTH, on_click=lambda _: date_picker.pick_date()),
                date_display
            ]),
            padding=10,
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=10
        ),
        ft.ElevatedButton(
            "KAYDET", 
            on_click=save_transaction, 
            width=400, 
            height=50,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
        )
    ], visible=False)

    def switch_page(index):
        summary_container.visible = (index == 0)
        add_transaction_view.visible = (index == 1)
        page.update()

    # Alt Navigasyon Çubuğu (Doğru İsimler Kullanıldı)
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.HOME_ROUNDED, label="Özet"),
            ft.NavigationDestination(icon=ft.icons.ADD_BOX_ROUNDED, label="İşlem Ekle"),
            ft.NavigationDestination(icon=ft.icons.ANALYTICS_ROUNDED, label="Rapor"),
        ],
        on_change=lambda e: switch_page(e.control.selected_index)
    )

    page.add(summary_container, add_transaction_view)
    refresh_dashboard()
    switch_page(0)

ft.app(target=main)
