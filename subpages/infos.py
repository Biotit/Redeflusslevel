import flet as ft
from pathlib import Path

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
                label_content=ft.Text("Burgenbuch\n&\nGermanCastleProductions", text_align=ft.TextAlign.CENTER),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.MAP_OUTLINED,
                selected_icon=ft.icons.MAP,
                label_content=ft.Text("OpenStreetMap"),
            ),
        ],
        on_change=lambda e: nav_changed(e, views=infosburgen))
    
    
    # -------- Infos über Burgen Seiten  --------
    
    md_infob_1 = Path("subpages/infos_texts/infob_1.md").read_text(encoding="utf-8")
    md_infob_2 = Path("subpages/infos_texts/infob_2.md").read_text(encoding="utf-8")
    
    
    md_infob_3 = Path("subpages/infos_texts/infob_3.md").read_text(encoding="utf-8")
    md_infob_3_germ = Path("subpages/infos_texts/infob_3_germ.md").read_text(encoding="utf-8")
    
    
    infob_1 = ft.Column(controls=[
                            ft.Markdown(
                                md_infob_1,
                                selectable=True,
                                soft_line_break=True,
                                extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                                on_tap_link=lambda e: page.launch_url(e.data),
                                )
                            ], visible=True, expand=True,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                            alignment=ft.MainAxisAlignment.START)
    infob_2 = ft.Column(controls=[
                            ft.Markdown(
                                md_infob_2,
                                selectable=True,
                                soft_line_break=True,
                                extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                                on_tap_link=lambda e: page.launch_url(e.data),
                                )
                            ],
                            visible=False, expand=True)
    infob_3 = ft.Column(controls=[
                            ft.Markdown(
                                md_infob_3_germ,
                                #md_infob_3,
                                selectable=True,
                                soft_line_break=True,
                                extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                                on_tap_link=lambda e: page.launch_url(e.data),
                                )
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
                    content=ft.Column(
                        controls=infosburgen
                    ),
                    expand=True,
                ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.START) # thats the import setting! :)
        ], alignment=ft.MainAxisAlignment.START,
        visible=False,
    )
    return infos_view
