 
# main.py

from flask import Flask, render_template, request, redirect, url_for
import smtplib

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_draft', methods=['POST'])
def generate_draft():
    recipient = request.form['recipient']
    subject = request.form['subject']
    body = request.form['body']

    # Generate the email draft
    draft = f"""
    To: {recipient}
    Subject: {subject}

    {body}
    """

    # Save the draft to a temporary location
    with open('draft.txt', 'w') as f:
        f.write(draft)

    # Redirect the user to the draft page
    return redirect(url_for('draft'))

@app.route('/draft')
def draft():
    # Retrieve the draft from the temporary location
    with open('draft.txt', 'r') as f:
        draft = f.read()

    # Render the draft page
    return render_template('draft.html', draft=draft)

@app.route('/send_email')
def send_email():
    # Retrieve the draft from the temporary location
    with open('draft.txt', 'r') as f:
        draft = f.read()

    # Send the email
    smtp_server = 'smtp.example.com'
    smtp_port = 587
    username = 'username'
    password = 'password'

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(username, password)
    server.sendmail(username, recipient, draft)
    server.quit()

    # Redirect the user to the success page
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
