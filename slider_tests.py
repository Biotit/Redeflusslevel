import flet as ft
from flet.matplotlib_chart import MatplotlibChart

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use("svg")


def main(page):
    page.title = "Olis Kontrollapp über Daniels Redefluss"
    page.scroll = ft.ScrollMode.ADAPTIVE

    def slider_changed(e):
        value = e.control.value
        if value <= 20:
            t.value = f"Hey! {value}% ist schon etwas fieß ... 🙁"
        elif value > 70:
            t.value = f"Uff! {value}% kann ganz schön anstregend sein! 🥵"
        elif 20 < value <= 70:
            t.value = f"{value}% hört sich nach einem angenehmen Level an. 🙂"
        else:
            t.value = f"Redeflusslevel auf {value}% eingestellt!"
        page.update()

    def close_banner(e):
        page.close(banner)
    
    def how_much_set(e):
        value = e.control.value
        page.open(ft.SnackBar(ft.Text(f"Redeflusslevel auf {value}% eingstellt!")))
        histogr(e)

    # -------- Banner --------

    banner = ft.Banner(
        bgcolor=ft.colors.AMBER_100,
        leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
        content=ft.Text(
            "Anleitung: Am folgenden Schieberegler durch Schieben nach rechts oder links das gewünschte Redeflusslevel von Daniel auswählen. Das Redeflusslevel kennzeichnet den angestrebten Anteil an gemeinsam verbrachter Zeit in der Daniel redet. Daniels tatsächliches Redeflusslevel kann durch eine Normalverteilung beschrieben werden, die sich um den eingestellten Wert als Mittelwert verteilt. Im Histogram wird diese beispielhaft beschrieben. Standardmäßig beschreibt das Histogram eine Normalverteilung mit 100 Proben, und einer Streuung von einer Standardabweichung. Um es zu präzisieren können auch manuell andere Werte eingegeben werden.",
            color=ft.colors.BLACK,
        ),
        actions=[
            ft.TextButton("OK", on_click=close_banner),
        ],
    )

    # -------- Histogram  --------
    def histogr(e):
        value = slid.value
        try:
            nsize = int(ns.value)
            stdn = int(std.value)
        except:
            nsize = 100
            stdn = 1
        ndv = np.random.normal(loc=value, scale=stdn, size=nsize)
        ax.clear()
        ax.hist(ndv, bins=20)
        ax.set_title(f"Zu erwartendes Redeflusshistogramm \n für einen Durchschnittswert von {value}%")
        ax.set_xlabel("Redefluss (%)")
        ax.set_ylabel("Häufigkeit")
        hist.update()

    
    
    
    
    # -------- Views --------

    t = ft.Text("Noch kein Wert eingestellt. Bitte Schieberegler betätigen.", theme_style=ft.TextThemeStyle.BODY_LARGE)
    
    fig, ax = plt.subplots(figsize=(4, 3), constrained_layout=True)
    hist = MatplotlibChart(fig, expand=True, isolated=True)
    ns = ft.TextField(label="Anzahl an Proben von einer Normalverteilung", on_change=histogr)
    std = ft.TextField(label="Streuung der Normalverteilung", on_change=histogr)
    slid = ft.Slider(
                min=0,
                max=100,
                divisions=10,
                label="{value}%",
                on_change=slider_changed,
                on_change_end=how_much_set
            )

    einstellung_view = ft.Column(controls=[
        ft.Row(
            controls=[
                ft.Column(
                controls=[
                    ft.Text("Gewünschte Redeflusszeit von Daniel (%)", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.ElevatedButton("Anleitung", on_click=lambda e: page.open(banner)),
                    slid,
                    t,
                    ft.Container(content=hist, width=500, height=500)
                    ],
                    expand=2
            ),
            ft.Column(
                controls=[
                    ns,
                    std,
                ]
            )
        ]),
        ],
        visible=True,
    )

    hintergrund_view = ft.Column(
        controls=[ft.Text("Hintergrund Inhalt")],
        visible=False,
    )

    infos_view = ft.Column(
        controls=[ft.Text("Infos über Burgen")],
        visible=False,
    )

    views = [einstellung_view, hintergrund_view, infos_view]
    

    # -------- Navigation --------

    def nav_changed(e):
        for i, view in enumerate(views):
            view.visible = i == e.control.selected_index
        page.update()

    page.navigation_bar = ft.NavigationBar(
        selected_index=0,
        on_change=nav_changed,
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.icons.SETTINGS_VOICE,
                selected_icon=ft.icons.SETTINGS_VOICE_OUTLINED,
                label="Einstellung",
            ),
            ft.NavigationBarDestination(
                icon=ft.icons.MY_LIBRARY_BOOKS,
                selected_icon=ft.icons.MY_LIBRARY_BOOKS_OUTLINED,
                label="Hintergrund",
            ),
            ft.NavigationBarDestination(
                icon=ft.icons.CASTLE,
                selected_icon=ft.icons.CASTLE_OUTLINED,
                label="Infos über Burgen",
            ),
        ],
    )

    page.add(
        einstellung_view,
        hintergrund_view,
        infos_view,
    )


ft.app(main)

