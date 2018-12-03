MESSAGE_GUIDE = '도움말\n\n' \
'1. 실행 환경 : Windows7\n\n' \
'2. 사용 방법\n' \
'   1) 만약, 양산버전일 경우 WTA 및 SCP 설치 필요\n' \
'   2) PC, TV 모두 같은 공유기에 연결\n' \
'   3) PC에서 Tool을 실행\n' \
'   4) Tool에서 Tool Password를 입력하고 확인버튼 선택\n' \
'   5) Tool 기능이 활성화됨\n' \
'   6) Tool에서 TV IP를 입력후 국가변경, App 검색, 화면캡쳐, 로그추출, 파일을 JIRA에 첨부 할 수 있음\n\n' \
'* SSH 기능 활성화를 위해 TV 에 WTA 설치 \n' \
'   (Intop 후 1회 설치 필요)\n' \
'   1) Acesss USB 연결\n' \
'   2) Event 모드로 변경\n' \
'   3) System1 > Baud Rate > 115200 변경\n' \
'   4) LG Term 에서 다음 실행\n' \
'   5) ‘debug’ + Enter 입력\n' \
'   6) F9 입력하여 ‘debug message enable’ 변경\n' \
'   7) ‘d’ 입력 후 debug menu 뜨면 ‘sh’ 입력하여 shell mode로 진입\n' \
'   8) Shell mode 진입 후 ‘nc atsagent.lge.com 9001 | /bin/bash &’ 입력\n\n' \
'* 파일다운로드를 위해 SCP 설치\n' \
'   (Power On 시 마다 a,c 단계 수행)\n' \
'   1) Putty 에서 SSH로 TV 연결 (id : root)\n' \
'   2) ‘root@LGwebOSTV : ~#’ 에서 wget swdqa.github.io/scp.sh 입력 \n' \
'   3) ‘root@LGwebOSTV : ~#’ 에서 sh scp.sh 입력\n' \
'   4) Password 요구 시 무시하고 Enter 키 3번 입력\n\n' \

MESSAGE_TV_ABNORMAL = 'TV 연결을 실패하였습니다. TV IP 또는 TV가 켜져 있는지 확인해주세요. \n만약 양산모드라면, WTA와 SCP를 설치해야합니다.' \
    + '\n* SSH 기능 활성화를 위해 TV 에 WTA 설치 방법 * \n' \
    + '1. Acesss USB 연결\n' \
    + '2. Event 모드로 변경\n' \
    + '3. System1 > Baud Rate > 115200 변경\n' \
    + '4. LG Term 에서 다음 실행\n' \
    + '5. ‘debug’ + Enter 입력\n' \
    + '6. F9 입력하여 ‘debug message enable’ 변경\n' \
    + '7. ‘d’ 입력 후 debug menu 뜨면 ‘sh’ 입력하여 shell mode로 진입\n' \
    + '8. Shell mode 진입 후 ‘nc atsagent.lge.com 9001 | /bin/bash &’  입력\n' \
    + '\n* 파일다운로드를 위해 TV 에 SCP 설치 방법 *\n' \
    + '1. Putty 에서 SSH로 TV 연결 (id : root)\n' \
    + '2. ‘root@LGwebOSTV : ~#’ 에서 wget xownsla1.dothome.co.kr/scp.sh 입력 \n' \
    + '3. ‘root@LGwebOSTV : ~#’ 에서 sh scp.sh 입력\n' \
    + '4. Password 요구 시 무시하고 Enter 키 3번 입력\n'

MESSAGE_NO_INPUT_TOOL_PWD = 'Tool을 사용하려면, Tool Password 를 입력하고 확인버튼을 선택해주세요.'
MESSAGE_ERROR_PWD = 'Tool Password 를 잘 못 입력하였습니다.'
MESSAGE_SUCCESS_PWD = 'Tool Password 확인을 완료하였습니다.'

MESSAGE_SCP_ERROR = '파일 다운로드 실패하였습니다. TV에서 SCP 명령어가 실행되는지 확인해주세요.'
MESSAGE_ERROR = '실패하였습니다.\n'

MESSAGE_NO_INPUT_INQUERY_COUNTRY = 'IP 를 입력하세요.'
MESSAGE_NO_INPUT_CHANGE_GROUP = 'IP, ContinentIndex, Language&Country, HWSettings 를 입력하세요.'
MESSAGE_NO_INPUT_CHANGE_COUNTRY = 'IP, LG Services Country 를 입력하세요.'
MESSAGE_NO_INPUT_SEARCH = 'IP, App Title 를 입력하세요.'
MESSAGE_NO_INPUT_CAPTURE = 'IP, 화면캡쳐 파일명을 입력하세요.'
MESSAGE_NO_INPUT_DOWNLOAD = 'IP, 로그 파일 또는 폴더 경로를 입력하세요.'
MESSAGE_NO_INPUT_APPINFO = 'IP 또는 App ID를 입력하세요.'
MESSAGE_NO_INPUT_ATTACH = 'ID, Password, Issue ID, 첨부할 파일를 입력하세요.'

