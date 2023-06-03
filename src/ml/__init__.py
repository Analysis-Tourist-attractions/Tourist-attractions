from utils import *

__HOST__ = "host"
__USER__ = "user"
__PASSWORD__ = "pw"
__DB__ = "DB"

mydb = get_mysql_connection(__HOST__, __USER__, __PASSWORD__, __DB__)

spend = execute_database("SELECT * FROM Expenditure")
search = execute_database("SELECT * FROM Search")
distance = execute_database("SELECT * FROM Distance")

spend_pv = make_pivot(spend, "Expenditure","Expenditure")
search_pv = make_pivot(search, "Search_count","Search_count")
dis_pv = make_pivot(distance, "Distance","Visitor_count")
dis_pv = dis_pv.fillna(0)

# 최종 사용 데이터
df = pd.concat([dis_pv,search_pv,spend_pv],axis=1)
X = df.drop(['Expenditure'],axis=1)
y = df[['Expenditure']]