import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QFileDialog, QMessageBox
from brownie import config, accounts
from brownie import send_ETH
import brownie.network as network
from scripts.send_eth import send_eth
from scripts.make_nft import mintNFT
from scripts.send_nft import send_token

class welcomescreen(QDialog):
	def __init__(self):
		super(welcomescreen, self).__init__()
		loadUi("C:/Users/tajta/Desktop/Project Github/scripts/New_frontend/welcomescreen.xml", self)
		self.create_NFT.clicked.connect(self.gotocreate_NFT)
		self.NFT.clicked.connect(self.gotoNFT)
		self.ethereum.clicked.connect(self.gotoethereum)

	def gotocreate_NFT(self):
		create = make_NFT()
		widget.addWidget(create)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def gotoNFT(self):
		NFT = NFTpage()
		widget.addWidget(NFT)
		widget.setCurrentIndex(widget.currentIndex()+2)
	
	def gotoethereum(self):
		ethereum = ethereumpage()
		widget.addWidget(ethereum)
		widget.setCurrentIndex(widget.currentIndex()+3)

class NFTpage(QDialog):
	def __init__(self):
		super(NFTpage, self).__init__()
		loadUi("C:/Users/tajta/Desktop/Project Github/scripts/New_frontend/NFTpage.xml", self)
		self.Back1.clicked.connect(self.goBack1)
		self.execute.clicked.connect(self.exect)
		self.exit2.clicked.connect(self.close2)

	def goBack1(self):
		widget.setCurrentIndex(widget.currentIndex()-2)
	
	def exect(self):
		det1 = self.acc1.text()
		det2 = self.acc2.text()
		det3 = self.tok.text()

		b = send_token(det1, det2, det3)

		msg3 = QMessageBox()
		msg3.setWindowTitle("View NFT")
		msg3.setText("Click to View the NFT Link")
		msg3.setIcon(QMessageBox.Information)
		msg3.setDetailedText(b)

		x = msg3.exec_()
	
	def close2(self):
		sys.exit(app.exec_())


class ethereumpage(QDialog):
	def __init__(self):
		super(ethereumpage, self).__init__()
		loadUi("C:/Users/tajta/Desktop/Project Github/scripts/New_frontend/ethereumpage.xml", self)
		self.Back2.clicked.connect(self.goBack2)
		self.execute2.clicked.connect(self.execution)
		self.exit3.clicked.connect(self.close3)


	def goBack2(self):
		widget.setCurrentIndex(widget.currentIndex()-3)
	
	def execution(self):
		key1 = self.acc3.text()
		key2 = self.acc4.text()
		amount = float(self.amount.text())

		z = send_eth(key1, key2, amount)

		if z == 0:
			msg1 = QMessageBox()
			msg1.setWindowTitle("Warning")
			msg1.setText("You need to send atleast $10 worth of ETH")
			msg1.setIcon(QMessageBox.Warning)

			x = msg1.exec_()
		else:
			msg2 = QMessageBox()
			msg2.setWindowTitle("Success")
			msg2.setText("Transaction Successful")
			msg2.setIcon(QMessageBox.Information)

			x = msg2.exec_()
	
	def close3(self):
		sys.exit(app.exec_())

path_name = ""
class make_NFT(QDialog):
	def __init__(self):
		super(make_NFT, self).__init__()
		loadUi("C:/Users/tajta/Desktop/Project Github/scripts/New_frontend/make_NFT.xml", self)
		self.Back3.clicked.connect(self.goBack3)
		self.uploadfile.clicked.connect(self.upload)
		self.send.clicked.connect(self.proceed)
		self.exit1.clicked.connect(self.close1)

	def goBack3(self):
		widget.setCurrentIndex(widget.currentIndex()-1)
	
	def upload(self):
		filename = QFileDialog.getOpenFileName()
		global path_name
		path_name = filename[0] 
	
	def proceed(self):
		nft_title = self.NFT_title.text()
		nft_desc =  self.NFT_desc.text()
		nft_auth = self.private_key.text()
		global path_name
		global upload_location, nft_token
		upload_location, nft_token = mintNFT(path_name, nft_title, nft_desc, nft_auth)

		msg = QMessageBox()
		msg.setWindowTitle("View NFT")
		msg.setText("Click to View the NFT Link")
		msg.setIcon(QMessageBox.Information)
		msg.setInformativeText("The Token ID is : " + str(nft_token))
		msg.setDetailedText(upload_location)

		x = msg.exec_()
	
	def close1(self):
		sys.exit(app.exec_())


app = QApplication(sys.argv)
welcome = welcomescreen()
widget = QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(550)
widget.setFixedWidth(600)
widget.setWindowFlags(QtCore.Qt.FramelessWindowHint)
widget.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
widget.show()
try:
	sys.exit(app.exec_())
except:
	print("Exiting")


def main():
	pass