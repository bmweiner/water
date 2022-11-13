import os
from flask import Flask
from flask import render_template
from water_data import today, daily

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('base.html', today=today(), daily=daily())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
