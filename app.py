from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Variabilă globală pentru a păstra datele încărcate
data = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global data
    file = request.files['file']
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        try:
            data = pd.read_csv(filepath)
            return jsonify({'status': 'success', 'columns': data.columns.tolist(), 'preview': data.head().to_dict()})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    return jsonify({'status': 'error', 'message': 'No file uploaded'})

@app.route('/statistics', methods=['GET'])
def statistics():
    global data
    if data is not None:
        stats = data.describe().to_dict()
        return jsonify({'status': 'success', 'statistics': stats})
    return jsonify({'status': 'error', 'message': 'No data loaded'})

@app.route('/plot', methods=['POST'])
def plot():
    global data
    if data is not None:
        column = request.json.get('column')
        if column in data.columns:
            plt.figure(figsize=(10, 6))
            data[column].plot(kind='hist', bins=30, color='skyblue', edgecolor='black')
            plt.title(f"Histogramă pentru {column}")
            plt.xlabel(column)
            plt.ylabel("Frecvență")
            plt.grid(True)
            plot_path = os.path.join(UPLOAD_FOLDER, 'plot.png')
            plt.savefig(plot_path)
            plt.close()
            return jsonify({'status': 'success', 'plot_url': '/uploads/plot.png'})
        return jsonify({'status': 'error', 'message': f"Coloana '{column}' nu există"})
    return jsonify({'status': 'error', 'message': 'No data loaded'})

@app.route('/uploads/<filename>')
def serve_file(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename))

if __name__ == '__main__':
    app.run(debug=True)
