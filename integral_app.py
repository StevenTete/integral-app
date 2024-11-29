import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QWidget, QGroupBox, QTabWidget, QMessageBox
)
from PyQt5.QtGui import QFont, QColor, QIcon
from PyQt5.QtCore import QSize
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class IntegralApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora de integración definida para métodos numéricos")
        self.setGeometry(200, 200, 900, 700)
        self.setWindowIcon(QIcon('integral-icon.png'))
        self.showMaximized()
        self.initUI()

    def initUI(self):
        # Cargar fuente Poppins
        QApplication.setFont(QFont("Poppins", 12))

        # Layout para la izquierda (inputs y botón)
        left_layout = QVBoxLayout()

        # Grupo para inputs
        inputs_group = QGroupBox("Parámetros de Entrada")
        inputs_group.setStyleSheet("QGroupBox { font-weight: medium; font-size: 24px;}")
        inputs_layout = QVBoxLayout()

        # Función
        self.func_input = QLineEdit("1/(1-0.8**2)*np.sqrt(1-0.8**2*(np.sin(x))**2)")
        inputs_layout.addWidget(self.create_input("Función f(x):", self.func_input))

        # Límite inferior
        self.a_input = QLineEdit("0.0")
        inputs_layout.addWidget(self.create_input("Límite inferior a:", self.a_input))

        # Límite superior
        self.b_input = QLineEdit("np.pi/2")
        inputs_layout.addWidget(self.create_input("Límite superior b:", self.b_input))

        # Número de rectángulos
        self.n_input = QLineEdit("8")
        inputs_layout.addWidget(self.create_input("Número de rectángulos n:", self.n_input))

        inputs_group.setLayout(inputs_layout)

        # Botón de calcular
        self.calculate_button = QPushButton("Calcular Integral")
        self.calculate_button.setFixedHeight(40)
        self.calculate_button.setFont(QFont("Poppins", 14, QFont.Bold))
        self.calculate_button.setIcon(QIcon('calculate-icon.png'))
        self.calculate_button.setIconSize(QSize(18, 18))
        self.calculate_button.setText(" Calcular")
        self.calculate_button.setStyleSheet("border-radius: 5px; cursor: pointer; border: 1px solid #ccc; background-color: #f0f0f0;")
        self.calculate_button.clicked.connect(self.start_calculation)

        left_layout.addWidget(inputs_group)
        left_layout.addWidget(self.calculate_button)

        # Layout para la derecha (tabla y gráfica en tabs)
        right_layout = QVBoxLayout()

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setFont(QFont("Poppins", 12))

        # Tab de tabla
        self.table_tab = QWidget()
        self.table_layout = QVBoxLayout(self.table_tab)
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Área Izquierda", "Área Derecha", "Área Central"])
        self.table.setFont(QFont("Poppins", 12))
        self.table.setStyleSheet("gridline-color: #dcdcdc;")
        self.table_layout.addWidget(self.table)

        # Tab de gráfica
        self.graph_tab = QWidget()
        self.graph_layout = QVBoxLayout(self.graph_tab)
        self.canvas = FigureCanvas(plt.figure())
        self.graph_layout.addWidget(self.canvas)

        # Agregar ambas pestañas al TabWidget
        self.tabs.addTab(self.table_tab, "Tabla de Resultados")
        self.tabs.addTab(self.graph_tab, "Gráfica")

        # Agregar tabs a la parte derecha
        right_layout.addWidget(self.tabs)

        # Layout principal
        central_widget = QWidget()
        central_layout = QHBoxLayout(central_widget)
        central_layout.addLayout(left_layout, 1)
        central_layout.addLayout(right_layout, 2)

        self.setCentralWidget(central_widget)

    def create_input(self, label_text, input_widget):
        container = QWidget()
        layout = QVBoxLayout(container)
        label = QLabel(label_text)
        label.setFont(QFont("Poppins", 12))
        layout.addWidget(label)
        input_widget.setFont(QFont("Poppins", 12))
        input_widget.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 5px;")
        layout.addWidget(input_widget)
        return container

    def start_calculation(self):
        try:
            # Obtener parámetros
            f = self.func_input.text()
            a = eval(self.a_input.text())
            b = eval(self.b_input.text())
            n = int(self.n_input.text())

            # Crear vector x y cálculos
            x = np.linspace(a, b, n + 1)
            x_centro = (x[1:] + x[:-1]) / 2
            delta_x = (b - a) / n

            # Evaluación de la función f(x)
            y = eval(f)
            y_centro = eval(f.replace('x', 'x_centro'))
            area_izq = [delta_x * y[i] for i in range(n)] + [np.sum(delta_x * y[:-1])]
            area_der = [delta_x * y[i + 1] for i in range(n)] + [np.sum(delta_x * y[1:])]
            area_centro = [delta_x * y_centro[i] for i in range(n)] + [np.sum(delta_x * y_centro)]

            # Mostrar resultados en la tabla
            self.table.setRowCount(n + 1)
            for i in range(n + 1):
                self.table.setItem(i, 0, QTableWidgetItem(str(area_izq[i])))
                self.table.setItem(i, 1, QTableWidgetItem(str(area_der[i])))
                self.table.setItem(i, 2, QTableWidgetItem(str(area_centro[i])))

            # Ajustar automáticamente el tamaño de las columnas
            self.table.resizeColumnsToContents()

            # Resaltar fila final (TOTAL)
            for col in range(3):
                self.table.item(n, col).setBackground(QColor("#ffb2b2"))
                self.table.item(n, col).setFont(QFont("Poppins", 12, QFont.Bold))

            # Mostrar gráfica
            self.plot_graph(x_centro, y, y_centro)

        except Exception as e:
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setWindowTitle("Error")
            error_dialog.setWindowIcon(QIcon('integral-icon.png'))
            error_dialog.setText("Por favor, revise los parámetros.")
            error_dialog.setInformativeText(str(e))
            error_dialog.setStandardButtons(QMessageBox.Ok)
            error_dialog.exec_()

    def plot_graph(self, x, y, y_centro):
        fig = self.canvas.figure
        fig.clf()
        ax = fig.add_subplot(111)
        ax.plot(x, y[:len(x)], label='f(x)', color='red')
        ax.fill_between(x, y[:len(x)], color='red', alpha=0.3)
        ax.grid(True)
        ax.set_title('Gráfica de la función', fontsize=14)
        ax.set_xlabel('x', fontsize=12)
        ax.set_ylabel('f(x)', fontsize=12)
        ax.legend()

        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IntegralApp()
    window.show()
    sys.exit(app.exec_())
