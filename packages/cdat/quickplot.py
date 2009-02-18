from cdat_cell import QCDATWidget
from core.modules.vistrails_module import (Module, ModuleError, NotCacheable)
from packages.spreadsheet.spreadsheet_controller import spreadsheetController
from packages.spreadsheet.spreadsheet_event import DisplayCellEvent
from PyQt4 import QtCore, QtGui

class quickplot(Module, NotCacheable):
    """hackiness to push a cdat plot to our spreadsheet.
       needs: QCDATWidget ref
              cdms2.open()d dataset
              blah this is out of date variable name"""

    def compute(self):
        args = []
        if not self.hasInputFromPort('dataset'):
            raise ModuleError(self, "'dataset' is mandatory.")
        if not self.hasInputFromPort('plot'):
            raise ModuleError(self, "'plot' is mandatory.")

        dataset = self.getInputFromPort('dataset')
        plotType = self.getInputFromPort('plot')
        axes = self.forceGetInputFromPort('axes')
        inCanvas = self.forceGetInputFromPort('canvas')
        if axes!=None:
            try:
                kwargs = eval(axes)
            except:
                raise ModuleError(self, "Invalid 'axes' specification", axes)
            dataset = dataset(**kwargs)

        outCanvas = None
        if inCanvas!=None:
            inCanvas.plot(dataset, 'ASD', plotType)
            outCanvas = inCanvas
        else:
            ev = DisplayCellEvent()
            ev.vistrail = {'locator': None, 'version': -1, 'actions': []}
            ev.cellType = QCDATWidget
            ev.inputPorts = (dataset, 'ASD', plotType)
            QtCore.QCoreApplication.processEvents()
            spreadsheetWindow = spreadsheetController.findSpreadsheetWindow()
            cdatWidget = spreadsheetWindow.displayCellEvent(ev)
            if cdatWidget!=None:
                outCanvas = cdatWidget.canvas
        self.setResult('dataset', dataset)
        self.setResult('canvas', outCanvas)
