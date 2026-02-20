import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QUrl, QLocale
from backend import Backend

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Notes")
    app.setOrganizationName("MyCompany")

    QLocale.setDefault(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates))

    icon_path = 'public/Logo_Ob.png'
    app.setWindowIcon(QIcon(icon_path))

    engine = QQmlApplicationEngine()
    backend = Backend()

    engine.rootContext().setContextProperty('backend', backend)

    qml_file = QUrl.fromLocalFile('main.qml')
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())