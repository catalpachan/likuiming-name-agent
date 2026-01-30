from flask import Flask, render_template, request, jsonify, send_from_directory
from datetime import datetime
import json
import os

from bazi_calculator import BaziCalculator
from name_generator import NameGenerator
from fortune_analyzer import FortuneAnalyzer
from pdf_generator import PDFGenerator

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({'status': 'ok', 'message': '服务正常运行'})

@app.route('/api/config', methods=['GET'])
def get_config():
    """获取小程序配置"""
    return jsonify({
        'success': True,
        'data': {
            'appName': '李居明起名系统',
            'version': '1.0.0',
            'features': [
                '八字分析',
                '五行配名',
                '三才五格',
                '运势分析',
                'PDF报告'
            ]
        }
    })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        print("Received data:", data)
        
        # 提取输入数据
        birth_date = data.get('birthDate')
        birth_time = data.get('birthTime')
        surname = data.get('surname')
        gender = data.get('gender')
        height = data.get('height')
        weight = data.get('weight')
        birth_order = data.get('birthOrder')
        birthplace = data.get('birthplace')
        ancestral_home = data.get('ancestralHome')
        parent_names = data.get('parentNames', [])
        parent_births = data.get('parentBirths', [])
        grandparent_names = data.get('grandparentNames', [])
        grandparent_births = data.get('grandparentBirths', [])
        
        print(f"Calculating for: {birth_date} {birth_time}, {surname}, {gender}")
        
        # 计算八字
        calculator = BaziCalculator()
        bazi_result = calculator.calculate(birth_date, birth_time)
        print("Bazi result:", bazi_result)
        
        # 生成姓名
        name_gen = NameGenerator()
        names_result = name_gen.generate_names(
            surname=surname,
            gender=gender,
            bazi=bazi_result,
            count=2
        )
        print("Names generated")
        
        # 生成备用字
        backup_chars = name_gen.generate_backup_chars(
            bazi=bazi_result,
            count=12
        )
        
        # 命理分析
        analyzer = FortuneAnalyzer()
        fortune_result = analyzer.analyze(bazi_result, names_result['primary_names'])
        print("Fortune analyzed")
        
        # 生成英文名建议
        english_names = name_gen.suggest_english_names(bazi_result)
        
        result = {
            'success': True,
            'birthInfo': {
                'solarDate': birth_date,
                'solarTime': birth_time,
                'lunarDate': bazi_result['lunar_date'],
                'lunarTime': bazi_result['lunar_time'],
                'gender': gender,
                'surname': surname,
                'height': height,
                'weight': weight,
                'birthOrder': birth_order,
                'birthplace': birthplace,
                'ancestralHome': ancestral_home,
                'parentNames': parent_names,
                'parentBirths': parent_births,
                'grandparentNames': grandparent_names,
                'grandparentBirths': grandparent_births
            },
            'bazi': {
                'year': bazi_result['year_pillar'],
                'month': bazi_result['month_pillar'],
                'day': bazi_result['day_pillar'],
                'hour': bazi_result['hour_pillar'],
                'dayMaster': bazi_result['day_master'],
                'yongShen': bazi_result['yong_shen']
            },
            'wuxing': bazi_result['wuxing_analysis'],
            'primaryNames': names_result['primary_names'],
            'backupChars': backup_chars,
            'englishNames': english_names,
            'fortune': fortune_result,
            'disclaimer': '八字命理占算，在科學觀點上祇可作為引証參考和研究，所提供之言論和方案，行使之決斷和成效上，責任在於問事本人。'
        }
        
        print("Sending response")
        return jsonify(result)
        
    except Exception as e:
        import traceback
        print("Error:", str(e))
        print("Traceback:", traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/generate-pdf', methods=['POST'])
def generate_pdf():
    try:
        data = request.json
        pdf_gen = PDFGenerator()
        pdf_path = pdf_gen.generate(data)
        filename = os.path.basename(pdf_path)
        return jsonify({'success': True, 'pdfUrl': f'/download/{filename}'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/download/<filename>')
def download_pdf(filename):
    try:
        return send_from_directory('/tmp', filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
