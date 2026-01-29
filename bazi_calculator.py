from datetime import datetime, timedelta
import math

class BaziCalculator:
    """八字计算器 - 包含农历转换、干支计算、五行分析"""
    
    # 天干
    TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    # 地支
    DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    # 五行
    WUXING = {
        '甲': '木', '乙': '木',
        '丙': '火', '丁': '火',
        '戊': '土', '己': '土',
        '庚': '金', '辛': '金',
        '壬': '水', '癸': '水',
        '子': '水', '丑': '土', '寅': '木', '卯': '木',
        '辰': '土', '巳': '火', '午': '火', '未': '土',
        '申': '金', '酉': '金', '戌': '土', '亥': '水'
    }
    # 地支藏干
    DI_ZHI_CANG_GAN = {
        '子': ['癸'],
        '丑': ['己', '癸', '辛'],
        '寅': ['甲', '丙', '戊'],
        '卯': ['乙'],
        '辰': ['戊', '乙', '癸'],
        '巳': ['丙', '庚', '戊'],
        '午': ['丁', '己'],
        '未': ['己', '丁', '乙'],
        '申': ['庚', '壬', '戊'],
        '酉': ['辛'],
        '戌': ['戊', '辛', '丁'],
        '亥': ['壬', '甲']
    }
    # 时辰对应表
    SHI_CHEN = [
        ('子', '23:00-01:00'), ('丑', '01:00-03:00'), ('寅', '03:00-05:00'),
        ('卯', '05:00-07:00'), ('辰', '07:00-09:00'), ('巳', '09:00-11:00'),
        ('午', '11:00-13:00'), ('未', '13:00-15:00'), ('申', '15:00-17:00'),
        ('酉', '17:00-19:00'), ('戌', '19:00-21:00'), ('亥', '21:00-23:00')
    ]
    # 农历月份名称
    LUNAR_MONTHS = ['正', '二', '三', '四', '五', '六', '七', '八', '九', '十', '冬', '腊']
    # 农历日期名称
    LUNAR_DAYS = [
        '初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十',
        '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
        '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十'
    ]
    
    def __init__(self):
        # 1900年农历正月初一的公历日期为1900年1月31日
        self.base_date = datetime(1900, 1, 31)
        # 农历1900年1月1日为甲子年
        self.base_gan_zhi_year = 36  # 1900年为庚子年，需要调整
        
    def solar_to_lunar(self, year, month, day):
        """公历转农历"""
        try:
            from lunardate import LunarDate
            lunar = LunarDate.fromSolarDate(year, month, day)
            return {
                'year': lunar.year,
                'month': lunar.month,
                'day': lunar.day,
                'is_leap': lunar.isLeapMonth
            }
        except:
            # 备用计算方法
            return self._solar_to_lunar_manual(year, month, day)
    
    def _solar_to_lunar_manual(self, year, month, day):
        """手动计算公历转农历"""
        # 简化的农历数据（1900-2100）
        lunar_info = [
            0x04bd8, 0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950, 0x16554, 0x056a0, 0x09ad0, 0x055d2,
            0x04ae0, 0x0a5b6, 0x0a4d0, 0x0d250, 0x1d255, 0x0b540, 0x0d6a0, 0x0ada2, 0x095b0, 0x14977,
            0x04970, 0x0a4b0, 0x0b4b5, 0x06a50, 0x06d40, 0x1ab54, 0x02b60, 0x09570, 0x052f2, 0x04970,
            0x06566, 0x0d4a0, 0x0ea50, 0x06e95, 0x05ad0, 0x02b60, 0x186e3, 0x092e0, 0x1c8d7, 0x0c950,
        ]
        
        # 计算从1900年1月1日到目标日期的天数
        target_date = datetime(year, month, day)
        base_date = datetime(1900, 1, 1)
        offset = (target_date - base_date).days
        
        # 查找对应的农历年份
        lunar_year = 1900
        days_in_year = 0
        for i in range(200):
            year_days = self._lunar_year_days(lunar_info[i] if i < len(lunar_info) else 0x04bd8)
            if offset < days_in_year + year_days:
                break
            days_in_year += year_days
            lunar_year += 1
        
        offset -= days_in_year
        
        # 查找对应的农历月份
        leap_month = self._leap_month(lunar_info[lunar_year - 1900] if lunar_year - 1900 < len(lunar_info) else 0)
        lunar_month = 1
        days_in_month = 0
        
        for i in range(1, 13):
            if leap_month > 0 and i == leap_month + 1:
                leap_days = self._leap_days(lunar_info[lunar_year - 1900] if lunar_year - 1900 < len(lunar_info) else 0)
                if offset < days_in_month + leap_days:
                    lunar_month = i - 1
                    is_leap = True
                    break
                days_in_month += leap_days
            
            month_days = self._month_days(lunar_year, i)
            if offset < days_in_month + month_days:
                lunar_month = i
                is_leap = False
                break
            days_in_month += month_days
        
        offset -= days_in_month
        lunar_day = offset + 1
        
        return {
            'year': lunar_year,
            'month': lunar_month,
            'day': lunar_day,
            'is_leap': is_leap if 'is_leap' in locals() else False
        }
    
    def _lunar_year_days(self, lunar_info):
        """计算农历年的天数"""
        days = 0
        for i in range(1, 13):
            days += self._month_days_from_info(lunar_info, i)
        if self._leap_month(lunar_info) > 0:
            days += self._leap_days(lunar_info)
        return days
    
    def _month_days_from_info(self, lunar_info, month):
        """从农历信息中获取某月天数"""
        return 29 + ((lunar_info >> (16 - month)) & 1)
    
    def _leap_month(self, lunar_info):
        """获取闰月"""
        return lunar_info & 0xf
    
    def _leap_days(self, lunar_info):
        """获取闰月天数"""
        if self._leap_month(lunar_info) == 0:
            return 0
        return 29 + ((lunar_info >> 16) & 1)
    
    def _month_days(self, year, month):
        """获取某年某月的天数"""
        lunar_info = [
            0x04bd8, 0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950, 0x16554, 0x056a0, 0x09ad0, 0x055d2,
        ]
        idx = year - 1900
        if idx < len(lunar_info):
            return self._month_days_from_info(lunar_info[idx], month)
        return 30
    
    def get_year_gan_zhi(self, year):
        """获取年柱干支"""
        # 以1984年（甲子年）为基准
        offset = (year - 1984) % 60
        gan_idx = offset % 10
        zhi_idx = offset % 12
        return self.TIAN_GAN[gan_idx] + self.DI_ZHI[zhi_idx]
    
    def get_month_gan_zhi(self, year, month, day, hour=12):
        """获取月柱干支"""
        # 年干决定月干起始
        year_gan_idx = self.TIAN_GAN.index(self.get_year_gan_zhi(year)[0])
        
        # 月干起始索引
        if year_gan_idx in [0, 5]:  # 甲己年
            month_gan_start = 2  # 丙
        elif year_gan_idx in [1, 6]:  # 乙庚年
            month_gan_start = 4  # 戊
        elif year_gan_idx in [2, 7]:  # 丙辛年
            month_gan_start = 6  # 庚
        elif year_gan_idx in [3, 8]:  # 丁壬年
            month_gan_start = 8  # 壬
        else:  # 戊癸年
            month_gan_start = 0  # 甲
        
        # 计算节气，确定月份
        # 简化处理：以农历月份为准
        lunar = self.solar_to_lunar(year, month, day)
        lunar_month = lunar['month']
        
        # 月干索引
        gan_idx = (month_gan_start + lunar_month - 1) % 10
        # 月支索引（正月建寅）
        zhi_idx = (lunar_month + 1) % 12
        
        return self.TIAN_GAN[gan_idx] + self.DI_ZHI[zhi_idx]
    
    def get_day_gan_zhi(self, year, month, day):
        """获取日柱干支"""
        # 以1900年1月31日为基准（甲子日）
        base_date = datetime(1900, 1, 31)
        target_date = datetime(year, month, day)
        offset = (target_date - base_date).days
        
        gan_idx = offset % 10
        zhi_idx = offset % 12
        
        return self.TIAN_GAN[gan_idx] + self.DI_ZHI[zhi_idx]
    
    def get_hour_gan_zhi(self, day_gan, hour):
        """获取时柱干支"""
        # 日干决定时干起始
        day_gan_idx = self.TIAN_GAN.index(day_gan[0])
        
        # 时干起始索引
        if day_gan_idx in [0, 5]:  # 甲己日
            hour_gan_start = 0  # 甲
        elif day_gan_idx in [1, 6]:  # 乙庚日
            hour_gan_start = 2  # 丙
        elif day_gan_idx in [2, 7]:  # 丙辛日
            hour_gan_start = 4  # 戊
        elif day_gan_idx in [3, 8]:  # 丁壬日
            hour_gan_start = 6  # 庚
        else:  # 戊癸日
            hour_gan_start = 8  # 壬
        
        # 计算时辰
        zhi_idx = (hour + 1) // 2 % 12
        gan_idx = (hour_gan_start + zhi_idx) % 10
        
        return self.TIAN_GAN[gan_idx] + self.DI_ZHI[zhi_idx]
    
    def get_shichen(self, hour, minute):
        """获取时辰名称"""
        total_minutes = hour * 60 + minute
        for i, (zhi, time_range) in enumerate(self.SHI_CHEN):
            start_hour = int(time_range.split('-')[0].split(':')[0])
            start_minute = int(time_range.split('-')[0].split(':')[1])
            end_hour = int(time_range.split('-')[1].split(':')[0])
            end_minute = int(time_range.split('-')[1].split(':')[1])
            
            start_total = start_hour * 60 + start_minute
            end_total = end_hour * 60 + end_minute
            
            if end_total < start_total:  # 跨天的情况（子时）
                if total_minutes >= start_total or total_minutes < end_total:
                    return zhi, time_range
            else:
                if start_total <= total_minutes < end_total:
                    return zhi, time_range
        return '子', '23:00-01:00'
    
    def analyze_wuxing(self, bazi):
        """分析五行"""
        wuxing_count = {'金': 0, '木': 0, '水': 0, '火': 0, '土': 0}
        
        # 统计四柱天干地支的五行
        for pillar in [bazi['year'], bazi['month'], bazi['day'], bazi['hour']]:
            gan = pillar[0]
            zhi = pillar[1]
            wuxing_count[self.WUXING[gan]] += 1
            wuxing_count[self.WUXING[zhi]] += 1
            
            # 地支藏干
            for cang_gan in self.DI_ZHI_CANG_GAN[zhi]:
                wuxing_count[self.WUXING[cang_gan]] += 0.5
        
        # 确定日主
        day_master = bazi['day'][0]
        day_master_wuxing = self.WUXING[day_master]
        
        # 分析五行强弱
        wuxing_strength = {}
        for wx in ['金', '木', '水', '火', '土']:
            if wx == day_master_wuxing:
                wuxing_strength[wx] = '日主'
            elif wuxing_count[wx] >= 3:
                wuxing_strength[wx] = '旺'
            elif wuxing_count[wx] >= 2:
                wuxing_strength[wx] = '平'
            else:
                wuxing_strength[wx] = '弱'
        
        # 分析相生相克关系
        sheng_relations = []
        ke_relations = []
        
        sheng_cycle = {'金': '水', '水': '木', '木': '火', '火': '土', '土': '金'}
        ke_cycle = {'金': '木', '木': '土', '土': '水', '水': '火', '火': '金'}
        
        for wx in ['金', '木', '水', '火', '土']:
            if wuxing_count[wx] > 0:
                sheng_to = sheng_cycle[wx]
                ke_to = ke_cycle[wx]
                if wuxing_count[sheng_to] > 0:
                    sheng_relations.append(f"{wx}生{sheng_to}")
                if wuxing_count[ke_to] > 0:
                    ke_relations.append(f"{wx}克{ke_to}")
        
        return {
            'counts': wuxing_count,
            'strength': wuxing_strength,
            'day_master': day_master,
            'day_master_wuxing': day_master_wuxing,
            'sheng_relations': sheng_relations,
            'ke_relations': ke_relations
        }
    
    def calculate_yong_shen(self, wuxing_analysis, bazi):
        """计算用神"""
        day_master_wuxing = wuxing_analysis['day_master_wuxing']
        wuxing_count = wuxing_analysis['counts']
        
        # 简单的用神判断逻辑
        # 根据日主五行强弱判断用神
        day_master_count = wuxing_count[day_master_wuxing]
        
        # 生克关系
        sheng_wo = {'金': '土', '木': '水', '水': '金', '火': '木', '土': '火'}[day_master_wuxing]
        wo_sheng = {'金': '水', '木': '火', '水': '木', '火': '土', '土': '金'}[day_master_wuxing]
        ke_wo = {'金': '火', '木': '金', '水': '土', '火': '水', '土': '木'}[day_master_wuxing]
        wo_ke = {'金': '木', '木': '土', '水': '火', '火': '金', '土': '水'}[day_master_wuxing]
        
        if day_master_count >= 3:
            # 日主旺，需要克泄耗
            yong_shen = [wo_ke, wo_sheng, ke_wo]
            yong_shen_desc = f"日主{day_master_wuxing}旺，用神为克我之{ke_wo}、我克之{wo_ke}、我生之{wo_sheng}"
        elif day_master_count <= 1:
            # 日主弱，需要生扶
            yong_shen = [sheng_wo, day_master_wuxing]
            yong_shen_desc = f"日主{day_master_wuxing}弱，用神为生我之{sheng_wo}、同我之{day_master_wuxing}"
        else:
            # 日主平和
            yong_shen = [day_master_wuxing, sheng_wo]
            yong_shen_desc = f"日主{day_master_wuxing}平和，用神为{day_master_wuxing}、{sheng_wo}"
        
        return {
            'yong_shen': yong_shen,
            'description': yong_shen_desc,
            'primary': yong_shen[0],
            'secondary': yong_shen[1] if len(yong_shen) > 1 else None
        }
    
    def calculate(self, birth_date_str, birth_time_str):
        """主计算函数"""
        # 解析日期和时间
        year, month, day = map(int, birth_date_str.split('-'))
        hour, minute = map(int, birth_time_str.split(':'))
        
        # 转换为农历
        lunar = self.solar_to_lunar(year, month, day)
        lunar_date_str = f"農曆{self.LUNAR_MONTHS[lunar['month']-1]}月{lunar['day']}日"
        
        # 获取时辰
        shichen, shichen_range = self.get_shichen(hour, minute)
        lunar_time_str = f"{shichen}時"
        
        # 计算四柱
        year_pillar = self.get_year_gan_zhi(lunar['year'])
        month_pillar = self.get_month_gan_zhi(year, month, day, hour)
        day_pillar = self.get_day_gan_zhi(year, month, day)
        hour_pillar = self.get_hour_gan_zhi(day_pillar, hour)
        
        bazi = {
            'year': year_pillar,
            'month': month_pillar,
            'day': day_pillar,
            'hour': hour_pillar
        }
        
        # 五行分析
        wuxing_analysis = self.analyze_wuxing(bazi)
        
        # 计算用神
        yong_shen = self.calculate_yong_shen(wuxing_analysis, bazi)
        
        return {
            'year_pillar': year_pillar,
            'month_pillar': month_pillar,
            'day_pillar': day_pillar,
            'hour_pillar': hour_pillar,
            'lunar_date': lunar_date_str,
            'lunar_time': lunar_time_str,
            'shichen': shichen,
            'day_master': wuxing_analysis['day_master'],
            'day_master_wuxing': wuxing_analysis['day_master_wuxing'],
            'yong_shen': yong_shen,
            'wuxing_analysis': wuxing_analysis
        }


# 测试代码
if __name__ == '__main__':
    calc = BaziCalculator()
    result = calc.calculate('2022-08-25', '21:15')
    print("八字计算结果:")
    print(f"年柱: {result['year_pillar']}")
    print(f"月柱: {result['month_pillar']}")
    print(f"日柱: {result['day_pillar']}")
    print(f"时柱: {result['hour_pillar']}")
    print(f"农历: {result['lunar_date']} {result['lunar_time']}")
    print(f"日主: {result['day_master']} ({result['day_master_wuxing']})")
    print(f"用神: {result['yong_shen']['yong_shen']}")
