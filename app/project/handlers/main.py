from project.handlers import WebHandler


class Landing(WebHandler):
	
	''' Returns the age-old, enigmatic success response. '''
	
	def get(self):
		self.render('main/helloworld.html')