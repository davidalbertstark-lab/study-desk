import smtplib

try:
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15)
    server.login(
        "davidthebuilder207@gmail.com",
        "eavepeuenyacimij",
    )
    print("LOGIN OK")
    server.quit()
except Exception as e:
    print(type(e).__name__)
    print(e)
