#!/usr/bin/env python
# coding: utf-8

###################################################################
#                                                                 #
#   2026 DS2 Database Project : Recommendation using SQL-Python   #
#                                                                 #
###################################################################

import mysql.connector
from tabulate import tabulate
import pandas as pd
import math
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

## Connect to Remote Database
## Insert database information

HOST = "astronaut.snu.ac.kr"
USER = "DS2026_00019"
PASSWD = "DS2026_00019"
DB = "DS2026_00019"

connection = mysql.connector.connect(
    host=HOST,
    port=7000,
    user=USER,
    passwd=PASSWD,
    db=DB,
    autocommit=True,  # to create table permanently
)

cur = connection.cursor(dictionary=True)

## 수정할 필요 없는 함수입니다.
# DO NOT CHANGE INITIAL TABLES IN prj.sql
def get_dump(mysql_con, filename):
    """
    connect to mysql server using mysql_connector
    load .sql file (filename) to get queries that create tables in an existing database (fma)
    """
    query = ""
    try:
        with mysql_con.cursor() as cursor:
            for line in open(filename, "r"):
                if line.strip():
                    line = line.strip()
                    if line[-1] == ";":
                        query += line
                        cursor.execute(query)
                        query = ""
                    else:
                        query += line

    except Warning as warn:
        print(warn)
        sys.exit()


## 수정할 필요 없는 함수입니다.
# SQL query 를 받아 해당 query를 보내고 그 결과 값을 dataframe으로 저장해 return 해주는 함수
def get_output(query):
    cur.execute(query)
    out = cur.fetchall()
    df = pd.DataFrame(out)
    return df

#-----test------
#query = "SELECT * FROM ratings WHERE rating IS NULL;"
#print(get_output(query))  #user/item/rating

#query = "SELECT * FROM user_similarity LIMIT 10;"
#print(get_output(query)) user_1, user_2, sim




#-----test------


# [Algorithm 1] Popularity-based Recommendation - 1 : Popularity by rating count
def popularity_based_count():
    user = int(input("User Id: "))
    rec_num = int(input("Number of recommendations?: "))

    print(f"Popularity Count based recommendation")
    print("=" * 99)

    # TODO: remove sample, return actual recommendation result as df
    # YOUR CODE GOES HERE !

    #--------------------------answer-----------------------
    # item별 rating count 집계를 하는데, 입력받은 사용자가 rating한 거는 제외하고 집계.
    query = f""" SELECT item, count(rating) as prediction
                FROM ratings
                WHERE item NOT IN ( SELECT DISTINCT item FROM ratings WHERE user = {user} and rating IS NOT NULL)
                GROUP BY item
                ORDER BY prediction desc , item
             ; """
    df = get_output(query)
    
    # 쿼리의 결과를 results 변수에 저장하세요.
    results = [(row["item"], row["prediction"]) for _, row in df.head(rec_num).iterrows()]
    
    #--------------------------answer-----------------------
    
    # 최종 결과 얻은 뒤, 중간 계산 중 만든 table 삭제
    # TODO end

    # Do not change this part
    # do not change column names
    df = pd.DataFrame(results, columns=["item", "prediction"])
    tab = tabulate(df, headers=df.columns, tablefmt="psql", showindex=False)
    print(tab)
    with open("pbc.txt", "w") as f:
        f.write(tab)
    print("Output printed in pbc.txt")


