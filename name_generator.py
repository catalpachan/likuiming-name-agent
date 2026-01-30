import random
import json

class NameGenerator:
    """姓名生成器 - 根據八字用神生成合適的姓名（港澳台熱門用字，性別分類）"""
    
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
    
    MALE_AUSPICIOUS = {
        '水': ['瀚', '濤', '浩', '洋', '海', '澤', '沛', '涵', '潤', '滔', '潺', '瀾', '瀛', '漢', '江', '河', '泉', '溪', '津', '泓', '浚'],
        '木': ['棟', '樺', '榮', '華', '英', '楠', '梓', '柏', '松', '梅', '桂', '桐', '林', '森', '東', '榆', '槐', '橋', '棠', '欽', '欖'],
        '火': ['耀', '輝', '照', '旭', '晨', '曦', '彤', '烈', '炬', '炳', '燁', '爍', '煜', '熙', '亮', '光', '曙', '暉', '炯', '炬'],
        '土': ['峰', '嶽', '岩', '嵐', '岱', '巍', '崇', '峻', '崔', '嵩', '昆', '侖', '堅', '城', '壇', '壑', '壓', '墟', '墨', '壇'],
        '金': ['鋒', '銘', '鋭', '鈞', '錦', '鐘', '鐵', '銅', '銀', '鋼', '鏗', '鏡', '鎖', '鍵', '鍋', '鐺', '銓', '錚', '錠', '錢']
    }
    
    FEMALE_AUSPICIOUS = {
        '水': ['涵', '淑', '淳', '沛', '淇', '潔', '澄', '潤', '濤', '漾', '瀚', '瀅', '沁', '漪', '灝', '濰', '濱', '瀛', '汝'],
        '木': ['蘭', '蕾', '藍', '藝', '芬', '芳', '萍', '芝', '菁', '萌', '萱', '蕙', '芷', '蓉', '蕊', '蔓', '蘊', '蘭', '芬'],
        '火': ['晴', '晶', '智', '靈', '耀', '煜', '彤', '熙', '昕', '曉', '曦', '暉', '暖', '旭', '晨', '映', '麗', '燁', '晴', '晶'],
        '土': ['怡', '媛', '婭', '婉', '婷', '婥', '妍', '姍', '婕', '媚', '嫣', '嫩', '嬌', '嬋', '嬉', '嬿', '婀', '姿', '嫣'],
        '金': ['詩', '雅', '靜', '雯', '琳', '玉', '琪', '瓊', '瑤', '珍', '珠', '瓔', '瑜', '瑟', '璽', '璐', '璟', '瑩', '環', '琴']
    }
    
    def __init__(self):
        pass
    
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
        auspicious_chars = self.MALE_AUSPICIOUS if gender == '男' else self.FEMALE_AUSPICIOUS
        
        for i in range(count):
            if random.random() < 0.35:
                name = random.choice(hot_names)
                if len(name) == 2:
                    char1, char2 = name[0], name[1]
                elif len(name) == 1:
                    char1 = name
                    primary_wuxing = yong_shen[0] if yong_shen else '水'
                    available_chars = auspicious_chars.get(primary_wuxing, auspicious_chars['水'])
                    available_chars = [c for c in available_chars if c not in used_chars]
                    char2 = random.choice(available_chars) if available_chars else auspicious_chars['水'][0]
                char1_strokes = 8
                char2_strokes = 8
            else:
                primary_wuxing = yong_shen[0] if yong_shen else '水'
                secondary_wuxing = yong_shen[1] if len(yong_shen) > 1 else primary_wuxing
                available_chars = auspicious_chars.get(primary_wuxing, auspicious_chars['水'])
                available_chars = [c for c in available_chars if c not in used_chars]
                if len(available_chars) < 2:
                    available_chars = auspicious_chars.get(secondary_wuxing, auspicious_chars['水'])
                    available_chars = [c for c in available_chars if c not in used_chars]
                if len(available_chars) >= 2:
                    char1 = random.choice(available_chars)
                    used_chars.add(char1)
                    available_chars2 = [c for c in available_chars if c != char1]
                    char2 = random.choice(available_chars2)
                    used_chars.add(char2)
                else:
                    char1 = random.choice(auspicious_chars[primary_wuxing])
                    char2 = random.choice(auspicious_chars[secondary_wuxing])
                char1_strokes = 8
                char2_strokes = 8
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
        
        return []
    
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
            '鋒': '鋒利、先鋒', '銘': '銘記、銘刻', '鋭': '銳利、敏銳', '錦': '錦繡、美好'
        }
        return meanings.get(char, '吉祥、美好')
