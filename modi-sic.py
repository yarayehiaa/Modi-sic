#returns no of bytes (in decimal)
def cal_bytes(mnemonic,operand):

	found=0
	noOfBytes=-1

	if(mnemonic=="RESW" or mnemonic=="RESB" or mnemonic=="WORD" or mnemonic=="BYTE"):
		found=1
		if(mnemonic=="RESW"):
			operand = int(operand)
			noOfBytes = operand*3
		elif(mnemonic=="RESB"):
			operand = int(operand)
			noOfBytes = operand
		elif(mnemonic=="WORD"):
			noOfBytes = 3
		elif(mnemonic=="BYTE"):
			length=len(operand)-3
			if(operand[0]=='X'):
				if(length%2==0): noOfBytes=length/2
				else: noOfBytes = (length/2)+1
			elif(operand[0]=='C'):
				noOfBytes=length
	
	
	if(found==0):
		opcode = open("OPCODE.txt","r")		#opcode file

		for opLine in opcode:
			op= opLine.split('\t')
		
			if(mnemonic==op[0]):
				found=1
				noOfBytes=op[1]
				break
				
		opcode.close()
		
	if(found==0):
		noOfBytes=-1
	
	noOfBytes = int(noOfBytes)
	return noOfBytes
	
		
	
#function to check if the symbol already exists or not
def notExists(symbol):
	
	symFileR = open("SymbTable.txt","r")
	
	found=0
	
	for aline in symFileR:
		line = aline
		line = line[:-1]
		spLine = line.split('\t')
		
		if(spLine[0]==symbol):
			found=1
			break
			

	symFileR.close()
			
	if(found==1):
		return 0
	else:
		return 1



#function returns the opcode of the operand
def retOpcode(mnemonic):
	
	opcodeF = open("OPCODE.txt","r")		#opcode file
	found=0
	
	for opLine in opcodeF:
			line = opLine
			line = line[:-1]
			op= line.split('\t')
		
			if(mnemonic==op[0]):
				found=1
				opcode=op[2]
				break
	
	opcodeF.close()
	
	if(found==1):
		return opcode
	else:
		return -1

#function returns the format of the operand
def retFormat(mnemonic):
	
	F = open("OPCODE.txt","r")		
	found=0
	
	for opLine in F:
			line = opLine
			line = line[:-1]
			op= line.split('\t')
		
			if(mnemonic==op[0]):
				found=1
				frm=op[1]
				break
	
	F.close()
	
	if(found==1):
		return frm
	else:
		return -1



#function returns address of label
def retAddress(label):
	
	symFileR = open("SymbTable.txt","r")	#to read addresses corresponding to labels
	
	found=0
	
	for aline in symFileR:
		line = aline
		line = line[:-1]
		spLine = line.split('\t')
		
		if(spLine[0]==label):
			found=1
			tAdd = spLine[1]
			return tAdd


	if(label.find('#')==0):
		
		return label
			
	symFileR.close()
			
	if(found==-1):
		return -1
		
		
#function that returns ascii code of a character
def retAscii(char):
	
	ascii = open("ASCII.txt","r")
	found=0

	for aline in ascii:			
		line = aline
		line = line[:-1]
		lineSp = line.split('\t')
				
		if(lineSp[1]==str(char)):
			found=1
			asciiCode = lineSp[0]
			break
							
	ascii.close()
	
	if(found==1):
		return asciiCode
	else:
		return -1
	
		
##################################################################################################
#The program execution begins from here.....
###################################################################################################

newfile=open("Program.txt","r")
inter = open("intermediatex.txt","w")
startx=newfile.readline() #assumption: first line of the code is the headings
startx=newfile.readline()

while(startx[0].isdigit()):
  startx=startx.partition('\t')[2]
  startx=startx.rsplit("!",1)
  inter.write(startx[0]+"\n")
  startx=newfile.readline()
  

inter.close()
x=open("intermediatex.txt","r")
y=open("intermediate.txt","w")
for line in x:
  if not line.isspace():
    
    y.write(line)
   
    y.flush()