# [Algorithm 2] Popularity-based Recommendation - 2 : Popularity by average rating
def popularity_based_rating():
    user = int(input("User Id: "))
    rec_num = int(input("Number of recommendations?: "))

    print(f"Popularity Rating based recommendation")
    print("=" * 99)

    # TODO: remove sample, return actual recommendation result as df
    # YOUR CODE GOES HERE !


    #--------------------------answer-----------------------

    # 1) item 상관없이 사용자별 min / max 값 저장한 table을 만들기.
    
    #-- 평점 한개도 없는 users는 없음.--
    #print(get_output(
    #    """ SELECT user, count(rating)
    #        FROM ratings
    #        GROUP BY user
    #        HAVING count(rating) = 0; """ )) 
    
    get_output("""DROP TABLE IF EXISTS min_max;""")

    get_output(""" CREATE TABLE min_max (
                user INTEGER,
                min_rating NUMERIC(2,1),
                max_rating NUMERIC(2,1));
            """)
    
    get_output(""" INSERT INTO min_max
                SELECT user, CASE WHEN 
               count(rating) = 1 THEN 0 ELSE MIN(rating) END, MAX(rating)
                FROM ratings
                GROUP BY user;
            """)
    # 2) 보정한 값을 rating에 cor_rating으로 넣기 
    try: 
        get_output("""ALTER TABLE ratings DROP COLUMN cor_rating;""")
    except: 
        pass

    get_output(""" ALTER TABLE ratings ADD cor_rating numeric(5,4)""")
    
    get_output(""" UPDATE ratings r
                LEFT JOIN min_max mm ON r.user = mm.user
            SET r.cor_rating = ROUND((r.rating - mm.min_rating) / (mm.max_rating - mm.min_rating),4)
            WHERE r.rating IS NOT NULL; """)
    
    #print(get_output(""" SELECT * FROM ratings"""))

    # 3) 보정된 평점을 기반으로 평균 평점이 높은 item을 추천. 사용자가 이미 평점 기록한 item은 제외.
    
    query = f""" SELECT item, round(avg(cor_rating),4) as prediction
                FROM ratings
                WHERE item NOT IN ( SELECT DISTINCT item FROM ratings WHERE user = {user} and cor_rating IS NOT NULL)
                GROUP BY item
                ORDER BY prediction desc , item
             ; """
    
    df = get_output(query)
    
    # 쿼리의 결과를 results 변수에 저장하세요.
    
    results = [(row["item"], row["prediction"]) for _, row in df.head(rec_num).iterrows()]
    
    #--------------------------answer-----------------------

    # 최종 결과 얻은 뒤, 중간 계산 중 만든 table 삭제
    #    min_max table drop
    get_output("DROP TABLE min_max;")
    #    rating에서 cor_rating column 삭제
    get_output("ALTER TABLE ratings DROP COLUMN cor_rating;")
    
    #----------------------TODO end------------------------

    # Do not change this part
    # do not change column names
    df = pd.DataFrame(results, columns=["item", "prediction"])
    tab = tabulate(df, headers=df.columns, tablefmt="psql", showindex=False)
    print(tab)
    with open("pbr.txt", "w") as f:
        f.write(tab)
    print("Output printed in pbr.txt")


