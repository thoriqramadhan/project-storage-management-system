def menuPrint(number, text):
    if (not number or not text ):
        print('Number or text is required')
        return
    print(f'{number}. {text}\n')

menus = ('Lihat Penyimpanan' , 'Ubah Penyimpanan')
while True:
    print('-------------- MENU STORAGE SYSTEM --------------')
    for i , val in enumerate(menus , start=1):
        menuPrint(i, val)
    choice = input(f'Pilih Menu 1 - {len(menus)} (atau "q" untuk keluar): ')
    if choice == 'q':
        print("Sampai jumpa!")
        break
    break