y.close()
x.close() 

asmFile = open("intermediate.txt","r")			#assembly code file
aCode = open("out_Pass1.txt","w")		#to store the assembly file with addresses
symFile = open("SymbTable.txt","w")	#to store addresses corresponding to labels

start = asmFile.readline();			#assumption: first line of the code is the start statement
while(start[0]=='.'):
	start = asmFile.readline();

start = start.strip()

firstLine = start.split('\t')
#print (firstLine)


Addf = firstLine[2]	#value of address in hex
Add = int(Addf,16)	#converted the value in decimal
Add1= Addf	
Add1=Add1.strip()
progname=firstLine[0]		


#convert the first address into decimal
#add correct no of bytes everytime (in decimal)
#then convert back to hexadecimal

print("\n")
for iline in asmFile:
    line = iline
    line = line.rstrip()
    lineSp = line.split()

    if (line[0] != '.'):
        if (lineSp[0] == "END"):
            break

        noOfBytes = 0
        if (len(lineSp) == 3):
            # returns no of bytes in decimal
            noOfBytes = cal_bytes(lineSp[1], lineSp[2])
        elif (len(lineSp) == 1):
            noOfBytes = cal_bytes(lineSp[0], 0)
        else:
            noOfBytes = cal_bytes(lineSp[0], lineSp[1])

        # ENTRY INTO SYMTAB
        if (len(lineSp) == 3):  # if label is not empty
            if (notExists(lineSp[0])):  # checks if the label is already present or not
                symbol = lineSp[0] + "\t" + Add1
                # print(symbol)
                symFile.write(symbol)
                symFile.write("\n")
                symFile.flush()
            else:
                error = "Error: " + lineSp[0] + " - Multiple declaration "
                print(error)
                input()
                exit(0)

        # WRITING INSTRUCTIONS ALONG WITH ASSIGNED ADDRESSES
        writeLine = Add1 + "\t" + line  # check if \n is a part of line	#Add1 is hex
        # print(writeLine)					#PRINTS ON-SCREEN
        aCode.write(writeLine)  # writes into file
        aCode.write("\n")
        aCode.flush()

        # CALCULATION OF NEXT ADDRESS
        Add = Add + noOfBytes  # performs decimal addition
        Add1 = str(format(Add, '04X'))  # converts to hex before storing


symFile.close()
asmFile.close()
aCode.close()



#intermediate file with appropriate addresses and SYMTAB have been created
#Begin Pass 2
################################################################################

aCodeI = open("out_Pass1.txt","r")	#assembly code file with addresses
objCode = open("objCODE.txt","w")	#to store the assembly file with object code
obj = open("Out_Pass2.txt","w")				#to store only the object code

aCodeI.seek(0)

