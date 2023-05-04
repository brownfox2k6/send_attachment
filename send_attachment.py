# /**
#  *    project: Send attachments through Email by command line interface (CLI)
#  *     author: brownfox2k6
#  *    created: 27/04/2023 18:31:34 Hanoi, Vietnam
# **/

from smtplib import SMTP
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
from ssl import create_default_context
from colorama import init as colorama_init
from email_validator import EmailNotValidError, validate_email
from os.path import splitext, basename
from tkinter import Tk
from tkinter.filedialog import askopenfilenames

class bg:
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

# Print text to terminal with color
def puts(color, statement):
    print(f"{color}{statement}{bg.ENDC}", end='')

# Make the terminal text have color
colorama_init(wrap=True)

# Define username & password (directly)
USERNAME = ""
PASSWORD = ""

# Initialize SMTP Gmail server
puts(bg.CYAN, "Initializing SMTP Gmail server...\n")
server = SMTP(host="smtp.gmail.com", port=587)
server.ehlo()
server.starttls(context=create_default_context())
server.ehlo()
puts(bg.GREEN, "Succeed!!\n")

# Login
puts(bg.CYAN, f"Login ")
puts(bg.HEADER, f"{USERNAME} ")
puts(bg.CYAN, "...\n")
server.login(USERNAME, PASSWORD)
puts(bg.GREEN, f"Succeed!!\nWelcome ")
puts(bg.HEADER, f"{USERNAME} ")
puts(bg.GREEN, "~\n\n")

# Initialize message
message = MIMEMultipart()
message["From"] = USERNAME

# Input <subject>
puts(bg.YELLOW, "Enter subject (Empty is ok): ")
message["Subject"] = input()
print()

# Input <recipient>
while True:
    try:
        puts(bg.YELLOW, "Enter recipient (just type username, \"@gmail.com\" is auto added): ")
        recipient = input() + "@gmail.com"
        validate_email(recipient)
        message["To"] = recipient
        break
    except EmailNotValidError as error:
        puts(bg.RED, f"{error}\n")

# Get directory of files
print()
Tk().withdraw()
queue = []
while True:
    full_paths = askopenfilenames(title="Choose files (\"Cancel\" to escape)")
    if not full_paths:
        break
    queue.extend(full_paths)

# Process files
for full_path in queue:
    try:
        # Open & encode
        with open(full_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)

        # Let user rename file
        name, ext = splitext(basename(full_path))
        puts(bg.YELLOW, "Rename ")
        puts(bg.HEADER, f"{full_path} ")
        puts(bg.YELLOW, "(Empty to keep unchanged): ")
        temp = input()
        if temp:
            name = temp

        # Attach it
        puts(bg.CYAN, "Attaching ")
        puts(bg.HEADER, f"{name}{ext} ")
        puts(bg.CYAN, "...\n")
        part.add_header("Content-Disposition", f"attachment; filename={name}{ext}")
        message.attach(part)
        puts(bg.GREEN, "Succeed!!\n\n")

    except Exception as error:
        puts(bg.RED, f"{error}\n")

# Send message
puts(bg.CYAN, "Sending...\n")
server.send_message(message)
puts(bg.GREEN, "Succeed!! Terminating...\n")
