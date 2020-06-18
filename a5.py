# -*- coding: utf-8 -*-
#
#  A5.py
#  
#  Author: overxfl0w13
#  

def header():
	print """
*******************************
 _______  _______         __   
(  ___  )(  ____ \     /\/  \  
| (   ) || (    \/    / /\/) ) 
| (___) || (____     / /   | | 
|  ___  |(_____ \   / /    | | 
| (   ) |      ) ) / /     | | 
| )   ( |/\____) )/ /    __) (_
|/     \|\______/ \/     \____/
*******************************\n\n\n
"""                            


## Register ##
class LFSR:
	
	def __init__(self,i,length,clockingBit,tappedBits): self.i,self.length,self.register,self.clockingBit,self.tappedBits = i,length,[0]*length,clockingBit,tappedBits
	
	def _getID(self):	  					return self.i
	def _getRegister(self): 				return self.register
	def _getBit(self,i):				    return self.register[i]
	def _getLength(self): 					return self.length
	def _getClockingBit(self): 				return self.register[self.clockingBit]
	def _getTappedBits(self):  				return self.tappedBits
	
	def _setID(self,i):	  					self.i = i
	def _setLength(self,length): 			self.length = length
	def _setRegister(self,register):        self.register = register
	def _setClockingBit(self,clockingBit): 	self.clockingBit = clockingBit
	def _setTappedBits(self,tappedBits):  	self.tappedBits = tappedBits
	
	
## Utils ##
def xor(x,y): return 0 if x==y else 1

def stepOne(): return (LFSR(1,19,8,[13,16,17,18]),LFSR(2,22,10,[20,21]),LFSR(3,23,10,[7,20,21,22]))

def stepTwo(lfsrOne,lfsrTwo,lfsrThree,sessionKey):
	for bit in sessionKey:
		bit = int(bit)
		# LFSRONE #
		nMsb = xor(xor(xor(xor(lfsrOne._getBit(13),lfsrOne._getBit(16)),lfsrOne._getBit(17)),lfsrOne._getBit(18)),bit)	
		lfsrOne._setRegister([nMsb]+lfsrOne._getRegister()[0:lfsrOne._getLength()-1])
		# LFSRTWO #
		nMsb = xor(xor(lfsrTwo._getBit(20),lfsrTwo._getBit(21)),bit)
		lfsrTwo._setRegister([nMsb]+lfsrTwo._getRegister()[0:lfsrTwo._getLength()-1])
		# LFSRTHREE #
		nMsb = xor(xor(xor(xor(lfsrThree._getBit(7),lfsrThree._getBit(20)),lfsrThree._getBit(21)),lfsrThree._getBit(22)),bit)
		lfsrThree._setRegister([nMsb]+lfsrThree._getRegister()[0:lfsrThree._getLength()-1])
		

def stepFour(lfsrOne,lfsrTwo,lfsrThree):
	for i in xrange(100):
		clockingBits = [lfsrOne._getClockingBit(),lfsrTwo._getClockingBit(),lfsrThree._getClockingBit()]
		oneCount,zeroCount = clockingBits.count(1),clockingBits.count(0)
		majorityBit  = 1 if max(oneCount,zeroCount)==oneCount else 0
		# LFSRONE #
		if lfsrOne._getClockingBit()==majorityBit:
			nMsb = xor(xor(xor(lfsrOne._getBit(13),lfsrOne._getBit(16)),lfsrOne._getBit(17)),lfsrOne._getBit(18))
			lfsrOne._setRegister([nMsb]+lfsrOne._getRegister()[0:lfsrOne._getLength()-1])	
		# LFSRTWO #
		if lfsrTwo._getClockingBit()==majorityBit:
			nMsb = xor(lfsrTwo._getBit(20),lfsrTwo._getBit(21))
			lfsrTwo._setRegister([nMsb]+lfsrTwo._getRegister()[0:lfsrTwo._getLength()-1])
		# LFSRTHREE #
		if lfsrThree._getClockingBit()==majorityBit:
			nMsb = xor(xor(xor(lfsrThree._getBit(7),lfsrThree._getBit(20)),lfsrThree._getBit(21)),lfsrThree._getBit(22))
			lfsrThree._setRegister([nMsb]+lfsrThree._getRegister()[0:lfsrThree._getLength()-1])

