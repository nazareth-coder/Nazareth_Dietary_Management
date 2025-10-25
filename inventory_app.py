import os
from ttkbootstrap import Window
from ui import InventoryApp
from db_utils import init_db

def main():
    init_db()
    root = Window(themename='minty')
    app = InventoryApp(root)
    root.mainloop()


if __name__ == '__main__':
    init_db()
    root = Window(themename='minty')
    try:
        # root.iconbitmap('icon.ico')
        root.iconbitmap(resource_path('icon.ico'))
    except Exception:
        pass
    root.title('Daito.dev')
    root.geometry('1366x768')
    app = InventoryApp(root)
    root.mainloop()
