import paramiko
import socket
import traceback
import os
import datetime
from common.Constants import *
from scp import SCPClient
from model.TvModel import *

class TvController:
    def __init__(self):
        print('TvController.init')
        paramiko.util.log_to_file('demo_sftp.log')

    def connect(self, ip):
        print('start to connect')
        self.ip = ip
        try:
            self.tvSocket = socket.socket()
            self.tvSocket.settimeout(4)
            self.tvSocket.connect((ip, 22))
            self.tvTransport = paramiko.Transport(self.tvSocket)
            self.tvTransport.connect()

            try:
                self.tvTransport.auth_none('root')
            except paramiko.BadAuthenticationType as err:
                print(err.allowed_types)
                return False
        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            return False
        print('finish to connect : success')
        return True

    def execCommand(self, command):
        tvModel = TvModel()
        print(command)
        try:
            session = self.tvTransport.open_session()
            session.exec_command(command + '\n')
            session.recv_exit_status()
            while session.recv_ready():
                byteText = session.recv(8000)
            message = byteText.decode(encoding='UTF-8')
            if '\"returnValue\":true' in message.replace(" ", ""):
                tvModel.resultType = RESULT_SUCCESS
                tvModel.resultValue = message
            else:
                tvModel.resultType = RESULT_FAIL
                tvModel.message = MESSAGE_ERROR + command + '\n' + message
                print(tvModel.message)

        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            tvModel.message = MESSAGE_ERROR + str(e)
            tvModel.resultType = RESULT_FAIL

        return tvModel

    def downloadFile(self, fileName):
        print('start to downloadFile : ' + fileName)
        tvModel = TvModel()
        try:
            with SCPClient(self.tvTransport) as scp:
                # print(str(os.path.isdir('download')))
                if os.path.isdir('download') is False:
                    os.mkdir('download')
                os.chdir('download')
                #now = datetime.datetime.now().strftime('%Y%m%d-%HH%MM%SS')
                # print(now)
                # os.mkdir(now)
                # os.chdir(now)
                scp.get(fileName, recursive=True)
                success = False
                for base, dirs, files in os.walk('./'):
                    for downloadedFiled in files:
                        success = True
                        break;
                    for downloadedDir in dirs:
                        success = True
                        break;
                # os.chdir('../../')
                scp.close()
                self.disconnect()

                if success:
                    tvModel.resultType = RESULT_SUCCESS
                else:
                    tvModel.message = MESSAGE_SCP_ERROR

        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            tvModel.message = MESSAGE_ERROR + str(e)
        finally:
            os.chdir('../')

        print('finish to download file')

        return tvModel

    def disconnect(self):
        # if self.tvTransport.isConnected():
        self.tvTransport.close()
        self.tvSocket.close()
