import random
import json

class NameGenerator:
    """姓名生成器 - 根據八字用神生成合適的姓名（港澳台熱門用字）"""
    
    # 港澳台熱門姓名庫（按性別分類，已去重）
    HOT_MALE_NAMES = [
        '梓軒', '宇軒', '子謙', '樂軒', '子朗', '家樂', '俊傑', '卓霖', '俊熙',
        '浩賢', '逸朗', '梓朗', '俊軒', '浩軒', '柏熹', '樂謙', '卓軒', '柏熙', '俊熹',
        '卓謙', '思齊', '嘉俊', '俊彥', '思澄', '家熙', '天樂', '家俊', '卓希', '嘉豪',
        '天朗', '梓樂', '樂然', '嘉熙', '智謙', '諾軒', '柏賢', '俊霖', '文希', '俊樂',
        '智朗', '博謙', '梓謙', '浚軒', '柏軒', '立言', '君豪', '梓熙', '諾言', '俊銘', '皓天', '英傑', '俊輝'
    ]
    
    HOT_FEMALE_NAMES = [
        '凱晴', '芷晴', '曉晴', '子晴', '凱琳', '曉彤', '紫晴', '嘉怡', '梓晴', '樂瑤',
        '芷欣', '心怡', '詩雅', '樂晴', '穎彤', '樂怡', '曉嵐', '曉琳', '嘉欣', '穎欣',
        '嘉慧', '心悅', '芷瑩', '嘉琪', '穎怡', '嘉敏', '凱婷', '天恩', '樂兒', '詠欣',
        '凱盈', '卓盈', '穎琳', '曉瑩', '嘉儀', '雅雯', '詠琳', '樂恩', '心柔', '曉澄',
        '思穎', '雅晴', '芷悠', '靜雯', '雅婷', '晞彤', '海晴', '芷琪', '凱欣', '嘉雯',
        '恩彤', '靜怡', '嘉晞', '凱喬', '可兒', '嘉琳', '曉楠', '可欣', '芷盈', '明慧', '凱淇'
    ]
    
    # 備用繁體字庫（按五行分類）
    CHAR_STROKES = {
        '水': ['沛', '汶', '沃', '沐', '澤', '洋', '海', '濤', '清', '涵', '淑', '淳', '渺', '淵', '潤', '浩', '淇', '瀚', '瀅', '瀛', '瀚', '濰'],
        '木': ['東', '林', '森', '傑', '楠', '梓', '榆', '桐', '樺', '棟', '梁', '梅', '松', '柏', '桂', '榮', '華', '英', '芳', '萍', '芝', '芬', '芸', '菁', '萌', '萱', '蘭', '芬', '儀', '蓓', '藍', '蕾', '蔓', '藝', '藍'],
        '火': ['炎', '煜', '暄', '煒', '爍', '煥', '炳', '燦', '靈', '明', '輝', '耀', '光', '照', '晴', '晶', '智', '暉', '曦', '倫', '燊', '爍', '炯', '烈', '煜', '耀', '燊'],
        '土': ['坤', '城', '培', '基', '堂', '堃', '均', '聖', '堅', '垚', '山', '岩', '峰', '岳', '峻', '崇', '嶺', '嵐', '岱', '巍', '嵐', '奎', '垣', '埕', '堯', '壇', '墨', '墻', '壁', '壇', '壑', '壓'],
        '金': ['鋒', '銘', '銳', '鈞', '錦', '鈺', '鑫', '鐵', '銅', '銀', '銘', '銳', '鈞', '錦', '鈺', '鐺', '銓', '錚', '錠', '錢', '鍋', '鍵', '鋒', '鏗', '鏡', '鐘', '銳', '鋒', '鐘', '銓', '錠']
    }
    
    AUSPICIOUS_CHARS = {
        '水': ['沛', '汶', '沃', '沐', '澤', '洋', '海', '濤', '清', '涵', '淑', '淳', '浩', '淇', '瀚', '濤', '潤', '滔', '潺', '瀚', '瀾', '瀛'],
        '木': ['東', '林', '森', '傑', '楠', '梓', '榆', '桐', '樺', '棟', '梁', '梅', '松', '柏', '桂', '榮', '華', '英', '芳', '萍', '芝', '芬', '芸', '藍', '蘭', '蕾', '蔓', '藝', '芬', '藍', '儀', '蕾', '藍'],
        '火': ['炎', '煜', '爍', '煥', '炳', '燦', '靈', '明', '輝', '耀', '光', '照', '晴', '晶', '智', '暉', '曦', '倫', '烈', '炬', '煜', '燁', '爍', '炯', '烈', '耀', '曦', '炬'],
        '土': ['坤', '城', '培', '基', '堂', '堃', '均', '聖', '堅', '山', '岩', '峰', '岳', '峻', '崇', '嶺', '嵐', '岱', '巍', '壇', '壑', '壓', '墟', '壕', '壇', '壑', '壓'],
        '金': ['鋒', '銘', '銳', '鈞', '錦', '鈺', '鑫', '銀', '銅', '鐵', '鋼', '鎖', '鍵', '錢', '鍋', '鏡', '鐘', '鐵', '銳', '鋒', '銘', '銳', '鈞', '錦', '鐘', '銳']
    }
    
    def __init__(self):
        pass
    
    def simplify_to_traditional(self, text):
        """簡體轉繁體"""
        mapping = {
            '东': '東', '广': '廣', '为': '為', '业': '業', '丝': '絲',
            '两': '兩', '严': '嚴', '个': '個', '丰': '豐', '临': '臨',
            '丽': '麗', '举': '舉', '义': '義', '乌': '烏', '乐': '樂',
            '乔': '喬', '书': '書', '买': '買', '乱': '亂', '了': '了',
            '争': '爭', '事': '事', '于': '於', '云': '雲', '五': '五',
            '亚': '亞', '产': '產', '京': '京', '亲': '親', '人': '人',
            '亿': '億', '什': '什', '仁': '仁', '仆': '僕', '仇': '仇',
            '今': '今', '介': '介', '仍': '仍', '从': '從', '仑': '侖',
            '仓': '倉', '仔': '仔', '仕': '仕', '他': '他', '仗': '仗',
            '付': '付', '仙': '仙', '代': '代', '令': '令', '以': '以',
            '仪': '儀', '们': '們', '仰': '仰', '仲': '仲', '件': '件',
            '价': '價', '任': '任', '仿': '仿', '企': '企', '伊': '伊',
            '伍': '伍', '伎': '伎', '伏': '伏', '伐': '伐', '休': '休',
            '众': '眾', '优': '優', '伙': '伙', '会': '會', '伞': '傘',
            '伟': '偉', '传': '傳', '伤': '傷', '伦': '倫', '伪': '偽',
            '伫': '佇', '伴': '伴', '伶': '伶', '伸': '伸', '伺': '伺',
            '似': '似', '伽': '伽', '伯': '伯', '估': '估', '体': '體',
            '何': '何', '余': '餘', '作': '作', '你': '你', '佣': '傭',
            '佩': '佩', '佳': '佳', '侍': '侍', '依': '依', '侠': '俠',
            '侦': '偵', '侧': '側', '侨': '僑', '俊': '俊', '保': '保',
            '俞': '俞', '信': '信', '修': '修', '俯': '俯', '俱': '俱',
            '倍': '倍', '倒': '倒', '倔': '倔', '候': '候', '倚': '倚',
            '借': '借', '倦': '倦', '倩': '倩', '倪': '倪', '倫': '倫',
            '偏': '偏', '偕': '偕', '做': '做', '停': '停', '健': '健',
            '偶': '偶', '偷': '偷', '偻': '僂', '偽': '偽', '偿': '償',
            '傅': '傅', '傍': '傍', '傑': '傑', '傲': '傲', '債': '債',
            '傷': '傷', '像': '像', '僕': '僕', '僧': '僧', '僵': '僵',
            '僻': '僻', '儀': '儀', '億': '億', '儆': '儆', '儉': '儉',
            '儒': '儒', '償': '償', '優': '優', '儲': '儲', '儿': '兒',
            '先': '先', '光': '光', '克': '克', '免': '免', '兔': '兔',
            '党': '黨', '兜': '兜', '兢': '兢', '入': '入', '內': '內',
            '全': '全', '八': '八', '公': '公', '六': '六', '共': '共',
            '关': '關', '兴': '興', '兵': '兵', '其': '其', '具': '具',
            '典': '典', '养': '養', '兼': '兼', '兽': '獸', '内': '內',
            '击': '擊', '刀': '刀', '刃': '刃', '分': '分', '切': '切',
            '刊': '刊', '刑': '刑', '划': '劃', '列': '列', '刘': '劉',
            '则': '則', '刚': '剛', '创': '創', '初': '初', '删': '刪',
            '利': '利', '别': '別', '剩': '剩', '劈': '劈', '勤': '勤',
            '勇': '勇', '勉': '勉', '勸': '勸', '匀': '勻', '匕': '匕',
            '化': '化', '北': '北', '匝': '匝', '匠': '匠', '匪': '匪',
            '匮': '匱', '区': '區', '占': '占', '卡': '卡', '卜': '卜',
            '卯': '卯', '印': '印', '危': '危', '即': '即', '卵': '卵',
            '卷': '卷', '卸': '卸', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠', '厂': '廠',
            '厂': '廠', '厂': '廠', '厂': '港', '厂': '澳', '厂': '台',
            '厂': '熱', '厂': '門', '厂': '姓', '厂': '名', '厂': '字',
            '库': '庫', '权': '權', '重': '重', '概': '概', '率': '率',
            '大': '大', '于': '於', '三': '三', '成': '成', '成': '成',
            '出': '出', '现': '現', '现': '現'
        }
        result = ''
        for char in text:
            result += mapping.get(char, char)
        return result
    
    def get_surname_strokes(self, surname):
        """獲取姓氏筆畫數"""
        SURNAME_STROKES = {
            '王': 4, '李': 7, '張': 11, '劉': 15, '陳': 16, '楊': 13, '黃': 12, '趙': 14, '吳': 7, '周': 8,
            '徐': 10, '孫': 10, '馬': 10, '朱': 6, '胡': 11, '郭': 15, '何': 7, '林': 8, '羅': 20, '高': 10,
            '鄭': 19, '梁': 11, '謝': 17, '宋': 7, '唐': 10, '許': 11, '韓': 17, '馮': 12, '鄧': 19, '曹': 11,
            '彭': 12, '曾': 12, '肖': 19, '田': 5, '董': 15, '袁': 10, '潘': 16, '於': 3, '蔣': 17, '蔡': 17,
            '余': 7, '杜': 7, '葉': 15, '程': 12, '蘇': 22, '魏': 18, '呂': 7, '丁': 2, '任': 6, '沈': 8,
            '姚': 9, '盧': 16, '姜': 9, '崔': 11, '鐘': 17, '譚': 19, '陸': 16, '汪': 8, '范': 11, '廖': 14,
            '石': 5, '金': 8, '韋': 9, '賈': 13, '夏': 10, '付': 5, '方': 4, '鄒': 17, '熊': 14, '白': 5,
            '孟': 8, '秦': 10, '邱': 12, '侯': 9, '江': 7, '尹': 4, '薛': 19, '間': 11, '段': 9, '雷': 13,
            '黎': 15, '史': 5, '龍': 16, '陶': 16, '賀': 12, '毛': 4, '郝': 14, '顧': 21, '龔': 22, '邵': 12,
            '萬': 15, '覃': 12, '武': 8, '錢': 16, '戴': 18, '嚴': 20, '莫': 13, '孔': 4, '向': 6, '湯': 13
        }
        return SURNAME_STROKES.get(surname, 8)
    
    def calculate_sancai(self, surname_strokes, name1_strokes, name2_strokes):
        """計算三才五格"""
        tiange = surname_strokes + 1
        renge = surname_strokes + name1_strokes
        dige = name1_strokes + name2_strokes
        zongge = surname_strokes + name1_strokes + name2_strokes
        waige = zongge - renge + 1
        return {
            'tiange': tiange,
            'renge': renge,
            'dige': dige,
            'zongge': zongge,
            'waige': waige
        }
    
    def get_wuxing_from_strokes(self, strokes):
        remainder = strokes % 10
        if remainder in [1, 2]:
            return '木'
        elif remainder in [3, 4]:
            return '火'
        elif remainder in [5, 6]:
            return '土'
        elif remainder in [7, 8]:
            return '金'
        else:
            return '水'
    
    def analyze_sancai_wuxing(self, sancai):
        tiange_wx = self.get_wuxing_from_strokes(sancai['tiange'])
        renge_wx = self.get_wuxing_from_strokes(sancai['renge'])
        dige_wx = self.get_wuxing_from_strokes(sancai['dige'])
        return {
            'tiange': tiange_wx,
            'renge': renge_wx,
            'dige': dige_wx,
            'configuration': f"{tiange_wx}-{renge_wx}-{dige_wx}"
        }
    
    def generate_names(self, surname, gender, bazi, count=2):
        """生成首選姓名"""
        yong_shen = bazi['yong_shen']['yong_shen']
        surname_strokes = self.get_surname_strokes(surname)
        
        names = []
        used_chars = set()
        hot_names = self.HOT_MALE_NAMES if gender == '男' else self.HOT_FEMALE_NAMES
        
        for i in range(count):
            if random.random() < 0.35:
                name = random.choice(hot_names)
                if len(name) == 2:
                    char1, char2 = name[0], name[1]
                elif len(name) == 1:
                    char1 = name
                    primary_wuxing = yong_shen[0] if yong_shen else '水'
                    available_chars = self.AUSPICIOUS_CHARS.get(primary_wuxing, self.AUSPICIOUS_CHARS['水'])
                    char2 = random.choice([c for c in available_chars if c not in used_chars])
                char1_strokes = self.get_char_strokes(char1, yong_shen[0] if yong_shen else '水')
                char2_strokes = self.get_char_strokes(char2, yong_shen[1] if len(yong_shen) > 1 else yong_shen[0] if yong_shen else '水')
            else:
                primary_wuxing = yong_shen[0] if yong_shen else '水'
                secondary_wuxing = yong_shen[1] if len(yong_shen) > 1 else primary_wuxing
                available_chars = self.AUSPICIOUS_CHARS.get(primary_wuxing, self.AUSPICIOUS_CHARS['水'])
                available_chars = [c for c in available_chars if c not in used_chars]
                if len(available_chars) < 2:
                    available_chars = self.AUSPICIOUS_CHARS.get(secondary_wuxing, self.AUSPICIOUS_CHARS['水'])
                    available_chars = [c for c in available_chars if c not in used_chars]
                if len(available_chars) >= 2:
                    char1 = random.choice(available_chars)
                    used_chars.add(char1)
                    available_chars2 = [c for c in available_chars if c != char1]
                    char2 = random.choice(available_chars2)
                    used_chars.add(char2)
                    char1_strokes = self.get_char_strokes(char1, primary_wuxing)
                    char2_strokes = self.get_char_strokes(char2, secondary_wuxing)
                else:
                    char1 = random.choice(self.AUSPICIOUS_CHARS[primary_wuxing])
                    char2 = random.choice(self.AUSPICIOUS_CHARS[secondary_wuxing])
                    char1_strokes = self.get_char_strokes(char1, primary_wuxing)
                    char2_strokes = self.get_char_strokes(char2, secondary_wuxing)
            sancai = self.calculate_sancai(surname_strokes, char1_strokes, char2_strokes)
            sancai_wuxing = self.analyze_sancai_wuxing(sancai)
            zongge = sancai['zongge']
            if 'secondary_wuxing' in dir():
                wuxing_list = [primary_wuxing, secondary_wuxing]
            else:
                wuxing_list = [yong_shen[0], yong_shen[1] if len(yong_shen) > 1 else yong_shen[0]]
            name_info = {
                'name': f"{surname}{char1}{char2}",
                'chars': [char1, char2],
                'strokes': [char1_strokes, char2_strokes],
                'sancai': sancai,
                'sancai_wuxing': sancai_wuxing,
                'zongge': zongge,
                'wuxing': wuxing_list
            }
            names.append(name_info)
        
        return {
            'primary_names': names,
            'surname_strokes': surname_strokes
        }
    
    def generate_backup_chars(self, bazi, count=12):
        """生成備用字"""
        yong_shen = bazi['yong_shen']['yong_shen']
        primary_wuxing = yong_shen[0] if yong_shen else '水'
        secondary_wuxing = yong_shen[1] if len(yong_shen) > 1 else primary_wuxing
        
        backup_chars = []
        used_chars = set()
        hot_chars = []
        hot_chars_extended = []
        for name in self.HOT_MALE_NAMES + self.HOT_FEMALE_NAMES:
            for char in name:
                if char not in hot_chars_extended:
                    hot_chars_extended.append(char)
        
        for char in hot_chars_extended:
            if len(backup_chars) < count // 2:
                backup_chars.append({'char': char, 'strokes': 8, 'wuxing': primary_wuxing})
        
        chars1 = self.AUSPICIOUS_CHARS.get(primary_wuxing, self.AUSPICIOUS_CHARS['水'])
        for char in chars1:
            if len(backup_chars) >= count:
                break
            if char not in [c['char'] for c in backup_chars]:
                strokes = self.get_char_strokes(char, primary_wuxing)
                backup_chars.append({'char': char, 'strokes': strokes, 'wuxing': primary_wuxing})
        
        chars2 = self.AUSPICIOUS_CHARS.get(secondary_wuxing, self.AUSPICIOUS_CHARS['木'])
        for char in chars2:
            if len(backup_chars) >= count:
                break
            if char not in [c['char'] for c in backup_chars]:
                strokes = self.get_char_strokes(char, secondary_wuxing)
                backup_chars.append({'char': char, 'strokes': strokes, 'wuxing': secondary_wuxing})
        
        return backup_chars[:count]
    
    def suggest_english_names(self, bazi):
        """根據用神推薦英文名"""
        yong_shen = bazi['yong_shen']['yong_shen']
        english_names = []
        for wx in yong_shen[:2]:
            names = self.ENGLISH_NAMES.get(wx, self.ENGLISH_NAMES['水'])
            english_names.extend(names[:10])
        english_names = list(set(english_names))
        random.shuffle(english_names)
        return english_names[:20]
    
    ENGLISH_NAMES = {
        '水': ['Andrew', 'Alfred', 'Anson', 'Alan', 'Keith', 'Aiden', 'Kelvin', 'Kenny', 'Samuel', 'Ivan', 'Samson', 'Thomas', 'Stewart', 'Steve', 'Jason', 'Scott', 'Raymond', 'Hugo', 'Herbert', 'Stanly', 'Ringo', 'Roger', 'Harold', 'Hank', 'Randy'],
        '木': ['David', 'Archie', 'Andy', 'Alvin', 'Kerwin', 'Addie', 'Dalvin', 'Alex', 'Karson', 'Daniel', 'Nelson', 'Nathan', 'Arthur', 'Albert', 'Antony', 'Damon', 'Denny', 'Adriel', 'Kenny', 'Edward', 'Eric', 'Ethan', 'Evan', 'Ben', 'Benji'],
        '火': ['Alfred', 'David', 'Andrew', 'Arthur', 'Albert', 'Antony', 'Damon', 'Denny', 'Adriel', 'Kenny', 'Nathan', 'Fibian', 'Felix', 'Martin', 'Marco', 'Marvel', 'Nelson', 'Patrick', 'William', 'Philip', 'Phoebe', 'Parry', 'Sunny', 'Vincent', 'Victor', 'Victor', 'Raymond'],
        '土': ['Fibian', 'Felix', 'Martin', 'Marco', 'Marvel', 'Nelson', 'Patrick', 'William', 'Phoebe', 'Parry', 'Wilson', 'Wayne', 'Damon', 'David', 'Mathew', 'Paul', 'Milton', 'Mark', 'Nathan', 'Nick', 'Nolan', 'Oscar', 'Owen', 'Olivia', 'Oliver'],
        '金': ['Hayson', 'Raymond', 'Hugo', 'Herbert', 'Stanly', 'Steve', 'Ringo', 'Roger', 'Harold', 'Hank', 'Randy', 'Smith', 'Stewart', 'Howard', 'Henry', 'Harry', 'Brian', 'Bruce', 'Barry', 'Bobby', 'Billy', 'Benson', 'Ben', 'Benjamin', 'Benji']
    }
    
    def get_char_strokes(self, char, wuxing):
        """獲取字的筆畫數"""
        return 8
    
    def get_name_meaning(self, char):
        """獲取字的寓意"""
        meanings = {
            '沛': '充沛、盛大', '汶': '文雅、溫和', '沃': '肥沃、豐富', '沐': '沐浴、恩澤',
            '東': '東方、朝氣', '林': '森林、茂盛', '森': '森林、繁榮', '傑': '傑出、卓越',
            '炎': '光明、熱情', '煜': '照耀、輝煌', '明': '明亮、智慧', '輝': '光輝、輝煌',
            '坤': '大地、厚德', '山': '高山、穩重', '峰': '山峰、卓越', '岳': '山岳、崇高',
            '鋒': '鋒利、先鋒', '銘': '銘記、銘刻', '銳': '銳利、敏銳', '錦': '錦繡、美好'
        }
        return meanings.get(char, '吉祥、美好')
