import aiomysql
import pymysql


class DbHander:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.connect()

    def connect(self) -> None:
        self.conn = pymysql.connect(host='localhost',
                                    user='root',
                                    password='',
                                    database='stn_dealer',
                                    cursorclass=pymysql.cursors.DictCursor,
                                    )

        self.cur = self.conn.cursor()

    def get_items(self) -> dict:
        sql = "select * from show_items order by id"
        self.cur.execute(sql)
        return self.cur.fetchall()

    def get_wallet(self) -> dict:
        sql = "select * from wallet"
        self.cur.execute(sql)
        return self.cur.fetchall()

    def disconnect(self):
        self.conn.close()


class AsyncDbHandler:

    def __init__(self):
        self.conn = None
        self.cur = None

    @staticmethod
    async def insert_stn_url(id, url, loop):
        conn = await aiomysql.connect(host='localhost',
                                      user='root',
                                      password='',
                                      db='stn_dealer',
                                      autocommit=True,
                                      loop=loop)
        await conn.query('SET GLOBAL connect_timeout=6000')
        cur = await conn.cursor()

        await cur.execute(f"insert into stn_url(item_id, url) values({id}, \"{url}\")")

        conn.close()
        cur.close()

    async def insert_item(self, loop, effect, quality, name, base_price, url, craftable, existing):
        conn = await aiomysql.connect(host='localhost',
                                      user='root',
                                      password='',
                                      db='stn_dealer',
                                      autocommit=True,
                                      loop=loop)
        cur = await conn.cursor()

        await conn.query("SET GLOBAL connect_timeout=6000")
        sql = ""
        await cur.execute(sql)

        conn.close()
        cur.close()
