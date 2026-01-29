from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os
from datetime import datetime

class PDFGenerator:
    """PDF生成器 - 生成传统风格的批命书"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._register_fonts()
        self.setup_styles()
    
    def _register_fonts(self):
        """注册中文字体"""
        font_paths = [
            '/Users/catalpachan/Library/Fonts/AlibabaPuHuiTi-3-55-Regular.ttf',
            '/Users/catalpachan/Library/Fonts/AlibabaPuHuiTi-3-65-Medium.ttf',
            '/Users/catalpachan/Library/Fonts/AlibabaPuHuiTi-3-75-SemiBold.ttf',
            '/Users/catalpachan/Library/Fonts/AlibabaPuHuiTi-3-85-Bold.ttf',
        ]
        
        available_fonts = []
        for font_path in font_paths:
            if os.path.exists(font_path):
                font_name = os.path.basename(font_path).replace('.ttf', '').replace('.otf', '')
                pdfmetrics.registerFont(TTFont(font_name, font_path))
                available_fonts.append(font_name)
        
        if not available_fonts:
            pdfmetrics.registerFont(TTFont('Heiti', '/System/Library/Fonts/STHeiti Medium.ttc'))
            self.font_normal = 'Heiti'
            self.font_bold = 'Heiti'
        else:
            self.font_normal = available_fonts[0]
            self.font_bold = available_fonts[2] if len(available_fonts) > 2 else available_fonts[0]
    
    def setup_styles(self):
        """设置PDF样式"""
        # 标题样式
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#8B0000'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName=self.font_bold
        )
        
        # 副标题样式
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#8B0000'),
            spaceAfter=15,
            alignment=TA_CENTER,
            fontName=self.font_bold
        )
        
        # 正文样式
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            textColor=colors.black,
            spaceAfter=10,
            leading=16,
            fontName=self.font_normal
        )
        
        # 标签样式
        self.label_style = ParagraphStyle(
            'LabelStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#8B0000'),
            fontName=self.font_bold
        )
        
        # 数值样式
        self.value_style = ParagraphStyle(
            'ValueStyle',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.black,
            fontName=self.font_normal
        )
        
        # 八字样式（大号）
        self.bazi_style = ParagraphStyle(
            'BaziStyle',
            parent=self.styles['Normal'],
            fontSize=20,
            textColor=colors.HexColor('#8B0000'),
            alignment=TA_CENTER,
            fontName=self.font_bold
        )
        
        # 姓名样式
        self.name_style = ParagraphStyle(
            'NameStyle',
            parent=self.styles['Normal'],
            fontSize=28,
            textColor=colors.HexColor('#8B0000'),
            alignment=TA_CENTER,
            fontName=self.font_bold,
            spaceAfter=10
        )
        
        # 居明评语样式
        self.juming_style = ParagraphStyle(
            'JuMingStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#FFD700'),
            backColor=colors.HexColor('#8B0000'),
            borderPadding=15,
            alignment=TA_CENTER,
            leading=20,
            fontName=self.font_normal
        )
        
        # 免责声明样式
        self.disclaimer_style = ParagraphStyle(
            'DisclaimerStyle',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#8B0000'),
            alignment=TA_CENTER,
            leading=14,
            fontName=self.font_normal
        )
    
    def generate(self, data, output_path=None):
        """生成PDF批命书"""
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f'/tmp/命理批算書_{timestamp}.pdf'
        
        # 创建PDF文档
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # 构建内容
        story = []
        
        # 标题
        story.append(Paragraph("李居明Agent", self.title_style))
        story.append(Paragraph("風水命理起名批算書", self.subtitle_style))
        story.append(Spacer(1, 20))
        
        # 基本信息
        story.extend(self._create_basic_info_table(data))
        story.append(Spacer(1, 20))
        
        # 八字信息
        story.extend(self._create_bazi_section(data))
        story.append(Spacer(1, 20))
        
        # 首选姓名
        story.extend(self._create_names_section(data))
        story.append(Spacer(1, 20))
        
        # 备用字
        story.extend(self._create_backup_chars_section(data))
        story.append(Spacer(1, 20))
        
        # 英文名
        story.extend(self._create_english_names_section(data))
        story.append(Spacer(1, 20))
        
        # 运势分析
        story.extend(self._create_fortune_section(data))
        story.append(Spacer(1, 20))
        
        # 居明评语
        story.extend(self._create_juming_comment(data))
        story.append(Spacer(1, 20))
        
        # 免责声明
        story.extend(self._create_disclaimer())
        
        # 生成PDF
        doc.build(story)
        
        return output_path
    
    def _create_basic_info_table(self, data):
        """创建基本信息表格"""
        birth_info = data.get('birthInfo', {})
        
        table_data = [
            [Paragraph('<b>姓氏</b>', self.label_style), birth_info.get('surname', ''),
             Paragraph('<b>性別</b>', self.label_style), birth_info.get('gender', '')],
            [Paragraph('<b>新曆</b>', self.label_style), birth_info.get('solarDate', ''),
             Paragraph('<b>時間</b>', self.label_style), birth_info.get('solarTime', '')],
            [Paragraph('<b>農曆</b>', self.label_style), birth_info.get('lunarDate', ''),
             Paragraph('<b>時辰</b>', self.label_style), birth_info.get('lunarTime', '')],
        ]
        
        table = Table(table_data, colWidths=[3*cm, 5*cm, 3*cm, 5*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#FFF8DC')),
            ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#FFF8DC')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#8B0000')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#8B0000')),
            ('FONTNAME', (0, 0), (-1, -1), self.font_normal),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        
        return [table]
    
    def _create_bazi_section(self, data):
        """创建八字部分"""
        elements = []
        elements.append(Paragraph("生辰八字", self.subtitle_style))
        
        bazi = data.get('bazi', {})
        
        # 八字表格
        table_data = [
            [Paragraph('年柱', self.label_style), 
             Paragraph('月柱', self.label_style), 
             Paragraph('日柱', self.label_style), 
             Paragraph('時柱', self.label_style)],
            [Paragraph(bazi.get('year', ''), self.bazi_style),
             Paragraph(bazi.get('month', ''), self.bazi_style),
             Paragraph(bazi.get('day', ''), self.bazi_style),
             Paragraph(bazi.get('hour', ''), self.bazi_style)]
        ]
        
        table = Table(table_data, colWidths=[4*cm, 4*cm, 4*cm, 4*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B0000')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#FFD700')),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#FFF8DC')),
            ('TEXTCOLOR', (0, 1), (-1, 1), colors.HexColor('#8B0000')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 2, colors.HexColor('#8B0000')),
            ('PADDING', (0, 0), (-1, -1), 15),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 10))
        
        # 用神信息
        yong_shen = bazi.get('yongShen', {})
        if isinstance(yong_shen, dict):
            yong_shen_str = '、'.join(yong_shen.get('yong_shen', ['木', '火']))
        else:
            yong_shen_str = str(yong_shen)
        
        elements.append(Paragraph(
            f"<b>用神：{yong_shen_str}</b>（日主{bazi.get('dayMaster', '')}）",
            ParagraphStyle('YongShen', parent=self.body_style, alignment=TA_CENTER, 
                          textColor=colors.HexColor('#8B0000'), fontSize=12)
        ))
        
        return elements
    
    def _create_names_section(self, data):
        """创建姓名部分"""
        elements = []
        elements.append(Paragraph("首選姓名", self.subtitle_style))
        
        primary_names = data.get('primaryNames', [])
        fortune = data.get('fortune', {})
        fortune_analysis = fortune.get('primary_names_analysis', [])
        
        for i, name in enumerate(primary_names):
            # 姓名卡片
            name_data = [
                [Paragraph(f"首選 {i+1}", self.label_style)],
                [Paragraph(name.get('name', ''), self.name_style)],
            ]
            
            # 添加笔画信息
            chars = name.get('chars', [])
            strokes = name.get('strokes', [])
            stroke_text = ' | '.join([f"{c} {s}劃" for c, s in zip(chars, strokes)])
            name_data.append([Paragraph(stroke_text, self.body_style)])
            
            # 添加运势信息
            if i < len(fortune_analysis):
                fa = fortune_analysis[i]
                zhu_yun = fa.get('zhu_yun', {})
                info_text = f"總格：{name.get('zongge', '')}劃 | 主運：{zhu_yun.get('gua_name', '')}"
                name_data.append([Paragraph(info_text, self.body_style)])
            
            name_table = Table(name_data, colWidths=[14*cm])
            name_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B0000')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#FFD700')),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FFF8DC')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#8B0000')),
                ('PADDING', (0, 0), (-1, -1), 10),
            ]))
            
            elements.append(name_table)
            elements.append(Spacer(1, 10))
        
        return elements
    
    def _create_backup_chars_section(self, data):
        """创建备用字部分"""
        elements = []
        elements.append(Paragraph("備用字選（可自行選配）", self.subtitle_style))
        
        backup_chars = data.get('backupChars', [])
        
        # 将备用字分成多行显示
        chars_per_row = 6
        rows = []
        current_row = []
        
        for char_info in backup_chars:
            char = char_info.get('char', '')
            strokes = char_info.get('strokes', '')
            cell_content = f"{char}\n{strokes}劃"
            current_row.append(Paragraph(cell_content, self.body_style))
            
            if len(current_row) == chars_per_row:
                rows.append(current_row)
                current_row = []
        
        if current_row:
            while len(current_row) < chars_per_row:
                current_row.append('')
            rows.append(current_row)
        
        if rows:
            table = Table(rows, colWidths=[2.3*cm]*chars_per_row)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFF8DC')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#8B0000')),
                ('PADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(table)
        
        return elements
    
    def _create_english_names_section(self, data):
        """创建英文名部分"""
        elements = []
        elements.append(Paragraph("英文名建議", self.subtitle_style))
        
        english_names = data.get('englishNames', [])
        
        # 将英文名分成多行
        names_per_row = 4
        rows = []
        current_row = []
        
        for name in english_names[:16]:  # 最多显示16个
            current_row.append(Paragraph(name, self.body_style))
            if len(current_row) == names_per_row:
                rows.append(current_row)
                current_row = []
        
        if current_row:
            while len(current_row) < names_per_row:
                current_row.append('')
            rows.append(current_row)
        
        if rows:
            table = Table(rows, colWidths=[3.5*cm]*names_per_row)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFF8DC')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#FFD700')),
                ('PADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(table)
        
        return elements
    
    def _create_fortune_section(self, data):
        """创建运势分析部分"""
        elements = []
        elements.append(Paragraph("運勢分析", self.subtitle_style))
        
        fortune = data.get('fortune', {})
        fortune_analysis = fortune.get('primary_names_analysis', [])
        
        if fortune_analysis:
            fa = fortune_analysis[0]
            
            fortune_data = [
                [Paragraph('<b>主運（總格）</b>', self.label_style),
                 Paragraph('<b>前運（人格）</b>', self.label_style),
                 Paragraph('<b>後運（地格）</b>', self.label_style)],
                [Paragraph(f"{fa.get('zongge', '')}劃", self.bazi_style),
                 Paragraph(f"{fa.get('renge', '')}劃", self.bazi_style),
                 Paragraph(f"{fa.get('dige', '')}劃", self.bazi_style)],
            ]
            
            # 添加卦名
            zhu_yun = fa.get('zhu_yun', {})
            qian_yun = fa.get('qian_yun', {})
            hou_yun = fa.get('hou_yun', {})
            
            fortune_data.append([
                Paragraph(zhu_yun.get('gua_name', ''), self.body_style),
                Paragraph(qian_yun.get('gua_name', ''), self.body_style),
                Paragraph(hou_yun.get('gua_name', ''), self.body_style)
            ])
            
            # 添加描述
            fortune_data.append([
                Paragraph(zhu_yun.get('description', ''), 
                         ParagraphStyle('Small', parent=self.body_style, fontSize=9)),
                Paragraph(qian_yun.get('description', ''), 
                         ParagraphStyle('Small', parent=self.body_style, fontSize=9)),
                Paragraph(hou_yun.get('description', ''), 
                         ParagraphStyle('Small', parent=self.body_style, fontSize=9))
            ])
            
            table = Table(fortune_data, colWidths=[4.6*cm, 4.6*cm, 4.6*cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B0000')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#FFD700')),
                ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#FFF8DC')),
                ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#8B0000')),
                ('TEXTCOLOR', (0, 2), (-1, 2), colors.HexColor('#FFD700')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#8B0000')),
                ('PADDING', (0, 0), (-1, -1), 8),
            ]))
            
            elements.append(table)
        
        return elements
    
    def _create_juming_comment(self, data):
        """创建居明评语部分"""
        elements = []
        
        fortune = data.get('fortune', {})
        fortune_analysis = fortune.get('primary_names_analysis', [])
        
        if fortune_analysis:
            fa = fortune_analysis[0]
            ju_ming = fa.get('ju_ming_comment', {})
            
            comment_text = ju_ming.get('comment', '')
            note_text = ju_ming.get('note', '')
            
            full_text = f"<b>居明評曰</b><br/><br/>{comment_text}<br/><br/><i>{note_text}</i>"
            
            elements.append(Paragraph(full_text, self.juming_style))
        
        return elements
    
    def _create_disclaimer(self):
        """创建免责声明"""
        disclaimer_text = """
        <b>【八字命理占算】</b><br/>
        在科學觀點上祇可作為引証參考和研究，所提供之言論和方案，<br/>
        行使之決斷和成效上，責任在於問事本人。
        """
        
        disclaimer_style = ParagraphStyle(
            'Disclaimer',
            parent=self.disclaimer_style,
            backColor=colors.HexColor('#FFE4E1'),
            borderColor=colors.HexColor('#8B0000'),
            borderWidth=1,
            borderPadding=10
        )
        
        return [Paragraph(disclaimer_text, disclaimer_style)]


# 测试代码
if __name__ == '__main__':
    generator = PDFGenerator()
    
    # 模拟数据
    test_data = {
        'birthInfo': {
            'surname': '黃',
            'gender': '男',
            'solarDate': '2025-04-08',
            'solarTime': '12:29',
            'lunarDate': '農曆三月十一日',
            'lunarTime': '午時'
        },
        'bazi': {
            'year': '乙巳',
            'month': '庚辰',
            'day': '丁未',
            'hour': '丙午',
            'dayMaster': '丁',
            'yongShen': '木火'
        },
        'primaryNames': [
            {
                'name': '黃智輝',
                'chars': ['智', '輝'],
                'strokes': [12, 15],
                'zongge': 37,
                'sancai_wuxing': {'configuration': '火-土-火'}
            }
        ],
        'backupChars': [
            {'char': '傑', 'strokes': 12}, {'char': '焯', 'strokes': 12},
            {'char': '智', 'strokes': 12}, {'char': '森', 'strokes': 12},
            {'char': '惠', 'strokes': 12}, {'char': '景', 'strokes': 12},
        ],
        'englishNames': ['Alfred', 'David', 'Andrew', 'Arthur', 'Albert'],
        'fortune': {
            'primary_names_analysis': [
                {
                    'zongge': 37,
                    'renge': 25,
                    'dige': 27,
                    'zhu_yun': {
                        'number': 37,
                        'gua_name': '猛虎出林卦',
                        'description': '主一生人之運勢，此數能得大財利，健康，名譽，財富三俱足。'
                    },
                    'qian_yun': {
                        'number': 25,
                        'gua_name': '英邁俊敏卦',
                        'description': '主前半生之運勢，此數男子必俊秀，有貴人緣，柔中帶剛，成功發達之數。'
                    },
                    'hou_yun': {
                        'number': 27,
                        'gua_name': '增長之數卦',
                        'description': '主中晚年之運勢，此數享權名壽祿，具才謀德澤，又能傳子孫。'
                    },
                    'ju_ming_comment': {
                        'comment': '「丁火生辰月，土金當旺，用神以木火，丁火身強，可更添健康財貴。智輝木火俱備，五行配合音佳且帶氣質之名。」',
                        'note': '(屬木可生火，音健)'
                    }
                }
            ]
        }
    }
    
    pdf_path = generator.generate(test_data)
    print(f"PDF已生成: {pdf_path}")
