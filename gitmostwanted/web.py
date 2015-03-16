from gitmostwanted.app import app
from flask import render_template


@app.route('/')
def hello():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
