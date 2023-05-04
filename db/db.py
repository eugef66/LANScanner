#!/usr/bin/env python
from datetime import datetime
import os
import json
from alert import send_down_alert
import config
from utils import get_default_device_name, get_vendor_by_mac


_db=None
_down_devices=[]
_new_devices=[]

def get_device(mac):
	load()
	return _db[mac]

def reset_online_flag():
	load()
	for mac in _db:
		_db[mac]["is_online"]=False
	return

def mac_exists(mac):
	load()
	return mac in _db

def get_alert_down_devices():
	load()
	return dict(filter(lambda device: device[1]["alert_down"]==True,_db.items()))

def is_online(mac):
	load()
	return _db[mac]["is_online"]

def create_device(mac, ip, vendor=None, is_online=None, description=None, alert_down=None, hostname=None, is_new=None):
	load()
	default_device_name = get_default_device_name()

	_db[mac] = {"ip": ip if ":" not in ip else None,
		   "ip6": ip if ":" in ip else None,
		   "is_online": False if is_online == None else is_online,
		   "description": default_device_name if description == None else description,
		   "vendor": get_vendor_by_mac() if vendor == None else vendor,
		   "hostname": default_device_name if hostname == None else hostname,
		   "alert_down": False if alert_down == None else alert_down,
		   "updateTS": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
		   "is_new": True if is_new == None else is_new,
		   }
	return

def update_device(mac, ip, vendor=None, is_online=None, description=None, alert_down=None, hostname=None, is_new=None):
	load()
	_db[mac] = {"ip": ip if ":" not in ip else _db[mac]["ip"],
		   "ip6": ip if ":" in ip else _db[mac]["ip"],
		   "is_online": _db[mac]["is_online"] if is_online == None else is_online,
		   "description": _db[mac]["description"] if description == None else description,
		   "vendor": _db[mac]["vendor"] if vendor == None else vendor,
		   "hostname": _db[mac]["hostname"] if hostname == None else hostname,
		   "alert_down": _db[mac]["alert_down"] if alert_down == None else alert_down,
		   "updateTS": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
		   "is_new": _db[mac]["is_new"] if is_new == None else is_new,
		   }
	return

def load(force_reload=False):
	global _db
	# Check is already loaded
	if (_db != None and force_reload==False):
		return _db

	print("--- loading database ---")
	if (os.path.exists(config.APP_PATH + "/db/db.json")):
		with open(config.APP_PATH + '/db/db.json', 'r') as _db_file:
			_db = json.load(_db_file)
	else:
		_db = {}
		save()
	return


def save():
	load()
	with open(config.APP_PATH + "/db/db.json", "w+") as _db_file:
		_db_file.write(json.dumps(_db, indent=4))
	return

def __init__():
	load()