# [Algorithm 3] User-based Recommendation
def ubcf():
    user = int(input("User Id: "))
    rec_num = float(input("Recommendation Threshold: "))

    print("=" * 99)
    print(f"User-based Collaborative Filtering")
    print(f"Recommendations for user {user}")

    # TODO: remove sample, return actual recommendation result as df
    # YOUR CODE GOES HERE !
    #--------------------------answer-----------------------
    #print(get_output("SELECT * FROM user_similarity;")) #user_1, user_2, sim
    
    # 1) 평점 보정 먼저 진행 -> 2번 가져오기.
    get_output("DROP TABLE IF EXISTS min_max;")

    get_output(""" CREATE TABLE min_max (
                user INTEGER,
                min_rating NUMERIC(2,1),
                max_rating NUMERIC(2,1));
            """)
    
    get_output(""" INSERT INTO min_max
                SELECT user, CASE WHEN 
               count(rating) = 1 THEN 0 ELSE MIN(rating) END, MAX(rating)
                FROM ratings
                GROUP BY user;
            """)
    # 2) 보정한 값을 rating에 cor_rating으로 넣기 
    try: 
        get_output("ALTER TABLE ratings DROP COLUMN cor_rating;")
    except: 
        pass

    get_output(""" ALTER TABLE ratings ADD cor_rating numeric(5,4)""")
    
    get_output(""" UPDATE ratings r
                LEFT JOIN min_max mm ON r.user = mm.user
            SET r.cor_rating = ROUND((r.rating - mm.min_rating) / (mm.max_rating - mm.min_rating),4)
            WHERE r.rating IS NOT NULL; """)
    
    #print(get_output(""" SELECT * FROM ratings"""))

    
    # 2) 유사도 높은 이웃 k=5 명 구한 SQL TABLE 만들기
    get_output("DROP TABLE IF EXISTS sim_k;")

    get_output(""" CREATE TABLE sim_k (
                user_1 INTEGER,
                user_2 INTEGER,
                sim NUMERIC(3,2));
            """)
    
    get_output(""" INSERT INTO sim_k
                SELECT user_1, user_2, sub.sim
               FROM (SELECT user_1, user_2 , ROW_NUMBER() OVER(
               PARTITION BY user_1 ORDER BY sim desc, user_2 ) rn_5 , sim
                FROM user_similarity
               ) sub
               WHERE sub.rn_5 <= 5;
            """)
    #print(get_output("""SELECT * FROM sim_k LIMIT 20""")) 

    ##sum table create
    
    get_output("DROP TABLE IF EXISTS sum_sim_k;")

    get_output(""" CREATE TABLE sum_sim_k (
                user_1 INTEGER,
                sum_sim NUMERIC(4,2));
            """)
    
    get_output(""" INSERT INTO sum_sim_k
                SELECT user_1, SUM(sim)
                FROM sim_k
                GROUP BY user_1;
            """)
    #print(get_output("""SELECT * FROM sum_sim_k ORDER BY user_1;"""))

    # SUM TABLE 기준으로 CORRECT 하기.
    try: 
        get_output("ALTER TABLE sim_k DROP COLUMN cor_sim;")
    except: 
        pass

    get_output(""" ALTER TABLE sim_k ADD cor_sim NUMERIC(5,4);""")

    get_output(""" UPDATE sim_k s
                LEFT JOIN sum_sim_k ss ON s.user_1 = ss.user_1
            SET s.cor_sim = ROUND(s.sim/ss.sum_sim,4); """)
    
    
    # print(get_output("""SELECT * FROM sim_k;"""))
    # print(get_output("""SELECT * FROM ratings;"""))

    
    # 보정된 거 기반으로 사용자, 아이템 평점 곱하기
    # u1의 정보 similartiy (sim_k의 user_2) 랑 item별 user_1이랑 join해서 row별로 곱해서 나와야함.

    try: 
        get_output("DROP TABLE IF EXISTS user_similarity_rating;")
    except: 
        pass
    
    get_output(""" CREATE TABLE user_similarity_rating (
                user INTEGER, 
                item INTEGER,
                user_rating NUMERIC(5,4) ); """)
    


    get_output(""" INSERT INTO user_similarity_rating
                SELECT usr.user_1, usr.item, usr.user_rating 
               FROM (
                     SELECT s.user_1 , r.item , ROUND(SUM(s.cor_sim*r.cor_rating),4) AS user_rating
                    FROM sim_k s LEFT JOIN ratings r 
                    ON s.user_2 = r.user
                    GROUP BY s.user_1, r.item
               ) usr; """)
    #user_similarity_rating 에서 item 제외하고, user도 그 유저로 선택
    
    query = (f""" SELECT item, user_rating as prediction
                FROM user_similarity_rating 
                WHERE item NOT IN ( SELECT DISTINCT r.item FROM ratings r WHERE r.user = {user} and r.cor_rating IS NOT NULL) 
                AND user_rating > {rec_num} and user = {user}
                ORDER BY prediction desc , item
             ; """)
    
    df = get_output(query)

    


    #--------------------------answer-----------------------
    
    # 쿼리의 결과를 results 변수에 저장하세요.
    #results = [(50 - x, x / 10) for x in range(50, math.ceil(rec_num * 10) - 1, -1)]
    results = [(row["item"], row["prediction"]) for _, row in df.iterrows()]
    
    # 최종 결과 얻은 뒤, 중간 계산 중 만든 table 삭제

    #    min_max table drop
    get_output("DROP TABLE min_max;")
    #    rating에서 cor_rating column 삭제
    get_output("ALTER TABLE ratings DROP COLUMN cor_rating;")
    #   sim_k table drop
    get_output("DROP TABLE sim_k;")
    #   sum_sim_k table drop
    get_output("DROP TABLE sum_sim_k;")
    #   user_similarity_rating drop
    get_output("DROP TABLE user_similarity_rating;")

    #----------------------TODO end------------------------

    # Do not change this part
    # do not change column names
    df = pd.DataFrame(results, columns=["item", "prediction"])
    tab = tabulate(df, headers=df.columns, tablefmt="psql", showindex=False)
    print(tab)
    with open("ubcf.txt", "w") as f:
        f.write(tab)
    print("Output printed in ubcf.txt")


