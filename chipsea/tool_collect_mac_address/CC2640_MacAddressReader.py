import sqlite3 as lite
import sys
import xlwt


def gen_xls(dic):
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet("chipsea")
    worksheet.write(0,0,"时间");worksheet.write(0,1,"MAC地址");
    i = 0;
    for mac,time in dic.items():
        i = i+1;
        print(time, mac)
        worksheet.write(i,0,time);worksheet.write(i,1,mac);
    # 保存xls
    workbook.save("chipsea.xls")


if __name__ == '__main__':

    try:
        con = None
        con = lite.connect('chipsea.db')
        cur = con.cursor()
        cur.execute('select sqlite_version()')
        version = cur.fetchone()
        print("version: %s"  %version)
        cur.execute("SELECT * FROM mac_address_table")
        address = cur.fetchall()
        # 新建字典装数据
        mac_dict = {}
        for row in address:
            print(row)
            mac_dict[row[1]] = row[0]
        # 保存到excle
        gen_xls(mac_dict)
    except Exception as e:
        print("发生异常")
        print(str(e))
        # sys.exit(1)

    finally:
        pass
        if con:
            con.close()
        input()