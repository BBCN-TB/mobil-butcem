import flet as ft
from datetime import datetime

def main(page: ft.Page):
    page.title = "Bütçem Pro"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 400
    page.window_height = 800
    
    # --- VERİ YAPISI ---
    # Gerçek uygulamalarda bu bir veritabanından gelir. 
    # Şimdilik uygulama çalıştığı sürece hafızada tutulacak.
    transactions = []

    # --- KATEGORİ SÖZLÜĞÜ ---
    categories = {
        "Gider": ["Kredi Kartı", "Kira", "Fatura", "Eğitim", "Diğer", "Mutfak"],
        "Gelir": ["Maaş", "Ek Gelir"],
        "Yatırım": ["Altın", "Döviz", "Borsa"]
    }

    # --- UI BİLEŞENLERİ ---
    
    # 1. Sayfa: Özet (Dashboard)
    summary_view = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    
    # 2. Sayfa: İşlem Ekleme Formu
    type_dropdown = ft.Dropdown(
        label="İşlem Türü",
        options=[ft.dropdown.Option(k) for k in categories.keys()],
        on_change=lambda e: update_categories(e.control.value)
    )
    
    category_dropdown = ft.Dropdown(label="Kategori", options=[])
    amount_input = ft.TextField(label="Tutar (₺)", keyboard_type=ft.KeyboardType.NUMBER)
    date_text = ft.Text(f"Seçilen Tarih: {datetime.now().strftime('%d.%m.%Y')}")
    
    selected_date = datetime.now()

    def handle_date_change(e):
        nonlocal selected_date
        selected_date = e.control.value
        date_text.value = f"Seçilen Tarih: {selected_date.strftime('%d.%m.%Y')}"
        page.update()

    date_picker = ft.DatePicker(
        on_change=handle_date_change,
        first_date=datetime(2020, 1, 1),
        last_date=datetime(2030, 12, 31),
    )
    page.overlay.append(date_picker)

    def update_categories(t_type):
        category_dropdown.options = [ft.dropdown.Option(c) for c in categories[t_type]]
        category_dropdown.value = None
        page.update()

    def add_transaction(e):
        if not amount_input.value or not type_dropdown.value or not category_dropdown.value:
            return # Boş bırakılırsa ekleme yapma
        
        # Yeni işlemi listeye ekle
        new_item = {
            "id": datetime.now().timestamp(),
            "type": type_dropdown.value,
            "category": category_dropdown.value,
            "amount": float(amount_input.value),
            "date": selected_date.strftime("%d.%m.%Y")
        }
        transactions.append(new_item)
        
        # Formu temizle ve Özet sayfasına dön
        amount_input.value = ""
        refresh_summary()
        page.navigation_bar.selected_index = 0
        navigate(0)
        page.update()

    def delete_transaction(t_id):
        # ID'ye göre işlemi bul ve sil
        nonlocal transactions
        transactions = [t for t in transactions if t["id"] != t_id]
        refresh_summary()
        page.update()

    def refresh_summary():
        summary_view.controls.clear()
        
        # Toplam Hesaplama
        total_gelir = sum(t["amount"] for t in transactions if t["type"] == "Gelir")
        total_gider = sum(t["amount"] for t in transactions if t["type"] == "Gider")
        
        # Özet Kartı
        summary_view.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("KALAN NAKİT", color="white70"),
                    ft.Text(f"₺ {total_gelir - total_gider:,.0f}", size=30, color="white", weight="bold"),
                ]),
                bgcolor="blue", padding=20, border_radius=15
            )
        )
        
        # Liste Başlığı
        summary_view.controls.append(ft.Text("Son İşlemler", size=20, weight="bold"))
        
        # İşlem Listesi
        for t in reversed(transactions): # En yeniyi üstte göster
            summary_view.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.icons.PAYMENT, color="green" if t["type"] == "Gelir" else "red"),
                    title=ft.Text(f"{t['category']} - {t['amount']} ₺"),
                    subtitle=ft.Text(f"{t['date']} | {t['type']}"),
                    trailing=ft.IconButton(
                        icon=ft.icons.DELETE_OUTLINE, 
                        on_click=lambda e, tid=t["id"]: delete_transaction(tid)
                    )
                )
            )

    # --- NAVİGASYON MANTIĞI ---
    add_view = ft.Column([
        ft.Text("Yeni İşlem Ekle", size=24, weight="bold"),
        type_dropdown,
        category_dropdown,
        amount_input,
        ft.Row([
            ft.ElevatedButton("Tarih Seç", icon=ft.icons.CALENDAR_MONTH, on_click=lambda _: date_picker.pick_date()),
            date_text
        ]),
        ft.ElevatedButton("Kaydet", on_click=add_transaction, width=400, height=50)
    ], visible=False)

    def navigate(index):
        summary_view.visible = (index == 0)
        add_view.visible = (index == 1)
        page.update()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.DASHBOARD, label="Özet"),
            ft.NavigationBarDestination(icon=ft.icons.ADD_CIRCLE, label="Ekle"),
            ft.NavigationBarDestination(icon=ft.icons.PAYMENTS, label="Rapor"),
        ],
        on_change=lambda e: navigate(e.control.selected_index)
    )

    page.add(summary_view, add_view)
    refresh_summary()
    navigate(0)

ft.app(target=main)
