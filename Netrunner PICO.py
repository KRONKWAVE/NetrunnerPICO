from menu import ident_menu, corp_menu, runner_menu, jinteki_menu, hb_menu, nbn_menu, weyland_menu, anarch_menu, criminal_menu, shaper_menu

menus = [ident_menu, corp_menu, runner_menu, jinteki_menu, hb_menu,
         nbn_menu, weyland_menu, anarch_menu, criminal_menu, shaper_menu]

ident_menu.active = True

while True:
    for menu in menus:
        if menu.active:
            next_menu = None
            next_menu = menu.run_menu()
            if next_menu == 'Main':
                ident_menu.active = True
            if next_menu == 'Corp':
                corp_menu.active = True
            if next_menu == 'Runner':
                runner_menu.active = True
            if next_menu == 'Jinteki':
                jinteki_menu.active = True
            if next_menu == 'Haas Bioroid':
                hb_menu.active = True
            if next_menu == 'NBN':
                nbn_menu.active = True
            if next_menu == 'Weyland':
                weyland_menu.active = True
            if next_menu == 'Anarch':
                anarch_menu.active = True
            if next_menu == 'Criminal':
                criminal_menu.active = True
            if next_menu == 'Shaper':
                shaper_menu.active = True
            menu.display.update()
