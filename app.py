from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True)
