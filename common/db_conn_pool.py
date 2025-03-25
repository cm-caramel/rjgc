import pymysql
from dbutils.pooled_db import PooledDB


class DBConnPool:
    def __init__(self, host, port, user, password, db):
        self.pool = PooledDB(
            creator=pymysql,
            maxconnections=10,
            mincached=3,
            maxcached=5,
            ping=1,
            blocking=True,
            host=host,
            port=port,
            user=user,
            password=password,
            db=db,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )

    def get_conn(self):
        return self.pool.connection()

    # def __init__(self, host, port, user, password, db):
    #     self.conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset='utf8')
    #     self.results = None
    #
    # def close(self):
    #     self.conn.close()
    #
    # def execute(self, sql):
    #     try:
    #         with self.conn.cursor() as cursor:
    #             cursor.execute(sql)
    #             self.conn.commit()
    #             self.results = cursor.fetchall()
    #     except Exception as e:
    #         self.conn.rollback()
    #         raise SqlException(f'\nSQL执行错误：\n{sql}\n{str(e)}\n\n') from e
    #
    # def exit_user(self, school, user, pwd):
    #     sql = f"SELECT * " \
    #           f"FROM v_user " \
    #           f"WHERE school_name = '{school}' AND user_account = '{user}' AND user_password = '{pwd}'"
    #     self.execute(sql)
    #     return len(self.results) > 0
