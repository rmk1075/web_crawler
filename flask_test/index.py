from flask import Flask, request, render_template

# Create the application.
APP = Flask(__name__)

@APP.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    APP.run(debug=True)