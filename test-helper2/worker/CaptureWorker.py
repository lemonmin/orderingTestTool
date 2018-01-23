from model.TvModel import *
from common.Constants import *
from common.TvController import *
import common.LunaCommands as LunaCommands
import traceback
import time
import cv2
import numpy as np

class CaptureWorker:
    def __init__(self):
        print('CaptureWorker.init')
        self.tvController = TvController()

    def doScreenCapture(self, ip, fileName):
        fileName = '/tmp/captured_' + fileName + '.jpg'
        print('captureApp : ' + fileName)
        result = TvModel()
        isConnected = self.tvController.connect(ip)
        if isConnected:
            result = self.tvController.execCommand(LunaCommands.doScreenCapture(self, fileName))
            if result.resultType == RESULT_SUCCESS:
                result = TvModel()
                result = self.tvController.downloadFile(fileName)
            self.tvController.disconnect()

        return result
