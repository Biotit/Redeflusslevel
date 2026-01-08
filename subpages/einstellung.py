import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import datetime
import uuid
matplotlib.use("svg")

def einstellung(page, trdata, PrimaryColor):

    
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

    # -------- Banner --------
    def close_banner(e):
        page.close(banner)
    
    banner = ft.Banner(
        #bgcolor=ft.colors.AMBER_100,
        leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, size=40), # color=ft.colors.AMBER,
        content=ft.Text(
            "Anleitung: Am folgenden Schieberegler durch Schieben nach rechts oder links das gewünschte Redeflusslevel von Daniel auswählen. Das Redeflusslevel kennzeichnet den angestrebten Anteil an gemeinsam verbrachter Zeit in der Daniel redet. Daniels tatsächliches Redeflusslevel kann durch eine Normalverteilung beschrieben werden, die sich um den eingestellten Wert als Mittelwert verteilt. Im Histogram wird diese beispielhaft beschrieben. Standardmäßig beschreibt das Histogram eine Normalverteilung mit 100 Proben, und einer Streuung von einer Standardabweichung. Um es zu präzisieren können auch manuell andere Werte eingegeben werden.\n \n Achtung! Zum Verändern des Werts den Slider schieben und an der gewünschten neuen Position loslassen, nicht einfach auf eine andere Position klicken!",
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

    # -------- Summarizing and return   --------
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
    return einstellung_view
