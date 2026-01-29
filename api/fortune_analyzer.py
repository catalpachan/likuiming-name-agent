import random

class FortuneAnalyzer:
    """命理分析器 - 分析主运、前运、后运等命理信息"""
    
    # 81数理吉凶表（部分）
    LING_SHU_JI_XIONG = {
        1: {'ji_xiong': '吉', 'meaning': '太极之数，万物开泰，生发无穷，利禄亨通'},
        2: {'ji_xiong': '凶', 'meaning': '两仪之数，混沌未开，进退保守，志望难达'},
        3: {'ji_xiong': '吉', 'meaning': '三才之数，天地人和，大事大业，繁荣昌隆'},
        4: {'ji_xiong': '凶', 'meaning': '四象之数，待于生发，万事慎重，不具营谋'},
        5: {'ji_xiong': '吉', 'meaning': '五行俱权，循环相生，圆通畅达，福祉无穷'},
        6: {'ji_xiong': '吉', 'meaning': '六爻之数，发展变化，天赋美德，吉祥安泰'},
        7: {'ji_xiong': '吉', 'meaning': '七政之数，精悍严谨，天赋之力，吉星照耀'},
        8: {'ji_xiong': '吉', 'meaning': '八卦之数，乾坎艮震，巽离坤兑，无穷无尽'},
        9: {'ji_xiong': '凶', 'meaning': '大成之数，蕴涵凶险，或成或败，难以把握'},
        10: {'ji_xiong': '凶', 'meaning': '终结之数，雪暗飘零，偶或有成，回顾茫然'},
        11: {'ji_xiong': '吉', 'meaning': '旱苗逢雨，万物更新，调顺发达，恢弘泽世'},
        12: {'ji_xiong': '凶', 'meaning': '掘井无泉，意志脆弱，家庭寂寞，难酬志向'},
        13: {'ji_xiong': '吉', 'meaning': '春日牡丹，才艺多能，智谋奇略，忍柔当事'},
        14: {'ji_xiong': '凶', 'meaning': '破兆之数，家庭缘薄，孤独遭难，谋事不达'},
        15: {'ji_xiong': '吉', 'meaning': '福寿圆满，富贵荣誉，涵养雅量，德高望重'},
        16: {'ji_xiong': '吉', 'meaning': '厚重之数，贵人得助，兴家兴业，名利双收'},
        17: {'ji_xiong': '吉', 'meaning': '刚强之数，突破万难，如能容忍，必获成功'},
        18: {'ji_xiong': '吉', 'meaning': '铁镜重磨，权威显达，博得名利，且养柔德'},
        19: {'ji_xiong': '凶', 'meaning': '多难之数，风云蔽日，辛苦重来，虽有智谋'},
        20: {'ji_xiong': '凶', 'meaning': '屋下藏金，非业破运，灾难重重，进退维谷'},
        21: {'ji_xiong': '吉', 'meaning': '明月中天，光风霁月，万物确立，官运亨通'},
        22: {'ji_xiong': '凶', 'meaning': '秋草逢霜，困难疾弱，虽出豪杰，人生波折'},
        23: {'ji_xiong': '吉', 'meaning': '壮丽之数，旭日东升，权威旺盛，功名荣达'},
        24: {'ji_xiong': '吉', 'meaning': '掘藏得金，家门余庆，金钱丰盈，白手成家'},
        25: {'ji_xiong': '吉', 'meaning': '英俊之数，资性英敏，才能奇特，涵养性情'},
        26: {'ji_xiong': '凶', 'meaning': '变怪之谜，英雄豪杰，波澜重叠，奏大功者'},
        27: {'ji_xiong': '吉', 'meaning': '增长之数，欲望无止，自我强烈，多受毁谤'},
        28: {'ji_xiong': '凶', 'meaning': '阔水浮萍，遭难之数，豪杰气概，四海漂泊'},
        29: {'ji_xiong': '吉', 'meaning': '智谋之数，财力归集，名闻海内，成就大业'},
        30: {'ji_xiong': '凶', 'meaning': '绝境之数，沉浮不定，凶吉难变，若明若暗'},
        31: {'ji_xiong': '吉', 'meaning': '春日花开，智勇得志，博得名利，统领众人'},
        32: {'ji_xiong': '吉', 'meaning': '宝马金鞍，侥幸多望，贵人得助，财帛如裕'},
        33: {'ji_xiong': '吉', 'meaning': '升天家门，鸾凤相会，名闻天下，隆昌至极'},
        34: {'ji_xiong': '凶', 'meaning': '破家之数，灾难不绝，难望成功，此数大凶'},
        35: {'ji_xiong': '吉', 'meaning': '高楼望月，温和平静，智达通畅，文昌技艺'},
        36: {'ji_xiong': '凶', 'meaning': '波澜重叠，沉浮万状，侠肝义胆，舍己成仁'},
        37: {'ji_xiong': '吉', 'meaning': '猛虎出林，权威显达，热诚忠信，宜着雅量'},
        38: {'ji_xiong': '凶', 'meaning': '磨铁成针，刻意经营，多劳少获，艺能发展'},
        39: {'ji_xiong': '吉', 'meaning': '富贵荣华，财帛丰盈，德泽四方，富贵至极'},
        40: {'ji_xiong': '凶', 'meaning': '退安之数，智谋胆力，冒险投机，沉浮不定'},
    }
    
    # 运势描述模板
    ZHU_YUN_TEMPLATES = {
        '吉': [
            "主一生人之運勢，此數能得大財利，健康，名譽，財富三俱足。",
            "主一生人之運勢，智仁勇三德兼備，能統眾人，至榮華富貴。",
            "主一生人之運勢，此數具才謀德澤，又能傳子孫，吉祥無上。",
            "主一生人之運勢，此數熱誠得人心、排除萬難，能成大事業之數。"
        ],
        '凶': [
            "主一生人之運勢，此數雖有智謀，但恐有波折，宜謹慎行事。",
            "主一生人之運勢，此數浮沉不定，宜修身養性，以靜制動。"
        ]
    }
    
    QIAN_YUN_TEMPLATES = {
        '吉': [
            "主前半生之運勢，此數能馴伏一切困難，能成大事業者。",
            "主前半生之運勢，此數具馴伏一切艱難之大氣慨，氣勢沖天，能成大事業者。",
            "主前半生之運勢，此數男子必俊秀，有貴人緣，柔中帶剛，成功發達之數。"
        ],
        '凶': [
            "主前半生之運勢，此數雖有波折，但堅持不懈終能成功。"
        ]
    }
    
    HOU_YUN_TEMPLATES = {
        '吉': [
            "主中晚年之運勢，此數享權名壽祿，具才謀德澤，又能傳子孫。",
            "主中晚年之運勢，富貴長壽之大吉數，此數熱誠得人心、排除萬難，能成大事業之數。",
            "主中晚年之運勢，榮華富貴，此數具才謀德澤，又能傳子孫，吉祥無上。"
        ],
        '凶': [
            "主中晚年之運勢，此數宜守成，修身養性，以享天年。"
        ]
    }
    
    # 居明評語模板
    JU_MING_COMMENTS = {
        '木': {
            '水': "『丁火生{month_zhi}月，土金當旺，水旺土弱，用神以木火，丁火身強，可更添健康財貴。智輝木火俱備，五行配合音佳且帶氣質之名。』",
            '火': "『丁火生{month_zhi}月，土金當旺，用神以木火，丁火身強，可更添健康財貴。』"
        },
        '火': {
            '木': "『丁火生{month_zhi}月，土金當旺，用神以木火，丁火身強，可更添健康財貴。』"
        },
        '水': {
            '金': "『{day_gan}金生{month_zhi}月，水旺金相，用神以金水，可更添健康財貴。』"
        },
        '金': {
            '水': "『{day_gan}金生{month_zhi}月，水旺金相，用神以金水，可更添健康財貴。』"
        },
        '土': {
            '火': "『{day_gan}土生{month_zhi}月，火土當旺，用神以火土，可更添健康財貴。』"
        }
    }
    
    # 卦名
    GUA_NAMES = {
        '大吉': ['金錢豐惠卦', '榮華富貴卦', '和順圓滿卦', '慈祥忠實卦'],
        '吉': ['壯麗果敢卦', '英邁俊敏卦', '智勇雙全卦', '德澤廣被卦'],
        '凶': ['波瀾起伏卦', '謹慎保守卦', '修身養性卦']
    }
    
    def __init__(self):
        pass
    
    def get_ling_shu_meaning(self, number):
        """获取81数理吉凶含义"""
        if number > 40:
            # 大于40的数，取个位数或循环
            number = number % 40 + 1
        return self.LING_SHU_JI_XIONG.get(number, {
            'ji_xiong': '平',
            'meaning': '中平之數，宜守不宜攻，穩重行事'
        })
    
    def analyze_zhu_yun(self, zongge):
        """分析主运（总格）"""
        ling_shu = self.get_ling_shu_meaning(zongge)
        ji_xiong = ling_shu['ji_xiong']
        
        # 选择描述
        if ji_xiong in self.ZHU_YUN_TEMPLATES:
            description = random.choice(self.ZHU_YUN_TEMPLATES[ji_xiong])
        else:
            description = random.choice(self.ZHU_YUN_TEMPLATES['吉'])
        
        # 选择卦名
        if ji_xiong == '吉':
            gua_name = random.choice(self.GUA_NAMES['大吉'] + self.GUA_NAMES['吉'])
        elif ji_xiong == '凶':
            gua_name = random.choice(self.GUA_NAMES['凶'])
        else:
            gua_name = random.choice(self.GUA_NAMES['吉'])
        
        return {
            'number': zongge,
            'ji_xiong': ji_xiong,
            'description': description,
            'gua_name': gua_name,
            'meaning': ling_shu['meaning']
        }
    
    def analyze_qian_yun(self, renge):
        """分析前运（人格）"""
        ling_shu = self.get_ling_shu_meaning(renge)
        ji_xiong = ling_shu['ji_xiong']
        
        if ji_xiong in self.QIAN_YUN_TEMPLATES:
            description = random.choice(self.QIAN_YUN_TEMPLATES[ji_xiong])
        else:
            description = random.choice(self.QIAN_YUN_TEMPLATES['吉'])
        
        if ji_xiong == '吉':
            gua_name = random.choice(self.GUA_NAMES['大吉'] + self.GUA_NAMES['吉'])
        elif ji_xiong == '凶':
            gua_name = random.choice(self.GUA_NAMES['凶'])
        else:
            gua_name = random.choice(self.GUA_NAMES['吉'])
        
        return {
            'number': renge,
            'ji_xiong': ji_xiong,
            'description': description,
            'gua_name': gua_name,
            'meaning': ling_shu['meaning']
        }
    
    def analyze_hou_yun(self, dige):
        """分析后运（地格）"""
        ling_shu = self.get_ling_shu_meaning(dige)
        ji_xiong = ling_shu['ji_xiong']
        
        if ji_xiong in self.HOU_YUN_TEMPLATES:
            description = random.choice(self.HOU_YUN_TEMPLATES[ji_xiong])
        else:
            description = random.choice(self.HOU_YUN_TEMPLATES['吉'])
        
        if ji_xiong == '吉':
            gua_name = random.choice(self.GUA_NAMES['大吉'] + self.GUA_NAMES['吉'])
        elif ji_xiong == '凶':
            gua_name = random.choice(self.GUA_NAMES['凶'])
        else:
            gua_name = random.choice(self.GUA_NAMES['吉'])
        
        return {
            'number': dige,
            'ji_xiong': ji_xiong,
            'description': description,
            'gua_name': gua_name,
            'meaning': ling_shu['meaning']
        }
    
    def generate_ju_ming_comment(self, bazi, name_info):
        """生成居明評語"""
        yong_shen = bazi.get('yong_shen', {})
        primary = yong_shen.get('primary', '木')
        secondary = yong_shen.get('secondary', '火')
        
        day_master = bazi.get('day_master', '丁')
        month_pillar = bazi.get('month_pillar', '庚辰')
        month_zhi = month_pillar[1] if len(month_pillar) > 1 else '辰'
        
        # 根据用神选择评语
        if primary in self.JU_MING_COMMENTS and secondary in self.JU_MING_COMMENTS[primary]:
            template = self.JU_MING_COMMENTS[primary][secondary]
        else:
            template = "『{day_gan}生{month_zhi}月，用神以{primary}{secondary}，五行配合，音佳且帶氣質之名。』"
        
        comment = template.format(
            day_gan=day_master,
            month_zhi=month_zhi,
            primary=primary,
            secondary=secondary
        )
        
        return {
            'comment': comment,
            'yong_shen': f"屬{primary}{secondary}",
            'note': f"(屬{primary}可生{secondary}，音健)"
        }
    
    def analyze(self, bazi, primary_names):
        """主分析函数"""
        results = []
        
        for name_info in primary_names:
            sancai = name_info.get('sancai', {})
            zongge = sancai.get('zongge', 24)
            renge = sancai.get('renge', 23)
            dige = sancai.get('dige', 16)
            
            # 分析各项运势
            zhu_yun = self.analyze_zhu_yun(zongge)
            qian_yun = self.analyze_qian_yun(renge)
            hou_yun = self.analyze_hou_yun(dige)
            
            # 生成居明評語
            ju_ming = self.generate_ju_ming_comment(bazi, name_info)
            
            result = {
                'name': name_info.get('name', ''),
                'zhu_yun': zhu_yun,
                'qian_yun': qian_yun,
                'hou_yun': hou_yun,
                'ju_ming_comment': ju_ming,
                'chars': name_info.get('chars', []),
                'strokes': name_info.get('strokes', []),
                'zongge': zongge,
                'renge': renge,
                'dige': dige
            }
            
            results.append(result)
        
        return {
            'primary_names_analysis': results,
            'summary': self._generate_summary(bazi)
        }
    
    def _generate_summary(self, bazi):
        """生成命理总结"""
        wuxing_analysis = bazi.get('wuxing_analysis', {})
        counts = wuxing_analysis.get('counts', {})
        day_master_wuxing = wuxing_analysis.get('day_master_wuxing', '火')
        
        # 分析五行强弱
        strong_wuxing = [wx for wx, count in counts.items() if count >= 2.5]
        weak_wuxing = [wx for wx, count in counts.items() if count <= 1]
        
        summary = f"日主{day_master_wuxing}"
        if day_master_wuxing in strong_wuxing:
            summary += "旺"
        elif day_master_wuxing in weak_wuxing:
            summary += "弱"
        else:
            summary += "平和"
        
        return {
            'day_master_analysis': summary,
            'strong_wuxing': strong_wuxing,
            'weak_wuxing': weak_wuxing,
            'wuxing_counts': counts
        }


