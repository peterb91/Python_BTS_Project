from database import DatabaseArchiver
from algorithm import power_management
from input import read_file
import sys

content = sys.stdin.readlines()

archiver = DatabaseArchiver('/tmp/BTS.db')
archiver.save_response(power_management())
archiver.save_measurement(read_file())

