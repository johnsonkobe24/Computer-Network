#!/usr/bin/env python
# coding: utf-8

# In[6]:


from socket import *
import base64
# Choose a mail server (e.g. Google mail server) and call it mailserver
#mailserver = 'mxa-00364e01.gslb.pphosted.com'
mailserver = 'mx.columbia.edu'

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, 25))


recv = clientSocket.recv(1024)
print (recv)
if recv[:3] != '220': 
    print (' 220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024)
print (recv1)
if recv1[:3] != '250':
    print ('250 reply not received from server.')
 


# Send MAIL FROM command and print server response.
Mail_From="MAIL FROM: <user@bar.com> \r\n"
clientSocket.send(Mail_From.encode())
recv2 = clientSocket.recv(1024).decode()
print("MAIL FROM OK"+ recv2)


# Send RCPT TO command and print server response.
RCPT_TO="RCPT TO: <nd2705@columbia.edu> \r\n"
clientSocket.send(RCPT_TO.encode())
recv3 = clientSocket.recv(1024).decode()
print("After RCPT OK"+recv3)
if recv3[:3] != '250':
    print('250 reply not received from server.')

# Send DATA command and print server response.
data = "DATA\r\n"
clientSocket.send(data.encode())
recv4 = clientSocket.recv(1024).decode()
print("After DATA OK"+recv4)
if recv4[:3] != '354':
    print('354 reply not received from server.')




#message data
Send= 'user@bar.com'
To='nd2705@columbia.edu'
Msg = 'from:%s\r\nto:%s\nsubject:Lakers 2021\r\nContent-Type:multipart/mixed;boundary="simple"\r\n\r\n--simple\r\n' % (Send, To) + '\r\n Welcome to Laker Nation\r\n'+'\r\n\r\n' + '--simple\r\n' + 'Content-Type:image/JPEG\r\nContent-transfer-encoding:base64\r\n\r\n'
with open ("laker2021.jpeg", "rb") as f:
    f = base64.b64encode(f.read())
Msg += f.decode()
Msg += '\r\n--simple\r\n'

# Send message data.
clientSocket.send(Msg.encode())

# Fill in end# Message ends with a single period.
End_Msg = '\r\n.\r\n'
clientSocket.send(End_Msg.encode())
recv5 = clientSocket.recv(1024).decode()
print(recv5)
if recv5[:3] != '250':
    print('end msg 250 reply not received from server.')



# Send QUIT command and get server response.
clientSocket.send('QUIT\r\n'.encode())
recv6 = clientSocket.recv(1024).decode()
print (recv6)
if recv6[:3] != '221':
    print ('221 reply not received from server.')

# Close the connect
clientSocket.close()






