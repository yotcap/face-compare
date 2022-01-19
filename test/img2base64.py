#coding=utf-8
import csv
import base64

def image_to_base64():
    '''封装把图片转换为base64编码格式'''
    o = open(r"./1-0.jpg", 'rb')
    base64_data = base64.b64encode(o.read())
    s = base64_data.decode()
    return ("data:image/png;base64,%s"%s)

def base64_write_csv():
    '''把生成的base64写入CSV文件'''
    f = open(r'./image.csv', 'wb')
    csv_writer = csv.writer(f)

    csv_writer.writerow(["image"])
    csv_writer.writerow([image_to_base64().encode()])
    f.close()

if __name__ == '__main__':
    base64_write_csv()

