from model.TvModel import *
from common.Constants import *
from common.TvController import *
import common.LunaCommands as LunaCommands
import traceback
import json

class PowerWorker:
    def __init__(self):
        print('PowerWorker.init')
        self.tvController = TvController()

    def reboot(self, ip):
        print('reboot')
        result = TvModel()
        isConnected = self.tvController.connect(ip)
        if isConnected:
            result = self.tvController.execCommand(LunaCommands.reboot(self))
            self.tvController.disconnect()

        return result
