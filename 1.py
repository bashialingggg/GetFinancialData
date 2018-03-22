# -*- coding:utf-8 -*-
import re
import requests
import cx_Oracle,time,datetime


#url = 'http://www.boc.cn/sourcedb/whpj/index.html'  # 网址


# 方式一：正则匹配
Cur=['阿联酋迪拉姆','澳大利亚元','巴西里亚尔','加拿大元','瑞士法郎','丹麦克朗','欧元',
          '英镑','港币','印尼卢比','印度卢比','日元','韩国元','澳门元','林吉特','挪威克朗','新西兰元','菲律宾比索',
          '卢布','沙特里亚尔','瑞典克朗','新加坡元','泰国铢','土耳其里拉','新台币','美元']
conn = cx_Oracle.connect('datacenter/cpic123456@10.39.0.86/xmcx1')
s = requests.session()
s.keep_alive = False #关闭多余的连接
def Download(Currency,page): #Currency 币种，url 中行汇率牌价网址
    url = 'http://www.boc.cn/sourcedb/whpj/index_%d.html' %page
    html = requests.get(url).content.decode('utf8')  # 获取网页源码（中间涉及到编码问题,这是个大坑，你得自己摸索）
    a = html.index("<td>{0}</td>".format(Currency))  # 取得“Currency”当前位置
    s = html[a:a + 300]  # 截取*Currency汇率那部分内容（从a到a+300位置）
    result = re.findall('<td>(.*?)</td>', s)  # 正则获取
    return result
#货币名称 现汇买入价 现钞买入价 现汇卖出价 现钞卖出价  中行折算价 发布时间

def Insertsql(conn,result):
    sql = []
    cursor = conn.cursor()
    for i in range(8):
        if result[i] == '':
            result[i] = 'NULL'
        else:
            result[i] = "'"+result[i]+"'"
    sql.append(
        "insert into dc_waihui(hbmc,xhmrj ,xcmrj ,xhmcj ,xcmcj ,zhzsj,fbrq ,fbsj )"
        "values({0},{1},{2},{3},{4},{5},{6},{7})".format(result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7]))
    cursor.execute(sql[0])
    conn.commit()
# 方式二：lxml获取
# result=etree.HTML(html).xpath('//table[@cellpadding="0"]/tr[18]/td/text()')

list = [1,2,3,4,5,6,7,8,9]
for page in list:
    for  i in range(26):
        Currency = Cur[i]
        result = Download(Currency,page)
        Insertsql(conn, result)


#写入txt
'''with open('C:/Users/admin/Desktop/汇率.txt', 'w+') as f:
    f.write(result[0] + '\n')
    f.write('现汇买入价：' + result[1] + '\n')
    f.write('现钞买入价：' + result[2] + '\n')
    f.write('现汇卖出价：' + result[3] + '\n')
    f.write('现钞卖出价：' + result[4] + '\n')
    f.write('中行折算价：' + result[5] + '\n')
    f.write('发布时间：' + result[6] +' '+ result[7] + '\n')'''