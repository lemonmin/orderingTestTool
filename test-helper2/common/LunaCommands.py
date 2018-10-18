APPLICATION_MANAGER = 'luna://com.palm.applicationManager'
CAPTURE_SERVICE = 'luna://com.webos.service.tv.capture'
POWER_SERVICE = 'luna://com.webos.service.tvpower'
CONFIG_SERVICE = 'luna://com.webos.service.config'
SDX_SERVICE = 'luna://com.webos.service.sdx'
SETTINGS_SERVICE = 'luna://com.webos.settingsservice'
SYSTEM_PROPERTY = 'luna://com.webos.service.tv.systemproperty'
NETWORK_INPUT = 'luna://com.webos.service.networkinput'
SURFACE_MANAGER = 'luna://com.webos.surfacemanager'

# TV Power Off
def reboot(self):
    return 'luna-send -n 1 -f ' + POWER_SERVICE + '/power/reboot \'{ "reason" : "reset" }\''

def keyBlock(self, block=True):
    if block:
        return 'luna-send -n 1 luna://com.lge.settingsservice/setSystemSettings \'{"category":"hotelMode", "settings":{"enableHotelMode": "on", "keyManagement" : "on", "enableIrRemote" : "blockAll" , "enableLocalKey" : "blockAll" }}\''
    else:
        return 'luna-send -n 1 luna://com.lge.settingsservice/setSystemSettings \'{"category":"hotelMode", "settings":{"enableHotelMode": "off", "keyManagement" : "off", "enableIrRemote" : "normal" , "enableLocalKey" : "normal" }}\''

# 약관동의 해제
def setEULA(self, state=False):
    if state:
        state = "true"
    else:
        state = "false"
    return 'luna-send -n 1 -f luna://com.lge.settingsservice/setSystemSettings \'{"settings":{"eulaStatus": {"acrAllowed": '+ state +',"additionalDataAllowed": '+ state +','+\
           '"cookiesAllowed": '+ state +',"customAdAllowed": '+ state +',"customadsAllowed": '+ state +',"generalTermsAllowed": '+ state +',"networkAllowed": '+ state +',"remoteDiagAllowed": '+ state +','+\
           '"voiceAllowed": '+ state +' }}}\''

def getCountryListPath(self):
    return 'luna-send -n 1 -f luna://com.webos.service.sdx/getCountryCodePath \'{}\''

# Input Key
def inputKey(self, key):
    return 'luna-send -n 1 -f ' + NETWORK_INPUT + '/sendSpecialKey \'{ "key" : ' + key + ' }\''

def getForegroundApp(self):
    return 'luna-send -n 1 -f luna://com.webos.applicationManager/getForegroundAppInfo \'{"subscribe":false, "extraInfo":true}\''

# confirm HOME is showing
def confirmCurrentState(self):
    return 'luna-send -n 1 -f ' + SURFACE_MANAGER + '/getCurrentState \'{}\''

# App Search
def searchApp(self, appTitle):
    #luna-send -n 1 -f luna://com.palm.applicationManager/launch '{"id" : "com.webos.app.voice", "params" : {"activateType" : "livemenu", "launchMode" : "runtext", "params" : {"text" : "apptitle"}}}'
    return 'luna-send -n 1 -f ' + APPLICATION_MANAGER + '/launch \'{"id" : "com.webos.app.voice", "params" : {"activateType":"livemenu", "launchMode":"runtext", "params":{"text": "' + appTitle + '"}}}\''

# Screen Capture
def doScreenCapture(self, fileName):
    #luna-send -n 1 luna://com.webos.service.tv.capture/executeOneShot '{"path":"/tmp/kids_eye.jpg", "method":"DISPLAY", "width":1920, "height":1080, "format":"JPEG"}'
    #luna-send -n 1 luna://com.webos.service.tv.capture/executeOneShot '{"path":"/tmp/ivi_TV_First_Screen.jpg", "method":"DISPLAY", "width":1280, "height":720, "format":"JPEG"}'
    # if resolution == 1280:
    return 'luna-send -n 1 -f ' + CAPTURE_SERVICE + '/executeOneShot \'{"path":"' + fileName + '", "method":"DISPLAY", "width":1920, "height":1080, "format":"PNG"}\''
    # else:
    #     return 'luna-send -n 1 luna://com.webos.service.tv.capture/executeOneShot \'{"path":"/tmp/' + filename + '", "method":"DISPLAY", "width":1920, "height":1080, "format":"JPEG"}\''

# Country Change
def getAreaOptionValues(self):
    return 'luna-send -n 1 -f ' + CONFIG_SERVICE + '/getConfigs \'{"configNames":["com.webos.app.factorywin.areaOption"]}\''

