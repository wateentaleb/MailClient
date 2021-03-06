# MailClient

## Project Overview 

This Project was completed in order to gain more understanding of the interaction of the OSI's Application layer. 


## The Application Layer 

A little overview of the Application Layer in the OSI model, 

The Application layer is the only layer that directly interacts with data from the user. Software applications like web browsers and email clients rely on the application layer to initiate communications. But it should be made clear that client software applications are not part of the application layer; rather the application layer is responsible for the protocols and data manipulation that the software relies on to present meaningful data to the user. Application layer protocols include HTTP as well as SMTP (Simple Mail Transfer Protocol is one of the protocols that enables email communications).

<img width="536" alt="applicationLayer" src="https://user-images.githubusercontent.com/16707828/74702729-d49bfd80-51d8-11ea-8470-e787725ea142.png">


## Project Objective

The task is to develop a simple mail client that sends email to any recipient. The client will need to connect to a mail server, dialogue with the mail server using the SMTP protocol, and send an email message to the mail server. Python provides a library, called smtplib, which has built in methods to send mail using SMTP protocol.. However, I will not be using this library for thsi project, as it hides most of the details of SMTP and socket programming I am to understand and learn.



## Implementation 

The Google's mail server (Gmail) is implemented in this project, port 587 was chosen to implement TLS
`````````````
mailserver = 'smtp.gmail.com'
serverPort = 587
`````````````


 Created a socket called clientSocket and established a TCP connection with mailserver
 The first parameter is indicating that the underlying network is using IPv4
 The second paramater is indicicating that were using a TCP socket and not UDP 
 
 `````````````
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, serverPort))
`````````````
To the user using this, change the email and password for your Gmail account below,  BELOW,
This is the only change that needs to be made to run, 
 `````````````
username = "talebwateen@gmail.com"
password = "xxxxxx"
`````````````

Encoding the username
 `````````````
 encodedUsername = username.encode()
`````````````

Encrypting it into base64 text because thats the language gmail server communicate in
 `````````````
base64User = base64.b64encode(encodedUsername)
`````````````

Encoding password
 `````````````
encodedPassword = password.encode()
`````````````

Encrypting it into base64 text because thats the language gmail server communicate in
 `````````````
base64Password = base64.b64encode(encodedPassword)
`````````````

Sending HELO command 
 `````````````
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
`````````````

Starting Secure Connection Request to the Gmail Servers 

 `````````````
tlsMessage = 'STARTTLS\r\n'
clientSocket.send(tlsMessage.encode())
`````````````

Creating a SSL wrapper on our socket to maintain a secured connection to Google's Mail Servers 

 `````````````
sslSocket = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_SSLv23)
sslCommand = 'AUTH LOGIN\r\n'
sslSocket.send(sslCommand.encode())
`````````````

Now that a secure connection has been established with Google's Mail Servers, the data sent and received are in ecrypted base64 text. The wrapped socket will need to be used from this point on whenever receiving/sending data with the Gmail's Servers such as: 

 `````````````
sslSocket.send(base64Password+"\r\n".encode())
`````````````

