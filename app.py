from flask import Flask, render_template, request, jsonify
import json, os

app = Flask(__name__)

CONFIG_FILE = 'config.json'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {
        "sheet_url": "",
        "professors": ["Laura", "Rodrigo", "Ewerton"]
    }

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

@app.route('/')
def index():
    config = load_config()
    return render_template('index.html', professors=config['professors'])

@app.route('/admin')
def admin():
    config = load_config()
    return render_template('admin.html', config=config)

@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify(load_config())

@app.route('/api/config/sheet', methods=['POST'])
def update_sheet():
    data = request.json
    config = load_config()
    config['sheet_url'] = data.get('sheet_url', '')
    save_config(config)
    return jsonify({'success': True, 'sheet_url': config['sheet_url']})

@app.route('/api/config/professors', methods=['POST'])
def update_professors():
    data = request.json
    config = load_config()
    action = data.get('action')
    name = data.get('name', '').strip()
    if action == 'add' and name and name not in config['professors']:
        config['professors'].append(name)
    elif action == 'remove' and name in config['professors']:
        config['professors'].remove(name)
    save_config(config)
    return jsonify({'success': True, 'professors': config['professors']})

@app.route('/api/n8n-webhook-url', methods=['GET'])
def get_n8n_url():
    config = load_config()
    return jsonify({'n8n_webhook': config.get('n8n_webhook', '')})

@app.route('/api/config/webhook', methods=['POST'])
def update_webhook():
    data = request.json
    config = load_config()
    config['n8n_webhook'] = data.get('n8n_webhook', '')
    save_config(config)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)