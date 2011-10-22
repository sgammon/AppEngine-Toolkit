# -*- coding: utf-8 -*-

## AppTools Imports
from apptools.core import BaseHandler
import logging

class WebHandler(BaseHandler):
	
	''' Handler for desktop web requests. '''
	
	def _bindRuntimeTemplateContext(self, context):
		
		context['page'] = {
		
			'ie': False,
			'mobile': False
		
		}
		
		## Detect if we're handling a request from IE, and if we are, tell the template context
		if self.uagent['browser']['name'] == 'MSIE':
			context['page']['ie'] = True
			
		return context
	
	
class MobileHandler(BaseHandler):
	
	''' Handler for mobile web requests. '''
	
	def _bindRuntimeTemplateContext(self, context):
		
		context['page'] = {
		
			'ie': False,
			'mobile': True
		
		}
		
		return context