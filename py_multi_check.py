import json
from pyhive import presto
from multiprocessing.dummy import Pool as ThreadPool
import datetime

results_arr = []
query_arr = [
    "select cast(sum(if(substr(msid,1,1) = '1',1,0)) as double)/count(1) as starts_with_1 from events.dbo.sites_29 where date_created between date '2018-05-01' and date '2018-05-02'",
    "select cast(sum(if(substr(msid,1,1) = '2',1,0)) as double)/count(1) as starts_with_1 from events.dbo.sites_29 where date_created between date '2018-05-01' and date '2018-05-02'",
    "select cast(sum(if(substr(msid,1,1) = '3',1,0)) as double)/count(1) as starts_with_1 from events.dbo.sites_29 where date_created between date '2018-05-01' and date '2018-05-02'",
    "select cast(sum(if(substr(msid,1,1) = '4',1,0)) as double)/count(1) as starts_with_1 from events.dbo.sites_29 where date_created between date '2018-05-01' and date '2018-05-02'"
]

def myLog(msg):
    print(str(datetime.datetime.now()) + " : " + msg)

def execute_query(query):
    myLog("Starting")
    cursor = presto.connect('presto.wixpress.com', port=8181).cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    results_arr.append(res)
    myLog(str(res))


def run_test():
    pool = ThreadPool(4)
    results = pool.map(execute_query, query_arr)
    myLog(str(results_arr))

if __name__ == "__main__":
    # execute_query(query_arr[0])
    run_test()