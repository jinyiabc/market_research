from PyQt5.Qt import *
from PyQt5.QtCore import pyqtSlot as Slot
from WindPy import w
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import globaldef
import ui_quote
import wsq

w.start()

MAC = True
try:
    from PyQt5.QtGui import qt_mac_set_native_menubar
except ImportError:
    MAC = False


class QuoteDlg(QDialog, ui_quote.Ui_Dialog):

    def __init__(self, parent=None):
        super(QuoteDlg, self).__init__(parent)
        self.setupUi(self)
        self.sec1Edit.setFocus()
        self.setWindowTitle("Wind API Demo---WSQ Subscrib")
        self.updateUi()
        self.initGraph()

    def initGraph(self):
        self.scene = QGraphicsScene()
        self.dr = Figure_Canvas()
        self.scene.addWidget(self.dr)
        self.graphicsView.setScene(self.scene)

    @Slot()
    def on_subscribeButton_clicked(self):
        self.subscribeButton.setEnabled(False)
        self.cancelButton.setEnabled(True)
        self.textBrowser.clear()
        globaldef.secID = []
        globaldef.indID = []
        globaldef.secID.extend([self.sec1Edit.text().upper(), self.sec2Edit.text().upper()])
        globaldef.indID.extend(['rt_time'.upper(), 'rt_bid1'.upper(), 'rt_ask1'.upper(),
                                'rt_bsize1'.upper(), 'rt_asize1'.upper(), 'rt_last'.upper()])
        self.qThread = wsq.feeder()
        self.qThread.start()
        self.qThread.update_data.connect(self.handle_display)
        self.qThread.update_data.connect(self.handle_graphic)

    def handle_display(self, data):
        # Update UI
        self.last1Edit.setText('{0:.4f}'.format(data[0][5]))
        self.last2Edit.setText('{0:.4f}'.format(data[1][5]))
        self.bidvol1Edit.setText('{0:.4f}'.format(data[0][3]))
        self.bidvol2Edit.setText('{0:.4f}'.format(data[1][3]))
        self.bid1Edit.setText('{0:.4f}'.format(data[0][1]))
        self.bid2Edit.setText('{0:.4f}'.format(data[1][1]))
        self.ask1Edit.setText('{0:.4f}'.format(data[0][2]))
        self.ask2Edit.setText('{0:.4f}'.format(data[1][2]))
        self.askvol1Edit.setText('{0:.4f}'.format(data[0][4]))
        self.askvol2Edit.setText('{0:.4f}'.format(data[1][4]))
        self.spread1Edit.setText('{0:.4f}'.format(globaldef.spreadBid))
        self.spread2Edit.setText('{0:.4f}'.format(globaldef.spreadAsk))
        self.textBrowser.append("<b>%s</b> | Spd_Bid:<b>%s</b> | Spd_Ask:<b>%s</b>|"
                                % (str(int(data[0][0])).zfill(6), '{0:.4f}'.format(globaldef.spreadBid),
                                   '{0:.4f}'.format(globaldef.spreadAsk)))

    def handle_graphic(self, data):
        self.dr.plot()

    @Slot()
    def on_cancelButton_clicked(self):
        self.subscribeButton.setEnabled(True)
        self.cancelButton.setEnabled(False)
        self.qThread.finished()

    @Slot(str)
    def on_sec1Edit_textEdited(self, text):
        self.updateUi()

    @Slot(str)
    def on_sec2Edit_textEdited(self, text):
        self.updateUi()

    def updateUi(self):
        enable = bool(self.sec1Edit.text()) and bool(self.sec2Edit.text())
        self.subscribeButton.setEnabled(enable)
        self.cancelButton.setEnabled(enable)


class Figure_Canvas(FigureCanvas):
    """
    Derived from class FigureCanvas, so that this class is both a Qwidget of PyQt5 and a FigureCanvas of matplotlib.
    This is a key step to link PyQt5 and matplotlib
    """

    def __init__(self, parent=None, width=7.4, height=5, dpi=100):
        # Create an Figure. Note that this is figure of matplotlib rather a figure of matplotlib.pyplot
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)  # Initialize the parent class
        self.setParent(parent)
        # Call method add_subplot of figure, which is similar to method subplot of matplotlib.pyplot
        self.axes1 = fig.add_subplot(311)
        self.axes2 = fig.add_subplot(312)
        self.axes3 = fig.add_subplot(313)

    def plot(self):
        self.axes1.clear()
        self.axes1.plot(globaldef.plotTime, globaldef.plotLast, color='k', alpha=0.9, linewidth=0.5)
        self.axes1.xaxis.set_visible(False)
        self.axes1.set_title("Real Time Spread_Last Trend Graph", fontsize=10)
        self.axes2.clear()
        self.axes2.plot(globaldef.plotTime, globaldef.plotBid, color='k', alpha=0.9, linewidth=0.5)
        self.axes2.xaxis.set_visible(False)
        self.axes2.set_title("Real Time Spread_Bid Trend Graph", fontsize=10)
        self.axes3.clear()
        self.axes3.plot(globaldef.plotTime, globaldef.plotAsk, color='k', alpha=0.9, linewidth=0.5)
        self.axes3.set_title("Real Time Spread_Ask Trend Graph", fontsize=10)
        self.draw()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = QuoteDlg()
    form.show()
    app.exec_()
