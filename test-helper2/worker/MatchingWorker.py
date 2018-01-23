from model.TvModel import *
from common.Constants import *
from common.TvController import *
import common.LunaCommands as LunaCommands
import traceback
import cv2
import numpy as np
import xlrd
import os
from matplotlib import pyplot as plt # 임시

class MatchingWorker:
    def __init__(self):
        print('MatchingWorker.init')
        self.tvController = TvController()

    # Capture 이미지를 load해서 CP기준으로 자른 이미지 list return
    def loadCaptureAndCrop(self, fileName):
        capturePath = "download/captured_"+fileName+".jpg"
        capture = cv2.imread(capturePath, cv2.IMREAD_UNCHANGED)
        capture = cv2.cvtColor(capture, cv2.COLOR_BGR2RGB)
        capture = capture[505:710, :, :]
        cps = self.divImg(capture)
        return cps

    # Capture 이미지의 각 CP를 잘라서 return
    def divImg(self, img):
        width = 133
        gap = 40
        startX = 44 + gap
        resultImg = []
        while startX <= img.shape[1]:
            startX -= gap
            resultImg.append(img[:, startX:startX+width,:])
            startX += width
        return resultImg

    def parsingExcel(self, excelPath, platform, countryCode):
        workbook = xlrd.open_workbook(excelPath)
        sheet_num = 0
        sheet = workbook.sheet_by_index(sheet_num)
        rowcnt = sheet.nrows # sheet의 row수
        colcnt = sheet.ncols # sheet의 column수
        activateRows = []
        strAppIds = {}
        # 현재 platform에 맞는 rows만 가져와야함
        # TBD : 플랫폼은 추후 선택 가능하도록. 지금은 일단 고정
        # Order Type이 HOME인것만 남겨둠
        # Country Code에 일치하는 것만 남겨둠
        orderType = "HOME"
        for row in range(rowcnt):
            loadPlatform = sheet.cell_value(row, 0) # 0번 Index가 Product-Platform
            loadCountryCode = sheet.cell_value(row, 5) # 5번 Index가 Country Code
            loadOrderType = sheet.cell_value(row, 6) # 6번 Index가 Order Type
            if platform in loadPlatform and orderType == loadOrderType\
            and countryCode == loadCountryCode:
                activateRows.append(row)
        # Ordering Number 순서대로 sorting
        # Str App Id를 받아옴
        for row in activateRows:
            loadOrderNumber = sheet.cell_value(row, 10) # 10번 Index가 Order Number
            strAppIds[loadOrderNumber] = sheet.cell_value(row, 9) # 10번 Index가 Str App Id
        # 순서대로 정렬된 str App Id 배열 return
        return strAppIds

    def readIcons(self, loadPath, strAppIds):
        # cpstub-apps 폴더에서 file list 받아옴
        # file list loop하며 strAppId와 일치하는 폴더 아래의 icon.png를 read해서 순서대로 배열 저장
        # 배열 return
        try:
            imgs = {}
            filenames = os.listdir(loadPath)
            for filename in filenames:
                for index in range(len(strAppIds)):
                    if strAppIds[str(index+1)] == filename:
                        filePath = os.path.join(loadPath, filename)
                        if os.path.isdir(filePath):
                            iconPath = os.path.join(filePath, "icon.png")
                            if os.path.exists(iconPath):
                                img = cv2.imread(iconPath, cv2.IMREAD_UNCHANGED)
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                imgs[index] = img
                            else:
                                print(iconPath,"is not exists!!!!!")
                        else:
                            print(filePath, "is not a dir!")
            return imgs
        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))

    # iconImage가 baseImage에 포함되어있는지를 확인하는 함수
    def checkImageIncluded(self, baseImg, iconImg):
        #baseImg = cv2.imread(baseImgPath, cv2.IMREAD_COLOR)
        #iconImg = cv2.imread(iconImagePath, cv2.IMREAD_COLOR)

        baseImgCopy = baseImg.copy()

        res = cv2.matchTemplate(baseImgCopy, iconImg, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res > 0.83)
        count = 0
        for i in zip(*loc[::-1]):
            count += 1
        if count>0:
            return True
        else:
            return False

    def doMatching(self, excelPath, platform, loadIconPath, captureFileName):
        countryCode = captureFileName.split('(')[1].split(',')[0] # get Country code from captureFileName
        strAppIds = self.parsingExcel(excelPath, platform, countryCode)
        iconImgs = self.readIcons(loadIconPath, strAppIds)
        cpImgs = self.loadCaptureAndCrop(captureFileName)
        preResultCondition = True
        for index in range(len(iconImgs)):
            resCondition = self.checkImageIncluded(cpImgs[index], iconImgs[index])
            '''
            if resCondition == False:
                print("****************** resCondition = ", resCondition)
                plt.subplot(121),plt.imshow(cpImgs[index],cmap = 'gray')
                plt.title('base'), plt.xticks([]), plt.yticks([])
                plt.subplot(122),plt.imshow(iconImgs[index],cmap = 'gray')
                plt.title('icon'), plt.xticks([]), plt.yticks([])
                plt.suptitle(resCondition)

                plt.show()
            '''
            preResultCondition = preResultCondition and resCondition
        return countryCode +" : "+str(preResultCondition)
