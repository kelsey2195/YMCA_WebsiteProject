from flask import *

app = Flask(__name__, static_folder='static')

@app.route('/')
def main():
    return render_template('main.html')

with app.test_request_context():
    print(url_for('main'))

if __name__ == '__main__':
    app.run()