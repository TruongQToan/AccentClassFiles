import xlrd
from xlutils.copy import copy
from xlutils.save import save
import sys

def fill(workbook):
    w = copy(workbook)
    s = w.get_sheet(0)
    sheet = workbook.sheet_by_index(0)
    value1 = None
    value2 = None
    change_value = True
    for row in range(sheet.nrows):
        if sheet.cell_type(row, 2) in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
            if value1 is not None: 
                value2 = value2 + 1
                s.write(row, 2, value2)
                s.write(row, 1, value1)
            change_value = False
        else: 
            value1 = int(sheet.col_values(1)[row])
            value2 = int(sheet.col_values(2)[row])
            change_value = True
    w.save('Mastering the American Accent - Quizlet-1.xlsx')

if __name__ == '__main__':
    workbook = xlrd.open_workbook('Mastering-the-American-Accent-Quizlet.xlsx')

    fill(workbook)
