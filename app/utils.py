import time
import ssl
import smtplib



def parse(keyword):
	keyword = keyword.replace(' ', '+')
	return keyword


def send_alert(receiver_email):
	port = 587
	smtp_server = "smtp.gmail.com"
	sender_email = "backupdrive199@gmail.com"
	sender_password = "backitup"
	# To-do: Add more info to email
	message = """\
	Subject: Price alert

	The price of a product on your wish list has dropped.""" 
	context = ssl.create_default_context()

	try:
		with smtplib.SMTP(smtp_server, port) as server:
			server.starttls(context=context)
			server.login(sender_email, sender_password)
			server.sendmail(sender_email, receiver_email, message)
		print("==========Email sent!==========")
	except Exception as e:
		print(e)


# To-do: convert string to float for price comparison
def check_price(table, threshold):
	bool_idx = table['price'] < threshold
	if sum(bool_idx):
		lowered_table = table[bool_idx]
		return lowered_table
	else:
		return False


