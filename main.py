import tkinter as tk
from tkinter import filedialog as fd
import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Charge les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupère les valeurs des variables d'environnement
GOOGLE_PASS = os.getenv('GOOGLE_PASS')
SERVEUR_SMTP = os.getenv('SERVEUR_SMTP', 'smtp.gmail.com')
PORT_SMTP = int(os.getenv('PORT_SMTP', '587'))
ADRESSE_EXPEDITEUR = os.getenv('ADRESSE_EXPEDITEUR')


def send_email_with_attachment(sender_email, receiver_email, subject, body, attachment_path, smtp_server, smtp_port,
                               smtp_username, smtp_password):
    try:
        # Créer le message email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Ajouter le corps de l'email
        msg.attach(MIMEText(body, 'plain'))

        # Attacher la pièce jointe
        with open(attachment_path, 'rb') as attachment_file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment_file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(attachment_path)}')
            msg.attach(part)

        # Envoyer l'email via le serveur SMTP
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Utiliser TLS pour sécuriser la connexion
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())

        print(f"Email envoyé avec la pièce jointe: {os.path.basename(attachment_path)}")

    except smtplib.SMTPAuthenticationError:
        print("Erreur d'authentification SMTP. Vérifiez vos identifiants.")
    except smtplib.SMTPException as e:
        print(f"Erreur SMTP lors de l'envoi de l'email : {e}")
    except Exception as e:
        print(f"Erreur inattendue lors de l'envoi de l'email : {e}")


def select_files():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )
    filenames = fd.askopenfilenames(title='Open files', initialdir='/', filetypes=filetypes)
    listbox_files.delete(0, tk.END)
    for file in filenames:
        listbox_files.insert(tk.END, file)


def send_emails():
    sender_email = entry_from.get()
    receiver_email = entry_to.get()
    subject = entry_subject.get()
    body = text_body.get("1.0", tk.END)

    for index in listbox_files.get(0, tk.END):
        send_email_with_attachment(sender_email, receiver_email, subject, body, index, SERVEUR_SMTP, PORT_SMTP,
                                   ADRESSE_EXPEDITEUR, GOOGLE_PASS)


root = tk.Tk()
root.title("Envoi de mail avec pièce jointe")

label_from = tk.Label(root, text="De :")
label_from.grid(row=0, column=0)
entry_from = tk.Entry(root, width=50)
entry_from.insert(0, ADRESSE_EXPEDITEUR)
entry_from.grid(row=0, column=1)

label_to = tk.Label(root, text="À :")
label_to.grid(row=1, column=0)
entry_to = tk.Entry(root, width=50)
entry_to.grid(row=1, column=1)

label_subject = tk.Label(root, text="Sujet :")
label_subject.grid(row=2, column=0)
entry_subject = tk.Entry(root, width=50)
entry_subject.grid(row=2, column=1)

label_body = tk.Label(root, text="Corps :")
label_body.grid(row=3, column=0)
text_body = tk.Text(root, width=50, height=10)
text_body.grid(row=3, column=1)

label_files = tk.Label(root, text="Fichiers :")
label_files.grid(row=4, column=0)
listbox_files = tk.Listbox(root, width=50)
listbox_files.grid(row=4, column=1)
button_files = tk.Button(root, text="Sélectionner", command=select_files)
button_files.grid(row=4, column=2)

button_send = tk.Button(root, text="Envoyer", command=send_emails)
button_send.grid(row=5, column=1)

root.mainloop()