MESSAGE_SUCCESS_INQUERY_COUNTRY = 'LG Services Country 관련 정보 조회를 완료하였습니다.'
MESSAGE_SUCCESS_CHANGE_GROUP = 'Area Option (Continent Index, Language&Country, HWSettings) 변경을 완료하였습니다.'
MESSAGE_SUCCESS_CHANGE_COUNTRY = 'LG Services Country 변경을 완료하였습니다.'
MESSAGE_SUCCESS_SEARCH = 'App 검색을 완료하였습니다.'
MESSAGE_SUCCESS_CAPTURE = '화면 캡쳐 및 화면 캡쳐파일 추출을 완료하였습니다.'
MESSAGE_SUCCESS_DOWNLOAD = '로그 추출을 완료하였습니다.'
MESSAGE_SUCCESS_APPINFO = 'appinfo.json 추출을 완료하였습니다.'
MESSAGE_SUCCESS_ATTACH = 'JIRA Issue에 파일 첨부를 완료하였습니다.'

MESSAGE_NO_INPUT_EXCEL_PATH = 'Ordering excel file의 경로가 제대로 선택되었는지 확인해 주세요.'
MESSAGE_NO_INPUT_RESOURCE_PATH = '실물과의 비교를 위한 Ordering resource 원본 파일들의 경로가 제대로 선택되었는지 확인해 주세요.'

RESULT_SUCCESS = True
RESULT_FAIL = False

LOAD_COUNTRY = 'Common'
ORDERING_TEST = 'Ordering'

PLATFROM_WEBOS3 = 'webOS3.0'
PLATFROM_WEBOS35 = 'webOS3.5/4.0'
PLATFROM_WEBOS45 = 'webOS4.5'

COUNTRY_CODES_FILE_WEBOS3 = '../resources/country_codes_v5_webOS3.xml'
COUNTRY_CODES_FILE_WEBOS35 = '../resources/country_codes_v5_webOS35.xml'

PLATFROMS = [PLATFROM_WEBOS35, PLATFROM_WEBOS3, PLATFROM_WEBOS45]
PLATFROMS_FILE = {PLATFROM_WEBOS3:COUNTRY_CODES_FILE_WEBOS3, PLATFROM_WEBOS35:COUNTRY_CODES_FILE_WEBOS35, PLATFROM_WEBOS45:COUNTRY_CODES_FILE_WEBOS35}
ORDERING_FILTER = ("None","OK","NG")
RESULT_VALUES = ("NG","OK")
DIV_CHIP_VALUES = ("DVB","ATSC","ARIB")
EXCEL_VERSION = ("webOS 4.0 이상", "webOS 3.5")

DISPLAY_TYPE_NAME = 'Country Name'
DISPLAY_TYPE_CODE2 = 'Country Code2'
DISPLAY_TYPE_CODE3 = 'Country Code3'

DISPLAY_TYPES = [DISPLAY_TYPE_NAME, DISPLAY_TYPE_CODE2, DISPLAY_TYPE_CODE3]

KEY_HOME = '"HOME"'
KEY_RIGHT = '"RIGHT"'
KEY_EXIT = '"EXIT"'
ORDER_TYPE = "HOME"
KEY_OK = '"ENTER"'

STATE_HOME = 'home'
STATE_ALERT = 'alertView'

SELECTED_FORM_X = 2#12
SELECTED_FORM_Y = 10#12#22
SELECTED_FORM_W = 350#250#350
SELECTED_FORM_H = 187

WO35_SIZE_INFO = {
'width' : int(133*1.5),
'gap' : int(40*1.5),
'y_margin' : int(20*1.5),
'startX' : int(84*1.5),
'crop_y_start' : int(505*1.5),
'crop_y_end' : int(710*1.5)
}

WO40_SIZE_INFO = {
'width' : int(133*1.5),
'gap' : int(40*1.5),
'y_margin' : int(20*1.5),
'startX' : int(84*1.5),
'crop_y_start' : int(505*1.5),
'crop_y_end' : int(710*1.5)
}

WO45_SIZE_INFO = {
'width' : 188,
'gap' : 46,
'y_margin' : 10,
'startX' : 443,
'crop_y_start' : 830,
'crop_y_end' : 1079
}

FX_FY = 1.0
# FX_FY = 0.6956521739130435
# FX_FY = 1.130434782608696

NONE_ICON_PATH = 'resources/NoneIcon.png'

INFO_CHANGERESULT_TO_OK = """
결과를 OK로 변경하시겠습니까?
만약 결과를 OK로 변경 후 해당 창을 종료할 시,
다시 이 결과 내용을 확인할 수 없게 됩니다.
"""


# temp
logFile = None
logFileContents = []
