import xlrd
import os


loc = os.path.abspath('websites.xlsx')
wb = xlrd.open_workbook(loc)
st = wb.sheet_by_index(0)
st.cell_value(0, 0)

site = input("Enter name: ")
url = ''

for i in range(st.nrows):
    if site == str(st.cell_value(i, 0)):
        url = st.cell_value(i, 1)
print(url)