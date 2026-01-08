import flet as ft
import subpages # import module for the subpages of the app

def main(page):
    page.title = "Olis Kontrollapp über Daniels Redefluss"
    page.scroll = ft.ScrollMode.ADAPTIVE


    # -------- Theme  -----------
    page.fonts = {
        "AtkinsonHyperlegibleNext":"fonts/AtkinsonHyperlegibleNext-Regular.ttf"
    }

    PrimaryColor = ft.colors.GREEN
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        color_scheme_seed=PrimaryColor,
        font_family="AtkinsonHyperlegibleNext"
    )
    
    def apply_bg():
        if page.theme_mode == ft.ThemeMode.DARK:
            page.bgcolor = "#121B2F" #ft.colors.BLACK
        else:
            page.bgcolor = ft.colors.WHITE
    apply_bg()

    # -------- Switch dark and lightmode   --------
    def handle_switch_change(e): # change dark and light mode
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            switch.thumb_icon = ft.icons.LIGHT_MODE
        else:
            switch.thumb_icon = ft.icons.DARK_MODE
            page.theme_mode = ft.ThemeMode.DARK
        apply_bg()
        page.update()
    
    switch = ft.Switch(thumb_icon=ft.icons.DARK_MODE, on_change=handle_switch_change)
    
    # -------- Data Saving --------
    trdata = [] # empty list for storing data and time as tuples, converted

    
    # -------- BottomSheet and Github Link   --------
    bottomsheet = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    ft.Text("Erstellt für Oli von Daniel. ❤️ \nGutschein zur Programmierung geschenkt zu Olis 23. Geburtstag am 20.08.2025. \nDaniel Schöndorf, 2026",
                        text_align=ft.TextAlign.CENTER),
                    ft.ElevatedButton("Alles klar!", on_click=lambda _: page.close(bottomsheet)),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True,
            ),
            padding=50,
        ),
        open=False
    )
    
    def open_repo(e):
        page.launch_url('https://github.com/Biotit/Redeflusslevel')
    
    bottomsheet_quellcode = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    ft.Text("Quellcode auf Github",
                        text_align=ft.TextAlign.CENTER),
                    #ft.ElevatedButton("Öffne Quellcode", on_click=open_repo)
                    ft.IconButton(icon=ft.icons.CODE, on_click=open_repo),
                    ft.Text(spans=[
                        ft.TextSpan("Von Daniel Schöndorf 2026\nmit "),
                        ft.TextSpan("Flet", url="https://github.com/flet-dev",
                            style=ft.TextStyle(
                                color=PrimaryColor,
                                decoration=ft.TextDecoration.UNDERLINE)),
                        ft.TextSpan(" (Apache License 2.0) erstellt.")
                        ], text_align=ft.TextAlign.CENTER),
                    #ft.Text("Von\nDaniel Schöndorf, 2026\nmit Flet erstellt.",
                     #   text_align=ft.TextAlign.CENTER),
                    ft.ElevatedButton("Jetzt nicht.", on_click=lambda _: page.close(bottomsheet_quellcode)),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True,
            ),
            padding=50,
        ),
        open=False
    )
    
    
    page.overlay.append(bottomsheet)
    
    
    # -------- Subpages  --------

    einstellung_view = subpages.einstellung(page, trdata, PrimaryColor)

    trend_view = subpages.trend(page, trdata, PrimaryColor)

    infos_view = subpages.infos(page)

    views = [einstellung_view, trend_view, infos_view]

    # -------- Navigation/Top and bottom bars  --------
    def nav_changed(e, views=views):
        for i, view in enumerate(views):
            view.visible = i == e.control.selected_index
        page.update()

    page.navigation_bar = ft.NavigationBar( # bottom bar
        selected_index=0,
        on_change=nav_changed,
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.icons.SETTINGS_VOICE_OUTLINED,
                selected_icon=ft.icons.SETTINGS_VOICE,
                label="Einstellung",
            ),
            ft.NavigationBarDestination(
                icon=ft.icons.MY_LIBRARY_BOOKS_OUTLINED,
                selected_icon=ft.icons.MY_LIBRARY_BOOKS,
                label="Verlauf",
            ),
            ft.NavigationBarDestination(
                icon=ft.icons.CASTLE_OUTLINED,
                selected_icon=ft.icons.CASTLE,
                label="Infos über Burgen",
            ),
        ],
    )
    
    
    page.appbar = ft.AppBar( # top bar
        leading=ft.Icon(ft.icons.RECORD_VOICE_OVER),
        leading_width=40,
        title=ft.Text(page.title),
        center_title=False,
        bgcolor=ft.colors.SURFACE_CONTAINER_HIGHEST,
        actions=[
            switch,
            ft.PopupMenuButton(
                items=[
                    #ft.PopupMenuItem(text="Item 1"),
                    #ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        text="Info", checked=None, on_click=lambda e: page.open(bottomsheet)
                    ),
                    ft.PopupMenuItem(
                        text="Quellcode", checked=None, on_click=lambda e: page.open(bottomsheet_quellcode)
                    )
                ]
            ),
        ],
    )

    page.add(
        einstellung_view,
        trend_view,
        infos_view,
    )


ft.app(main, assets_dir="assets") #  web_renderer=ft.WebRenderer.HTML

