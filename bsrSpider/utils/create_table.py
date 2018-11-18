import re
import time
from conf.config import BASE_TYPE
from conf.config import DATADB_CONFIG
import psycopg2
import datetime
a = 888
d = datetime.datetime.now().strftime('%Y-%m-%d')
conn = psycopg2.connect(**DATADB_CONFIG[BASE_TYPE])
cur = conn.cursor()
cur.execute('''CREATE TABLE AMAZON_BSR_QTY
       (ID              SERIAL        PRIMARY KEY     NOT NULL,
       CATEGORY         CHAR(300)            NOT NULL,
       STATE            SMALLINT                  NOT NULL,
       TM               BIGINT                 NOT NULL,
       BSR              INT                  NOT NULL,
       MOON_SALE_QTYM    INT                  NOT NULL,
       BSR_ID           VARCHAR(100)         NOT NULL  DEFAULT '',
       IS_SYNC          SMALLINT             NOT NULL  DEFAULT 0,
       SYNC_TM          INT                  NOT NULL   DEFAULT 0);''')

cur.execute('''CREATE TABLE AMAZON_DRUID_BSR_QTY
       (ID              SERIAL        PRIMARY KEY     NOT NULL,
       CATEGORY         CHAR(300)            NOT NULL,
       STATE            SMALLINT                  NOT NULL,
       TM               BIGINT                 NOT NULL,
       BSR              INT                  NOT NULL,
       MOON_SALE_QTYM    INT                  NOT NULL,
       BSR_ID           VARCHAR(100)         NOT NULL  DEFAULT '',
       ADAY             DATE                 NOT NULL,
       IS_SYNC          SMALLINT             NOT NULL  DEFAULT 0,
       SYNC_TM          INT                  NOT NULL   DEFAULT 0);''')
# cur.execute(
#     "INSERT INTO "+UPDATE_TABEL_NAME+" (CATEGORY, STATE, TM, BSR, MOON_SALE_QTYM) VALUES ( 'Appliances', 1, 1499825149257, 1, '"+str(a)+"')");
# cur.execute(
#     "INSERT INTO "+DRUID_TABEL_NAME+" (CATEGORY, STATE, TM, BSR, MOON_SALE_QTYM, ADAY) VALUES ( 'Appliances', 1, 1499825149257, 1, '"+str(a)+"', '"+d+"' )");

conn.commit()
conn.close()

