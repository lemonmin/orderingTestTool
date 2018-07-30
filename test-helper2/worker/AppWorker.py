from model.TvModel import *
from common.Constants import *
from common.TvController import *
import common.LunaCommands as LunaCommands
import traceback
import json

CURRENT_STATE = 'currentState'


class AppWorker:
    def __init__(self):
        print('AppWorker.init')
        self.tvController = TvController()

    def searchApp(self, ip, appTitle):
        print('searchApp : ' + appTitle)
        result = TvModel()
        isConnected = self.tvController.connect(ip)
        if isConnected:
            result = self.tvController.execCommand(LunaCommands.searchApp(self, appTitle))
            self.tvController.disconnect()
        else:
            result.message = MESSAGE_TV_ABNORMAL

        return result

    def inputKey(self, ip, key, times):
        result = TvModel()
        isConnected = self.tvController.connect(ip)
        if isConnected:
            for i in range(times):
                result = self.tvController.execCommand(LunaCommands.inputKey(self, key))
            self.tvController.disconnect()

        return result

    def checkHomeShowing(self, ip):
        print('checkHomeShowing')
        result = TvModel()
        isConnected = self.tvController.connect(ip)
        if isConnected:
            result = self.tvController.execCommand(LunaCommands.confirmCurrentState(self))
            self.tvController.disconnect()
            if self.__loadCurrentState(result.resultValue) == STATE_HOME:
                return True, STATE_HOME
            elif self.__loadCurrentState(result.resultValue) == STATE_ALERT:
                print("STATE ALERT!!!!!!!!!!!!!!!!!!!!!")
                return False, STATE_ALERT
            else:
                return False, 'None'

    def __loadCurrentState(self, currentState):
        print('__loadCurrentState : ' + currentState)
        currentStateDict = json.loads(currentState)
        print(currentStateDict[CURRENT_STATE])
        return currentStateDict[CURRENT_STATE]
