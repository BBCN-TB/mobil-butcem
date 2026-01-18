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

    # --- VERİ ---
    def verileri_yukle():
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
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

    # --- SAYFALAR ---
    summary_col = ft.Column(scroll="auto", expand=True)
    summary_view = ft.Container(content=summary_col, expand=True, visible=True)

    add_col = ft.Column(expand=True, spacing=20)
    add_view = ft.Container(content=add_col, expand=True, visible=False, padding=20)

    # --- NAV ---
    def switch_page(name):
        summary_view.visible = name == "summary"
        add_view.visible = name == "add"
        page.update()

    # --- FORM ---
    def update_cats(e):
        t = type_dd.value
        if t in categories_data:
            category_dd.options = [ft.dropdown.Option(x) for x in categories_data[t]]
            category_dd.value = None
            page.update()

    def save_data(e):
        if not amt_in.value or not type_dd.value or not category_dd.value:
            return
        try:
            tutar = float(amt_in.value.replace(",", "."))
        except:
            return

        transactions.append({
            "id": datetime.now().timestamp(),
            "type": type_dd.value,
            "category": category_dd.value,
            "amount": tutar,
            "date": selected_date.strftime("%d.%m.%Y")
        })

        verileri_kaydet()
        amt_in.value = ""
        refresh_ui()
        switch_page("summary")

    def delete_item(tid):
        nonlocal transactions
        transactions = [t for t in transactions if t["id"] != tid]
        verileri_kaydet()
        refresh_ui()

    # --- UI GÜNCELLE ---
    def refresh_ui():
        summary_col.controls.clear()

        gelir = sum(t["amount"] for t in transactions if t["type"] == "Gelir")
        gider = sum(t["amount"] for t in transactions if t["type"] == "Gider")

        summary_col.controls.append(
            ft.Container(
                bgcolor="blue",
                padding=25,
                border_radius=ft.border_radius.only(bottom_left=30, bottom_right=30),
                content=ft.Column([
                    ft.Text("OCAK 2026", color="white70", size=12),
                    ft.Text(f"₺ {gelir - gider:,.2f}", size=32, color="white", weight="bold"),
                    ft.Row([
                        ft.Text(f"Gelir: ₺{gelir:,.0f}", color="white"),
                        ft.Text(f"Gider: ₺{gider:,.0f}", color="white")
                    ], alignment="spaceBetween")
                ])
            )
        )

        list_col = ft.Column(spacing=10)

        for t in reversed(transactions):
            list_col.controls.append(
                ft.Container(
                    bgcolor="white",
                    padding=10,
                    border_radius=10,
                    border=ft.border.all(1, "#eeeeee"),
                    content=ft.Row([
                        ft.Icon("payments", color="green" if t["type"] == "Gelir" else "red"),
                        ft.Column([
                            ft.Text(t["category"], weight="bold"),
                            ft.Text(t["date"], size=12, color="grey")
                        ], expand=True),
                        ft.Text(f"{t['amount']:,.2f} ₺", weight="bold"),
                        ft.IconButton("delete_outline", on_click=lambda e, tid=t["id"]: delete_item(tid))
                    ])
                )
            )

        summary_col.controls.append(ft.Container(content=list_col, padding=20))
        page.update()

    # --- FORM ELEMANLARI ---
    type_dd = ft.Dropdown(label="İşlem Türü",
                          options=[ft.dropdown.Option(k) for k in categories_data.keys()],
                          on_change=update_cats)
    category_dd = ft.Dropdown(label="Kategori")
    amt_in = ft.TextField(label="Tutar (₺)", keyboard_type="number")
    selected_date = datetime.now()

    def on_date_select(e):
        nonlocal selected_date
        selected_date = e.control.value

    dp = ft.DatePicker(on_change=on_date_select)
    page.overlay.append(dp)

    add_col.controls = [
        ft.Text("Yeni İşlem Ekle", size=24, weight="bold"),
        type_dd,
        category_dd,
        amt_in,
        ft.ElevatedButton("Tarih Seç", icon="calendar_today", on_click=lambda _: dp.pick_date()),
        ft.ElevatedButton("İŞLEMİ KAYDET", on_click=save_data, bgcolor="blue", color="white", height=50)
    ]

    # --- NAV BAR ---
    nav = ft.Container(
        padding=10,
        bgcolor="#f8f9fa",
        border=ft.border.only(top=ft.BorderSide(1, "#cccccc")),
        content=ft.Row([
            ft.IconButton("home", expand=True, on_click=lambda _: switch_page("summary")),
            ft.IconButton("add_circle", expand=True, on_click=lambda _: switch_page("add"))
        ], alignment="spaceAround")
    )

    page.add(
        ft.Column([
            ft.Stack([summary_view, add_view], expand=True),
            nav
        ], expand=True, spacing=0)
    )

    refresh_ui()

ft.app(target=main)
