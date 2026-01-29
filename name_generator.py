import random
import json

class NameGenerator:
    """姓名生成器 - 根据八字用神生成合适的姓名"""
    
    # 康熙字典笔画数（常用字）
    CHAR_STROKES = {
        # 水属性字
        '水': {'沛': 8, '汶': 8, '沃': 8, '沐': 8, '泽': 17, '洋': 10, '海': 11, '涛': 18, '清': 12, '涵': 12, 
               '淑': 12, '淳': 12, '淼': 12, '渊': 12, '润': 16, '涵': 12, '淳': 12, '淼': 12, '渊': 12, '润': 16,
               '浩': 11, '涵': 12, '淳': 12, '淼': 12, '渊': 12, '润': 16, '淇': 12, '淳': 12, '淼': 12, '渊': 12},
        # 木属性字
        '木': {'東': 8, '林': 8, '森': 12, '杰': 12, '楠': 13, '梓': 11, '榆': 13, '桐': 10, '桦': 16, '栋': 12,
               '梁': 11, '梅': 11, '松': 8, '柏': 9, '桂': 10, '荣': 14, '华': 14, '英': 11, '芳': 10, '萍': 14,
               '芝': 10, '芬': 10, '芹': 10, '芸': 10, '茜': 12, '莉': 13, '莎': 13, '菁': 14, '萌': 14, '萱': 15},
        # 火属性字
        '火': {'炎': 8, '煜': 13, '煊': 13, '炜': 13, '烨': 14, '烁': 19, '焕': 13, '炳': 9, '灿': 17, '灵': 24,
               '炎': 8, '煜': 13, '煊': 13, '炜': 13, '烨': 14, '烁': 19, '焕': 13, '炳': 9, '灿': 17, '灵': 24,
               '明': 8, '辉': 15, '耀': 20, '光': 6, '照': 13, '晴': 12, '晶': 12, '智': 12, '晖': 13, '曦': 20},
        # 土属性字
        '土': {'坤': 8, '城': 10, '培': 11, '基': 11, '堂': 11, '堃': 11, '均': 7, '圣': 13, '坚': 11, '坤': 8,
               '垚': 9, '培': 11, '基': 11, '堂': 11, '堃': 11, '均': 7, '圣': 13, '坚': 11, '坤': 8, '垚': 9,
               '山': 3, '岩': 8, '峰': 10, '岳': 8, '峻': 10, '崇': 11, '岭': 17, '岗': 11, '岚': 12, '岱': 8},
        # 金属性字
        '金': {'鋒': 15, '銘': 14, '銳': 15, '鈞': 12, '錦': 16, '鈺': 13, '銘': 14, '銳': 15, '鈞': 12, '錦': 16,
               '鑫': 24, '銘': 14, '銳': 15, '鈞': 12, '錦': 16, '鈺': 13, '銘': 14, '銳': 15, '鈞': 12, '錦': 16,
               '金': 8, '银': 14, '铜': 14, '铁': 21, '钢': 16, '铭': 14, '锐': 15, '钧': 12, '锦': 16, '钰': 13}
    }
    
    # 姓氏笔画数（常见姓氏）
    SURNAME_STROKES = {
        '王': 4, '李': 7, '张': 11, '刘': 15, '陈': 16, '杨': 13, '黄': 12, '赵': 14, '吴': 7, '周': 8,
        '徐': 10, '孙': 10, '马': 10, '朱': 6, '胡': 11, '郭': 15, '何': 7, '林': 8, '罗': 20, '高': 10,
        '郑': 19, '梁': 11, '谢': 17, '宋': 7, '唐': 10, '许': 11, '韩': 17, '冯': 12, '邓': 19, '曹': 11,
        '彭': 12, '曾': 12, '肖': 19, '田': 5, '董': 15, '袁': 10, '潘': 16, '于': 3, '蒋': 17, '蔡': 17,
        '余': 7, '杜': 7, '叶': 15, '程': 12, '苏': 22, '魏': 18, '吕': 7, '丁': 2, '任': 6, '沈': 8,
        '姚': 9, '卢': 16, '姜': 9, '崔': 11, '钟': 17, '谭': 19, '陆': 16, '汪': 8, '范': 11, '廖': 14,
        '石': 5, '金': 8, '韦': 9, '贾': 13, '夏': 10, '付': 5, '方': 4, '邹': 17, '熊': 14, '白': 5,
        '孟': 8, '秦': 10, '邱': 12, '侯': 9, '江': 7, '尹': 4, '薛': 19, '闫': 11, '段': 9, '雷': 13,
        '黎': 15, '史': 5, '龙': 16, '陶': 16, '贺': 12, '毛': 4, '郝': 14, '顾': 21, '龚': 22, '邵': 12,
        '万': 15, '覃': 12, '武': 8, '钱': 16, '戴': 18, '严': 20, '莫': 13, '孔': 4, '向': 6, '汤': 13
    }
    
    # 吉祥寓意字库
    AUSPICIOUS_CHARS = {
        '水': ['沛', '汶', '沃', '沐', '泽', '洋', '海', '涛', '清', '涵', '淑', '淳', '淼', '渊', '润', '浩', '淇', '淳'],
        '木': ['東', '林', '森', '杰', '楠', '梓', '榆', '桐', '桦', '栋', '梁', '梅', '松', '柏', '桂', '荣', '华', '英', '芳', '萍'],
        '火': ['炎', '煜', '煊', '炜', '烨', '烁', '焕', '炳', '灿', '灵', '明', '辉', '耀', '光', '照', '晴', '晶', '智', '晖', '曦'],
        '土': ['坤', '城', '培', '基', '堂', '堃', '均', '圣', '坚', '垚', '山', '岩', '峰', '岳', '峻', '崇', '岭', '岗', '岚', '岱'],
        '金': ['鋒', '銘', '銳', '鈞', '錦', '鈺', '鑫', '金', '银', '铜', '铁', '钢', '铭', '锐', '钧', '锦', '钰', '铮', '铠', '铄']
    }
    
    # 英文名库（按五行分类）
    ENGLISH_NAMES = {
        '水': ['Andrew', 'Alfred', 'Anson', 'Alan', 'Keith', 'Aiden', 'Kelvin', 'Kenny', 'Samuel', 'Ivan', 
               'Samson', 'Thomas', 'Stewart', 'Steve', 'Jason', 'Scott', 'Hayson', 'Raymond', 'Hugo', 'Herbert',
               'Stanly', 'Steve', 'Ringo', 'Roger', 'Harold', 'Hank', 'Randy'],
        '木': ['David', 'Archie', 'Andy', 'Alvin', 'Kerwin', 'Addie', 'Dalvin', 'Alex', 'Karson', 'Daniel',
               'Nelson', 'Nathan', 'Arthur', 'Albert', 'Antony', 'Damon', 'Denny', 'Adriel', 'Kenny'],
        '火': ['Alfred', 'David', 'Andrew', 'Arthur', 'Albert', 'Antony', 'Damon', 'Denny', 'Adriel', 'Kenny',
               'Nathan', 'Fibian', 'Felix', 'Martin', 'Marco', 'Marvel', 'Nelson', 'Patrick', 'William'],
        '土': ['Fibian', 'Felix', 'Martin', 'Marco', 'Marvel', 'Nelson', 'Patrick', 'William', 'Phoebe', 'Parry',
               'Wilson', 'Wayne', 'Damon', 'David', 'Mathew', 'Paul', 'Milton', 'Mark', 'Nathan', 'Nick'],
        '金': ['Hayson', 'Raymond', 'Hugo', 'Herbert', 'Stanly', 'Steve', 'Ringo', 'Roger', 'Harold', 'Hank',
               'Randy', 'Smith', 'Stewart', '鋒', '銘', '銳', '鈞', '錦', '鈺', '鑫']
    }
    
    def __init__(self):
        self.load_char_database()
    
    def load_char_database(self):
        """加载字库数据"""
        # 这里可以扩展为从数据库或文件加载
        pass
    
    def get_surname_strokes(self, surname):
        """获取姓氏笔画数"""
        return self.SURNAME_STROKES.get(surname, 8)  # 默认8画
    
    def get_char_strokes(self, char, wuxing):
        """获取字的笔画数"""
        if wuxing in self.CHAR_STROKES and char in self.CHAR_STROKES[wuxing]:
            return self.CHAR_STROKES[wuxing][char]
        return 8  # 默认8画
    
    def calculate_sancai(self, surname_strokes, name1_strokes, name2_strokes):
        """计算三才五格"""
        # 天格 = 姓氏笔画 + 1（单姓）
        tiange = surname_strokes + 1
        
        # 人格 = 姓氏笔画 + 名字第一字笔画
        renge = surname_strokes + name1_strokes
        
        # 地格 = 名字两字笔画之和（双名）
        dige = name1_strokes + name2_strokes
        
        # 总格 = 姓氏 + 名字总笔画
        zongge = surname_strokes + name1_strokes + name2_strokes
        
        # 外格 = 总格 - 人格 + 1
        waige = zongge - renge + 1
        
        return {
            'tiange': tiange,
            'renge': renge,
            'dige': dige,
            'zongge': zongge,
            'waige': waige
        }
    
    def get_wuxing_from_strokes(self, strokes):
        """根据笔画数判断五行"""
        # 1、2为木，3、4为火，5、6为土，7、8为金，9、10为水
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
        """分析三才五行配置"""
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
        """生成首选姓名"""
        yong_shen = bazi['yong_shen']['yong_shen']
        surname_strokes = self.get_surname_strokes(surname)
        
        names = []
        used_chars = set()
        
        for i in range(count):
            # 根据用神选择五行属性
            primary_wuxing = yong_shen[0] if yong_shen else '水'
            secondary_wuxing = yong_shen[1] if len(yong_shen) > 1 else primary_wuxing
            
            # 选择名字用字
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
            else:
                char1 = random.choice(self.AUSPICIOUS_CHARS[primary_wuxing])
                char2 = random.choice(self.AUSPICIOUS_CHARS[secondary_wuxing])
            
            # 计算笔画和三才五格
            char1_strokes = self.get_char_strokes(char1, primary_wuxing)
            char2_strokes = self.get_char_strokes(char2, secondary_wuxing)
            
            sancai = self.calculate_sancai(surname_strokes, char1_strokes, char2_strokes)
            sancai_wuxing = self.analyze_sancai_wuxing(sancai)
            
            # 计算总格数理吉凶
            zongge = sancai['zongge']
            
            name_info = {
                'name': f"{surname}{char1}{char2}",
                'chars': [char1, char2],
                'strokes': [char1_strokes, char2_strokes],
                'sancai': sancai,
                'sancai_wuxing': sancai_wuxing,
                'zongge': zongge,
                'wuxing': [primary_wuxing, secondary_wuxing]
            }
            
            names.append(name_info)
        
        return {
            'primary_names': names,
            'surname_strokes': surname_strokes
        }
    
    def generate_backup_chars(self, bazi, count=12):
        """生成备用字"""
        yong_shen = bazi['yong_shen']['yong_shen']
        primary_wuxing = yong_shen[0] if yong_shen else '水'
        secondary_wuxing = yong_shen[1] if len(yong_shen) > 1 else primary_wuxing
        
        backup_chars = []
        used_chars = set()
        
        # 从主要用神五行中取字
        chars1 = self.AUSPICIOUS_CHARS.get(primary_wuxing, self.AUSPICIOUS_CHARS['水'])
        for char in chars1:
            if len(backup_chars) >= count // 2:
                break
            if char not in used_chars:
                strokes = self.get_char_strokes(char, primary_wuxing)
                backup_chars.append({
                    'char': char,
                    'strokes': strokes,
                    'wuxing': primary_wuxing
                })
                used_chars.add(char)
        
        # 从次要用神五行中取字
        chars2 = self.AUSPICIOUS_CHARS.get(secondary_wuxing, self.AUSPICIOUS_CHARS['木'])
        for char in chars2:
            if len(backup_chars) >= count:
                break
            if char not in used_chars:
                strokes = self.get_char_strokes(char, secondary_wuxing)
                backup_chars.append({
                    'char': char,
                    'strokes': strokes,
                    'wuxing': secondary_wuxing
                })
                used_chars.add(char)
        
        return backup_chars[:count]
    
    def suggest_english_names(self, bazi):
        """根据用神推荐英文名"""
        yong_shen = bazi['yong_shen']['yong_shen']
        
        english_names = []
        for wx in yong_shen[:2]:  # 取前两个用神五行
            names = self.ENGLISH_NAMES.get(wx, self.ENGLISH_NAMES['水'])
            english_names.extend(names[:10])  # 每种五行取10个
        
        # 去重并随机选择
        english_names = list(set(english_names))
        random.shuffle(english_names)
        
        return english_names[:20]  # 返回20个英文名
    
    def get_name_meaning(self, char):
        """获取字的寓意"""
        meanings = {
            '沛': '充沛、盛大', '汶': '文雅、温和', '沃': '肥沃、丰富', '沐': '沐浴、恩泽',
            '東': '东方、朝气', '林': '森林、茂盛', '森': '森林、繁荣', '杰': '杰出、卓越',
            '炎': '光明、热情', '煜': '照耀、辉煌', '明': '明亮、智慧', '辉': '光辉、辉煌',
            '坤': '大地、厚德', '山': '高山、稳重', '峰': '山峰、卓越', '岳': '山岳、崇高',
            '鋒': '锋利、先锋', '銘': '铭记、铭刻', '銳': '锐利、敏锐', '錦': '锦绣、美好'
        }
        return meanings.get(char, '吉祥、美好')


# 测试代码
if __name__ == '__main__':
    gen = NameGenerator()
    
    # 模拟八字结果
    bazi = {
        'yong_shen': {
            'yong_shen': ['水', '木'],
            'primary': '水',
            'secondary': '木'
        }
    }
    
    # 生成姓名
    result = gen.generate_names('潘', '男', bazi, 2)
    print("生成的姓名:")
    for name_info in result['primary_names']:
        print(f"  {name_info['name']} - 总格{name_info['zongge']}画")
        print(f"    三才: {name_info['sancai_wuxing']['configuration']}")
    
    # 生成备用字
    backup = gen.generate_backup_chars(bazi, 12)
    print("\n备用字:")
    for char_info in backup:
        print(f"  {char_info['char']}({char_info['wuxing']}) - {char_info['strokes']}画")
    
    # 英文名建议
    english = gen.suggest_english_names(bazi)
    print("\n英文名建议:")
    print("  ", ", ".join(english[:10]))
