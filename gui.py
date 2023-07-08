import sys
import numpy as np
import sounddevice as sd
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QSizePolicy,
    QComboBox,
    QDial,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

volts_divs_limits = [1, 20]
time_divs_limits = [10 * 10, 50 * 10 ** (6)]

n_volts_divs = 8
n_time_divs = 10


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualizador de Ondas")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()

    def audio_settings(self):
        self.sample_rate = 44100
        self.chunk_size = 256

    def canvas_fig(self):
        figure = Figure()
        self.axis = figure.add_subplot(111)
        self.canvas = FigureCanvas(figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def settings_widget_generator(self):
        self.label_mode = QLabel("Mode")
        self.comboBox_mode = QComboBox()
        self.comboBox_mode.setGeometry(QtCore.QRect(20, 80, 101, 25))
        self.comboBox_mode.addItem("AC")
        self.comboBox_mode.addItem("DC")
        self.comboBox_mode.addItem("Cal")

        self.label_range = QLabel("Input Range")
        self.comboBox_range = QComboBox()
        self.comboBox_range.setGeometry(QtCore.QRect(20, 80, 101, 25))
        self.comboBox_range.addItem("10 → 100")
        self.comboBox_range.addItem("1 → 10")
        self.comboBox_range.addItem("0.1 → 1")
        self.comboBox_range.addItem("0.01 → 0.1")

        self.label_probe = QLabel("Probe")
        self.comboBox_probe = QComboBox()
        self.comboBox_probe.setGeometry(QtCore.QRect(20, 80, 101, 25))
        self.comboBox_probe.addItem("x 1")
        self.comboBox_probe.addItem("x 10")

        _layout = QVBoxLayout()
        _layout.addWidget(self.label_mode)
        _layout.addWidget(self.comboBox_mode)
        _layout.addWidget(self.label_range)
        _layout.addWidget(self.comboBox_range)
        _layout.addWidget(self.label_probe)
        _layout.addWidget(self.comboBox_probe)

        settings_widget = QWidget(self)
        settings_widget.setLayout(_layout)

        return settings_widget

    def vertical_widget_generator(self):
        self.label_vert = QLabel("Vertical")
        self.label_vert_pos = QLabel("Position")
        self.label_vert_pos.setAlignment(QtCore.Qt.AlignCenter)
        self.dial_vert_pos = QDial()
        self.dial_vert_pos.setGeometry(QtCore.QRect(10, 160, 121, 91))
        self.label_vert_scale = QLabel("Scale")
        self.label_vert_scale.setAlignment(QtCore.Qt.AlignCenter)
        self.dial_vert_scale = QDial()
        self.dial_vert_scale.setRange(volts_divs_limits[0], volts_divs_limits[1])
        self.dial_vert_scale.setGeometry(QtCore.QRect(10, 60, 121, 61))

        _layout = QVBoxLayout()
        _layout.addWidget(self.label_vert)
        _layout.addWidget(self.label_vert_pos)
        _layout.addWidget(self.dial_vert_pos)
        _layout.addWidget(self.label_vert_scale)
        _layout.addWidget(self.dial_vert_scale)

        vertical_widget = QWidget(self)
        vertical_widget.setLayout(_layout)

        return vertical_widget

    def horizontal_widget_generator(self):
        self.label_hor = QLabel("Horizontal")
        self.label_hor_pos = QLabel("Position")
        self.label_hor_pos.setAlignment(QtCore.Qt.AlignCenter)
        self.dial_hor_pos = QDial()
        self.dial_hor_pos.setGeometry(QtCore.QRect(10, 160, 121, 91))
        self.label_hor_scale = QLabel("Scale")
        self.label_hor_scale.setAlignment(QtCore.Qt.AlignCenter)
        self.dial_hor_scale = QDial()
        self.dial_hor_scale.setRange(time_divs_limits[0], time_divs_limits[1])
        self.dial_hor_scale.setGeometry(QtCore.QRect(10, 60, 121, 61))

        _layout = QVBoxLayout()
        _layout.addWidget(self.label_hor)
        _layout.addWidget(self.label_hor_pos)
        _layout.addWidget(self.dial_hor_pos)
        _layout.addWidget(self.label_hor_scale)
        _layout.addWidget(self.dial_hor_scale)

        horizontal_widget = QWidget(self)
        horizontal_widget.setLayout(_layout)

        return horizontal_widget

    def trigger_widget_generator(self):
        self.label_trigger = QLabel("Trigger")
        self.label_trigger_pos = QLabel("Slope")
        self.label_trigger_pos.setAlignment(QtCore.Qt.AlignCenter)
        self.comboBox_slope = QComboBox()
        self.comboBox_slope.setGeometry(QtCore.QRect(20, 80, 101, 25))
        self.comboBox_slope.addItem("Rising (↑)")
        self.comboBox_slope.addItem("Falling (↓)")
        self.label_trigger_level = QLabel("Level")
        self.label_trigger_level.setAlignment(QtCore.Qt.AlignCenter)
        self.dial_trigger_level = QDial()
        self.dial_trigger_level.setGeometry(QtCore.QRect(10, 60, 121, 61))

        _layout = QVBoxLayout()
        _layout.addWidget(self.label_trigger)
        _layout.addWidget(self.label_trigger_pos)
        _layout.addWidget(self.comboBox_slope)
        _layout.addWidget(self.label_trigger_level)
        _layout.addWidget(self.dial_trigger_level)

        trigger_widget = QWidget(self)
        trigger_widget.setLayout(_layout)

        return trigger_widget

    def setup_ui(self):
        self.audio_settings()
        # Configurar el diseño de la ventana
        main_widget = QWidget(self)
        main_layout = QVBoxLayout()

        # Graph
        self.canvas_fig()
        main_layout.addWidget(self.canvas)

        # Panel settings
        panel_widget = QWidget(self)
        panel_layout = QHBoxLayout()

        ## Settings widget
        panel_layout.addWidget(self.settings_widget_generator())

        ## Vertical widget
        panel_layout.addWidget(self.vertical_widget_generator())

        ## Horizontal widget
        panel_layout.addWidget(self.horizontal_widget_generator())

        ## Trigger widget
        panel_layout.addWidget(self.trigger_widget_generator())

        panel_widget.setLayout(panel_layout)
        main_layout.addWidget(panel_widget)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Iniciar la captura de audio
        self.audio_stream = sd.InputStream(callback=self.audio_callback)
        self.audio_stream.start()

        # Mostrar la ventana
        self.show()

    def audio_callback(self, indata, frames, time, status):
        # Obtener los datos de audio y convertirlos a valores de amplitud
        waveform_data = np.mean(indata, axis=1)

        self.axis.clear()
        y_max = 0.1
        self.axis.set_ylim((-y_max, y_max))

        # Vertical set
        vert_dial_value = self.dial_vert_scale.value() * 10 ** (-3) * n_volts_divs
        self.axis.set_ylim((-vert_dial_value / 2, vert_dial_value / 2))

        # Horizontal set
        hor_dial_value = self.dial_hor_scale.value() * 10 ** (-9) * n_time_divs
        self.axis.set_xlim(xmax=hor_dial_value)

        time_array = np.arange(len(waveform_data)) / self.sample_rate
        self.axis.plot(time_array, waveform_data, "-")

        # Actualizar el gráfico en el lienzo
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
