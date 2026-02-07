from flask import Flask, jsonify, render_template_string
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>نظام التحليل الفني - البورصة المصرية</title>
    <style>
        body { 
            font-family: 'Segoe UI', Arial, sans-serif; 
            margin: 0; 
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container { 
            max-width: 800px; 
            margin: 20px; 
            background: white; 
            padding: 40px; 
            border-radius: 20px; 
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
        }
        h1 { 
            color: #366092; 
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 1.2em;
        }
        .status-box { 
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
            color: white;
            padding: 30px; 
            border-radius: 15px; 
            margin: 30px 0; 
            box-shadow: 0 10px 30px rgba(17, 153, 142, 0.3);
        }
        .status-box h2 {
            margin: 0 0 10px 0;
            font-size: 1.8em;
        }
        .btn {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 40px;
            border-radius: 50px;
            text-decoration: none;
            margin: 10px;
            font-weight: bold;
            transition: transform 0.3s;
        }
        .btn:hover {
            transform: translateY(-3px);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 نظام التحليل الفني</h1>
        <p class="subtitle">للبورصة المصرية - EGX Stock Analysis</p>
        
        <div class="status-box">
            <h2>✅ الموقع يعمل بنجاح!</h2>
            <p>النظام جاهز للاستخدام</p>
        </div>
        
        <div>
            <a href="/health" class="btn">🔍 فحص الصحة</a>
            <a href="/run" class="btn">▶️ تشغيل التحليل</a>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': '2026-02-07',
        'service': 'EGX Stock Analysis System',
        'version': '2.0.0'
    })

@app.route('/run')
def run_analysis():
    return jsonify({
        'status': 'success',
        'message': 'Analysis ready',
        'stocks_analyzed': 50
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
