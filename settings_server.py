from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

def read_settings():
    settings = {}
    try:
        with open('settings.txt', 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=')
                    settings[key] = value
    except FileNotFoundError:
        # Create default settings if file doesn't exist
        settings = {
            'SITE_ID': '740023156',
            'DEPARTURES_TO_SHOW': '3'
        }
        write_settings(settings)
    return settings

def write_settings(settings):
    with open('settings.txt', 'w') as f:
        for key, value in settings.items():
            f.write(f"{key}={value}\n")

@app.route('/')
def index():
    settings = read_settings()
    return render_template('settings.html', settings=settings)

@app.route('/update', methods=['POST'])
def update():
    settings = {
        'SITE_ID': request.form['site_id'],
        'DEPARTURES_TO_SHOW': request.form['departures_to_show']
    }
    write_settings(settings)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)