def stepFive(lfsr1,lfsr2,lfsr3):
	keyStream = ""
	keyStream += str(lfsrOne._getBit(lfsrOne._getLength()-1)^lfsrTwo._getBit(lfsrTwo._getLength()-1)^lfsrThree._getBit(22))	
	for i in xrange(227):
		clockingBits = [lfsrOne._getClockingBit(),lfsrTwo._getClockingBit(),lfsrThree._getClockingBit()]
		oneCount,zeroCount = clockingBits.count(1),clockingBits.count(0)
		majorityBit  = 1 if max(oneCount,zeroCount)==oneCount else 0
		# LFSRONE #
		if lfsrOne._getClockingBit()==majorityBit:
			nMsb = xor(xor(xor(lfsrOne._getBit(13),lfsrOne._getBit(16)),lfsrOne._getBit(17)),lfsrOne._getBit(18))
			lfsrOne._setRegister([nMsb]+lfsrOne._getRegister()[0:lfsrOne._getLength()-1])	
		# LFSRTWO #
		if lfsrTwo._getClockingBit()==majorityBit:
			nMsb = xor(lfsrTwo._getBit(20),lfsrTwo._getBit(21))
			lfsrTwo._setRegister([nMsb]+lfsrTwo._getRegister()[0:lfsrTwo._getLength()-1])
		# LFSRTHREE #
		if lfsrThree._getClockingBit()==majorityBit:
			nMsb = xor(xor(xor(lfsrThree._getBit(7),lfsrThree._getBit(20)),lfsrThree._getBit(21)),lfsrThree._getBit(22))
			lfsrThree._setRegister([nMsb]+lfsrThree._getRegister()[0:lfsrThree._getLength()-1])
		keyStream += str(lfsrOne._getBit(lfsrOne._getLength()-1)^lfsrTwo._getBit(lfsrTwo._getLength()-1)^lfsrThree._getBit(22))	
	return keyStream

def stepSix(plainText,keyStream): return "".join([str(xor(keyStream[i%228],plainText[i])) for i in xrange(len(plainText))])

def padding228(plainText):
	while len(plainText)%228!=0: plainText += "0"
	return plainText
	
if __name__ == "__main__":
	header()
	plainText = padding228(raw_input("Msg> "))
	# Step One #
	print "\nInitializing LFSR..."
	lfsrs = stepOne()
	lfsrOne,lfsrTwo,lfsrThree = lfsrs[0],lfsrs[1],lfsrs[2]
	# Step Two #
	sessionKey = padding228(raw_input("\nSession key> "))
	stepTwo(lfsrOne,lfsrTwo,lfsrThree,sessionKey)
	print "\nLFSR after step two:"
	print lfsrOne._getRegister()
	print lfsrTwo._getRegister()
	print lfsrThree._getRegister()
	print "\n\n"
	# Step Three #
	print "LFSR after step three:"
	print lfsrOne._getRegister()
	print lfsrTwo._getRegister()
	print lfsrThree._getRegister()
	print "\n\n"
	# Step Four  #
	print "LFSR after step four:"
	stepFour(lfsrOne,lfsrTwo,lfsrThree)
	print lfsrOne._getRegister()
	print lfsrTwo._getRegister()
	print lfsrThree._getRegister()
	print "\n\n"
	# Step Five #
	print "KeyStream 228b generated:"
	keyStream  = stepFive(lfsrOne,lfsrTwo,lfsrThree)
	print keyStream
	# Step Six  #
	print "\nCipher text:"
	cipherText = stepSix(plainText,keyStream)
	print cipherText,"\n\n"
