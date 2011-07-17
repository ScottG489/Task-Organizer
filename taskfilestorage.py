import pickle
import task
import re

class TaskFileStorage():
	def add(self, my_task):
#TODO:Auto create ID's
		task_file = open('taskfile', 'a')
		pickle.dump(my_task, task_file, 0)
		task_file.close()
	def find(self, regex):
		task_file = open('taskfile', 'r')
		task_list = []
		while True:
			try:
				task_list.append(pickle.load(task_file))
			except EOFError:
				break
		match_list = []
		for task_item in task_list:
##TODO:Valid the input regular expression here or somewhere
			if re.search(r'' + regex + '', task_item.title):
				match_list.append(task_item)

		return match_list

