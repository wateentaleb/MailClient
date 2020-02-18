from socket import *
import ssl
import requests
import base64






msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"


# Choose a mail server (e.g. Google mail server) and call it mailserver

#Chose the gmail server
mailserver = 'smtp.gmail.com'
# connection the the secure port of gmail used for TLS communication, the port
# Google has instructed to use was 587
serverPort = 587

# string variable storing the email where the email will be sent from
emailFrom = 'talebwateen@gmail.com'


# TO THE TA RUNNING THIS, CHANGE YOUR EMAIL AND PASSWORD FOR YOUR GMAIL ACCOUNT BELOW,
# THIS IS THE ONLY CHANGE YOU NEED TO MAKE
username = "talebwateen@gmail.com"

#this is my personal password so i did not want to submit it on OWL
password = "xxxxxx"


#encoding the username
encodedUsername = username.encode()

#then encrypting it into base64 text because thats the language gmail server communicate in
base64User = base64.b64encode(encodedUsername)

#encoding password
encodedPassword = password.encode()

#then encrypting it into base64 text because thats the language gmail server communicate in
base64Password = base64.b64encode(encodedPassword)


# the string variable storing the email where the email will be received
emailTo = 'talbyte.co@gmail.com'


# Create socket called clientSocket and establish a TCP connection with mailserver
#Fill in start

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, serverPort))

recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':

    print('220 reply not received from server.')
#Fill in end






# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':

    print('250 reply not received from server.')


# Got the following message
#530 5.7.0 Must issue a STARTTLS command first. t17sm237930ioc.18 - gsmtp
# therefore i need to initiate a tls connection to establish a communication line with google servers
# i will put the STARTTLS command next before doing the send mail from command

tlsMessage = 'STARTTLS\r\n'
clientSocket.send(tlsMessage.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != "220":
        print('220 reply not received from server')


# now that it says its ready, all communication needs to be done over a ssl socket
#which is why im going to wrap my clientsocket into a sslsocket

#the auth login command sends message in base64
#without doing so the following messages shows
#334 VXNlcm5hbWU6

#creating a ssl wrapper on our socket to establish a secured connection
sslSocket = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_SSLv23)
sslCommand = 'AUTH LOGIN\r\n'
sslSocket.send(sslCommand.encode())
recv1 = sslSocket.recv(1024).decode()

# if the following string is received it means username, its just encrypted in base64 text
if 'VXNlcm5hbWU6' in recv1:
    print('334 Username:')
else:
    print('334 reply not received from server.')




#sending my username

sslSocket.send(base64User + "\r\n".encode())
recv2 = sslSocket.recv(1024).decode()
# if the following string is received it means password, its just encrypted in base64 text
if 'UGFzc3dvcmQ6' in recv2:
    print('334 Password:')
else:
    print('334 reply not received from server')

# sending password

sslSocket.send(base64Password+"\r\n".encode())
recv2 = sslSocket.recv(1024).decode()

print('\r\n'+recv2)
if recv2[:3] !='235':
    print('235 reply not received from server.')





# Send MAIL FROM command and print server response.

mailFromCommand = 'MAIL FROM:<'+emailFrom+'>\r\n'
sslSocket.send(mailFromCommand.encode())
recv1 = sslSocket.recv(1024).decode()
print(recv1)
if recv1[:3] !='250':
    print('250 reply not received from server.')


# Fill in start




# Fill in end



# Send RCPT TO command and print server response.

# Fill in start
mailToCommand = 'RCPT TO:<'+emailTo+'>\r\n'
sslSocket.send(mailToCommand.encode())
recv1 = sslSocket.recv(1024).decode()
print(recv1)
if recv1[:3] !='250':
    print('250 reply not received from server.')


# Fill in end




# Send DATA command and print server response.

# Fill in start
dataCommand = 'DATA\r\n'
sslSocket.send(dataCommand.encode())
recv1 = sslSocket.recv(1024).decode()
print(recv1)
if recv1[:3] !='354':
    print('250 reply not received from server.')

# Fill in end




# Send message data.

msg = msg + '\r\n'
sslSocket.send(msg.encode())

# Fill in end

# Message ends with a single period.


# Fill in start
sslSocket.send(endmsg.encode())
recv1 = sslSocket.recv(1024).decode()
print(recv1)
if recv1[:3] !='250':
    print('250 response not received from server.')

# Fill in end




# Send QUIT command and get server response.


# Fill in start
quitCommand = 'QUIT\r\n'
sslSocket.send(quitCommand.encode())
recv1 = sslSocket.recv(1024).decode()
print(recv1)
if recv1[:3] !='221':
    print('221 response not received from server.')

# Fill in end
