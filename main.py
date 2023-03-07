from functools import partial

from PySide6 import QtCore
from PySide6.QtCore import QDir, QItemSelectionModel, QSize, QStandardPaths
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QToolBar, QTreeView, QListView, QSlider, QHBoxLayout, QMainWindow, \
    QFileSystemModel, QHeaderView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyExplorer")
        self.setup_ui()
        self.create_file_model()

    def setup_ui(self):
        self.create_widgets()
        self.create_layouts()
        self.modify_widgets()
        self.add_widgets_to_layouts()
        self.add_actions_to_toolbar()
        self.setup_connections()

    def create_widgets(self):
        self.toolbar = QToolBar()
        self.tree_view = QTreeView()
        self.list_view = QListView()
        self.sld_iconSize = QSlider()
        self.main_widget = QWidget()

    def modify_widgets(self):
        #ajout du fichier pour changer la colométrie de l'interface
        css_file = "ressources/style.css"
        with open(css_file, "r") as f:
            self.setStyleSheet(f.read())

        #Modification la taille des dossiers/fichers dans l'apparence de la liste
        self.list_view.setViewMode(QListView.IconMode)
        self.list_view.setUniformItemSizes(True)
        self.list_view.setIconSize(QSize(48, 48))

        #Modification de la valeur de base de la slidebar
        self.sld_iconSize.setRange(48, 256)
        self.sld_iconSize.setValue(48)

        #Modification de la gestion de l'arborésence
        self.tree_view.setSortingEnabled(True)
        self.tree_view.setAlternatingRowColors(True)
        self.tree_view.header().setSectionResizeMode(QHeaderView.ResizeToContents)

    def create_layouts(self):
        self.main_layout = QHBoxLayout(self.main_widget)

    def add_widgets_to_layouts(self):
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)
        self.setCentralWidget(self.main_widget)
        self.main_layout.addWidget(self.tree_view)
        self.main_layout.addWidget(self.list_view)
        self.main_layout.addWidget(self.sld_iconSize)

    def add_actions_to_toolbar(self):
        locations = ["home", "desktop", "documents", "movies", "pictures", "music"]
        for location in locations:
            icon = f"./ressources/{location}.svg"
            action = self.toolbar.addAction(QIcon(icon), location.capitalize())
            action.triggered.connect(partial(self.change_location, location))

    def setup_connections(self):
        self.tree_view.clicked.connect(self.treeview_clicked)
        self.list_view.clicked.connect(self.listview_clicked)
        self.list_view.doubleClicked.connect(self.listview_double_clicked)
        self.sld_iconSize.valueChanged.connect(self.change_icon_size)

    def change_icon_size(self, value):
        self.list_view.setIconSize(QSize(value, value))

    def change_location(self, location):
        path = eval(f"QStandardPaths().standardLocations(QStandardPaths.{location.capitalize()}Location)")
        path = path[0]
        self.tree_view.setRootIndex(self.model.index(path))
        self.list_view.setRootIndex(self.model.index(path))

    def create_file_model(self):
        self.model = QFileSystemModel()
        root_path = QDir.rootPath()
        self.model.setRootPath(root_path)
        self.tree_view.setModel(self.model)
        self.list_view.setModel(self.model)
        self.list_view.setRootIndex(self.model.index(root_path))
        self.tree_view.setRootIndex(self.model.index(root_path))

    def treeview_clicked(self, index):
        if self.model.isDir(index):
            self.list_view.setRootIndex(index)
        else:
            self.list_view.setRootIndex(index.parent())

    def listview_clicked(self, index):
        self.tree_view.selectionModel().setCurrentIndex(index, QItemSelectionModel.ClearAndSelect)

    def listview_double_clicked(self, index):
        self.list_view.setRootIndex(index)


if __name__ == '__main__':
    app = QApplication()
    main_window = MainWindow()
    main_window.resize(1200, 600)
    main_window.show()
    app.exec()
