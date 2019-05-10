from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.utils import platform


Builder.load_string('''
#:import lv kivy.uix.listview
#:import la kivy.adapters.listadapter

<MyWidget>:
    drives_list: drives_list
    file_chooser: file_chooser
    ListView:
        id: drives_list
        adapter:
            la.ListAdapter(data=root.get_win_drives(), selection_mode='single', allow_empty_selection=False, cls=lv.ListItemButton)
    FileChooserListView:
        id: file_chooser
''')

class MyWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)
        self.drives_list.adapter.bind(on_selection_change=self.drive_selection_changed)

    def get_win_drives(self):
        if platform == 'win':
            import win32api

            drives = win32api.GetLogicalDriveStrings()
            drives = drives.split('\000')[:-1]

            return drives
        else:    
            return []

    def drive_selection_changed(self, *args):
        selected_item = args[0].selection[0].text
        self.file_chooser.path = selected_item

class TrucApp(App):
    def build(self):
        return MyWidget()

if __name__ == '__main__':
    TrucApp().run()