def getCurrentAreaOption(self):
    #luna-send -n 1 -f palm://com.webos.service.config/getConfigs '{"configNames":["tv.model.hwSettingGroup", "tv.model.languageCountrySel"]}'
    return 'luna-send -n 1 -f ' + CONFIG_SERVICE + '/getConfigs \'{"configNames":["tv.model.languageCountrySel", "tv.model.hwSettingGroup", "tv.model.continentIndx"]}\''

def getContiArea2All(self):
    return 'luna-send -n 1 -f ' + SYSTEM_PROPERTY + '/getProperties \'{"keys":["contiArea2All"]}\''

def reconfigure(self):
    return 'luna-send -n 1 luna://com.webos.service.config/reconfigure \'{}\''

def changeAreaOption(self, languageCountry, hwSettings, continentIndx):
    #luna-send -n 1 palm://com.webos.service.config/setConfigs '{"configs":{"tv.model.hwSettingGroup":"JP","tv.model.languageCountrySel":"JP"}}'
    return 'luna-send -n 1 -f ' + CONFIG_SERVICE + '/setConfigs \'{"configs":{"tv.model.languageCountrySel":"' + languageCountry + '", "tv.model.hwSettingGroup":"' + hwSettings + '", "tv.model.continentIndx":' + continentIndx + '}}\''

def setContinentIndex(self, continentIndex):
    return 'luna-send -n 1 -f ' + SYSTEM_PROPERTY + '/setProperties \'{ "contiContiIdx":"' + continentIndex + '" }\''

def setLanguageCountry(self, languageCountry):
    if len(languageCountry) != 2:
        languageCountry = languageCountry.title().replace(" ", "")
    languageCountry = 'langSel' + languageCountry
    index = languageCountry.find('Eu')
    if index > 0:
        languageCountry = languageCountry[0:index] + languageCountry[index:index+2].upper()

    print(languageCountry)
    return 'luna-send -n 1 -f ' + SYSTEM_PROPERTY + '/setProperties \'{ "contiLangCountrySel":"' + languageCountry + '" }\''

def getLanguageCountry(self):
    return 'luna-send -n 1 -f ' + SYSTEM_PROPERTY + '/getProperties \'{ "keys":["contiLangCountrySel"]}\''

def setHwSettings(self, hwSettings):
    hwSettings = 'hwsetting' + hwSettings.title().replace(" ", "")
    return 'luna-send -n 1 -f ' + SYSTEM_PROPERTY + '/setProperties \'{ "contiHwSettingGroup":"' + hwSettings + '" }\''

def getCountry(self):
    #luna-send -f -n 1 luna://com.webos.settingsservice/getSystemSettings '{"category":"option", "key":"smartServiceCountryCode3"}'
    return 'luna-send -n 1 -f ' + SETTINGS_SERVICE + '/getSystemSettings \'{"category":"option", "key":"smartServiceCountryCode3"}\''

def changeCountry(self, code2, code3):
    #luna-send -n 1 -f luna://com.webos.service.sdx/setCountrySettingByManual '{"code2": "GB", "code3": "GBR", "type": "smart"}'
    return 'luna-send -n 1 -f ' + SDX_SERVICE + '/setCountrySettingByManual \'{"code2": "' + code2 + '", "code3": "' + code3 + '", "type": "smart"}\''

def rebootTv(self):
    return 'luna-send -n 1 -f luna://com.webos.service.tvpower/power/reboot \'{"reason":"cpuCommand"}\''

# def agreeTerm(self):
#     return 'luna-send -n 1 -f palm://com.webos.settingsservice/setSystemSettings \'{"settings":{"eulaStatus":{"generalTermsAllowed": true, "additional3Allowed": false,\
#            "additionalDataAllowed": false, "additional2Allowed": false, "additional1Allowed": false, "networkAllowed": true, "generalTermsAllowed": false, "customAdAllowed": false, "remoteDiagAllowed": false, \
#            "cookiesAllowed": false, "customadsAllowed": false, "additional5Allowed": false, "acrAllowed": false, "voiceAllowed": false, "additional4Allowed": false}}}\''
#
# def disagreeTerm(self):
#     return 'luna-send -n 1 -f palm://com.webos.settingsservice/setSystemSettings \'{"settings":{"eulaStatus":{"generalTermsAllowed": false, "additional3Allowed": false,\
#            "additionalDataAllowed": false, "additional2Allowed": false, "additional1Allowed": false, "networkAllowed": true, "generalTermsAllowed": false, "customAdAllowed": false, "remoteDiagAllowed": false,\
#            "cookiesAllowed": false, "customadsAllowed": false, "additional5Allowed": false, "acrAllowed": false, "voiceAllowed": false, "additional4Allowed": false}}}\''
#
# def launchEula(self):
#     return 'luna-send -n 1 -f luna://com.palm.applicationManager/launch \'{ "id": "com.webos.app.eula"}\''