for aline in aCodeI: 
	line = aline
	line = line[:-1]
	lineSp = line.split('\t')

	address=lineSp[0]
	label = lineSp[1]
	mnemonic = lineSp[2]
	if(len(lineSp)==4):
		operand = lineSp[3]
		
	
	if(mnemonic!="RESW"	and	mnemonic!="RESB"):
		if(mnemonic=="BYTE"):					#OBJECT CODING for mnemonic: BYTE
			arr = operand.split('\'')
			if(arr[0]=="X"):
				objLine = arr[1]
			elif(arr[0]=="C"):
				chars = list(arr[1])			
				objLine = ""
				
				for char in chars:				#for each x in C'xxx'
					asciiCode = retAscii(char)
					
					if(asciiCode==-1):
						print("Error: Invalid character in BYTE")
						input()
						exit(0)
				
					objLine = objLine + asciiCode
												
		elif(mnemonic=="WORD"):					#OBJECT CODING for mnemonic: WORD
			operand = int(operand)
			objLine = str(format(operand,'06X'))				
			
		elif(mnemonic=="RSUB"):					#OBJECT CODING for mnemonic: RSUB
			opcode = retOpcode(mnemonic)
			if(opcode==-1):
				print("Error: Opcode for RSUB could not be found")
				input()
				exit(0)
			objLine = opcode + "0000"
			
		else:									#OBJECT CODING for all other mnemonics
			opcode = retOpcode(mnemonic)
			frm=retFormat(mnemonic)
			if(opcode==-1):
				error="Error: Opcode for " + mnemonic + " could not be found"
				print(error)
				input()
				exit(0)
			elif(frm=='3'):
				operandSp = operand.split(',')
				length = len(operandSp)
				targetAdd = retAddress(operandSp[0])
				if(targetAdd==-1):
					error="Error: Target address of " + operandSp[0] + " could not be found"
					print(error)
					input()
					exit(0)
			
				if(length==2 and operandSp[1]=="X"):
					string=targetAdd
					part1 = string[:1]
					part2 = string[1:]
				
					part1 = int(part1)
					part1 = part1 + 8
					part1 = str(format(part1,'01X'))
				
					targetAdd = part1+part2		
				if(targetAdd.find('#')==0):
					targetAdd=targetAdd[1:]
					targetAdd = '{:0>4}'.format(targetAdd)
					targetAdd=hex(int(targetAdd))
					print(targetAdd)
					opcode=int(opcode,2)+int('1',2)
					opcode=int(opcode)
					opcode='{:0>2}'.format(opcode)
			elif(frm=='1'):
				targetAdd="\t"	
				opcode= "\t"+opcode
			objLine = opcode + targetAdd
			
		if(mnemonic=="RSUB"):
			writeLine = line + "\t\t" + objLine	
		else:
			writeLine = line + "\t" + objLine	
		objCode.write(writeLine)				#object code along with instructions
		objCode.write("\n")
		obj.write(objLine)						#only object code file
		obj.write("\n")			
	
	else:
		objCode.write(line)
		objCode.write(" --- \n")
		
		
aCodeI.close()
objCode.close()
obj.close()

#object code written in appropriate files
#################################################################################################

objCode = open("objCODE.txt","r")

for aline in objCode:
	line = aline[:-1]
	print(line)

#print HTE Records
#################################################################################################

i=open("objCODE.txt","r").readlines()
p=open("HTE.txt","w")
object_code=[]
address=[]

for x in i:
    
    x=x[:-1]
    op=x.split("\t")
    if(op[2]=='RESW' or op[2]=='RESB'):
        object_code.append("---")
        continue
       
    
    object_code.append(op[4])
    

for x in i:
    
    x=x[:-1]
    op=x.split("\t")
    
    
    address.append(op[0])
length=int(address[len(address)-1],16)
endadd=int(address[0],16)
length=hex(length-endadd)
length=int(length,16)

p.write("H." +'{:0>6}'.format(progname)+"."+'{:0>6}'.format(address[0])+ "."+ '{:06X}'.format(length)+"\n")
#print("H." +'{:0>6}'.format(progname)+"."+'{:0>6}'.format(address[0])+ "."+ '{:06X}'.format(length)+"\n")

C=hex(0)
y=open("objCODE.txt","r").readline()
h=0
Add1=4096
flag=0
lines=len(object_code)
while(h<lines and flag==0):
    printable=[]
    C=0
    while(C<0x1e ): 
        if( h<lines and object_code[h] != "---" ):
            printable.append(object_code[h])
            C=int(C+len(object_code[h])/2)
            
            h+=1
        elif(h<lines): 
            

            h=h+1
            break
        else:
            flag=1
            break
            
    
    
    if(len(printable)!=0):
        p.write("T.")
        p.write(('{:06x}'.format(Add1))+".")
        print(('{:06x}'.format(Add1))+".")
        p.write(('{:02x}'.format(C))+".")
        
        str1=''.join(map(str,printable))
        p.write (str1+"\n")
		
   
    if(h<lines and object_code[h]!="---"):
        Add1=int(Add1)+C
    elif(h<lines):
        Add1=int(address[h+1],16)
        


p.write("E."+'{:0>6}'.format(address[0])) 
p.close()