# [Algorithm 4] (Optional) User similarity
def user_similarity():

    print("=" * 99)
    print(f"User similarity")

    # TODO: remove sample, return actual recommendation result as df
    # YOUR CODE GOES HERE !
    #-------------------------------------------------------------------
    # 1. ratings의 item끼리 join해서 곱해서 합한 전치 행렬 곱 구해야함.
    # 2. ratings의 user별 합의 제곱근 SQRT(X) 로 ITEM 상관없이
    # 3. 2번을 서로 JOIN해서 다시 곱한다. USER X USER = SUM 이때 서로 동일한 USER = USER값은 0이 되도록 SETTING
    # 4. 1번에서 구한 값을 3번에서 구한 값으로 나누는데, ROUND(X,1) 표현.

    # -------------------------- TODO ----------------------------------
    # 1. ratings의 item끼리 join해서 곱해서 합한 전치 행렬 곱 구해야함.
    
    # temp_rr (rating-rating)
    try: 
        get_output("DROP TABLE IF EXISTS temp_rr;")
    except: 
        pass
    
    get_output(""" CREATE TABLE temp_rr (
                user_1 INTEGER, 
                user_2 INTEGER,
                temp_rating NUMERIC(10,4) ); """)
    
    
    get_output(""" INSERT INTO temp_rr
                SELECT usr.user_1, usr.user_2, usr.temp_rating 
               FROM (
                     SELECT r1.user as user_1, r2.user as user_2 , ROUND(SUM(CASE WHEN r1.user <> r2.user THEN r1.rating*r2.rating ELSE 0 END),4) AS temp_rating
                    FROM ratings r1 LEFT JOIN ratings r2 
                    ON r1.item = r2.item
                    GROUP BY r1.user ,r2.user
               ) usr; """)
    #print(get_output("""SELECT * FROM temp_rr ORDER BY user_1, user_2"""))

    
    # 2. ratings의 user별 합의 제곱근 SQRT(X) 로 ITEM 상관없이
    # temp_sqrt
    try: 
        get_output("DROP TABLE IF EXISTS temp_sqrt;")
    except: 
        pass
    
    get_output(""" CREATE TABLE temp_sqrt (
                user INTEGER, 
                sqrt_rating NUMERIC(6,4) ); """)
    
    get_output(""" INSERT INTO temp_sqrt
                SELECT temp.user , temp.temp_rating 
               FROM (
                     SELECT user , SQRT(SUM(rating*rating)) AS temp_rating
                    FROM ratings r
                    GROUP BY user
               ) temp; """)
    
    #print(get_output("""SELECT * FROM temp_sqrt ORDER BY user;"""))

    # 3. 2번을 서로 JOIN해서 다시 곱한다. USER X USER = SUM 이때 서로 동일한 USER = USER값은 0이 되도록 SETTING
    # tmep_rating
    try: 
        get_output("DROP TABLE IF EXISTS temp_rating;")
    except: 
        pass
    
    get_output(""" CREATE TABLE temp_rating (
                user_1 INTEGER,
                user_2 INTEGER, 
                temp_sqrt_sum NUMERIC(10,4) ); """)
    
    get_output(""" INSERT INTO temp_rating
               SELECT temp.user_1 , temp.user_2 , CASE WHEN temp.user_1 <> temp.user_2 THEN temp.rating ELSE 0 END  
               FROM (
                    SELECT r1.user AS user_1, r2.user AS user_2 , (r1.sqrt_rating * r2.sqrt_rating) AS rating
                    FROM temp_sqrt r1 CROSS JOIN temp_sqrt r2
                    ) temp ;""")
    #print(get_output("""SELECT * FROM temp_rating ORDER BY user_1,user_2;"""))


    # 4. 1번에서 구한 값을 3번에서 구한 값으로 나누는데, ROUND(X,1) 표현.
    # temp_rr , temp_rating을 나누기.
    
    # temp_rr : user_1, user_2 , temp_rating
    # temp_rating : user_1 , user_2 , temp_sqrt_sum
    # row 별로 나누기 해야하는데, 이때 이미 분모가 0(temp_sqrt_sum)이면 그냥 0으로 들어가기.

    try: 
        get_output("""ALTER TABLE temp_rr DROP COLUMN cor_similarity;""")
    except: 
        pass

    get_output(""" ALTER TABLE temp_rr ADD cor_similarity numeric(7,3)""")
    
    get_output(""" UPDATE temp_rr rr
                JOIN temp_rating rt ON rr.user_1 = rt.user_1 and rr.user_2 = rt.user_2
            SET rr.cor_similarity = ROUND(rr.temp_rating / rt.temp_sqrt_sum , 1)
            WHERE rt.temp_sqrt_sum <> 0 ; """)
    
    #print(get_output("""SELECT * FROM temp_rr ORDER BY user_1,user_2 LIMIT 30;"""))
    
    get_output("""CREATE TABLE my_user_similarity AS
                SELECT * FROM temp_rr;""")




    # 유사도 연산을 직접 구현하여 my_user_similarity 테이블에 저장하세요.
    df = get_output("SELECT * FROM my_user_similarity")
    # 최종 결과 얻은 뒤, 중간 계산 중 만든 table 삭제
    get_output("DROP TABLE IF EXISTS temp_rr;")
    get_output("DROP TABLE IF EXISTS temp_sqrt;")
    get_output("DROP TABLE IF EXISTS temp_rating;")
    get_output("""ALTER TABLE temp_rr DROP COLUMN cor_similarity;""")

    # TODO end

    # Do not change this part
    tab = tabulate(df, headers=df.columns, tablefmt="psql", showindex=False)
    # do not print since it is too large
    print(tab)
    with open("user_similarity.txt", "w") as f:
        f.write(tab)
    print("Output printed in user_similarity.txt")


