from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        print(f"Contact Form Submission:\nName: {name}\nEmail: {email}\nMessage: {message}")
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True) 