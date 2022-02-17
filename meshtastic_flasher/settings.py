"""class for the settings"""


from PySide6.QtWidgets import QTabWidget, QMainWindow

import meshtastic.serial_interface

from meshtastic_flasher.wifi_and_mqtt_form import Wifi_and_MQTT_Form
from meshtastic_flasher.user_form import UserForm
from meshtastic_flasher.position_form import PositionForm
from meshtastic_flasher.power_form import PowerForm
from meshtastic_flasher.radio_form import RadioForm


class Settings(QMainWindow):
    """settings"""

    def __init__(self):
        """constructor"""
        super(Settings, self).__init__()

        self.port = None
        self.interface = None

        width = 800
        height = 600
        self.setMinimumSize(width, height)
        self.setWindowTitle("Settings")

        self.wifi_and_mqtt_form = Wifi_and_MQTT_Form()
        self.user_form = UserForm()
        self.position_form = PositionForm()
        self.power_form = PowerForm()
        self.radio_form = RadioForm()

        self.tabs = QTabWidget()

        self.tabs.blockSignals(True) # just for not showing initial message
        self.tabs.currentChanged.connect(self.on_change_tabs)

        #tabs.setTabPosition(QTabWidget.West)
        self.tabs.setTabPosition(QTabWidget.North)

        self.tabs.addTab(self.wifi_and_mqtt_form, "Wifi/MQTT")
        self.tabs.addTab(self.position_form, "Position")
        self.tabs.addTab(self.user_form, "User")
        self.tabs.addTab(self.power_form, "Power")
        self.tabs.addTab(self.radio_form, "Radio")

        self.setCentralWidget(self.tabs)

        self.tabs.blockSignals(False) # now listen the currentChanged signal


    def on_change_tabs(self, i):
        """On change of each tab """
        print(f'on_change_tabs:{i}')
        if i == 0:
            print('wifi_and_mqtt_form run()')
            self.wifi_and_mqtt_form.run(port=self.port, interface=self.interface)
        elif i == 1:
            print('position run()')
            self.position_form.run(port=self.port, interface=self.interface)
        elif i == 2:
            print('user run()')
            self.user_form.run(port=self.port, interface=self.interface)
        elif i == 3:
            print('power run()')
            self.power_form.run(port=self.port, interface=self.interface)
        elif i == 4:
            print('radio run()')
            self.radio_form.run(port=self.port, interface=self.interface)


    # pylint: disable=unused-argument
    def closeEvent(self, event):
        """On close of the Settings window"""
        print('closed Settings')
        self.port = None
        self.interface.close()
        self.interface = None # so any saved values are re-read upon next form use


    def run(self, port=None):
        """load the form"""
        self.port = port
        self.show()
        if self.interface is None:
            try:
                self.interface = meshtastic.serial_interface.SerialInterface(devPath=self.port)
            except Exception as e:
                print(f'Exception:{e}')
        self.wifi_and_mqtt_form.run(port=self.port, interface=self.interface)
