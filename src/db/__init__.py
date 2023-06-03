import utils

mydb = utils.get_mysql_connection(host, user, password, database)
mycursor = mydb.cursor()

# Visitor 테이블 칼럼
visitor_c = [
    "Region",
    "Local_government",
    "Year",
    "Month",
    "Visitor_count",
    "Visitor_ratio",
]

# Expenditure 테이블 칼럼
expenditure_c = [
    "Region",
    "Local_government",
    "Year",
    "Month",
    "Expenditure",
    "Expenditure_ratio",
]

# Search 테이블 칼럼
search_c = [
    "Region",
    "Local_government",
    "Category",
    "Year",
    "Month",
    "Search_count",
    "Search_count_ratio",
    "Category_count",
    "Category_count_ratio",
]

# Distance 테이블 칼럼
distance_c = [
    "Region",
    "Local_government",
    "Year",
    "Month",
    "Distance",
    "Visitor_count",
    "Visitor_ratio",
]

# 크롤링 테이블 칼럼
crawl_c = ["Local", "Content"]
