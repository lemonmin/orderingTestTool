from model.TvModel import *
from common.Constants import *
from common.TvController import *
import common.LunaCommands as LunaCommands
import traceback
import cv2
import numpy as np
import xlrd
import os
import json
import shutil
import collections
from PIL import Image
from matplotlib import pyplot as plt # 임시
import os
from pathlib import Path

class MatchingWorker:
    def __init__(self):
        self.tvController = TvController()
        self.countries = []

    # Capture 이미지를 load해서 CP기준으로 자른 이미지 list return
    def loadCaptureAndCrop(self, fileName):
        captureDir = "download/"+fileName
        if not os.path.exists(captureDir):
            os.makedirs(captureDir)
        capture = self.getOnlyOrderingPartOfCapture(fileName)
        cps = self.divImg(capture, captureDir)
        return cps

    def getOnlyOrderingPartOfCapture(self, fileName):
        capturePath = "download/captured_"+fileName+".png"

        capture = cv2.imread(capturePath, cv2.IMREAD_UNCHANGED)
        capture = cv2.cvtColor(capture, cv2.COLOR_BGR2RGB)
        # resize, 1920 1080 캡쳐일때
        capture = cv2.resize(capture, (1280, 720))

        capture = capture[495:720, :, :]

        return capture

    # Capture 이미지의 각 CP를 잘라서 return
    def divImg(self, img, captureDir):
        width = 140
        gap = 40
        y_margin = 60
        startX = 80 + gap # 44
        resultImg = []
        index = 0
        while startX <= img.shape[1]:
            startX -= gap
            im = img[y_margin:-y_margin, startX+25:startX+width-25, :]
            resultImg.append(im)
            cv2.imwrite(captureDir+"/"+str(index)+".png", cv2.cvtColor(im, cv2.COLOR_RGB2BGR))
            startX += width
            index += 1
        return resultImg

    def loadAllCountriesInCurrentPlatform(self, excelPath, platform):
        workbook = xlrd.open_workbook(excelPath)
        sheet_num = 0
        sheet = workbook.sheet_by_index(sheet_num)
        rowcnt = sheet.nrows # sheet의 row수
        colcnt = sheet.ncols # sheet의 column수

        for row in range(rowcnt):
            loadPlatform = sheet.cell_value(row, 0)  # 0번 Index가 Product-Platform
            if platform in loadPlatform:
                #loadCountry = sheet.cell_value(row, 4)  # 4번 Index가 Country name
                loadCountry = sheet.cell_value(row, 5)  # 5번 Index가 Country code
                loadCountry = loadCountry.strip()
                if loadCountry not in self.countries:
                    self.countries.append(loadCountry)

    def loadAllCountriesInCurrentPlatformForWO35(self, excelFolderPath, platform):
        files = os.listdir(excelFolderPath)
        for f in files:
            print(">>>>>>>>>>>>>>>> f : ",f," >>>>> platform : ",platform)
            if platform in f:
                print("if platform in f:")
                try:
                    excelPath = Path(Path(excelFolderPath) / Path(f))
                    workbook = xlrd.open_workbook(excelPath)
                    for sheet_num in range(4):
                        sheet = workbook.sheet_by_index(sheet_num)
                        rowcnt = sheet.nrows # sheet의 row수
                        colcnt = sheet.ncols # sheet의 column수

                        for row in range(rowcnt):
                            loadCountry = sheet.cell_value(row, 4).strip()  # 5번 Index가 Country code
                            if loadCountry not in self.countries:
                                if loadCountry != "Country Code":
                                    self.countries.append(loadCountry)
                except IndexError:
                    print("현재 Excel의 sheet 수는 기존보다 적습니다.")
                    continue

    def parsingPlatformExcel(self, excelPath):
        workbook = xlrd.open_workbook(excelPath)
        sheet_num = 0
        sheet = workbook.sheet_by_index(sheet_num)
        rowcnt = sheet.nrows # sheet의 row수
        colcnt = sheet.ncols # sheet의 column수
        platforsmList = []

        for row in range(rowcnt):
            loadPlatform = sheet.cell_value(row, 0)  # 0번 Index가 Product-Platform
            platformStr = loadPlatform.split(',')
            for plat in platformStr:
                stripPlat = plat.strip()
                if stripPlat not in platforsmList:
                    platforsmList.append(stripPlat)

        return platforsmList

    def parsingOrderingExcel(self, excelPath, platform, countryCode, excelVer):
        strAppIds = {}
        if excelVer == EXCEL_VERSION[0]: #4.0
            workbook = xlrd.open_workbook(excelPath)
            sheet_num = 0
            sheet = workbook.sheet_by_index(sheet_num)
            rowcnt = sheet.nrows # sheet의 row수
            colcnt = sheet.ncols # sheet의 column수

            # 현재 platform에 맞는 rows만 가져와야함
            # Order Type이 HOME인것만 남겨둠
            # Country Code에 일치하는 것만 남겨둠
            for row in range(rowcnt):
                loadPlatform = sheet.cell_value(row, 0) # 0번 Index가 Product-Platform
                loadCountryCode = sheet.cell_value(row, 5) # 5번 Index가 Country Code
                loadOrderType = sheet.cell_value(row, 6) # 6번 Index가 Order Type
                if platform in loadPlatform and ORDER_TYPE == loadOrderType\
                and countryCode == loadCountryCode:
                    loadOrderNumber = sheet.cell_value(row, 10) # 10번 Index가 Order Number
                    strAppIds[int(loadOrderNumber)] = sheet.cell_value(row, 9) # 10번 Index가 Str App Id
        else:
            files = os.listdir(excelPath)
            for f in files:
                if platform in f:
                    workbookPath = Path(Path(excelPath) / Path(f))
                    workbook = xlrd.open_workbook(workbookPath)
                    for sheet_num in range(4):
                        try:
                            sheet = workbook.sheet_by_index(sheet_num)
                            rowcnt = sheet.nrows # sheet의 row수
                            colcnt = sheet.ncols # sheet의 column수
                            for row in range(rowcnt):
                                loadCountryCode = sheet.cell_value(row, 4).strip() # 4번 Index가 Country Code
                                if countryCode == loadCountryCode:
                                    loadOrderNumber = sheet.cell_value(row, 5).strip() # 5번 Index가 Order Number
                                    if loadOrderNumber != '-':
                                        strAppIds[int(loadOrderNumber)] = sheet.cell_value(row, 9) # 9번 Index가 Str App Id
                        except IndexError:
                            print("현재 Excel의 sheet 수는 기존보다 적습니다.")
                            continue
        # Str App Id를 받아옴
        '''
        for row in activateRows:
            loadOrderNumber = sheet.cell_value(row, 10) # 10번 Index가 Order Number
            strAppIds[loadOrderNumber] = sheet.cell_value(row, 9) # 10번 Index가 Str App Id
        '''
        strAppIds = collections.OrderedDict(sorted(strAppIds.items()))
        return strAppIds

    def copyAllIcons(self, zipPath, loadPath):
        ### TBD : 나중에 Path 다 받아와야함
        #zipPath = "C:/Program Files/7-Zip"
        folderPath = loadPath
        ipkList = []
        ipkName = []

        for files in os.listdir(folderPath):
            if files.find('.ipk') != -1:
                ipkList.append(files)

        currPath = os.getcwd()
        os.chdir(zipPath)
        for ipk in ipkList:
            try:
                temp = ipk.split('.')
                ipkName.append(temp[0])
                for dir in os.listdir(folderPath):
                    if dir == temp[0]:
                        break;
                else:
                    os.system('7z x ' + folderPath + '\\'+ipk + ' -o'+folderPath+'\\'+temp[0])
                    os.system('7z x ' + folderPath + '\\'+temp[0] + '\\data.tar.gz' + ' -o'+folderPath+'\\'+temp[0]+'\\data.tar')
                    os.system('7z x ' + folderPath + '\\'+temp[0] + '\\data.tar\\data.tar' + ' -o'+folderPath+'\\'+temp[0]+'\\data.tar\\data')
            except:
                print('fail to unzip '+temp)

        os.chdir(currPath)
        self.copyIcons(ipkName, loadPath)

    def copyIcons(self, ipkName, loadPath):
        dstDir = loadPath+'/__serverResource'
        try:
            os.mkdir(dstDir)
        except:
            print('__serverResource is already exist!')

        for value in ipkName:
            path = loadPath+'/' + value + '/data.tar/data/usr/palm/applications/'
            forders = os.listdir(path)
            for forder in forders:
                appForderPath = path + forder
                appinfoFile = open(appForderPath+'/appinfo.json','r',encoding="utf8")
                appinfo = json.loads(appinfoFile.read())
                appinfoFile.close()
                try:
                    dstPath = dstDir+'/'+appinfo['id']
                    os.mkdir(dstPath)
                    iconFileName = appinfo['icon']
                    targetIconPath = appForderPath + '/' + iconFileName
                    shutil.copy(targetIconPath, dstPath+"/icon.png")
                except:
                    print(forder,'is already exist!')

    def readIcons(self, loadPath, strAppIds):
        # cpstub-apps 폴더에서 file list 받아옴
        # file list loop하며 strAppId와 일치하는 폴더 아래의 icon.png를 read해서 순서대로 배열 저장
        # 배열 return
        try:
            imgs = {}
            loadPath = loadPath+"/__serverResource"
            filenames = os.listdir(loadPath)
            index = 0
            includeCheck = False
            extenstions = ['png','jpg','jpeg','gif','bmp']
            nonImg = cv2.imread(str(Path(NONE_ICON_PATH)), cv2.IMREAD_UNCHANGED)
            nonImg = cv2.cvtColor(nonImg, cv2.COLOR_BGR2RGB)
            for strIDKey in strAppIds.keys():
                for filename in filenames:
                    if strAppIds[strIDKey] == filename:
                        filePath = os.path.join(loadPath, filename)
                        if os.path.isdir(filePath):
                            iconPath = os.path.join(filePath, "icon.png")
                            if os.path.exists(iconPath):
                                img = cv2.imread(str(Path(iconPath)), cv2.IMREAD_UNCHANGED)
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                imgs[index] = (iconPath, img)
                                index += 1
                                includeCheck = True
                            else:
                                filePathNames = os.listdir(filePath)
                                check = False
                                for f in filePathNames:
                                    f_ex = f.split(".")[-1]
                                    if f_ex in extenstions:
                                        iconPath = str(Path(filePath) / f)
                                        #iconPath = os.path.join(filePath, f)
                                        img = cv2.imread(iconPath, cv2.IMREAD_UNCHANGED)
                                        if type(img) is None:
                                            print("img is None!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                            imgs[index] = (NONE_ICON_PATH, nonImg)
                                            index += 1
                                        else:
                                            height, width, _ = img.shape
                                            if height == width == 80:
                                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                                imgs[index] = (iconPath, img)
                                                index += 1
                                                check = True
                                                break
                                if check == False:
                                    print(strIDKey,"is not exists!!!!!")
                                    imgs[index] = (NONE_ICON_PATH, nonImg)
                                    index += 1
                                includeCheck = True
                        else:
                            print(filePath, "is not a dir!")
                            imgs[index] = (NONE_ICON_PATH, nonImg)
                            index += 1
                        break
                if includeCheck == False:
                    print("index",strAppIds[strIDKey],"can't find!!!!!")
                    imgs[index] = (NONE_ICON_PATH, nonImg)
                    index += 1
            return imgs
        except Exception as e:
            print('*** readIcons, Caught exception: %s: %s' % (e.__class__, e))

    # iconImage가 baseImage에 포함되어있는지를 확인하는 함수
    def checkImageIncluded(self, baseImg, iconImg):
        #baseImg = cv2.imread(baseImgPath, cv2.IMREAD_COLOR)
        #iconImg = cv2.imread(iconImagePath, cv2.IMREAD_COLOR)

        baseImgCopy = baseImg.copy()
        #res = cv2.matchTemplate(baseImgCopy, iconImg, cv2.TM_CCOEFF_NORMED)
        res = cv2.matchTemplate(baseImgCopy, iconImg, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res > 0.84)
        count = 0
        for i in zip(*loc[::-1]):
            count += 1
        if count>0:
            return True
        else:
            return False

    def doMatching(self, excelPath, platform, loadIconPath, captureFileName, excelVer):
        countryCode = captureFileName.split('(')[1].split(',')[0] # get Country code from captureFileName
        countryName = captureFileName.strip('.png').strip()
        strAppIds = self.parsingOrderingExcel(excelPath, platform, countryCode, excelVer)
        ngIcons = []
        if strAppIds != None:
            # iconImage = (iconPath, img)
            iconImgs = self.readIcons(loadIconPath, strAppIds) # 0부터 시작
            cpImgs = self.loadCaptureAndCrop(captureFileName) # 0부터 시작
            preResultCondition = True
            for index in range(len(iconImgs)):
                resCondition = self.checkImageIncluded(cpImgs[index], iconImgs[index][1])
                '''
                if resCondition == False:
                    print("****************** resCondition = ", resCondition)
                    plt.subplot(121),plt.imshow(cpImgs[index],cmap = 'gray')
                    plt.title('base'), plt.xticks([]), plt.yticks([])
                    plt.subplot(122),plt.imshow(iconImgs[index][1],cmap = 'gray')
                    plt.title('icon'), plt.xticks([]), plt.yticks([])
                    plt.suptitle(resCondition)

                    plt.show()
                '''
                if resCondition == False:
                    # index도 0부터 시작
                    ngIcons.append([index, cpImgs[index], iconImgs[index]])
                # List 중 하나라도 False가 있을 경우 전체 False
                preResultCondition = preResultCondition and resCondition
            if preResultCondition:
                return [countryName+":"+ORDERING_FILTER[1], None]
            else:
                return [countryName+":"+ORDERING_FILTER[2], ngIcons]
        else:
            return None
