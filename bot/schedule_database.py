from schedule_parser import get_all_schedule
from schedule_pretify import weekly_to_img
import json
import os
from typing import List


def add_schedule_to_db(group: str) -> bool:
	''' Parses group schedule and loads into database 
		Returns True if it was loaded sucessfuly or False '''
	schedule = get_all_schedule(group)
	if schedule is not None:
		with open('schedules/{}.json'.format(group), 'w') as f:
			json.dump(schedule, f, indent=4)
		add_schedule_images(schedule, group)
		return True
	return False

def add_schedule_images(schedule, group: str) -> None:
	''' Adds schedule images of group to database'''
	images = weekly_to_img(schedule, group)
	images[0].save('schedules/images/{}_1.png'.format(group))
	images[1].save('schedules/images/{}_2.png'.format(group))

def get_schedule(group: str) -> List[dict]:
	''' Returns schedule if the group exists or None if it does not exists'''
	exists = os.path.exists('./schedules/{}.json'.format(group))
	if not exists:
		if not add_schedule_to_db(group):
			return None
	with open('schedules/{}.json'.format(group), 'r') as f:
		return json.load(f)

def get_schedule_images(group: str) -> tuple:
	''' Returns schedule images of group if they exist '''
	path = './schedules/images/{}_{}.png'
	exists = os.path.exists(path.format(group, 1))
	if not exists:
		if not add_schedule_to_db(group):
			return None
	img1 = open(path.format(group, 1), 'rb')
	img2 = open(path.format(group, 2), 'rb')
	return (img1, img2)
