import flet as ft
from flet.matplotlib_chart import MatplotlibChart

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import uuid
import datetime
matplotlib.use("svg")


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

    # -------- Slider --------
    def slider_changed(_):
        value = slid.value
        if value <= 20:
            t.value = f"Hey! {value}% ist schon etwas fieß ... 🙁"
        elif value > 70:
            t.value = f"Uff! {value}% kann ganz schön anstrengend sein! 🥵"
        elif 20 < value <= 70:
            t.value = f"{value}% hört sich nach einem angenehmen Level an. 🙂"
        else:
            t.value = f"Redeflusslevel auf {value}% eingestellt!"
        page.update()
    
    t = ft.Text("Noch kein Wert eingestellt. Bitte Schieberegler betätigen.", 
        theme_style=ft.TextThemeStyle.BODY_LARGE, 
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER)

    def how_much_set(_, new=True):
        value = slid.value
        if not new:
            page.open(ft.SnackBar(ft.Text(f"Empfange externe Änderungen. Redeflusslevel oder Histogram geändert!")))
        if new:
            page.open(ft.SnackBar(ft.Text(f"Redeflusslevel auf {value}% eingestellt!")))
        trdata.append((datetime.datetime.now(), value)) # save data in list to plot history
        histogr(new)
    
    slid = ft.Slider(
                min=0,
                max=100,
                divisions=10,
                label="{value}%",
                on_change=slider_changed,
                on_change_end=how_much_set
            )
        
    # -------- Synchronisation --------
    # using PubSub, see flet help.
    # need to have same port to work.
    # e.g. flet run --web --port 8000 app.py
    
    session_id = str(uuid.uuid4()) # necessary to prevent receiving the own message send
    
    # subscribe to broadcast messages
    def on_message(msg):
        if msg.get("sender") == session_id: # if the message is from myself, then dont update
            return
        slid.value = msg["slid"]
        ns.value = msg["ns"]
        std.value = msg["std"]
        how_much_set(None, new=False) # prevent loops from one instance to the other by giving new=False
        slider_changed(None)
        page.update()
    
    page.pubsub.subscribe(on_message)
    
    def send():
        msg = {
            "sender": session_id,
            "slid":slid.value,
            "ns":ns.value,
            "std":std.value}
        page.pubsub.send_all(msg)
    
    # -------- Banner --------
    
    def close_banner(e):
        page.close(banner)
    
    banner = ft.Banner(
        #bgcolor=ft.colors.AMBER_100,
        leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, size=40), # color=ft.colors.AMBER,
        content=ft.Text(
            "Anleitung: Am folgenden Schieberegler durch Schieben nach rechts oder links das gewünschte Redeflusslevel von Daniel auswählen. Das Redeflusslevel kennzeichnet den angestrebten Anteil an gemeinsam verbrachter Zeit in der Daniel redet. Daniels tatsächliches Redeflusslevel kann durch eine Normalverteilung beschrieben werden, die sich um den eingestellten Wert als Mittelwert verteilt. Im Histogram wird diese beispielhaft beschrieben. Standardmäßig beschreibt das Histogram eine Normalverteilung mit 100 Proben, und einer Streuung von einer Standardabweichung. Um es zu präzisieren können auch manuell andere Werte eingegeben werden.",
            color=ft.colors.BLACK,
        ),
        actions=[
            ft.TextButton("OK", on_click=close_banner),
        ],
    )

    # -------- Histogram  --------
    def histogr(new=True): # new=False prevents loops of synchronisation, when calling histogr from a loop
        value = slid.value
        try:
            nsize = int(ns.value)
            stdn = int(std.value)
        except:
            nsize = 100
            stdn = 1
        ndv = np.random.normal(loc=value, scale=stdn, size=nsize)
        ax.clear()
        ax.hist(ndv, bins=20, color=PrimaryColor)
        ax.set_title(f"Zu erwartendes Redeflusshistogramm \n für einen Durchschnittswert von {value}%")
        ax.set_xlabel("Redefluss (%)")
        ax.set_ylabel("Häufigkeit")
        hist.update()
        if new:
            send() # only if new set value, send new values to other instances. Otherwise would end in loop between instances...

    fig, ax = plt.subplots(figsize=(4, 3), constrained_layout=True)
    hist = MatplotlibChart(fig, expand=True, isolated=True)
    ns = ft.TextField(label="Anzahl an Proben von einer Normalverteilung", on_blur=histogr)
    std = ft.TextField(label="Streuung der Normalverteilung", on_blur=histogr)

    # -------- Trend and violin plot --------
    def trend(_):
        if len(trdata) > 1:
            times, values = zip(*trdata) # unzip the tuples, only possible if there is already data.
            
            # Trend plot
            ax2[0].clear()
            ax2[0].plot(times, values, color=PrimaryColor)
            #ax.set_title("")
            ax2[0].set_xlabel("Datum")
            ax2[0].set_ylabel("Gewünschter Redefluss (%)")
            ax2[0].set_ylim(0,100)
            
            # Violin plot
            ax2[1].clear()
            ax2[1].set_xlabel("Wahrscheinlichkeits-\ndichtefunktion")
            violin_parts = ax2[1].violinplot(values, showmeans = True, showextrema = True, showmedians = True)
            
            # Violin marker statistics colors
            for partname in ('cbars','cmins','cmaxes', 'cmeans','cmedians'):
                vp = violin_parts[partname]
                vp.set_edgecolor(PrimaryColor)
            
            # main colors of the violin
            for pc in violin_parts['bodies']:
                pc.set_facecolor(PrimaryColor)
                pc.set_edgecolor('black')
            
            vert.value = f"Gewünschter Redefluss von {times[0]} bis {times[-1]}."
            trfig.update()
        elif len(trdata) == 1:
            vert.value = f"Bisher erst einen Datenpunkt. Bitte weitere Daten mit dem Schieberegler erzeugen."
        else:
            vert.value = f"Keine Daten zum Redefluss bisher. Bitte einige Daten mit dem Schieberegler erzeugen."
        page.update()
            
    
    fig2, ax2 = plt.subplots(1, 2, sharey=True, width_ratios=[3, 1], figsize=(6, 4), constrained_layout=True)
    trfig = MatplotlibChart(fig2, expand=True, isolated=True) # plotting trend data
    trdata = [] # empty list for storing data and time as tuples, converted
    
    vert = ft.Text("Noch keine Daten.", 
        theme_style=ft.TextThemeStyle.BODY_LARGE, 
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER)
    
    
    
    # -------- BottomSheet   --------
    bottomsheet = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    ft.Text("Erstellt für Oli von Daniel. ❤️ \nGutschein zur Programmierung geschenkt zu Olis 23. Geburtstag am 20.08.2025.",
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
    page.overlay.append(bottomsheet)

    # -------- Page layouts  --------
    

    einstellung_view = ft.Column(controls=[
        ft.Row(
            controls=[
                ft.Divider(leading_indent=15, trailing_indent=15),
                ft.Column(
                controls=[
                    ft.Text("Gewünschte Redeflusszeit von Daniel (%)", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                    slid,
                    t,
                    ft.Container(content=hist, width=500, height=500)
                    ],
                    expand=2,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            ft.Column(
                controls=[
                    ft.ElevatedButton("Anleitung", on_click=lambda e: page.open(banner)),
                    #ft.Divider(leading_indent=100, trailing_indent=100),
                    ns,
                    std,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.START
            )
        ], expand=True),
        ],
        visible=True,
    )

    trend_view = ft.Column(controls=[
        ft.Row(controls=[
            ft.Divider(leading_indent=15, trailing_indent=15),
            ft.Column(controls=[
                ft.Text("Verlauf", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                vert,
                ft.Container(content=trfig, width=800, height=600)
            ], expand=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Column(controls=[
                ft.ElevatedButton("Update Trend", on_click=trend)
            ], expand=0.5),
            ft.Divider(leading_indent=15, trailing_indent=15)
        ])
        ],
        visible=False,
    )

    infos_view = ft.Column(
        controls=[
            ft.Text("Infos über Burgen"),
            ft.Divider(leading_indent=15, trailing_indent=15)
        ],
        visible=False,
    )

    views = [einstellung_view, trend_view, infos_view]
    

    # -------- Navigation/Top and bottom bars  --------

    def nav_changed(e):
        for i, view in enumerate(views):
            view.visible = i == e.control.selected_index
        page.update()

    page.navigation_bar = ft.NavigationBar( # bottom bar
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
                label="Verlauf",
            ),
            ft.NavigationBarDestination(
                icon=ft.icons.CASTLE,
                selected_icon=ft.icons.CASTLE_OUTLINED,
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

