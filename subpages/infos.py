import flet as ft

def infos(page):
    # -------- Navigation rail on Infos über Burgen -----
    def nav_changed(e, views):
        for i, view in enumerate(views):
            view.visible = i == e.control.selected_index
        page.update()
    
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        #leading=ft.FloatingActionButton(
        #    icon=ft.icons.CREATE, text="Add", on_click=lambda e: print("FAB clicked!")
        #),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.FORT_OUTLINED,
                selected_icon=ft.icons.FORT,
                label_content=ft.Text("Geschichte\n&\nBauformen", text_align=ft.TextAlign.CENTER),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.LIBRARY_BOOKS_OUTLINED,
                selected_icon=ft.icons.LIBRARY_BOOKS,
                label_content=ft.Text("Daniels\nBurgenbuch", text_align=ft.TextAlign.CENTER),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.MAP_OUTLINED,
                selected_icon=ft.icons.MAP,
                label_content=ft.Text("OpenStreetMap"),
            ),
        ],
        on_change=lambda e: nav_changed(e, views=infosburgen))
    
    
    # -------- Infos über Burgen Seiten  --------
    infob_1 = ft.Column(controls=[
                            ft.Text('Geschichte & Bauformen', 
                                theme_style=ft.TextThemeStyle.HEADLINE_SMALL)
                            ], visible=True, expand=True,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                            alignment=ft.MainAxisAlignment.START)
    infob_2 = ft.Column(controls=[
                            ft.Text('Daniels Burgenbuch',
                                theme_style=ft.TextThemeStyle.HEADLINE_SMALL)
                            ], visible=False, expand=True)
    infob_3 = ft.Column(controls=[
                            ft.Text('OpenStreetMap', 
                                theme_style=ft.TextThemeStyle.HEADLINE_SMALL)
                            ], visible=False, expand=True)
    infosburgen = [infob_1, infob_2, infob_3]
    
    
    # -------- Summary and return --------
    infos_view = ft.Column(
        controls=[
            ft.Row(controls=[
                ft.Container(
                    content=rail,
                    height=page.height,
                 ),
                ft.VerticalDivider(width=1),
                ft.Container(
                    content=ft.Column(controls=infosburgen), # directly pass list as control list
                    height=page.height)
                ])
        ], expand=True,
        visible=False,
    )
    return infos_view
