from flask import Flask, request, render_template
from icrawler.builtin import GoogleImageCrawler
import os
import zipfile
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

def download_images(keyword, num_images):
    output_dir = f'./downloads/{keyword}'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    google_crawler = GoogleImageCrawler(storage={'root_dir': output_dir})

    google_crawler.crawl(keyword=keyword, max_num=num_images)

    zip_file_path = f'{output_dir}.zip'
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for root, _, files in os.walk(output_dir):
            for file in files:
                zipf.write(os.path.join(root, file), arcname=file)

    return zip_file_path

def send_email(recipient_email, zip_file_path):
    sender_email = "aagarwal_be22@thapar.edu" 
    sender_password = "phdw wnpi wgec xiht" 

    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Your Downloaded Images"

    msg.set_content("Attached are the images you requested.")

    with open(zip_file_path, "rb") as attachment:
        msg.add_attachment(attachment.read(), maintype='application', subtype='zip', filename=os.path.basename(zip_file_path))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download_images', methods=['POST'])
def download_images_route():
    keyword = request.form['keyword']
    num_images = int(request.form['num_images'])
    email = request.form['email']

    zip_file_path = download_images(keyword, num_images)
    send_email(email, zip_file_path)

    return f"Images for '{keyword}' have been downloaded and sent to {email}."

if __name__ == "__main__":
    app.run(debug=True)
