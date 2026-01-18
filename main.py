import flet as ft
from datetime import datetime
from supabase import create_client, Client

# --- SUPABASE AYARLARI ---
# Burayı kendi bilgilerine göre doldur
URL = "https://buraya_url_gelecek.supabase.co"
KEY = "buraya_anon_key_gelecek"
supabase: Client = create_client(URL, KEY)

def main(page: ft.Page):
    page.title = "Bütçem 2026 - Streamlit Pro"
    page.theme_mode = "light"
    page.padding = 0
    page.spacing = 0

    # --- DURUM YÖNETİMİ ---
    transactions = []
    current_date = datetime.now()

    cats = {
        "Gider": ["Kredi Kartı", "Kira", "Fatura", "Eğitim", "Mutfak", "Diğer"],
        "Gelir": ["Maaş", "Ek Gelir"],
        "Yatırım": ["Altın", "Döviz", "Borsa"]
    }

    # --- VERİTABANI İŞLEMLERİ ---
    def load_data():
        nonlocal transactions
        try:
            res = supabase.table("transactions").select("*").execute()
            transactions = res.data
            update_views()
        except: pass

    def save_data(item):
        supabase.table("transactions").insert(item).execute()
        load_data()

    def delete_data(tid):
        supabase.table("transactions").delete().eq("id", tid).execute()
        load_data()

    # --- SAYFA YAPILARI (CONTAINERS) ---
    summary_page = ft.Column(scroll="auto", expand=True)
    add_page = ft.Column(visible=False, expand=True, spacing=20)
    report_page = ft.Column(visible=False, expand=True, scroll="auto")

    # --- UI GÜNCELLEME (RE-RENDER) ---
    def update_views():
        # 1. Özet Sayfası Yenileme
        summary_page.controls.clear()
        gelir = sum(t["amount"] for t in transactions if t["type"] == "Gelir")
        gider = sum(t["amount"] for t in transactions if t["type"] == "Gider")
        yatirim = sum(t["amount"] for t in transactions if t["type"] == "Yatırım")
        
        summary_page.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("TOPLAM VARLIK", color="white70", size=12),
                    ft.Text(f"₺ {gelir - gider:,.2f}", size=34, color="white", weight="bold"),
                    ft.Row([
                        ft.Text(f"Gelir: {gelir:,.0f}", color="white"),
                        ft.Text(f"Gider: {gider:,.0f}", color="white"),
                    ], alignment="spaceBetween")
                ]),
                bgcolor="blue", padding=30, border_radius=ft.border_radius.only(bottom_left=30, bottom_right=30)
            )
        )
        
        list_area = ft.Column(padding=20, spacing=10)
        for t in reversed(transactions):
            list_area.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon("payments", color="green" if t["type"]=="Gelir" else "red"),
                        ft.Column([ft.Text(t["category"], weight="bold"), ft.Text(t["date"], size=12)], expand=True, spacing=0),
                        ft.Text(f"{t['amount']} ₺", weight="bold"),
                        ft.IconButton("delete", on_click=lambda e, tid=t["id"]: delete_data(tid))
                    ]),
                    padding=10, border=ft.border.all(1, "#eee"), border_radius=10
                )
            )
        summary_page.controls.append(list_area)

        # 2. Rapor Sayfası Yenileme (Pie Chart)
        report_page.controls.clear()
        if transactions:
            # Gider Dağılımı Verisi
            gider_toplam = sum(t["amount"] for t in transactions if t["type"] == "Gider")
            chart = ft.PieChart(
                sections=[
                    ft.PieChartSection(t["amount"], title=f"%{int(t['amount']/gider_toplam*100)}", color=ft.colors.random(t["category"]))
                    for t in transactions if t["type"] == "Gider"
                ],
                sections_space=2, center_space_radius=40, height=200
            )
            report_page.controls.append(ft.Container(content=ft.Column([
                ft.Text("Gider Dağılımı", size=20, weight="bold"),
                chart,
                ft.Text(f"Toplam Gider: {gider_toplam} ₺", size=16)
            ]), padding=20))

        page.update()

    # --- FORM ELEMANLARI ---
    type_dd = ft.Dropdown(label="Tür", options=[ft.dropdown.Option(k) for k in cats.keys()],
                         on_change=lambda e: (setattr(cat_dd, "options", [ft.dropdown.Option(c) for c in cats[type_dd.value]]), page.update()))
    cat_dd = ft.Dropdown(label="Kategori")
    amt_tf = ft.TextField(label="Tutar", keyboard_type="number")
    
    dp = ft.DatePicker(on_change=lambda e: (globals().update(current_date=e.control.value)))
    page.overlay.append(dp)

    add_page.controls = [
        ft.Container(content=ft.Column([
            ft.Text("Yeni İşlem", size=24, weight="bold"),
            type_dd, cat_dd, amt_tf,
            ft.ElevatedButton("Tarih Seç", icon="calendar_today", on_click=lambda _: dp.pick_date()),
            ft.ElevatedButton("KAYDET", on_click=lambda _: (save_data({
                "type": type_dd.value, "category": cat_dd.value, "amount": float(amt_tf.value), 
                "date": current_date.strftime("%d.%m.%Y")
            }), switch("home")), bgcolor="blue", color="white", width=400, height=50)
        ]), padding=20)
    ]

    # --- NAVİGASYON ---
    def switch(t):
        summary_page.visible = (t == "home")
        add_page.visible = (t == "add")
        report_page.visible = (t == "report")
        page.update()

    nav = ft.Container(
        content=ft.Row([
            ft.IconButton("home", on_click=lambda _: switch("home"), expand=True),
            ft.IconButton("add", on_click=lambda _: switch("add"), expand=True),
            ft.IconButton("pie_chart", on_click=lambda _: switch("report"), expand=True),
        ]), bgcolor="#f8f9fa", height=65
    )

    page.add(ft.Column([
        ft.Container(content=summary_page, expand=True),
        ft.Container(content=add_page, expand=True),
        ft.Container(content=report_page, expand=True),
        nav
    ], expand=True, spacing=0))

    load_data()

ft.app(target=main)
