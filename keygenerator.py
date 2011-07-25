import os

class KeyGenerator():
	def __init__(self, key_filename='keyfile'):
		self.key_filename = key_filename	# Will hold the ID of the NEXT task

	#TODO:Make private?
	#	* raise more informative messages? (ex. if path exists as a dir)
	def read(self):
		try:
			# Try to open file for reading
			key_file = open(self.key_filename, 'r')
			# Try to read the key
			try:
				key = int(key_file.read())
				key_file.close()
				# Try to validate the read file contents.
				try:
					self.validate(key)
				# If file is not valid; raise
				except TypeError:
					raise
			# If key won't load, check if it's empty
			except:
				# If the file is empty create first key
				if os.stat(self.key_filename).st_size == 0:
					key = 0
				# If also not empty, file is in an unreadable format; raise
				else:
					raise
		# If file won't open for reading, check that it exists as a file
		except:
			# If path doesn't exist as a file, create it and first key
			if not os.path.exists(self.key_filename):
				temp_file_handler = open(self.key_filename, 'w').close()
				key = 0
			# If it also exists then we can't use it; raise.
			else:
				raise


		return key

	#TODO:Make private?
	def write(self, key):
		try:
			# Try to open file for	writing 
			key_file = open(self.key_filename, 'w')
			# Try to read key
			try:
				key = int(key_file.read())
				# Try to validate read key
				try:
					self.validate(key)
				# If file is not valid; raise
				except TypeError:
					raise
				# If the file is valid, write to it
				key_file.write(str(key))
			# If key won't load, check if it's empty
			except:
				# If the file is empty there is nothing to read; write key
				if os.stat(self.key_filename).st_size == 0:
					key_file.write(str(key))
				# If also not empty, file is in an unreadable format; raise
				else:
					raise
		# If file won't open for writing, we can't do anything; raise
		except:
			raise

		key_file.close()
		
	def validate(self, key):
		if key < 0:
			raise TypeError('invalid or corrupt key file')

		return True

	def get(self):
		try:
			key = self.read()
		except:
			raise
		try:
			self.write(key)
		except:
			raise
		
		self.update(key)

		return key

	def update(self, key):
		key += 1
		try:
			self.write(key)
		except:
			raise

		return key
