import configparser

config = configparser.ConfigParser()
config.read("config.ini")
sec = config.sections()
print(sec[0])