## 수정할 필요 없는 함수입니다.
# Print and execute menu
def menu():
    print("=" * 99)
    print("0. Initialize")
    print("1. Popularity Count-based Recommendation")
    print("2. Popularity Rating-based Recommendation")
    print("3. User-based Collaborative Filtering")
    print("4. User similarity (Optional)")
    print("5. Connector example")
    print("6. Exit database")
    print("=" * 99)

    while True:
        m = int(input("Select your action : "))
        if m < 0 or m > 6:
            print("Wrong input. Enter again.")
        else:
            return m


def execute():
    terminated = False
    while not terminated:
        m = menu()
        if m == 0:
            # 수정할 필요 없는 함수입니다.
            # Upload prj.sql before this
            # If autocommit=False, always execute after making cursor
            try:
                file_path = os.path.join(BASE_DIR, 'prj.sql')
                get_dump(connection, file_path)
                print("Database initialized successfully.")
            except:
                print("Error initializing database.")
        elif m == 1:
            popularity_based_count()
        elif m == 2:
            popularity_based_rating()
        elif m == 3:
            ubcf()
        elif m == 4:
            user_similarity()
        elif m == 5:
            # 수정할 필요 없는 함수입니다.
            # mysql connector 사용 방법 예시입니다.
            connector_example()
        elif m == 6:
            terminated = True


def connector_example():
    print("Connector example")
    print("=" * 99)
    rat_num = int(input("Number of rows in ratings?: "))
    sim_num = int(input("Number of rows in similarity?: "))

    query = f"SELECT * FROM ratings LIMIT {rat_num}"
    df = get_output(query)
    tab = tabulate(df, headers=df.columns, tablefmt="psql", showindex=False)
    print(tab)

    query = f"SELECT * FROM user_similarity LIMIT {sim_num}"
    df = get_output(query)
    tab = tabulate(df, headers=df.columns, tablefmt="psql", showindex=False)
    print(tab)

    query = "DROP TABLE IF EXISTS test;"
    df = get_output(query)

    query = "CREATE TABLE test AS SELECT * FROM ratings LIMIT 5;"
    df = get_output(query)

    query = "SELECT * FROM test;"
    df = get_output(query)
    tab = tabulate(df, headers=df.columns, tablefmt="psql", showindex=False)
    print(tab)

    query = "DROP TABLE test;"
    df = get_output(query)


# DO NOT CHANGE
if __name__ == "__main__":
    #execute()
    #ubcf()
    user_similarity()