import re
import pandas as pd
host_pattern=r'(^\S+\.[\S+\.]+\.\S+)\s'
timestamp_pattern=r'\[(\d{2}\/\w{3}\/\d{4}\:\d{2}\:\d{2}\:\d{2} -\d{4})\]'
request_pattern=r'\"(\S+)\s(\S+)\s*(\S*)\"'
status_pattern=r'\s(\d{3})\s'
length_pattern=r'\s(\d+)$'


n=100
with open("E:\\python_projects\\Springboard\\datasets\\access_log_Aug95.txt","r") as f:
    firstn=[f.readline() for i in range(n)]
data_list=[]

for line in firstn:
    hostname=re.search(host_pattern,line).group(1)
    timestamp=re.search(timestamp_pattern,line).group(1)
    request=re.search(request_pattern,line).group()
    request_method=request.split(" ")[0].replace('"','')
    request_endpoint = request.split(" ")[1]
    request_protocol = request.split(" ")[2].replace('"','')
    status=re.search(status_pattern,line).group(1)
    length = re.search(length_pattern, line).group(1)
    print(line)
    data_list.append({'hostname':hostname,'timestamp':timestamp,'request_method':request_method,'request_endpoint':request_endpoint,'request_protocol':request_protocol,'status':status,'length':length})


df=pd.DataFrame(data_list)
print(df)

