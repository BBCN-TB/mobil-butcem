import flet as ft
from datetime import datetime
import json
import os

DATA_FILE = "veriler.json"

def main(page: ft.Page):
    page.title = "Bütçem 2026"
    page.theme_mode = "light"
    page.padding = 0
    page.window_width = 400
    page.window_height = 800

    # --- VERİ YÖNETİMİ ---
    def verileri_yukle():
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except: return []
        return []

    def verileri_kaydet():
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(transactions, f, ensure_ascii=False, indent=4)

    transactions = verileri_yukle()

    categories_data = {
        "Gider": ["Kredi Kartı", "Kira", "Fatura", "Eğitim", "Mutfak", "Diğer"],
        "Gelir": ["Maaş", "Ek Gelir"],
        "Yatırım": ["Altın", "Döviz", "Borsa"]
    }

    # --- SAYFA YAPILARI ---
    # Özet Sayfası
    summary_col = ft.Column(scroll="auto", expand=True)
    
    # Ekleme Sayfası
    add_col = ft.Column(expand=True, spacing=20)
    add_view_wrapper = ft.Container(
        content=add_col,
        visible=False,
        expand=True,
        padding=20
    )

    # --- FONKSİYONLAR ---
    def switch_page(page_name):
        summary_col.visible = (page_name == "summary")
        add_view_wrapper.visible = (page_name == "add")
        page.update()

    def update_cats(e):
        t_type = type_dd.value
        if t_type in categories_data:
            category_dd.options = [ft.dropdown.Option(c) for c in categories_data[t_type]]
            category_dd.value = None
            page.update()

    def save_data(e):
        if not amt_in.value or not type_dd.value: return
        try:
            tutar = float(amt_in.value.replace(",", "."))
        except: return

        new_item = {
            "id": datetime.now().timestamp(),
            "type": type_dd.value,
            "category": category_dd.value if category_dd.value else "Genel",
            "amount": tutar,
            "date": selected_date.strftime("%d.%m.%Y")
        }
        transactions.append(new_item)
        verileri_kaydet()
        amt_in.value = ""
        refresh_ui()
        switch_page("summary")

    def delete_item(tid):
        nonlocal transactions
        transactions = [t for t in transactions if t["id"] != tid]
        verileri_kaydet()
        refresh_ui()

    def refresh_ui():
        summary_col.controls.clear()
        t_gelir = sum(t["amount"] for t in transactions if t["type"] == "Gelir")
        t_gider = sum(t["amount"] for t in transactions if t["type"] == "Gider")
        
        # Üst Kısım
        summary_col.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("OCAK 2026", color="white70", size=12),
                    ft.Text(f"₺ {t_gelir - t_gider:,.2f}", size=32, color="white", weight="bold"),
                    ft.Row([
                        ft.Text(f"Gelir: ₺{t_gelir:,.0f}", color="white"),
                        ft.Text(f"Gider: ₺{t_gider:,.0f}", color="white"),
                    ], alignment="spaceBetween")
                ]),
                bgcolor="blue", padding=25, border_radius=ft.border_radius.only(bottom_left=30, bottom_right=30)
            )
        )
        
        # İŞTE HATALI OLAN KISIM BURAYDI, DÜZELTİLDİ:
        list_items = ft.Column(spacing=10) # Padding kaldırıldı!
        
        for t in reversed(transactions):
            list_items.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon("payments", color="green" if t["type"] == "Gelir" else "red"),
                        ft.Column([
                            ft.Text(f"{t['category']}", weight="bold"),
                            ft.Text(f"{t['date']}", size=12, color="grey"),
                        ], expand=True, spacing=2),
                        ft.Text(f"{t['amount']} ₺", weight="bold"),
                        ft.IconButton("delete_outline", on_click=lambda e, tid=t["id"]: delete_item(tid))
                    ]),
                    padding=10, border_radius=10, bgcolor="white", border=ft.border.all(1, "#eeeeee")
                )
            )
        
        # Sütuna dışarıdan boşluk vermek için bir Container içine aldık
        summary_col.controls.append(ft.Container(content=list_items, padding=20))
        page.update()

    # --- FORM ELEMANLARI ---
    type_dd = ft.Dropdown(label="İşlem Türü", options=[ft.dropdown.Option(k) for k in categories_data.keys()], on_change=update_cats)
    category_dd = ft.Dropdown(label="Kategori Seçin")
    amt_in = ft.TextField(label="Tutar (₺)", keyboard_type="number")
    selected_date = datetime.now()
    
    def on_date_select(e):
        nonlocal selected_date
        selected_date = e.control.value
        page.update()

    dp = ft.DatePicker(on_change=on_date_select)
    page.overlay.append(dp)

    add_col.controls = [
        ft.Text("Yeni İşlem Ekle", size=24, weight="bold"),
        type_dd, category_dd, amt_in,
        ft.ElevatedButton("Tarih Seç", icon="calendar_today", on_click=lambda _: dp.pick_date(), width=400),
        ft.ElevatedButton("İŞLEMİ KAYDET", on_click=save_data, bgcolor="blue", color="white", height=50, width=400)
    ]

    # --- NAVİGASYON ---
    custom_nav = ft.Container(
        content=ft.Row([
            ft.IconButton("home", on_click=lambda _: switch_page("summary"), expand=True),
            ft.IconButton("add_circle", on_click=lambda _: switch_page("add"), expand=True),
        ], alignment="around"),
        bgcolor="#f8f9fa", padding=10, border=ft.border.only(top=ft.BorderSide(1, "#cccccc"))
    )

    page.add(
        ft.Column([
            ft.Container(content=summary_col, expand=True),
            add_view_wrapper,
            custom_nav
        ], expand=True, spacing=0)
    )

    refresh_ui()

ft.app(target=main)
