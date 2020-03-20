import time
import ssl
import smtplib



def parse(keyword):
	keyword = keyword.replace(' ', '&')
	return keyword


def alert(receiver_email):
	port = 587
	smtp_server = "smtp.gmail.com"
	sender_email = "some_bot@gmail.com" # To-do: Make an account
	password = "some_bot_password" # To-do: Make an account
	# To-do: Add more info to email
	message = """\
	Subject: Price drop alert

	The price of a product on your wish list has dropped.""" 
	context = ssl.create_default_context()

	try:
		with smtplib.SMTP(smtp_server, port) as server:
			server.ehlo()
			server.starttls(context=context)
			server.ehlo()
			server.login(sender_email, password)
			server.sendmail(sender_email, receiver_email, message)
		print("==========Email sent!==========")
	except Exception as e:
		print(e)
	finally:
		server.quit()


def check_price(table, threshold):
	bool_idx = table['price'] < threshold
	if sum(bool_idx):
		lowered_table = table[bool_idx]
		return lowered_table
	else:
		return False


