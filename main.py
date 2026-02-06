from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>🚀 نظام التحليل الفني للبورصة المصرية</h1>
    <h2>الموقع يعمل بنجاح!</h2>
    <p>جاري إعداد النظام...</p>
    <a href="/health">فحص الصحة</a>
    """

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': '2026-02-06',
        'message': 'System is running'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
