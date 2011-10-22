# -*- coding: utf-8 -*-
import os
import sys
import logging

try:
	import json
except ImportError, e:
	try:
		import simplejson as json
	except ImportError, e:
		try:
			from django.utils import simplejson as json
		except ImportError, e:
			logging.critical('Could not find compatible JSON adapter. Imploding.')
			raise
		finally:
			exit()

import bootstrap
bootstrap.AppBootstrapper.prepareImports()

import ndb
import config

## App Engine Imports
import webapp2 as webapp
from protorpc import registry
from protorpc.webapp import forms
from webapp2_extras import protorpc

from google.appengine.ext.webapp import util

from apptools.services import RemoteServiceHandlerFactory

## Get services configuration
services_config = config.config.get('apptools.project.services')


def core_log(message, level='debug'):
	
	""" Outputs properly formatted log messages from this file. """

	logging.info('SERVICES_CORE: '+str(message))
	

def enable_appstats(app):
	
	""" Utility function that enables appstats middleware."""
	
	from google.appengine.ext.appstats import recording
	app = recording.appstats_wsgi_middleware(app)
	return app


def enable_apptrace(app):

	""" Utility function that enables apptrace middleware. """

	from apptrace import middleware
	middleware.Config.URL_PATTERNS = ['^/$']
	app.wsgi_app = middleware.apptrace_middleware(app.wsgi_app)
	return app


def generateServiceMappings(svc_cfg, registry_path=forms.DEFAULT_REGISTRY_PATH):
	
	""" Utility function that reads the services config and generates URL mappings to service classes. """
	
	services = []
	
	## Generate service mappings in tuple(<invocation_url>, <classpath>) format
	for service, cfg in svc_cfg['services'].items():
		if cfg['enabled'] == True:
			services.append(('/'.join(svc_cfg['config']['url_prefix'].split('/')+[service]), cfg['service']))
			
	services = protorpc._normalize_services(services)
	mapping = []
	registry_map = {}

	if registry_path is not None:
		registry_service = registry.RegistryService.new_factory(registry_map)
		services = list(services) + [(registry_path, registry_service)]
		forms_handler = forms.FormsHandler(registry_path=registry_path)
		mapping.append((registry_path + r'/form(?:/)?', forms_handler))
		mapping.append((registry_path + r'/form/(.+)', forms.ResourceHandler))

	paths = set()
	for path, service in services:
		service_class = getattr(service, 'service_class', service)
		if not path:
			path = '/' + service_class.definition_name().replace('.', '/')

		if path in paths:
			raise service_handlers.ServiceConfigurationError(
				'Path %r is already defined in service mapping'
				% path.encode('utf-8'))
		else:
			paths.add(path)

		# Create service mapping for webapp2.
		new_mapping = RemoteServiceHandlerFactory.default(service).mapping(path)
		mapping.append(new_mapping)

		# Update registry with service class.
		registry_map[path] = service_class

	return mapping
		
		
def enable_jinja2_debugging():

	""" Enables blacklisted modules that help Jinja2 debugging. """

	# Enables better debugging info for errors in Jinja2 templates.
	from google.appengine.tools.dev_appserver import HardenedModulesHook
	HardenedModulesHook._WHITE_LIST_C_MODULES += ['_ctypes', 'gestalt']
				
	
ndb.debug = config.debug ## set NDB to production on production (60% speedup or something like that...)

service_mappings = generateServiceMappings(services_config, '/_registry')
application = webapp.WSGIApplication(service_mappings)


class ServicesDisabledHandler(webapp.RequestHandler):
	
	def get(self):
		
		response = {
		
			'status': 'error',
			'error': {
				'code': 'SERVICES_DISABLED',
				'message': 'API services are currently disabled.'
			}
		
		}
		
		self.response.headers['Content-Type'] = "application/json"
		self.response.out.write(json.dumps(response))
	

def main(environ=None, start_response=None):
	
	global application
	
	if services_config.get('enabled', False) == True:

		if service_mappings is not None:
					
			## Consider services config
			services_cfg = config.config.get('apptools.services')

			if services_cfg.get('hooks', {}).get('appstats', {}).get('enabled', False) == True:
				core_log('AppStats middleware enabled.')
				try:
					application = enable_appstats(application)
				except Exception, e:
					core_log('Error encountered enabling AppStats: '+str(e), 'error')

			if config.debug:

				## Next up - apptrace (Memory footprint tracking)
				if services_cfg.get('hooks', {}).get('apptrace', {}).get('enabled', False) != False:
					core_log('AppTrace middleware enabled.')
					try:
						application = enable_apptrace(application)

					except Exception, e:
						core_log('Error encountered enabling AppTrace: '+str(e), 'error')

				## Execution tree + CPU time tracking
				if services_cfg.get('hooks', {}).get('profiler', {}).get('enabled', False) == True:
					try:
						import cProfile
						core_log('Profiler middleware enabled.')

						def profile_run(app):
							filepath = services_cfg['hooks']['apptrace'].get('filename', "var/export/performance/AppServicesProfile.profile")
							enable_jinja2_debugging()
							core_log('Kickstarting profiler, export target = "%s"' % filepath)
							cProfile.runctx("application.run()", globals(), locals(), filename=filepath)

						action = profile_run ## Set our action to the profiler

					except Exception, e:
						core_log('Error encountered enabling profiler: '+str(e), 'error')
						
				else:
					def run(app):
						logging.debug('Running service subsystem in CGI mode...')
						app.run()
						
					action = run
				
			if environ is not None and start_response is not None:
				def run_wsgi(app, environ, start_response):
					logging.debug('Running service subsystem in WSGI mode...')
					return app(environ, start_response)
					
				return run_wsgi(application, environ, start_response) ## run wsgi
				
			return action(application) ## run CGI

		else:
			print "Content-Type: text/html"
			print ""
			print "API services do not exist for this application."
			return


	else:
		application = webapp.WSGIApplication([webapp.Route('/.*', handler=ServicesDisabledHandler, name='services-disabled')])
		return application.run()


if __name__ == '__main__':
	main()