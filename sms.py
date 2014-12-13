import imaplib, urllib, re
from email.header import decode_header

def conn(server,port,login,passw):
	connection = imaplib.IMAP4(server,port)
	connection.login(login, passw)
	return connection

def disconn(connection):
	connection.close()
	connection.logout()

def chdecode(tup):
	if tup[1] != None:
		return tup[0].decode(tup[1],'ignore')
	else:
		return tup[0]

def smssend(num,text):                      #function to send sms via bytehand.com sms gateway. use it or change it for your gateway
	url = 'http://bytehand.com:3800/send?'
	params = {
				'id'  : 'x' ,
				'key' : 'x',
				'to'  : num,
				'from': 'x',
				'text': text
	}
	result = urllib.urlopen(url + urllib.urlencode(params)).read()
	if result.find('"status":0') == 1:
		return True
	else:
		return result


def getmsg(connection):
	r, data = connection.search(None, 'ALL')
	for msg in data[0].split():
		r, flag = connection.fetch(str(msg),"FLAGS")
		match = re.search(r'\\Recent',str(flag))	

		if match:
			r, frm = connection.fetch(str(msg),"(BODY.PEEK[HEADER.FIELDS (From)])")
			r, subj = connection.fetch(str(msg),"(BODY.PEEK[HEADER.FIELDS (Subject)])")
	
			frm = decode_header(frm[0][1][6:].replace('\r\n',''))
			subj = decode_header(subj[0][1][9:].replace('\r\n',''))
			frm = chdecode(frm[0])
			subj = chdecode(subj[0])

			if len(subj) > 20:
				subj = subj[:20] + "..."

			text = frm + " " + subj
			smssend("x",text) #recipient's phone number

mbox = conn("x","x","x","x") #ip, port, login, pass
mbox.select("INBOX")
getmsg(mbox)
disconn(mbox)
