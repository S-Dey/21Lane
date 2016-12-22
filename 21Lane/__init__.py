from PyQt5.QtWidgets import QApplication, QDialog
import app, sys

if __name__=="__main__":
    if not ((sys.version_info.major == 3) and \
        (sys.version_info.minor >= 5)):
        print ("Sorry. PyQt5 requires at least Python3.5")
        sys.exit()
    q = QApplication([])
    d = QDialog()
    u = app.GUI(d)
    sys.exit(q.exec_())
