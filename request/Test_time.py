import datetime
from time import sleep

JST = datetime.timezone(datetime.timedelta(hours=9), "JST")
start = datetime.datetime.now(JST)
sleep(67)
end = datetime.datetime.now(JST)
ans = end - start
# time = datetime.timedelta(hours=1)
# print(str(time))
print(str(start))
# if ans >= time:
#     print("規定よりたった")