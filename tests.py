from PrestoLogCollector import Semi_JSON_parse



rec = []
Semi_JSON_parse(rec," [test2] , test1 ")
print(rec)


rec = []
Semi_JSON_parse(rec,"test, [test2] , test1 ")
print(rec)



rec = []
Semi_JSON_parse(rec,"test, 1test1, [2test2,[ 4test4[], 5test5 ], 3test3]")
print(rec)



rec = []
Semi_JSON_parse(rec,"")
print(rec)

rec = []
Semi_JSON_parse(rec,"test")
print(rec)


rec = []
Semi_JSON_parse(rec,"test[],test1")
print(rec)


