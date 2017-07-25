from database import DatabaseArchiver
from database import HTTPArchiver
from algorithm import power_management
from input import read_file
from save_output_txt import write_to_txt
from input_charts import input_charts
from config import read_config
import sys

content = sys.stdin.readlines()
data = read_file(content)
output = power_management(data)
config = read_config()

if config[6] == 0:
    archiver = DatabaseArchiver('/tmp/BTS.db')
else:
    archiver = HTTPArchiver('http://localhost:5000')

for item in data:
    archiver.save_measurement(item)

for item in output:
    archiver.save_response(item)

archiver.flush()

write_to_txt(output)
input_charts(data)
