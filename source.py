from database import DatabaseArchiver
from algorithm import power_management
from input import read_file
import sys

content = sys.stdin.readlines()
data = read_file(content)

archiver = DatabaseArchiver('/tmp/BTS.db')
archiver.save_measurement(data)
archiver.save_response(power_management(data))

