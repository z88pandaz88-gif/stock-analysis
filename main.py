from flask import Flask, jsonify, send_file, render_template_string
from database.models import init_database, get_session, Analysis
from agents.data_collector import collect_all_data
from agents.technical_analysis import analyze_all_stocks, get_top_picks
from agents.report_generator import generate_excel_report
from utils.helpers import logger, get_cairo_time
from utils.config import EGYPTIAN_STOCKS
import os

app = Flask(__name__)

# Dashboard HTML Template
DASHBOARD_HTML = """
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <title>نظام التحليل الفني - البورصة المصرية</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
        h1 { color: #333; text-align: center; }
        .stats { display: flex; justify-content: space-around; margin: 20px 0; }
        .stat-box { background: #366092; color: white; padding: 20px; border-radius: 5px; text-align: center; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th { background: #366092; color: white; padding: 10px; }
        td { padding: 10px; border-bottom: 1px solid #ddd; text-align: center; }
        .buy { background: #90EE90; }
        .sell { background: #FF6B6B; }
        .hold { background: #FFD700; }
        button { background: #366092; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        button:hover { background: #254a73; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 نظام التحليل الفني للبورصة المصرية</h1>
        <p style="text-align: center;">آخر تحديث: {{ timestamp }}</p>
        
        <div class="stats">
            <div class="stat-box">
                <h3>إجمالي الأسهم</h3>
                <h2>{{ total_stocks }}</h2>
            </div>
            <div class="stat-box">
                <h3>توصيات شراء</h3>
                <h2>{{ buy_count }}</h2>
            </div>
            <div class="stat-box">
                <h3>توصيات بيع</h3>
                <h2>{{ sell_count }}</h2>
            </div>
        </div>
        
        <div style="text-align: center;">
            <a href="/run-analysis"><button>🔄 تشغيل التحليل الكامل</button></a>
            <a href="/download-report"><button>📊 تحميل تقرير Excel</button></a>
        </div>
        
        <h2>أفضل 10 توصيات</h2>
        <table>
            <tr>
                <th>الترتيب</th>
                <th>الرمز</th>
                <th>السعر</th>
                <th>الإشارة</th>
                <th>النقاط</th>
                <th>الاتجاه</th>
            </tr>
            {% for stock in top_stocks %}
            <tr>
                <td>{{ loop.index }}</td>
                <td><strong>{{ stock.symbol }}</strong></td>
                <td>{{ "%.2f"|format(stock.current_price) }}</td>
                <td class="{{ stock.signal.lower() }}">{{ stock.signal }}</td>
                <td>{{ stock.score }}</td>
                <td>{{ stock.trend }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """الصفحة الرئيسية - Dashboard"""
    session = get_session()
    
    # إحصائيات
    total = session.query(Analysis).count()
    buy = session.query(Analysis).filter(Analysis.signal == 'BUY').count()
    sell = session.query(Analysis).filter(Analysis.signal == 'SELL').count()
    
    # أفضل 10
    top = get_top_picks(10)
    
    return render_template_string(
        DASHBOARD_HTML,
        timestamp=get_cairo_time().strftime('%Y-%m-%d %H:%M'),
        total_stocks=total,
        buy_count=buy,
        sell_count=sell,
        top_stocks=top
    )

@app.route('/run-analysis')
def run_analysis():
    """تشغيل التحليل الكامل"""
    try:
        logger.info("🚀 Starting full analysis...")
        
        # 1. جمع البيانات
        logger.info("Step 1: Data Collection")
        collection = collect_all_data()
        
        # 2. التحليل الفني
        logger.info("Step 2: Technical Analysis")
        analysis = analyze_all_stocks()
        
        # 3. إنشاء التقرير
        logger.info("Step 3: Report Generation")
        report_path = generate_excel_report()
        
        return jsonify({
            'status': 'success',
            'timestamp': get_cairo_time().isoformat(),
            'stocks_collected': len(collection['success']),
            'stocks_analyzed': len(analysis),
            'report': report_path,
            'top_5': [
                {'symbol': a['symbol'], 'signal': a['signal'], 'score': a['score']}
                for a in analysis[:5]
            ]
        })
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/download-report')
def download_report():
    """تحميل تقرير Excel"""
    report_path = generate_excel_report()
    if report_path and os.path.exists(report_path):
        return send_file(report_path, as_attachment=True)
    return "No report available", 404

@app.route('/health')
def health():
    """فحص الصحة"""
    return jsonify({
        'status': 'healthy',
        'timestamp': get_cairo_time().isoformat(),
        'stocks_tracked': len(EGYPTIAN_STOCKS)
    })

if __name__ == '__main__':
    init_database()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)