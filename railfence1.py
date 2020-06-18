rail=int(input("enter 1 for Rail cipher and 2 for Column cipher : "))
s=input("Enter the message : ")
cipher=""

if(rail==2):
	n = int(input("Enter number of Columns : "))
	if(len(s)%n!=0):
		for i in range(0,n-(len(s)%n)):
			s=s+"*"
	n = len(s)//n
else:
	n=2
	if(len(s)%n!=0):
		#for i in range(0,n-(len(s)%n)):
			s=s+"*"

for i in range(0,n):
	for j in range(i,len(s),n):
		cipher=cipher+str(s[j])

print("Cipher : "+cipher)

decipher=""

n=len(cipher)//n
for i in range(0,n):
	for j in range(i,len(s),n):
		decipher=decipher+cipher[j]

print("Decipher : "+decipher)
