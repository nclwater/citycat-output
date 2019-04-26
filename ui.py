from PyQt5.QtWidgets import QApplication, QFileDialog
from citycat_output import Run
import sys

app = QApplication([])
Run(QFileDialog.getExistingDirectory()).to_netcdf()
sys.exit()
