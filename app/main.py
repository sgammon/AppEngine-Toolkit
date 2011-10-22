# -*- coding: utf-8 -*-

""" main.py - everything starts here. """

import os
import sys

import bootstrap
bootstrap.AppBootstrapper.prepareImports()

import ndb
import config
import logging
import webapp2

from urls import get_rules

rules = get_rules()
	

def enable_appstats(app):
	
	""" Utility function that enables appstats middleware."""
	
	from google.appengine.ext.appstats.recording import appstats_wsgi_middleware
	app.app = appstats_wsgi_middleware(app.app)
	return app
	
	
def enable_apptrace(app):
	
	""" Utility function that enables apptrace middleware. """
	
	from apptrace import middleware
	middleware.Config.URL_PATTERNS = ['^/$']
	app.app = middleware.apptrace_middleware(app.app)
	return app
	

def enable_jinja2_debugging():

	""" Enables blacklisted modules that help Jinja2 debugging. """

	# Enables better debugging info for errors in Jinja2 templates.
	from google.appengine.tools.dev_appserver import HardenedModulesHook
	HardenedModulesHook._WHITE_LIST_C_MODULES += ['_ctypes', 'gestalt']
	
	
def run(app):

	""" Default run case - no profiler, via CGI. """
	
	app.run()
	
	
def run_wsgi(app, environ, start_response):
	
	""" Run in WSGI mode with the Python 2.7 runtime. """
	
	return app(environ, start_response)
	
	
def enable_filesystem_wb():
	from google.appengine.tools.dev_appserver import FakeFile
	FakeFile.ALLOWED_MODES = frozenset(['a','r', 'w', 'rb', 'U', 'rU', 'wb'])
	return


def main(environ=None, start_response=None):

	""" INCEPTION! :) """

	global run
	global rules
	
	if environ is not None and start_response is not None:
		logging.info('Running in WSGI mode... :)')
		action = run_wsgi
	else:
		action = run
	
	if config.debug:
		rules = get_rules()
		
	## Grab debug and system config
	debug = config.debug
	ndb.debug = debug
	sys_config = config.config.get('apptools.system')
	
	## Create the app, get it ready for middleware
	app = webapp2.WSGIApplication(rules, debug=debug, config=config.config)

	try:
		## If we're in debug mode, automatically activate some stuff
		if debug:
			logging.info('CORE: Jinja2 debugging enabled.')
			enable_jinja2_debugging()
			enable_filesystem_wb()

		## Consider system hooks
		if sys_config.get('hooks', False) != False:
		
			## First up - appstats (RPC tracking)
			if sys_config['hooks'].get('appstats', False) != False:
				if sys_config['hooks']['appstats']['enabled'] == True:
					logging.info('CORE: AppStats enabled.')		
					app = enable_appstats(app)
				
			## Next up - apptrace (Memory footprint tracking)
			if sys_config['hooks'].get('apptrace', False) != False:
				if sys_config['hooks']['apptrace']['enabled'] == True:
					logging.info('CORE: AppTrace enabled.')
					app = enable_apptrace(app)

			## Execution tree + CPU time tracking
			if sys_config['hooks']['profiler']['enabled'] == True:
				import cProfile
				def profile_run(app):
					logging.info('CORE: Profiling enabled.')
					enable_jinja2_debugging()
					dump_path = '/'.join(os.path.realpath(__file__).split('/')[0:-1]+['FatCatMap.profile'])
					cProfile.runctx("run(app)", globals(), locals(), filename=dump_path)
				action = profile_run ## Set our action to the profiler

	except Exception, e:
		logging.critical('CORE: CRITICAL FAILURE: Unhandled exception in main: "'+str(e)+'".')
		if config.debug:
			raise
	
	else:
		if environ is not None and start_response is not None:
			return action(app, environ, start_response) ## run in wsgi mode
		else:
			return action(app) ## run in cgi mode


def services(environ=None, start_response=None):
	import services as APIServices	
	return APIServices.main(environ, start_response)

def pipelines(environ=None, start_response=None):
	from pipeline.handlers import _APP as PipelinesApp	
	return PipelinesApp(environ, start_response)
	
def warmup(environ=None, start_response=None):
	from warmup import Warmup as WarmupApp
	return WarmupApp(environ, start_response)
	
def backend(environ=None, start_response=None):
	logging.info('==== BACKEND STARTING ====')
	return warmup(environ, start_response)

if __name__ == '__main__':
	main()