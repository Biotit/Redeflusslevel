import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
matplotlib.use("svg")


def trend(page, trdata, PrimaryColor):
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
            
            # Violin marker statistics Colors
            for partname in ('cbars','cmins','cmaxes', 'cmeans','cmedians'):
                vp = violin_parts[partname]
                vp.set_edgecolor(PrimaryColor)
            
            # main Colors of the violin
            for pc in violin_parts['bodies']:
                pc.set_facecolor(PrimaryColor)
                pc.set_edgecolor('black')
            
            page.open(ft.SnackBar(ft.Text(f"Verlaufsabbildungen auf dem neusten Stand. 📊")))
            vert.value = f"Gewünschter Redefluss von {np.datetime64(times[0], 's')} bis {np.datetime64(times[-1], 's')}."
            trfig.update()
        elif len(trdata) == 1:
            vert.value = f"Bisher erst einen Datenpunkt. Bitte weitere Daten mit dem Schieberegler erzeugen oder Daten laden."
            page.open(ft.SnackBar(ft.Text(f"⚠️ Daten zum Redefluss nicht ausreichend.")))
        else:
            vert.value = f"Keine Daten zum Redefluss bisher. Bitte einige Daten mit dem Schieberegler erzeugen."
            page.open(ft.SnackBar(ft.Text(f"⚠️ Keine Daten zum Redefluss.")))
        page.update()
            
    
    fig2, ax2 = plt.subplots(1, 2, sharey=True, width_ratios=[3, 1], figsize=(6, 4), constrained_layout=True)
    trfig = MatplotlibChart(figure=fig2, expand=True, isolated=True) # plotting trend data

    
    vert = ft.Text("Noch keine Daten.", 
        theme_style=ft.TextThemeStyle.BODY_LARGE, 
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER)
    
    
    def del_trend(_):
        if len(trdata) == 0:
            page.open(ft.SnackBar(ft.Text(f"⚠️ Es gibt keinen aktuellen Verlauf zum löschen.")))
        else:
            trdata.clear()
            page.open(ft.SnackBar(ft.Text(f"Verlauf gelöscht. 🗑️")))
            ax2[0].clear() # necessary otherwise figure content not deleted, see function trend(_) for len(trdata)==0.
            ax2[1].clear()
            trfig.update()
            trend(_)
        
    def save_trend(_):
        if len(trdata) == 0:
            page.open(ft.SnackBar(ft.Text(f"⚠️ Es gibt keinen Verlauf zum speichern.")))
        else:
            np.savetxt('trend_save/trend.csv', trdata, delimiter=",", fmt='%s')
            page.open(ft.SnackBar(ft.Text(f"Verlauf gespeichert. 💾")))
        
    def load_trend(_):
        try:
            loaded_trdata = np.genfromtxt('trend_save/trend.csv', dtype=str, 
                 delimiter=",", encoding="utf-8")
            #print(loaded_trdata)
            #print(loaded_trdata[:,0])
            times = [datetime.fromisoformat(t) for t in loaded_trdata[:, 0]]
            values = loaded_trdata[:, 1].astype(float)
            loaded_trdata = zip(times, values)
            trdata.clear()
        except:
            page.open(ft.SnackBar(ft.Text(f"⚠️ Alter Verlauf konnte nicht geladen werden! Vermutlich keiner oder leerer Verlauf bisher gespeichert. Bisheriger aktueller Verlauf nicht gelöscht.")))
        else:
            trdata.extend(loaded_trdata)
            page.open(ft.SnackBar(ft.Text(f"Alter Verlauf geladen. 📈")))
    
    def del_saved_trend(_):
        if os.path.exists("trend_save/trend.csv"):
            os.remove("trend_save/trend.csv")
            page.open(ft.SnackBar(ft.Text(f"Gespeicherter Verlauf gelöscht!")))
        else:
            page.open(ft.SnackBar(ft.Text(f"⚠️ Es existiert kein gespeicherter Verlauf.")))

    
    # -------- Summary and return --------
    trend_view = ft.Column(controls=[
        ft.ResponsiveRow(controls=[
            ft.Column(controls=[
                ft.Text("Verlauf", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                vert,
                ft.Container(content=trfig, width=800, height=600)
            ], 
            col={"sm": 12, "md": 9},
            expand=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Column(controls=[
                ft.ElevatedButton("Abbildung aktualisieren", on_click=trend),
                ft.ElevatedButton("Verlauf speichern", on_click=save_trend),
                ft.ElevatedButton("Gespeicherten Verlauf laden", on_click=load_trend),
                ft.ElevatedButton("Aktuellen Verlauf löschen", on_click=del_trend,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.RED_400,
                        color=ft.Colors.WHITE)),
                ft.ElevatedButton("Gespeicherten Verlauf löschen", 
                    on_click=del_saved_trend, style=ft.ButtonStyle(
                        bgcolor=ft.Colors.RED_400,
                        color=ft.Colors.WHITE))
            ], 
            expand=0.5, col={"sm": 12, "md": 3},
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER)
        ])
        ],
        visible=False,
    )
    return trend_view
