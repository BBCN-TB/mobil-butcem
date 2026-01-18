import flet as ft
from datetime import datetime
from supabase import create_client, Client

# --- SUPABASE BAĞLANTISI (Buraya kendi bilgilerini yapıştır) ---
URL = "https://zzvadgfshqdgnmtkemyj.supabase.co"
KEY = "sb_secret_VbEtaMYtVsAR6YUbSGpEvA_pNIhRHuD"
supabase: Client = create_client(URL, KEY)

def main(page: ft.Page):
    page.title = "Bütçem 2026 Pro"
    page.theme_mode = "light"
    page.padding = 0
    page.window_width = 400
    page.window_height = 800

    # --- KATEGORİ VERİLERİ ---
    categories_data = {
        "Gider": ["Kredi Kartı", "Kira", "Fatura", "Eğitim", "Mutfak", "Diğer"],
        "Gelir": ["Maaş", "Ek Gelir"],
        "Yatırım": ["Altın", "Döviz", "Borsa"]
    }

    # --- DEĞİŞKENLER ---
    transactions = []
    selected_date = datetime.now()

    # --- FONKSİYONLAR (VERİTABANI) ---
    def load_from_cloud():
        nonlocal transactions
        try:
            response = supabase.table("transactions").select("*").execute()
            transactions = response.data
            render_ui()
        except Exception as e:
            print(f"Hata: {e}")

    def save_to_cloud(item):
        supabase.table("transactions").insert(item).execute()
        load_from_cloud()

    def delete_from_cloud(tid):
        supabase.table("transactions").delete().eq("id", tid).execute()
        load_from_cloud()

    # --- UI MANTIĞI ---
    summary_list = ft.Column(scroll="auto", expand=True, spacing=10)
    summary_view = ft.Container(content=summary_list, expand=True)

    add_col = ft.Column(spacing=20)
    add_view = ft.Container(content=add_col, visible=False, expand=True, padding=20)

    def switch_tab(target):
        summary_view.visible = (target == "home")
        add_view.visible = (target == "add")
        page.update()

    def on_type_change(e):
        val = type_dd.value
        category_dd.options = [ft.dropdown.Option(c) for c in categories_data[val]]
        category_dd.value = None
        page.update()

    def handle_save(e):
        if not amt_in.value or not type_dd.value: return
        
        new_item = {
            "type": type_dd.value,
            "category": category_dd.value or "Diğer",
            "amount": float(amt_in.value.replace(",", ".")),
            "date": selected_date.strftime("%d.%m.%Y")
        }
        save_to_cloud(new_item)
        amt_in.value = ""
        switch_tab("home")

    def render_ui():
        summary_list.controls.clear()
        
        gelir = sum(i["amount"] for i in transactions if i["type"] == "Gelir")
        gider = sum(i["amount"] for i in transactions if i["type"] == "Gider")
        yatirim = sum(i["amount"] for i in transactions if i["type"] == "Yatırım")
        
        # Mavi Özet Kartı
        summary_list.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("NET BAKİYE", color="white70", size=12),
                    ft.Text(f"₺ {gelir - gider:,.2f}", size=32, color="white", weight="bold"),
                    ft.Row([
                        ft.Text(f"Gelir: {gelir:,.0f}", color="white"),
                        ft.Text(f"Gider: {gider:,.0f}", color="white"),
                        ft.Text(f"Yatırım: {yatirim:,.0f}", color="yellow"),
                    ], alignment="spaceBetween")
                ], spacing=5),
                bgcolor="blue", padding=25, border_radius=ft.border_radius.only(bottom_left=30, bottom_right=30)
            )
        )

        # İşlem Listesi
        for t in reversed(transactions):
            summary_list.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon("payments", color="green" if t["type"] == "Gelir" else "red" if t["type"] == "Gider" else "orange"),
                        ft.Column([
                            ft.Text(f"{t['category']}", weight="bold"),
                            ft.Text(f"{t['date']} | {t['type']}", size=12, color="grey"),
                        ], expand=True, spacing=0),
                        ft.Text(f"{t['amount']} ₺", weight="bold"),
                        ft.IconButton("delete_outline", on_click=lambda e, tid=t["id"]: delete_from_cloud(tid))
                    ]),
                    padding=10, margin=ft.margin.symmetric(horizontal=15),
                    bgcolor="white", border_radius=10, border=ft.border.all(1, "#eeeeee")
                )
            )
        page.update()

    # --- FORM ELEMANLARI ---
    type_dd = ft.Dropdown(label="İşlem Türü", options=[ft.dropdown.Option(k) for k in categories_data.keys()], on_change=on_type_change)
    category_dd = ft.Dropdown(label="Kategori")
    amt_in = ft.TextField(label="Tutar", keyboard_type="number")
    
    date_display = ft.Text(f"Seçilen Tarih: {selected_date.strftime('%d.%m.%Y')}")
    def on_date_change(e):
        nonlocal selected_date
        selected_date = e.control.value
        date_display.value = f"Seçilen Tarih: {selected_date.strftime('%d.%m.%Y')}"
        page.update()

    dp = ft.DatePicker(on_change=on_date_change)
    page.overlay.append(dp)

    add_col.controls = [
        ft.Text("Yeni İşlem Ekle", size=24, weight="bold"),
        type_dd, category_dd, amt_in,
        ft.Row([ft.IconButton("calendar_today", on_click=lambda _: dp.pick_date()), date_display]),
        ft.ElevatedButton("KAYDET", on_click=handle_save, bgcolor="blue", color="white", width=400, height=50)
    ]

    # --- ALT NAVİGASYON ---
    nav = ft.Container(
        content=ft.Row([
            ft.IconButton("home", on_click=lambda _: switch_tab("home"), expand=True),
            ft.IconButton("add", on_click=lambda _: switch_tab("add"), expand=True),
        ]),
        bgcolor="#f8f9fa", height=70, border=ft.border.only(top=ft.BorderSide(1, "#eeeeee"))
    )

    page.add(ft.Column([summary_view, add_view, nav], expand=True, spacing=0))
    load_from_cloud()

ft.app(target=main)
