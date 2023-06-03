import os
import csv
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings(action="ignore")

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rc


def get_mysql_connection(host, user, password, database):
    import mysql.connector

    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
    )
    return mydb


def execute_database(query):
    result = pd.read_sql(con=mydb, sql=query)
    return result


def preprocessing_index(df):
    # 지역명 중복 방지
    df["local"] = df["Region"] + "_" + df["Local_government"]
    # 날짜 인덱스 만들기
    df["date"] = df["Year"].astype(str).str.cat(df["Month"].astype(str), sep="-")
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m")
    df = df.set_index("date")
    return df


def make_pivot(df, columns, values):
    result_df = df.pivot_table(index=["local", "date"], columns=columns, values=values)
    return result_df
