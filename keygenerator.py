
file_name = 'keyfile'

class KeyGenerator():
#TODO:Add error handling for malformed file
#	* Make prvate?
#	* Return empty list instead of raise?
#	* Duplicate functionality of read() in TaskFileStorage?
	def read(self):
		key_file = open(file_name, 'r')
		try:
			key = int(key_file.read())
		except (EOFError, IOError, ValueError):
			raise
		
		return key
	
	def write(self, key):
		key_file = open(file_name, 'w')
		key_file.write(str(key))
		key_file.close()
		
	def get_key(self):
		try:
			key = self.read()
		except (EOFError, IOError, ValueError):
			key = 0
			self.write(key)
		
		return key

	def update_key(self):
		key = self.get_key()
		key += 1
		self.write(key)
