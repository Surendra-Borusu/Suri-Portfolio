from flask import Flask, render_template, request, flash, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv
from flask_mail import Mail, Message

# Debug: Print current working directory and .env file location
print(f"Current working directory: {os.getcwd()}")
print(f"Files in current directory: {os.listdir('.')}")

# Try to load .env file with explicit path
env_path = os.path.join(os.getcwd(), '.env')
print(f"Looking for .env file at: {env_path}")
print(f".env file exists: {os.path.exists(env_path)}")

# Try to read .env file directly
try:
    with open(env_path, 'r') as f:
        print("\nContents of .env file:")
        print(f.read())
except Exception as e:
    print(f"Error reading .env file: {str(e)}")

# Load environment variables from config.env
load_dotenv('config.env', override=True)

app = Flask(__name__)
app.secret_key = '19828282'  # Required for flash messages

# Get email configuration from environment variables
sender_email = os.getenv('MAIL_USERNAME')
sender_password = os.getenv('MAIL_PASSWORD')
receiver_email = os.getenv('MAIL_RECIPIENT')

# Debug: Print configuration (without password)
print(f"\nEmail Configuration:")
print(f"Sender Email: {sender_email}")
print(f"Receiver Email: {receiver_email}")
print(f"Password is set: {'Yes' if sender_password else 'No'}")

# Print all environment variables for debugging
print("\nAll environment variables:")
for key, value in os.environ.items():
    if 'MAIL' in key:
        print(f"{key}: {value}")

# Ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

def init_db():
    db_path = os.path.join(app.instance_path, 'messages.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  email TEXT NOT NULL,
                  message TEXT NOT NULL,
                  date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def get_db():
    db_path = os.path.join(app.instance_path, 'messages.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

# Initialize Flask-Mail
mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/messages')
def view_messages():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM messages ORDER BY date DESC')
    messages = c.fetchall()
    conn.close()
    return render_template('messages.html', messages=messages)

@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Store message in database
        conn = get_db()
        c = conn.cursor()
        c.execute('INSERT INTO messages (name, email, message) VALUES (?, ?, ?)',
                 (name, email, message))
        conn.commit()
        conn.close()
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = f"New Contact Form Message from {name}"
            
            body = f"""
            Name: {name}
            Email: {email}
            Message: {message}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Create SMTP session
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()
            
            flash('Your message has been sent successfully! We will get back to you soon.', 'success')
            return redirect(url_for('success'))
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            flash('Sorry, there was an error sending your message. Please try again later.', 'error')
            return redirect(url_for('home'))

@app.route('/send_email', methods=['POST'])
def send_email():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        try:
            msg = Message(
                subject=f'New Contact Form Submission from {name}',
                recipients=[os.getenv('MAIL_USERNAME')],
                body=f'''
                Name: {name}
                Email: {email}
                Message: {message}
                '''
            )
            mail.send(msg)
            flash('Your message has been sent successfully!', 'success')
        except Exception as e:
            flash('An error occurred while sending your message. Please try again later.', 'error')
            print(f"Error sending email: {str(e)}")
        
        return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000) 