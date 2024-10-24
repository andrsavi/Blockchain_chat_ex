import socket
import threading
import sys, os
import random
import string
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'BlockChain'))
import BlockChain
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'AES_Cyptography'))
import AES_Cyptography

from colorama import init
init()
from colorama import Fore, Back, Style

blockchain = BlockChain.Blockchain()
genesisBlock = blockchain.head

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

class Server:
	port = 0
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connections = []
	def __init__(self,port):
		self.port = port
		self.sock.bind(('0.0.0.0',int(port)))
		self.sock.listen(1)
	def sendBoardcast(self):
		while True:
			try:
				data = bytes(input(""),'utf-8')
				if(len(data.split()) == 2):
					BlockChain.editBlock(blockchain,genesisBlock, int(data.split()[1]))
				if(data == "exit"):
					print("Close Server")
					os.kill(os.getpid(), 9)
			except EOFError as error:
				print("Close Server")
				os.kill(os.getpid(), 9)
	def handler(self,c,a):
		while True:
			try:
				data = c.recv(1024)
			except Exception as error:
				print(str(a[0])+':'+str(a[1])+" disconnected")
				self.connections.remove(c)
				c.close()
				break
			block = BlockChain.Block(data.decode('utf-8'))
			blockchain.mine(block)
			for connection in self.connections:
				connection.send(bytes(str(block.data),'utf-8'))
			if not data:
				print(str(a[0])+':'+str(a[1])+" disconnected")
				self.connections.remove(c)
				c.close()
				break
	def run(self):
		iThread = threading.Thread(target=self.sendBoardcast)
		iThread.daemon = True
		iThread.start()
		os.system('cls')
		os.system('clear')
		print("//////////// Welcome to BlockCain Chat ///////////////////")

		print("////////////////// This is SERVER /////////////////////////")
		print("SERVER running on port "+str(socket.gethostbyname(socket.gethostname()))+":"+str(self.port))
		# Wait for Client connected
		while True:
			c,a = self.sock.accept()
			cThread = threading.Thread(target=self.handler,args=(c,a))
			cThread.daemon = True
			cThread.start()
			self.connections.append(c)
			print(str(a[0])+':'+str(a[1])+" connected")

class Client:
	key_aes = ''
	name = ''
	groupId = ''
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	def sendMsg(self):
		while True:
			try:
				private_msg = input("")
				if(private_msg == "exit"):
					print("Close connection")
					os.kill(os.getpid(), 9)
				secret_key = self.key_aes
				data = {
					"groupId" : str(self.groupId),
					"sender" : str(self.name),
					"msg" : str(AES_Cyptography.AESCipher(secret_key).encrypt(private_msg).decode('utf-8'))
				}
				jsonData = json.dumps(data)
				self.sock.send(bytes(jsonData,"utf-8"))
			except EOFError as error:
				print("Close connections")
				os.kill(os.getpid(), 9)
	def __init__(self,address,port):
		self.sock.connect((address,int(port)))
		print(Fore.LIGHTGREEN_EX)
		os.system('cls')
		os.system('clear')
		print("//////////// Welcome to BlockCain Chat ///////////////////")

		print("////////////////// This is CLIENT /////////////////////////")
		self.name = input("ENTER your name : ")
		print("==========================")
		print("    Choose mode")
		print("==========================")
		print("ENTER 1 to CREATE new group:")
		print("ENTER 2 to JOIN group:")
		print("==========================")
		while True:
			mode = input("Mode : ")
			if(mode == "1"):
				print("/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/")
				print("You select mode 1 (create new group chat):")
				print("/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/=/")
				self.key_aes = randomString(20).upper()
				self.groupId = randomString(10).upper()
				print("==============================================================")
				print(Fore.LIGHTGREEN_EX,"This is your group id (send to your friend) : ")
				print(Fore.LIGHTCYAN_EX,str(self.groupId))
				print(Fore.LIGHTGREEN_EX,"This is your secrete group key (send to your friend) : ")
				print(Fore.LIGHTCYAN_EX,str(self.key_aes))
				print(Fore.LIGHTGREEN_EX,"==============================================================")
				break
			elif(mode == "2"):
				print("==================================")
				self.groupId = input("Enter Group ID :")
				self.key_aes = input("Please enter secrete group key : ")
				break

		print(Fore.LIGHTYELLOW_EX)
		print("////////// WELCOME TO CHAT ROOM ///////////")
		print(" CHAT ROOM Group_id : "+self.groupId +" Started!!!")
		print(" You are : "+self.name)
		print("///////////////////////////////////////////")
		print(Fore.LIGHTGREEN_EX)
		iThread = threading.Thread(target=self.sendMsg)
		iThread.daemon = True
		iThread.start()
		while True:
			data = self.sock.recv(1024)
			if not data:
				break
			newBlock = json.loads(data.decode("utf-8"))
			groupId = newBlock["groupId"]
			sender = newBlock["sender"]
			msg = newBlock["msg"]
			if (groupId == self.groupId):
				print(str(sender) + " : " + str(AES_Cyptography.AESCipher(self.key_aes).decrypt(msg).decode('utf-8')))

if(len(sys.argv)>2):
	client = Client(sys.argv[1],sys.argv[2])
else:
	server = Server(sys.argv[1])
	server.run()