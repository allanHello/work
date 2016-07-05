# -*- coding: utf-8 -*-
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.append(['艺术家姓名', '序号', '名称', '估价', '成交价',
           '拍卖日期', '拍卖机构', '名称2', '尺寸', '作品分类',
           '创作年代', '估价', '成交价', '专场', '拍卖时间', '拍卖公司',
           '拍卖会', '说明1', '说明2', '说明3'])
wb.save("data.xlsx")
