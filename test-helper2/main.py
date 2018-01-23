from PyQt5 import uic, QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox
import time
import sys
import re
import pickle
import os
from worker.CountryWorker import *
from worker.AppWorker import *
from worker.CaptureWorker import *
from worker.FileWorker import *
from worker.JiraWorker import *
from worker.PowerWorker import *
from worker.MatchingWorker import *
from common.Constants import *
import common.Utils as Utils
import threading

KEY_IP = 'ip'
KEY_LOG_FILE = 'logFile'
KEY_APP_ID = 'appId'
KEY_ID = 'id'
KEY_PWD = 'passwd'
KEY_IS_QTRACKER = 'isQtracker'

MSG_TYPE = 'TYPE_WARNING'
TOOL_PASSWD = '1234'#'apptest2017^'

class MyWindowClass(QtWidgets.QMainWindow):
    taskFinished = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        print('MyWindowClass.init ')
        mainUI = os.path.join('.', 'resources', 'mainForm.ui')
        self.form_class = uic.loadUi(mainUI, self)## Widget으로 구성된 ui일 경우 index 참조 없이 loadui를 호출하면 된다.
        self.form_class.show()
        self.countryWorker = CountryWorker()
        self.appWorker = AppWorker()
        self.captureWorker = CaptureWorker()
        self.fileWorker = FileWorker()
        self.jiraWorker = JiraWorker()
        self.powerWorker = PowerWorker()
        self.matchingWorker = MatchingWorker()
        self.__initUI()
        self.taskFinished.connect(self.putResultToWindow)

    def __initUI(self):
        try:
            self.platformCombo.addItems(PLATFROMS)
            self.displayTypeCombo.addItems(DISPLAY_TYPES)
            self.jiraIssueEdit.setText('GSWDIM-12539')
            self.qRadioButton.setChecked(False)
            self.devRadioButton.setChecked(True)
            self.okBtnClicked()
            mydata = pickle.load(open('mydata.pickle', 'rb'))
            self.ipEdit.setText(mydata[KEY_IP])
            self.logFileNameEdit.setText(mydata[KEY_LOG_FILE])
            self.appIdEdit.setText(mydata[KEY_APP_ID])
            if mydata[KEY_IS_QTRACKER] is True:
                self.qRadioButton.setChecked(True)
                self.devRadioButton.setChecked(False)
            else:
                self.qRadioButton.setChecked(False)
                self.devRadioButton.setChecked(True)
            self.jiraIdEdit.setText(mydata[KEY_ID])
            self.jiraPwdEdit.setText(mydata[KEY_PWD])
        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            self.ipEdit.setText('192.168.0.10')
            self.logFileNameEdit.setText('/var/log/messages')
            self.qRadioButton.setChecked(True)

    def closeEvent(self, event):
        print("save data and then exit the app.")
        ip = self.ipEdit.text().strip()
        logFile = self.logFileNameEdit.text().strip()
        appId = self.appIdEdit.text().strip()
        id = self.jiraIdEdit.text().strip()
        passwd = self.jiraPwdEdit.text().strip()
        isQtracker = self.qRadioButton.isChecked()
        try:
            mydata = {KEY_IP:ip, KEY_LOG_FILE:logFile, KEY_APP_ID:appId, KEY_ID:id, KEY_PWD:passwd, KEY_IS_QTRACKER:isQtracker}
            pickle.dump(mydata, open('mydata.pickle', 'wb'))
            QtWidgets.QMainWindow.closeEvent(self, event)
        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))

    def okBtnClicked(self):
        toolPasswd = self.toolPwdEdit.text()
        now = time.localtime()
        date = str(now.tm_year) + str(now.tm_mon) + str(now.tm_mday) + TOOL_PASSWD
        if date == toolPasswd:
            self.functionArea.setEnabled(True)
            self.tabWidget.setEnabled(True)
            self.resultText.setText(MESSAGE_SUCCESS_PWD)
        else:
            self.functionArea.setEnabled(False)
            self.tabWidget.setEnabled(False)
            if not Utils.isEmpty(self, toolPasswd):
                self.resultText.setText(MESSAGE_ERROR_PWD)
            else:
                self.resultText.setText(MESSAGE_NO_INPUT_TOOL_PWD)


    def inqueryCountryBtnClicked(self):
        try:
            ip = self.ipEdit.text().strip()

            currentTab = self.tabWidget.currentWidget()

            if not Utils.isEmpty(self, ip):
                platform = self.platformCombo.currentText()
                displayType = self.displayTypeCombo.currentText()
                if currentTab == self.countryWithGroupTab:
                    result = self.countryWorker.inquery(ip, platform, displayType, True)
                    if result.resultType == RESULT_SUCCESS:
                        self.__refreshCountryWithGroupTab()
                        self.resultText.setText(MESSAGE_SUCCESS_INQUERY_COUNTRY)
                        return
                    else:
                        self.resultText.setText(result.message)
                else:
                    result = self.countryWorker.inquery(ip, platform, displayType, False)
                    if result.resultType == RESULT_SUCCESS:
                        self.__refreshCountryTab()
                        self.resultText.setText(MESSAGE_SUCCESS_INQUERY_COUNTRY)
                        return
                    else:
                        self.resultText.setText(result.message)
            else:
                self.resultText.setText(MESSAGE_NO_INPUT_INQUERY_COUNTRY)

        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()

    def __refreshCountryWithGroupTab(self):
        self.clearCountryInfo()
        countryModel = self.countryWorker.countryModel
        self.continentIndexCombo.addItems(countryModel.continentIndexList)
        self.continentIndexCombo.setCurrentIndex(countryModel.currentContinentIndex)
        self.languageCountryCombo.addItems(countryModel.languageCountryList)
        self.languageCountryCombo.setCurrentIndex(self.languageCountryCombo.findText(countryModel.currentLanguageCountry))
        self.hwSettingsCombo.addItems(countryModel.hwSettingsList)
        self.hwSettingsCombo.setCurrentIndex(self.hwSettingsCombo.findText(countryModel.currentHwSettings))
        self.countryWithGroupCombo.addItems(countryModel.countryNameList)
        self.countryWithGroupCombo.setCurrentIndex(self.countryWithGroupCombo.findText(countryModel.currentCountry))
        self.changeGroupButton.setEnabled(True)
        self.changeCountryWithGroupButton.setEnabled(True)

    def __refreshCountryTab(self):
        self.clearCountryInfo()
        countryModel = self.countryWorker.countryModel
        self.countryCombo.addItems(countryModel.countryNameList)
        self.countryCombo.setCurrentIndex(self.countryCombo.findText(countryModel.currentCountry))
        self.changeCountryButton.setEnabled(True)
        self.oderingTVCheckStartBtn.setEnabled(True)

    def clearCountryInfo(self):
        self.continentIndexCombo.clear()
        self.languageCountryCombo.clear()
        self.hwSettingsCombo.clear()
        self.countryWithGroupCombo.clear()
        self.countryCombo.clear()
        self.changeGroupButton.setEnabled(False)
        self.changeCountryWithGroupButton.setEnabled(False)
        self.changeCountryButton.setEnabled(False)

    def changeGroupBtnClicked(self):
        try:
            ip = self.ipEdit.text().strip()
            self.countryCombo.clear()
            continentIndex = self.continentIndexCombo.currentText()
            languageCountry = self.languageCountryCombo.currentText()
            hwSettings = self.hwSettingsCombo.currentText()

            if not Utils.isEmpty(self, ip, continentIndex, languageCountry, hwSettings):
                result = self.countryWorker.changeAreaOption(ip, continentIndex, languageCountry, hwSettings)
                if result.resultType == RESULT_SUCCESS:
                    self.__refreshCountryWithGroupTab()
                    self.resultText.setText(MESSAGE_SUCCESS_CHANGE_GROUP)
                    return
                else:
                    self.resultText.setText(result.message)
            else:
                self.resultText.setText(MESSAGE_NO_INPUT_CHANGE_GROUP)
            self.changeCountryButton.setEnabled(False)
        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()

    def groupChanged(self):
        self.countryCombo.clear()
        self.changeCountryButton.setEnabled(False)

    def changeCountryWithGroupBtnClicked(self):
        try:
            ip = self.ipEdit.text().strip()
            countryName = self.countryWithGroupCombo.currentText()
            print(ip)
            print(countryName)
            if not Utils.isEmpty(self, ip, countryName):
                result = self.countryWorker.changeCountryWithGroup(ip, countryName)
                if result.resultType == RESULT_SUCCESS:
                    self.resultText.setText(MESSAGE_SUCCESS_CHANGE_COUNTRY)
                else:
                    self.resultText.setText(result.message)
            else:
                self.resultText.setText(MESSAGE_NO_INPUT_CHANGE_COUNTRY)
        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()

    def changeCountryBtnClicked(self):
        try:
            ip = self.ipEdit.text().strip()
            countryName = self.countryCombo.currentText()

            if not Utils.isEmpty(self, ip, countryName):
                result = self.countryWorker.changeCountry(ip, countryName)
                if result.resultType == RESULT_SUCCESS:
                    self.resultText.setText(MESSAGE_SUCCESS_CHANGE_COUNTRY)
                else:
                    self.resultText.setText(result.message)
            else:
                self.resultText.setText(MESSAGE_NO_INPUT_CHANGE_COUNTRY)
        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()

    def searchBtnClicked(self):
        try:
            ip = self.ipEdit.text().strip()
            appTitle = self.appTitleEdit.text()

            if not Utils.isEmpty(self, ip, appTitle):
                result = self.appWorker.searchApp(ip, appTitle)
                if result.resultType == RESULT_SUCCESS:
                    self.resultText.setText(MESSAGE_SUCCESS_SEARCH)
                else:
                    self.resultText.setText(result.message)
            else:
                self.resultText.setText(MESSAGE_NO_INPUT_SEARCH)
        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()

    def appTitleRetrunPressed(self):
        self.searchBtnClicked()

    def captureBtnClicked(self):
        try:
            ip = self.ipEdit.text().strip()
            fileName = self.fileNameEdit.text().strip().replace(' ', '')

            if not Utils.isEmpty(self, ip, fileName):
                result = self.captureWorker.doScreenCapture(ip, fileName)
                if result.resultType == RESULT_SUCCESS:
                    self.resultText.setText(MESSAGE_SUCCESS_CAPTURE)
                else:
                    self.resultText.setText(result.message)
            else:
                self.resultText.setText(MESSAGE_NO_INPUT_CAPTURE)
        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()

    def captureReturnPressed(self):
        self.captureBtnClicked()

    def downloadBtnClicked(self):
        try:
            ip = self.ipEdit.text().strip()
            fileName = self.logFileNameEdit.text().strip().replace(' ', '')

            if not Utils.isEmpty(self, ip, fileName):
                result = self.fileWorker.downloadFile(ip, fileName)
                if result.resultType == RESULT_SUCCESS:
                    self.resultText.setText(MESSAGE_SUCCESS_DOWNLOAD)
                else:
                    self.resultText.setText(result.message)
            else:
                self.resultText.setText(MESSAGE_NO_INPUT_DOWNLOAD)
        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()

    def downloadReturnPressed(self):
        self.downloadBtnClicked()

    def appInfoDownloadBtnClicked(self):
        try:
            ip = self.ipEdit.text().strip()
            fileName = self.appIdEdit.text().strip().replace(' ', '')

            if not Utils.isEmpty(self, ip, fileName):
                fileName = '/media/cryptofs/apps/usr/palm/applications/' + fileName + '/appinfo.json'
                result = self.fileWorker.downloadFile(ip, fileName)
                if result.resultType == RESULT_SUCCESS:
                    self.resultText.setText(MESSAGE_SUCCESS_APPINFO)
                else:
                    self.resultText.setText(result.message)
            else:
                self.resultText.setText(MESSAGE_NO_INPUT_APPINFO)
        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()

    def appInfoDownloadReturnPressed(self):
        self.appInfoDownloadBtnClicked()

    def fileSelectBtnClicked(self):
        print('fileSelectBtnClicked : ')
        files = QtWidgets.QFileDialog.getOpenFileNames(self,"Select files","./")
        if str(files) != '':
            fileInfo = re.sub("[\[()\]]", "", str(files)).replace(", ''", "").replace("'", "")
            print(fileInfo)
            self.fileList = fileInfo.split(', ')
            self.selectedFilesEdit.setText(fileInfo)

    def attachBtnClicked(self):
        try:
            id = self.jiraIdEdit.text().strip()
            passwd = self.jiraPwdEdit.text().strip()
            issueId = self.jiraIssueEdit.text().strip()
            files = self.selectedFilesEdit.text().strip()

            if not Utils.isEmpty(self, id, passwd, issueId, files):
                result = self.jiraWorker.attachFiles(id, passwd, issueId, self.fileList, self.qRadioButton.isChecked())
                if result == RESULT_SUCCESS:
                    self.resultText.setText(MESSAGE_SUCCESS_ATTACH)
                else:
                    self.resultText.setText(result.message)
            else:
                self.resultText.setText(MESSAGE_NO_INPUT_ATTACH)
        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()

    def qRadioButtonClicked(self):
        if self.qRadioButton.isChecked() == True:
            self.devRadioButton.setChecked(False)
        else:
            self.devRadioButton.setChecked(True)

    def devRadioButtonClicked(self):
        if self.devRadioButton.isChecked() == True:
            self.qRadioButton.setChecked(False)
        else:
            self.qRadioButton.setChecked(True)

    def helpBtnClicked(self):
        print('test')
        try:
            self.showDialog('TYPE_INFORMATION', MESSAGE_GUIDE)
        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
        # help(self)
    def orderingCheckLoop(self, countryModel, testList):
        try:
            ip = self.ipEdit.text().strip()
            failList = [] # 국가 변경이나 capture 실패한 것들 재실행을 위한 List
            ngList = [] # check 후 NG인 애들 report용
            # 첫 번째 Tab에서 받아온 CountryNameList로 loop.
            for i in testList:
                if not Utils.isEmpty(self, ip, str(i)):
                    # i번째 국가로 변경 요청
                    resultCountry = self.countryWorker.changeCountry(ip, str(i))
                    if resultCountry.resultType == RESULT_SUCCESS:
                        #self.resultText.setText(MESSAGE_SUCCESS_CHANGE_COUNTRY)
                        ## TBD : sleep 구문 적절한걸로 변경
                        ## TV Controller connect 다 동시에 사용하도록 변경해야할듯. ##
                        time.sleep(1)
                        print("**** current country :",countryModel.currentCountry)
                        resultReboot = self.powerWorker.reboot(ip)
                        time.sleep(40)
                        # 현재 국가 이름이 요청 국가 이름과 같을 경우
                        if countryModel.currentCountry == str(i):
                            # Home Key 실행
                            self.appWorker.inputKey(ip, KEY_HOME, 1)
                            # 현재 Home이 떠 있는 상황인지 Check
                            isHome = self.appWorker.checkHomeShowing(ip)
                            while not isHome:
                                self.appWorker.inputKey(ip, KEY_HOME, 1)
                                isHome = self.appWorker.checkHomeShowing(ip)
                            # 10칸 오른쪽 옆으로 감 (모든 CP Apps Capture를 위해)
                            self.appWorker.inputKey(ip, KEY_RIGHT, 10)
                            # Home이 떠 있는 상황일 때 Capture 진행
                            print("HOME!!!!!!!!! ",isHome)
                            resultCapture = self.captureWorker.doScreenCapture(ip, str(i))
                            time.sleep(2.5)
                            if resultCapture.resultType == RESULT_SUCCESS:
                                print("Capture Success!!")
                                # TBD : 각 인자들을 선택 가능하게 만들기
                                resultText = self.matchingWorker.doMatching("excel.xls", "W18A", 'Y:/local/cpstub-apps', str(i))
                                self.taskFinished.emit(resultText)
                                time.sleep(2)
                            else:
                                print("Capture Fail!!!!!!")
                                failList.append(str(i))
                                print("Fail List : ",failList)
                                continue

                            # 국가 이름으로 폴더 만들어서 Capture 저장
                            # 키 하나씩 이동해서 오더링순서를 이름으로 저장

                            # 열려 있는 Launcher를 닫는 용도
                            self.appWorker.inputKey(ip, KEY_EXIT, 1)
                        else: # 현재 국가랑 str i 국가가 다를 경우
                            # 국가 기록하고 continue..
                            print("Not Same country!!!!!!!!!!!!!")
                            failList.append(str(i))
                            print("Fail List : ",failList)
                            continue
                    else: # 국가 변경 실패
                        #self.resultText.setText(result.message)
                        print("FAIL CHANGE COUNTRY!!!!!!!!!!!!!!!!!")
                        failList.append(str(i))
                        print("Fail List : ",failList)
                        continue # TBD : 기록하고 넘어가기로 변경
                else:
                    self.resultText.setText(MESSAGE_NO_INPUT_CHANGE_COUNTRY)
            print("END!!!! Fail List :", failList)
            return failList
        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()


    def orderingTestFunction(self):
        ## TBD : 맨 처음에 국가정보 받아온거 없으면 받아오는 구문 추가
        try:
            tryCount = 0
            countryModel = self.countryWorker.countryModel
            failList = self.orderingCheckLoop(countryModel, countryModel.countryNameList)
            # 확인에 실패한 국가 list를 최대 100회까지 모두 다 확인하기 위한 while문
            while len(failList) != 0 and tryCount < 20:
                failList = self.orderingCheckLoop(countryModel, failList)
                tryCount += 1
                print("******* Try Count : ", tryCount)
            # TBD : 모든 확인 이후 처리구문
            if len(failList)>0:
                print("Not Tested list : ", failList)
            else:
                print("Finished.")
        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
        '''
        'Home은 app이 아니므로 app정보 api로는 확인 불가'
        luna-send -n 1 -f luna://com.webos.surfacemanager/getCurrentState \'{}\'
        '''

    def orderingTVCheckStartBtnClicked(self):
        ## TBD : Thread 중에 disable하고, 현재 Thread 진행 상태 Progress bar or lading bar 표시
        print('orderingTVCheckStartBtnClicked')
        try:
            # 실행 중 Main UI가 멈추기때문에 Thread로 구현
            orderingTestThread = threading.Thread(target=self.orderingTestFunction)
            orderingTestThread.start()
        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()

    def putResultToWindow(self, res):
        self.resultText.append(res)

    def showDialog(self, msgType, message):
        # print(message)
        msg = QMessageBox()
        if msgType == 'TYPE_WARNING':
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QMessageBox.Ok)
        elif msgType == 'TYPE_INFORMATION':
            # msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Test Helper 도움말")
            msg.setStandardButtons(QMessageBox.Ok)
        elif msgType == 'TYPE_QUESTION':
            msg.setIcon(QMessageBox.Question)
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        else:
            msg.setIcon(QMessageBox.NoIcon)
        msg.setText(message)
        # textEdit = msg.findChild(QtGui.QTextEdit)
        # textEdit.setMaximumWidth(16777215)
        msg.setStyleSheet(self.form_class.styleSheet())
        msg.setWindowIcon(self.form_class.windowIcon())
        msg.setMaximumWidth(2000)
        retval = msg.exec_()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myWindow = MyWindowClass(None)
    app.exec_()
