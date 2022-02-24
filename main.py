from flask import *

app = Flask(__name__, static_folder='static')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/program_search')
def program_search():
    return render_template('program_search.html')

with app.test_request_context():
    print(url_for('main'))

if __name__ == '__main__':
    app.run()
