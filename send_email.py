import smtplib

sender_email="arpitasamant828@gmail.com"
password="tvxl cpbw yzce pbya"

server=smtplib.SMTP("smtp.gmail.com",587)
server.starttls()
server.login(sender_email,password)

file=open("low_attendance.csv","r")

for line in file:
    roll,name,email,attendance=line.strip().split(",")

    subject="Attendance Warning"
    body=f"Hello {name}, your attendance is {attendance}%. Please improve it."

    message=f"Subject:{subject}\n\n{body}"

    server.sendmail(sender_email,email,message)

file.close()
server.quit()