# -*- coding: utf-8 -*-
"""

	###################################### Asset configuration. ######################################


"""
config = {}


# Installed Assets
config['apptools.project.assets'] = {

	'debug': False, ## Output log messages about what's going on.
	'verbose': False, ## Raise debug-level messages to 'info'.

	# JavaScript Libraries & Includes
	'js': {


		### Core Dependencies ###
		('core', 'core'): {

			'config': {
				'version_mode': 'getvar',
				'bundle': 'dependencies.bundle.min.js'
			},
			
			'assets': {
				'backbone': {'min': True, 'version': '0.5.1'}, # Backbone.JS - site MVC core
				'amplify': {'min': True, 'version': '1.0.0'}, # AmplifyJS - for request, local storage + pubsub management
				'modernizr': {'min': True, 'version': '2.0'}, # Modernizr - browser polyfill + compatibility testing
				'lawnchair': {'version': '0.6.3'}, # Lawnchair: Client-side persistent storage
			}
		
		},
		
		### FatCatMap Platform Scripts ###
		('apptools', 'apptools'): {

			'config': {
				'version_mode': 'getvar',
				'bundle': 'core.bundle.min.js'
			},

			'assets': {
				'base': {'min': True, 'version': 0.1}, # milk (mustasche for coffee), _underscore, _root
				'rpc': {'min': True, 'version': 0.1}, # rpc framework, rpc caching
				'storage': {'min': True, 'version': 0.1}, # local storage adapter
			}
	
		},
		
		### Browser feature Polyfills ###
		('polyfills', 'core/polyfills'): { 

			'config': {
				'version_mode': 'getvar',
				'bundle': 'polyfills.bundle.min.js'
			},
			
			'assets': {
				'json2': {'min': True}, # Adds JSON support to old IE and others that don't natively support it
				'history': {'min': True}, # Adds support for history management to old browsers
				'rgbcolor': {'min': True}, # Adds support for RGB color for CanVG
				'canvg': {'min': True} # Renders SVG over canvas (good for &droid)
			}

		},
		
		### jQuery Core & Plugins ###
		('jquery', 'jquery'): { 
		
			'config': {
				'version_mode': 'getvar',				
				'bundle': 'jquery.bundle.min.js'
			},
			
			'assets': {
				'core': {'name': 'jquery', 'min': True, 'version': '1.6.1'}, # jQuery Core
				'easing': {'path': 'interaction/easing.min.js'}, # Easing transitions for smoother animations
				'mousewheel': {'path': 'interaction/mousewheel.min.js'} # jQuery plugin for mousewheel events + interactions
			}
			
		},
		
		'belated_png': {'path': 'util/dd_belatedpng.js'} # Belated PNG fix
	
	},


	# Cascading Style Sheets
	'style': {
		
		# Compiled (SASS) FCM Stylesheets
		('compiled', 'compiled'): {
		
			'config': {
				'min': True,
				'version_mode': 'getvar'
			},
		
			'assets': {
				'main': {'version': 0.1}, # reset, main, layout, forms
				'ie': {'version': 0.1}, # fixes for internet explorer (grrr...)
				'print': {'version': 0.1} # proper format for printing
			}
		
		},
		
		# Content-section specific stylesheets
		('site', 'compiled/site'): {
		
			'config': {
				'min': True,
				'version_mode': 'getvar'
			},
			
			'assets': {
			}
		
		},
			
	},

	
	# Other Assets
	'ext': {
	 },
	
}