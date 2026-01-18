import flet as ft
from datetime import datetime
from supabase import create_client, Client

# --- SUPABASE BAĞLANTISI (Görsellerden Alınan Bilgiler) ---
URL = "https://zzvadgfshqdgnmtkemyj.supabase.co"
# Not: Görselde anahtarın sonu görünmediği için kopyala butonuna basıp tam halini kontrol etmen iyi olur.
KEY = "sb_publishable_wNArCAGDrgo2y4etu7iSVg_40bWI6Z0Z6Z0" 

supabase: Client = create_client(URL, KEY)

def main(page: ft.Page):
    page.title = "Bütçem 2026 - Pro"
    page.theme_mode = "light"
    page.window_width = 400
    page.window_height = 800
    page.padding = 0
    page.spacing = 0

    # --- DURUM VE KATEGORİLER ---
    transactions = []
    selected_date = datetime.now()

    categories_map = {
        "Gider": ["Kredi Kartı", "Kira", "Fatura", "Eğitim", "Mutfak", "Diğer"],
        "Gelir": ["Maaş", "Ek Gelir"],
        "Yatırım": ["Altın", "Döviz", "Borsa"]
    }

    # --- VERİTABANI FONKSİYONLARI ---
    def load_data():
        nonlocal transactions
        try:
            # Verileri tarihe göre sıralı çekiyoruz
            res = supabase.table("transactions").select("*").order("created_at").execute()
            transactions = res.data
            render_all()
        except Exception as e:
            print(f"Veri yükleme hatası: {e}")

    def save_item(e):
        if not amt_in.value or not type_dd.value or not cat_dd.value:
            return
        
        new_data = {
            "type": type_dd.value,
            "category": cat_dd.value,
            "amount": float(amt_in.value.replace(",", ".")),
            "date": selected_date.strftime("%d.%m.%Y")
        }
        
        try:
            supabase.table("transactions").insert(new_data).execute()
            amt_in.value = ""
            load_data()
            switch_tab("summary")
        except Exception as ex:
            print(f"Kaydetme hatası: {ex}")

    def delete_item(tid):
        try:
            supabase.table("transactions").delete().eq("id", tid).execute()
            load_data()
        except Exception as ex:
            print(f"Silme hatası: {ex}")

    # --- SAYFA YAPILARI ---
    summary_col = ft.Column(scroll="auto", expand=True, spacing=10)
    summary_view = ft.Container(content=summary_col, expand=True)

    add_form = ft.Column(spacing=20)
    add_view = ft.Container(content=add_form, expand=True, visible=False, padding=25)

    report_col = ft.Column(scroll="auto", expand=True, spacing=20)
    report_view = ft.Container(content=report_col, expand=True, visible=False, padding=20)

    # --- ARAYÜZÜ YENİLEME ---
    def render_all():
        # 1. Özet Sayfası
        summary_col.controls.clear()
        t_gelir = sum(t["amount"] for t in transactions if t["type"] == "Gelir")
        t_gider = sum(t["amount"] for t in transactions if t["type"] == "Gider")
        
        summary_col.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("NET BAKİYE", color="white70", size=12, weight="bold"),
                    ft.Text(f"₺ {t_gelir - t_gider:,.2f}", size=34, color="white", weight="bold"),
                    ft.Row([
                        ft.Text(f"Gelir: ₺{t_gelir:,.0f}", color="white"),
                        ft.Text(f"Gider: ₺{t_gider:,.0f}", color="white"),
                    ], alignment="spaceBetween")
                ], spacing=5),
                bgcolor=ft.colors.BLUE_700, padding=30, 
                border_radius=ft.border_radius.only(bottom_left=35, bottom_right=35)
            )
        )

        list_area = ft.Column(padding=ft.padding.symmetric(horizontal=20))
        for t in reversed(transactions):
            list_area.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon("payments", color="green" if t["type"] == "Gelir" else "red" if t["type"] == "Gider" else "orange"),
                        ft.Column([
                            ft.Text(t["category"], weight="bold"),
                            ft.Text(f"{t['date']} | {t['type']}", size=11, color="grey")
                        ], expand=True, spacing=0),
                        ft.Text(f"{t['amount']} ₺", weight="bold"),
                        ft.IconButton("delete_outline", on_click=lambda e, tid=t["id"]: delete_item(tid), icon_color="grey")
                    ]),
                    padding=12, border=ft.border.all(1, "#f0f0f0"), border_radius=12, bgcolor="white"
                )
            )
        summary_col.controls.append(list_area)

        # 2. Rapor Sayfası (Pie Chart)
        report_col.controls.clear()
        gider_toplam = sum(t["amount"] for t in transactions if t["type"] == "Gider")
        
        if gider_toplam > 0:
            # Giderleri kategorilere göre grupla
            cat_sums = {}
            for t in transactions:
                if t["type"] == "Gider":
                    cat_sums[t["category"]] = cat_sums.get(t["category"], 0) + t["amount"]

            chart = ft.PieChart(
                sections=[
                    ft.PieChartSection(val, title=f"{cat}\n%{int(val/gider_toplam*100)}", 
                                       color=ft.colors.random(), radius=50)
                    for cat, val in cat_sums.items()
                ],
                center_space_radius=40, height=250
            )
            report_col.controls.append(ft.Text("Gider Analizi", size=22, weight="bold"))
            report_col.controls.append(ft.Container(content=chart, alignment=ft.alignment.center))
        else:
            report_col.controls.append(ft.Text("Henüz raporlanacak gider verisi yok.", color="grey"))

        page.update()

    # --- FORM ELEMANLARI ---
    type_dd = ft.Dropdown(label="İşlem Türü", options=[ft.dropdown.Option(k) for k in categories_map.keys()])
    
    def on_type_change(e):
        cat_dd.options = [ft.dropdown.Option(c) for c in categories_map[type_dd.value]]
        cat_dd.value = None
        page.update()
    
    type_dd.on_change = on_type_change
    cat_dd = ft.Dropdown(label="Kategori")
    amt_in = ft.TextField(label="Tutar", keyboard_type="number", prefix_text="₺ ")
    
    date_label = ft.Text(f"Tarih: {selected_date.strftime('%d.%m.%Y')}", weight="bold")
    def handle_date(e):
        nonlocal selected_date
        selected_date = e.control.value
        date_label.value = f"Tarih: {selected_date.strftime('%d.%m.%Y')}"
        page.update()

    dp = ft.DatePicker(on_change=handle_date)
    page.overlay.append(dp)

    add_form.controls = [
        ft.Text("İşlem Ekle", size=26, weight="bold"),
        type_dd, cat_dd, amt_in,
        ft.Row([ft.IconButton("calendar_today", on_click=lambda _: dp.pick_date()), date_label]),
        ft.ElevatedButton("İŞLEMİ KAYDET", on_click=save_item, bgcolor="blue", color="white", height=55, width=400)
    ]

    # --- NAVİGASYON ---
    def switch_tab(target):
        summary_view.visible = (target == "summary")
        add_view.visible = (target == "add")
        report_view.visible = (target == "report")
        page.update()

    nav_bar = ft.Container(
        content=ft.Row([
            ft.IconButton("home", on_click=lambda _: switch_tab("summary"), expand=True, tooltip="Özet"),
            ft.IconButton("add_circle", on_click=lambda _: switch_tab("add"), expand=True, tooltip="Ekle"),
            ft.IconButton("analytics", on_click=lambda _: switch_tab("report"), expand=True, tooltip="Raporlar"),
        ], alignment="around"),
        bgcolor="#f8f9fa", height=70, border=ft.border.only(top=ft.BorderSide(1, "#eeeeee"))
    )

    page.add(
        ft.Column([
            ft.Container(content=summary_view, expand=True),
            add_view,
            report_view,
            nav_bar
        ], expand=True, spacing=0)
    )

    load_data()

ft.app(target=main)
