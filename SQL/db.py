import pymysql
import mysql.connector
import pandas as pd


# MySQL에 연결
conn = pymysql.connect(host='localhost', user='root', password='0000', db='youngdb1', charset='utf8')

cur = conn.cursor()

# 쿼리 실행
query = "SELECT * FROM department"
df = pd.read_sql(query, conn)

# 결과를 CSV 파일로 저장
df.to_csv('department.csv', index=False, encoding='utf-8-sig')

# 연결 종료
conn.close()