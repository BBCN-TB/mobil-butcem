import flet as ft

def main(page: ft.Page):
    # --- GENEL AYARLAR ---
    page.title = "Cüzdanım"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = "#333333"

    # Toplam tutarı tutacak değişken
    toplam_para = 0

    # --- FONKSİYONLAR ---
    def harcama_sil(e, liste_ogesi, tutar):
        nonlocal toplam_para
        liste_kutusu.controls.remove(liste_ogesi)
        toplam_para -= float(tutar)
        toplam_text.value = f"₺ {toplam_para:.2f}"
        page.update()

    def harcama_ekle(e):
        nonlocal toplam_para
        
        if not isim_input.value or not tutar_input.value:
            isim_input.border_color = "red"
            page.update()
            return

        isim_input.border_color = None

        try:
            girilen_tutar = float(tutar_input.value)
        except ValueError:
            tutar_input.border_color = "red"
            page.update()
            return

        # Listeye eklenecek satır
        yeni_oge = ft.Dismissible(
            key=isim_input.value + tutar_input.value, 
            on_dismiss=lambda x: harcama_sil(x, yeni_oge, girilen_tutar),
            background=ft.Container(bgcolor="red", padding=20, content=ft.Icon("delete", color="white")),
            content=ft.Container(
                padding=10,
                bgcolor="white",
                border_radius=10,
                margin=ft.margin.only(bottom=5),
                shadow=ft.BoxShadow(blur_radius=5, color="grey"),
                content=ft.Row([
                    ft.Row([
                        ft.Icon("shopping_bag", color="blue", size=30),
                        ft.VerticalDivider(width=10, color="transparent"),
                        ft.Column([
                            ft.Text(isim_input.value, weight="bold", size=16),
                            ft.Text("Harcama", size=12, color="grey")
                        ], spacing=2)
                    ]),
                    ft.Text(f"-{girilen_tutar} TL", weight="bold", size=16, color="red")
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            )
        )

        liste_kutusu.controls.append(yeni_oge)
        toplam_para += girilen_tutar
        toplam_text.value = f"₺ {toplam_para:.2f}"

        isim_input.value = ""
        tutar_input.value = ""
        isim_input.focus()
        page.update()

    # --- ARAYÜZ PARÇALARI ---
    
    toplam_text = ft.Text("₺ 0.00", color="white", size=30, weight="bold")
    
    ust_kart = ft.Container(
        width=350,
        height=120,
        bgcolor="blue",
        border_radius=20,
        padding=20,
        content=ft.Column([
            ft.Text("Toplam Harcama", color="white70", size=14),
            toplam_text
        ], alignment=ft.MainAxisAlignment.CENTER)
    )

    isim_input = ft.TextField(
        label="Harcama Adı", bgcolor="white", border_radius=10, height=45, text_size=14, expand=True
    )
    tutar_input = ft.TextField(
        label="Tutar", bgcolor="white", border_radius=10, height=45, text_size=14, width=100, keyboard_type=ft.KeyboardType.NUMBER
    )
    
    ekle_buton = ft.ElevatedButton(
        content=ft.Text("Ekle", color="white"),
        bgcolor="black",
        height=45,
        on_click=harcama_ekle,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    liste_kutusu = ft.Column(scroll=ft.ScrollMode.AUTO, height=400)

    # --- TELEFON ÇERÇEVESİ ---
    mobil_ekran = ft.Container(
        width=390,
        height=800,
        bgcolor="#f2f2f7",
        border_radius=30,
        padding=20,
        clip_behavior=ft.ClipBehavior.HARD_EDGE, 
        content=ft.Column([
            ft.Container(
                content=ft.Text("Cüzdanım", size=20, weight="bold", color="black"),
                # HATALI KISIM DÜZELTİLDİ:
                alignment=ft.Alignment(0, 0), 
                padding=10
            ),
            ust_kart,
            ft.Divider(height=20, color="transparent"),
            ft.Row([isim_input, tutar_input]),
            ft.Container(width=350, content=ekle_buton),
            ft.Divider(height=20),
            ft.Text("Son Hareketler", size=16, weight="bold", color="grey"),
            liste_kutusu
        ])
    )

    page.add(mobil_ekran)


import os # En üste ekleyin

# ... (tüm kodlarınız aynı kalıyor)

# En alttaki ft.app satırını bununla değiştirin:
if __name__ == "__main__":
    ft.app(
        target=main, 
        view=ft.AppView.WEB_BROWSER, 
        port=int(os.getenv("PORT", 8080)), # Render'ın verdiği portu kullanır
        host="0.0.0.0" # Dış dünyaya açılmasını sağlar
    )
