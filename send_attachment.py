# /**
#  *    project: Send attachments through Email by command line interface (CLI)
#  *     author: brownfox2k6
#  *    created: 27/04/2023 18:31:34 Hanoi, Vietnam
# **/

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from os.path import basename, getsize, splitext
from smtplib import SMTP
from ssl import create_default_context
from tkinter import Tk
from tkinter.filedialog import askopenfilenames

from colorama import init as colorama_init
from email_validator import EmailNotValidError, validate_email


class bg:
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

# Print text to terminal with color
puts = lambda color, statement: print(f"{color}{statement}{bg.ENDC}", end='')

# Convert B (bytes) to MB (megabytes)
to_MB = lambda x: round(x / 1048576, ndigits=2)

# Make the terminal text have color
colorama_init(wrap=True)

# Define username & password (directly)
USERNAME = "brfox2k6@gmail.com"
PASSWORD = "tsdlufmldorjhsaj"

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
title = input()
message["Subject"] = title
print()

# Input <recipient>
recipients = []
while True:
    try:
        puts(bg.YELLOW, "Enter recipients (separated by space, just type usernames, \"@gmail.com\" is auto added): ")
        recipients = input().split()
        for x in recipients:
            validate_email(x + "@gmail.com")
        recipients = ", ".join(recipients)
        message["To"] = recipients
        break
    except EmailNotValidError as error:
        puts(bg.RED, f"Error on {x}: {error}\nTry again!\n")

# Get directory of files
print()
Tk().withdraw()
queue = []
available = 26214400   # Maximum total file size allowed is 25 MB (26214400 B)
while True:
    full_paths = askopenfilenames(title="Choose files (\"Cancel\" to escape)")
    if not full_paths:
        break
    s = sum(getsize(full_path) for full_path in full_paths)
    if s <= available:
        for full_path in full_paths:
            queue.append([full_path, basename(full_path), f"{to_MB(getsize(full_path))} MB"])
        available -= s
    else:
        puts(bg.RED, f"Maximum total file size (25 MB) exceeded!! Try again! (You have ")
        puts(bg.HEADER, f"{to_MB(available)} ")
        puts(bg.RED, "MB left)\n")

if not queue:
    puts(bg.RED, "No file to send. Terminating...\n")
    exit()

# Process files
for i in range(len(queue)):
    try:
        # Open & encode
        with open(queue[i][0], "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)

        # Let user rename file
        name, ext = splitext(queue[i][1])
        puts(bg.YELLOW, "Rename ")
        puts(bg.HEADER, f"{queue[i][0]} ")
        puts(bg.YELLOW, "(No need extension, empty to keep unchanged): ")
        temp = input()
        if temp:
            name = temp
            queue[i][1] = f"{name}{ext}"

        # Attach it
        puts(bg.CYAN, "Attaching ")
        puts(bg.HEADER, f"{name}{ext} ")
        puts(bg.CYAN, "...\n")
        part.add_header("Content-Disposition", f"attachment; filename={name}{ext}")
        message.attach(part)
        puts(bg.GREEN, "Succeed!!\n\n")

    except Exception as error:
        puts(bg.RED, f"{error}\n")

# Initialize & print out the summary table
width_to_print = [11, 12]
temp = tuple(zip(*queue))
for i in range(2):
    width_to_print[i] = max(max(len(x) for x in temp[i]) + 2, width_to_print[i])

puts(bg.CYAN, "----- Summary -----\n")
puts(bg.CYAN, f"- Sender: ")
puts(bg.HEADER, f"{USERNAME}\n")
puts(bg.CYAN, f"- Recipient(s): ")
puts(bg.HEADER, f"{recipients}\n")
puts(bg.CYAN, f"- Title: ")
puts(bg.HEADER, f"{title}\n")
puts(bg.CYAN, f"File path{' ' * (width_to_print[0] - 9)}")
puts(bg.CYAN, f"Final name{' ' * (width_to_print[1] - 10)}")
puts(bg.CYAN, f"File size\n")

for item in queue:
    puts(bg.HEADER, f"{item[0]}{' ' * (width_to_print[0] - len(item[0]))}")
    puts(bg.HEADER, f"{item[1]}{' ' * (width_to_print[1] - len(item[1]))}")
    puts(bg.HEADER, f"{item[2]}\n")

# Send or abort?
puts(bg.YELLOW, "Type 'y' or 'Y' to send: ")
if input().strip().lower() == 'y':
    try:
        puts(bg.CYAN, "Sending...\n")
        # server.send_message(message)
        puts(bg.GREEN, "Succeed!! Terminating...\n")
    except Exception as error:
        puts(bg.RED, f"{error}\n")
else:
    puts(bg.RED, "Aborted. Terminating...\n")
