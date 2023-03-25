

i=open("objCODE.txt","r").readlines()
p=open("HTE.txt","w")
object_code=[]
address=[]
progname="COPY"
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

C=hex(0)
h=0
add1=4096
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
        p.write(('{:06x}'.format(add1))+".")
        print(C)
        p.write(('{:02x}'.format(C))+".")
        
        str1=''.join(map(str,printable))
        p.write (str1+"\n")
   
    if(h<lines and object_code[h]!="---"):
        add1=int(add1)+C
    elif(h<lines):
        add1=int(address[h+1],16)
        


p.write("E."+'{:0>6}'.format(address[0])) 
      
        
        
    







