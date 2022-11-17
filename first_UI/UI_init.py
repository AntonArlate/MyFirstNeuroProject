import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from neural_network.network import neural_matrix as n_matr


class Neuron_matrix(QtWidgets.QGroupBox):
    def __init__(self, pa, tag_line):
        super().__init__(par)
        self.setObjectName("NeuronMatrix")
        self.layers = []

        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName(tag_line)

    



    def add_layer (self, tag_title, tag_line):
        temp = self.Neuron_layer(self, tag_line)
        temp.setObjectName(tag_title)
        temp.setTitle(tag_title)
        self.layers.append(temp)
        self.horizontalLayout.addWidget(temp)


    
    class Neuron_layer(QtWidgets.QGroupBox):
        def __init__(self, par, tag_line):
            super().__init__(par)
            self.neurons = []

            self.verticalLayout = QtWidgets.QHBoxLayout(self)
            self.verticalLayout.setObjectName(tag_line)

    def add_neuron (self, line, tag_title, tag_line):
        temp = self.layers[line].Neuron_number(self, tag_line)
        temp.setObjectName(tag_title)
        temp.setTitle(tag_title)
        self.neurons.append(temp)
        self.verticalLayout.addWidget(temp)


        class Neuron_number:

            class Neuron_data:
                pass

# aaa = Neuron_matrix(self.centralwidget, "horizontalLayout")
# aaa.setGeometry(QtCore.QRect(40, 20, 221, 361))
# aaa.setObjectName("NeuronMatrix")

# for n_layer in range(len(n_matr)):
#     aaa.add_layer("Layer " + str(n_layer))
#     for neuron_num in range(len(n_matr[n_layer])):
#         aaa.layers[n_layer].add_neuron(tag_title, tag_line)
#         Neuron_matrix.Neuron_layer.add_neuron




class Ui_Wiever(object):
    def setupUi(self, Wiever):
        Wiever.setObjectName("Wiever")
        Wiever.resize(840, 607)
        Wiever.setAnimated(True)
        self.centralwidget = QtWidgets.QWidget(Wiever)
        self.centralwidget.setObjectName("centralwidget")
        self.NeuronMatrix = QtWidgets.QGroupBox(self.centralwidget)
        self.NeuronMatrix.setGeometry(QtCore.QRect(40, 20, 221, 550))
        self.NeuronMatrix.setObjectName("NeuronMatrix")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.NeuronMatrix)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.neuron_layer = []
        self.vertical_lay = []
        for n_layer in range(len(n_matr)):

            self.neuron_layer.append (QtWidgets.QGroupBox(self.NeuronMatrix))
            self.neuron_layer[n_layer].setObjectName("Layer" + str(n_layer))
            self.neuron_layer[n_layer].setTitle("Layer " + str(n_layer))
            self.vertical_lay.append(QtWidgets.QVBoxLayout(self.neuron_layer[n_layer]))
            self.vertical_lay[n_layer].setObjectName("vertical_lay" + str(n_layer))

            self.NeuronData = []
            self.verticalLayout_n_data = []
            for neuron_num_iter in range(len(n_matr[n_layer])):
                self.NeuronData.append(QtWidgets.QGroupBox(self.neuron_layer[n_layer]))
                self.NeuronData[neuron_num_iter].setFlat(False)
                self.NeuronData[neuron_num_iter].setCheckable(False)
                self.NeuronData[neuron_num_iter].setObjectName("Neuron num" + str(neuron_num_iter))
                self.NeuronData[neuron_num_iter].setTitle("N "+ str(neuron_num_iter))
                self.verticalLayout_n_data.append(QtWidgets.QVBoxLayout(self.NeuronData[neuron_num_iter]))
                self.verticalLayout_n_data[neuron_num_iter].setObjectName("verticalLayout_n_data" + str(neuron_num_iter))
            
                self.label = []
                for data_value_iter in range(1):
                    self.label.append(QtWidgets.QLabel(self.NeuronData[neuron_num_iter]))
                    self.label[data_value_iter].setEnabled(True)
                    self.label[data_value_iter].setObjectName("label" + str(data_value_iter))
                    self.verticalLayout_n_data[neuron_num_iter].addWidget(self.label[data_value_iter])
                    self.label[data_value_iter].setText((str(n_matr[n_layer][neuron_num_iter])))
                self.vertical_lay[n_layer].addWidget(self.NeuronData[neuron_num_iter])
            self.horizontalLayout.addWidget(self.neuron_layer[n_layer])

        self.btn_start_stop = QtWidgets.QPushButton(self.centralwidget)
        self.btn_start_stop.setGeometry(QtCore.QRect(690, 500, 91, 41))
        self.btn_start_stop.setCheckable(False)
        self.btn_start_stop.setAutoDefault(False)
        self.btn_start_stop.setDefault(False)
        self.btn_start_stop.setFlat(False)
        self.btn_start_stop.setObjectName("btn_start_stop")
        Wiever.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Wiever)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 840, 21))
        self.menubar.setObjectName("menubar")
        Wiever.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Wiever)
        self.statusbar.setObjectName("statusbar")
        Wiever.setStatusBar(self.statusbar)

        self.retranslateUi(Wiever)
        QtCore.QMetaObject.connectSlotsByName(Wiever)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.upd)
        self.timer.start(100)

    def upd(self):
        for l in range(len(n_matr)):
            for n in range(len(n_matr[l])):
                self.label[0].setText((str(n_matr[l][n])))
                # print(l, ' ', n, ' - ', n_matr[l][n])


    def retranslateUi(self, Wiever):
        _translate = QtCore.QCoreApplication.translate
        Wiever.setWindowTitle(_translate("Wiever", "MainWindow"))
        self.NeuronMatrix.setTitle(_translate("Wiever", "NeuronMatrix"))



        self.btn_start_stop.setText(_translate("Wiever", "Start/Stop"))


def start_pyqt (thr_name, q):

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Wiever()
    ui.setupUi(MainWindow)
    MainWindow.show()

    q.task_done()

    sys.exit(app.exec_())

if __name__ == '__main__':
    start_pyqt("aaa", 14)