# 测试代码
if __name__ == '__main__':
    analyzer = FortuneAnalyzer()
    
    # 模拟数据
    bazi = {
        'day_master': '丁',
        'month_pillar': '庚辰',
        'yong_shen': {
            'primary': '木',
            'secondary': '火'
        },
        'wuxing_analysis': {
            'counts': {'金': 1, '木': 3, '水': 1, '火': 2, '土': 1},
            'day_master_wuxing': '火'
        }
    }
    
    primary_names = [
        {
            'name': '黃智輝',
            'chars': ['智', '輝'],
            'strokes': [12, 15],
            'sancai': {'zongge': 37, 'renge': 25, 'dige': 27}
        }
    ]
    
    result = analyzer.analyze(bazi, primary_names)
    
    print("命理分析结果:")
    for analysis in result['primary_names_analysis']:
        print(f"\n姓名: {analysis['name']}")
        print(f"主運({analysis['zongge']}劃): {analysis['zhu_yun']['gua_name']}")
        print(f"  {analysis['zhu_yun']['description']}")
        print(f"前運({analysis['renge']}劃): {analysis['qian_yun']['gua_name']}")
        print(f"  {analysis['qian_yun']['description']}")
        print(f"後運({analysis['dige']}劃): {analysis['hou_yun']['gua_name']}")
        print(f"  {analysis['hou_yun']['description']}")
        print(f"居明評曰: {analysis['ju_ming_comment']['comment']}")
