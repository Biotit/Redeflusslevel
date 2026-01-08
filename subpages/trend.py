import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
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
            
            # Violin marker statistics colors
            for partname in ('cbars','cmins','cmaxes', 'cmeans','cmedians'):
                vp = violin_parts[partname]
                vp.set_edgecolor(PrimaryColor)
            
            # main colors of the violin
            for pc in violin_parts['bodies']:
                pc.set_facecolor(PrimaryColor)
                pc.set_edgecolor('black')
            
            page.open(ft.SnackBar(ft.Text(f"Verlaufsabbildungen auf dem neusten Stand. 📊")))
            vert.value = f"Gewünschter Redefluss von {np.datetime64(times[0], 's')} bis {np.datetime64(times[-1], 's')}."
            trfig.update()
        elif len(trdata) == 1:
            vert.value = f"Bisher erst einen Datenpunkt. Bitte weitere Daten mit dem Schieberegler erzeugen."
        else:
            vert.value = f"Keine Daten zum Redefluss bisher. Bitte einige Daten mit dem Schieberegler erzeugen."
        page.update()
            
    
    fig2, ax2 = plt.subplots(1, 2, sharey=True, width_ratios=[3, 1], figsize=(6, 4), constrained_layout=True)
    trfig = MatplotlibChart(fig2, expand=True, isolated=True) # plotting trend data

    
    vert = ft.Text("Noch keine Daten.", 
        theme_style=ft.TextThemeStyle.BODY_LARGE, 
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER)
    
    
    def del_trend(_):
        trdata.clear()
        page.open(ft.SnackBar(ft.Text(f"Verlauf gelöscht. 🗑️")))
        ax2[0].clear() # necessary otherwise figure content not deleted, see function trend(_) for len(trdata)==0.
        ax2[1].clear()
        trfig.update()
        trend(_)
    
    
    # -------- Summary and return --------
    trend_view = ft.Column(controls=[
        ft.Row(controls=[
            ft.Divider(leading_indent=15, trailing_indent=15),
            ft.Column(controls=[
                ft.Text("Verlauf", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                vert,
                ft.Container(content=trfig, width=800, height=600)
            ], expand=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Column(controls=[
                ft.ElevatedButton("Update Trend", on_click=trend),
                ft.ElevatedButton("Verlauf löschen", on_click=del_trend)
            ], expand=0.5),
            ft.Divider(leading_indent=15, trailing_indent=15)
        ])
        ],
        visible=False,
    )
    return trend_view
