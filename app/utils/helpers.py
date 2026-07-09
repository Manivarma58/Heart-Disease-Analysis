from datetime import date, datetime


def age_from_dob(dob):
    born = datetime.strptime(dob, "%Y-%m-%d").date()
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def send_ntfy_email(email_address, subject, body):
    import urllib.request
    # Clean the email to form a valid URL path topic
    clean_email = email_address.replace("@", "_").replace(".", "_")
    url = f"https://ntfy.sh/cardioviz_verification_{clean_email}"
    
    req = urllib.request.Request(url, data=body.encode('utf-8'))
    req.add_header("X-Email", email_address)
    req.add_header("X-Title", subject)
    try:
        with urllib.request.urlopen(req) as response:
            return response.read()
    except Exception as e:
        print(f"Error sending email via ntfy.sh to {email_address}:", e)


def send_real_email_async(email, subject, body):
    import threading
    thread = threading.Thread(target=send_ntfy_email, args=(email, subject, body))
    thread.start()
