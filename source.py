from database import DatabaseArchiver
from algorithm import power_management
from input import read_file
from save_output_txt import write_to_txt
from input_charts import input_charts
import sys

#content = sys.stdin.readlines()
content = ""
data = read_file(content)
output = power_management(data)

archiver = DatabaseArchiver('/tmp/BTS.db')
archiver.save_measurement(data)
archiver.save_response(output)
write_to_txt(output)
input_charts(data)
