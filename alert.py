import config
import smtplib
import db.db as db



def send_down_alert(macs):
	print (" -- Sending Down Alert --")
	message = "Following Devices are down:"
	for mac in macs:
		device = db.get_device(mac)
		message += device["description"] + " : " + mac + " : " + device["ip"] + " : " + device["vendor"]
	send_email("Devices Down Alert", message)
	return


def send_new_alert(macs):
	print (" -- Sending New Device Alert --")
	return

def send_email(subject, text):

	#msg = MIMEMultipart('alternative')
	#msg['Subject'] = 'Pi.Scanner Report'
	#msg['From'] = REPORT_FROM
	#msg['To'] = REPORT_TO
	#msg.attach (MIMEText (pText, 'plain'))
	#msg.attach (MIMEText (pHTML, 'html'))

	header = "To: " + config.EMAIL_TO + "\nFrom: " + \
		config.SMTP_USERNAME + "\n" + "Subject: " + subject
	body = text

	s = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
	s.ehlo()
	s.starttls()
	s.ehlo()
	s.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
	# print body + "\n==================================="
	s.sendmail(config.SMTP_USERNAME, config.EMAIL_TO, header + '\n\n' + body)
	s.quit()

