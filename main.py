import requests, smtplib, imghdr, pandas
from email.message import EmailMessage
from PIL import Image, ImageDraw, ImageFont
word = None

def checking_words(text):
    global word
    full_text = text.split(" ")
    spaced_words = " ".join(full_text[0: 9])
    rem_words = " ".join(full_text[9: len(full_text)])

    if len(full_text) > 13:
        word = f"{spaced_words}\n\n{rem_words}"
    else:
        word = spaced_words

def center_text(img, font, text, color="white"):
    draw = ImageDraw.Draw(img)
    text_width, text_height = draw.textsize(text, font)
    position = ((strip_width-text_width)/2,(strip_height-text_height)/2)
    draw.text(position, text, color, font=font)
    return img.save("./today_boost.jpg")

# INCOMING TEXT

quote_response = requests.get("https://winterly-backend.herokuapp.com/quote")
quote_response.raise_for_status()
quote_data = quote_response.json()
quote_text = quote_data["text"]
quote_author = quote_data["author"]
quote = f"{quote_text} -- {quote_author}"


# INCOMING IMAGE

image_response = requests.get("https://source.unsplash.com/1600x900/?nature")
image_response.raise_for_status()
background = image_response.content

with open("image.jpg", mode="wb") as image:
    print(image.write(background))

# RESIZING THE INCOMING IMAGE RESOLUTION

image = Image.open('image.jpg')
new_image = image.resize((800, 450))
new_image.save('image_800.jpg')

# INPUT TEXT ON IMAGE

strip_width, strip_height = 800, 450
text = quote

# WORD CHECK FUNC.
checking_words(text)

# CENTER TEXT FUNC.
background = Image.open("./image_800.jpg")
font = ImageFont.truetype("arial.ttf", 30)
center_text(background, font, word)

# Getting Mail Address From Mail List

mails = pandas.read_csv("mails.csv")
length_mail = len(mails["email_address"])

mail_list = []

def mail_address():
    for _ in range(0, length_mail):
        mail_list.append(mails["email_address"][_])
    return mail_list

receiver_mail = mail_address()

# EMAIL SENDING
my_email = "muhammed15211000@gmail.com"
password = "hgbagdovsjcdimpq"

newMessage = EmailMessage()  # creating an object of EmailMessage class
newMessage['Subject'] = "Here Is A BOOST!!! 4D Day..."  # Defining email subject
newMessage['From'] = my_email  # Defining sender email
newMessage['To'] = receiver_mail  # Defining reciever email
newMessage.set_content('HOPE THIS MADE YOUR DAY... and HAVE A GREAT TIME.')  # Defining email body

with open('today_boost.jpg', 'rb') as image:
    image_data = image.read()
    image_name = image.name
    image_type = imghdr.what(image_name)

newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

with smtplib.SMTP("smtp.gmail.com", 587) as connection:
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.send_message(newMessage)
