import MySQLdb

if __name__ == "__main__":
    # 打开数据库连接
    db = MySQLdb.connect("129.211.27.244", "root", "123456", "ipfs", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 删除语句
    sql = "DELETE FROM users_copy1 WHERE id != ''"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交修改
        db.commit()
        print("delete OK")
    except:
        # 发生错误时回滚
        db.rollback()
    # 关闭连接
    db.close()
