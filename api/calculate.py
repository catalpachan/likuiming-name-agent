import json
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bazi_calculator import BaziCalculator
from name_generator import NameGenerator
from fortune_analyzer import FortuneAnalyzer

def handler(request):
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': ''
        }
    
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        data = request.json
        
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
        
        # 计算八字
        calculator = BaziCalculator()
        bazi_result = calculator.calculate(birth_date, birth_time)
        
        # 生成姓名
        name_gen = NameGenerator()
        names_result = name_gen.generate_names(
            surname=surname,
            gender=gender,
            bazi=bazi_result,
            count=2
        )
        
        # 生成备用字
        backup_chars = name_gen.generate_backup_chars(
            bazi=bazi_result,
            count=12
        )
        
        # 命理分析
        analyzer = FortuneAnalyzer()
        fortune_result = analyzer.analyze(bazi_result, names_result['primary_names'])
        
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
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(result)
        }
        
    except Exception as e:
        import traceback
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'success': False, 'error': str(e), 'traceback': traceback.format_exc()})
        }
