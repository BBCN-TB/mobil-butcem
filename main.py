import flet as ft
from datetime import datetime
import json
import os

# Veri dosyası
DATA_FILE = "veriler.json"

def main(page: ft.Page):
    # Başlangıç Ayarları
    page.title = "Butcem 2026 - Versiyon 9"
    page.theme_mode = "light"
    page.window_width = 400
    page.window_height = 800
    page.spacing = 0
    page.padding = 0

    print("--- UYGULAMA BASLATILDI (V9) ---")

    # --- VERİ FONKSİYONLARI ---
    def load_data():
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except: return []
        return []

    def save_data_to_file():
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(transactions, f, ensure_ascii=False, indent=4)

    transactions = load_data()

    # --- KATEGORİLER ---
    cats = {
        "Gider": ["Kredi Kartı", "Kira", "Fatura", "Eğitim", "Mutfak", "Diğer"],
        "Gelir": ["Maaş", "Ek Gelir"],
        "Yatırım": ["Altın", "Döviz", "Borsa"]
    }

    # --- SAYFA YAPILARI (İçerik Alanları) ---
    summary_list = ft.Column(scroll="auto", expand=True, spacing=10)
    # Özet sayfası için ana kap
    summary_view = ft.Container(content=summary_list, expand=True)

    # Ekleme sayfası için ana kap
    add_form_elements = ft.Column(spacing=20)
    add_view = ft.Container(
        content=add_form_elements,
        visible=False,
        expand=True,
        padding=20 # Container içinde padding GÜVENLİDİR
    )

    # --- FONKSİYONLAR ---
    def change_tab(target):
        summary_view.visible = (target == "home")
        add_view.visible = (target == "add")
        page.update()

    def on_type_change(e):
        val = type_dd.value
        category_dd.options = [ft.dropdown.Option(c) for c in cats[val]]
        category_dd.value = None
        page.update()

    def handle_save(e):
        if not amt_in.value or not type_dd.value: return
        try:
            val = float(amt_in.value.replace(",", "."))
        except: return

        item = {
            "id": datetime.now().timestamp(),
            "type": type_dd.value,
            "category": category_dd.value if category_dd.value else "Diğer",
            "amount": val,
            "date": selected_date.strftime("%d.%m.%Y")
        }
        transactions.append(item)
        save_data_to_file()
        amt_in.value = ""
        render_summary()
        change_tab("home")

    def handle_delete(tid):
        nonlocal transactions
        transactions = [t for t in transactions if t["id"] != tid]
        save_data_to_file()
        render_summary()

    def render_summary():
        summary_list.controls.clear()
        
        # Hesaplamalar
        gelir = sum(i["amount"] for i in transactions if i["type"] == "Gelir")
        gider = sum(i["amount"] for i in transactions if i["type"] == "Gider")
        
        # Mavi Kart
        summary_list.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("TOPLAM DURUM", color="white", size=12),
                    ft.Text(f"₺ {gelir - gider:,.2f}", size=32, color="white", weight="bold"),
                    ft.Row([
                        ft.Text(f"Gelir: {gelir}", color="white"),
                        ft.Text(f"Gider: {gider}", color="white"),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ], spacing=5),
                bgcolor="blue",
                padding=20,
                border_radius=ft.border_radius.only(bottom_left=20, bottom_right=20)
            )
        )

        # Liste Elemanları
        for t in reversed(transactions):
            summary_list.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon("payments", color="green" if t["type"] == "Gelir" else "red"),
                        ft.Column([
                            ft.Text(t["category"], weight="bold"),
                            ft.Text(t["date"], size=12),
                        ], expand=True, spacing=0),
                        ft.Text(f"{t['amount']} TL"),
                        ft.IconButton("delete", on_click=lambda e, tid=t["id"]: handle_delete(tid))
                    ]),
                    padding=10,
                    border=ft.border.all(1, "#eeeeee"),
                    border_radius=10,
                    margin=ft.margin.symmetric(horizontal=15)
                )
            )
        page.update()

    # --- FORM ELEMANLARI ---
    type_dd = ft.Dropdown(label="Tür", options=[ft.dropdown.Option(k) for k in cats.keys()], on_change=on_type_change)
    category_dd = ft.Dropdown(label="Kategori")
    amt_in = ft.TextField(label="Tutar", keyboard_type="number")
    selected_date = datetime.now()
    
    dp = ft.DatePicker(on_change=lambda e: globals().update(selected_date=e.control.value))
    page.overlay.append(dp)

    add_form_elements.controls = [
        ft.Text("İşlem Ekle", size=24, weight="bold"),
        type_dd,
        category_dd,
        amt_in,
        ft.ElevatedButton("Tarih Seç", icon="calendar_today", on_click=lambda _: dp.pick_date()),
        ft.ElevatedButton("KAYDET", on_click=handle_save, bgcolor="blue", color="white", width=400, height=50)
    ]

    # --- NAVİGASYON ---
    nav_bar = ft.Container(
        content=ft.Row([
            ft.IconButton("home", on_click=lambda _: change_tab("home"), expand=True),
            ft.IconButton("add", on_click=lambda _: change_tab("add"), expand=True),
        ]),
        bgcolor="#eeeeee",
        height=60
    )

    # Ana Sayfaya Ekle
    page.add(
        ft.Column([
            summary_view,
            add_view,
            nav_bar
        ], expand=True, spacing=0)
    )

    render_summary()

# Uygulamayı Başlat
ft.app(target=main)
