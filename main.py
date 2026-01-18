import flet as ft
from datetime import datetime
import json, os, math

DATA_FILE = "veriler.json"

def main(page: ft.Page):
    page.title = "Bütçem PRO"
    page.padding = 0
    page.window_width = 400
    page.window_height = 800

    # ---------------- DATA ----------------
    def load_data():
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_data():
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    data = load_data()

    def month_key(date):
        return date.strftime("%Y-%m")

    # ---------------- UI ----------------
    summary_col = ft.Column(expand=True, scroll="auto")
    summary_view = ft.Container(content=summary_col, expand=True)

    add_col = ft.Column(spacing=15)
    add_view = ft.Container(content=add_col, padding=20, expand=True, visible=False)

    def switch(v):
        summary_view.visible = v == "summary"
        add_view.visible = v == "add"
        page.update()

    # ---------------- Taksit Botu ----------------
    def add_installments(total, count, base_item):
        base = math.floor((total / count) * 100) / 100
        kalan = round(total - (base * count), 2)

        for i in range(count):
            d = selected_date.replace(month=selected_date.month + i)
            amount = base
            if i == count - 1:
                amount += kalan

            key = month_key(d)
            if key not in data:
                data[key] = []

            data[key].append({
                "date": d.strftime("%d.%m.%Y"),
                "type": base_item["type"],
                "category": base_item["category"],
                "amount": amount,
                "note": f"{i+1}/{count} taksit"
            })

    # ---------------- KAYDET ----------------
    def save(e):
        if not amount.value or not t_type.value or not category.value:
            return

        try:
            tutar = float(amount.value.replace(",", "."))
        except:
            return

        key = month_key(selected_date)

        if key not in data:
            data[key] = []

        item = {
            "date": selected_date.strftime("%d.%m.%Y"),
            "type": t_type.value,
            "category": category.value,
            "amount": tutar,
            "note": ""
        }

        if taksit.value and int(taksit.value) > 1:
            add_installments(tutar, int(taksit.value), item)
        else:
            data[key].append(item)

        save_data()
        refresh()
        switch("summary")

    # ---------------- UI UPDATE ----------------
    def refresh():
        summary_col.controls.clear()

        now_key = month_key(datetime.now())
        items = data.get(now_key, [])

        gelir = sum(x["amount"] for x in items if x["type"] == "Gelir")
        gider = sum(x["amount"] for x in items if x["type"] == "Gider")

        summary_col.controls.append(
            ft.Container(
                padding=20,
                bgcolor="blue",
                border_radius=ft.border_radius.only(bottom_left=25, bottom_right=25),
                content=ft.Column([
                    ft.Text(now_key, color="white70"),
                    ft.Text(f"₺ {gelir-gider:,.2f}", size=30, color="white", weight="bold"),
                    ft.Row([
                        ft.Text(f"Gelir: ₺{gelir:,.0f}", color="white"),
                        ft.Text(f"Gider: ₺{gider:,.0f}", color="white"),
                    ], alignment="spaceBetween")
                ])
            )
        )

        col = ft.Column(spacing=8)
        for x in items:
            col.controls.append(
                ft.Container(
                    padding=10,
                    bgcolor="white",
                    border_radius=10,
                    border=ft.border.all(1, "#eee"),
                    content=ft.Row([
                        ft.Text(x["category"], expand=True),
                        ft.Text(f"{x['amount']:,.2f} ₺", weight="bold")
                    ])
                )
            )

        summary_col.controls.append(ft.Container(content=col, padding=20))
        page.update()

    # ---------------- FORM ----------------
    t_type = ft.Dropdown(label="Tür", options=[
        ft.dropdown.Option("Gelir"),
        ft.dropdown.Option("Gider"),
        ft.dropdown.Option("Yatırım")
    ])

    category = ft.TextField(label="Kategori")
    amount = ft.TextField(label="Tutar", keyboard_type="number")
    taksit = ft.TextField(label="Taksit (opsiyonel)", keyboard_type="number")

    selected_date = datetime.now()
    dp = ft.DatePicker(on_change=lambda e: None)
    page.overlay.append(dp)

    add_col.controls = [
        ft.Text("Yeni İşlem", size=22, weight="bold"),
        t_type, category, amount, taksit,
        ft.ElevatedButton("Kaydet", on_click=save)
    ]

    nav = ft.Container(
        padding=10,
        border=ft.border.only(top=ft.BorderSide(1, "#ccc")),
        content=ft.Row([
            ft.IconButton("home", on_click=lambda _: switch("summary")),
            ft.IconButton("add_circle", on_click=lambda _: switch("add")),
        ], alignment="spaceAround")
    )

    page.add(
        ft.Column([
            ft.Stack([summary_view, add_view], expand=True),
            nav
        ], expand=True, spacing=0)
    )

    refresh()

ft.app(target=main)
