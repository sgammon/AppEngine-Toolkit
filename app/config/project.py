# -*- coding: utf-8 -*-
""" 

	######################################## AppTools Project configuration. ########################################

"""
config = {}


## App settings
config['apptools.project'] = {

	'name': 'AppTools',

	'version': {
		'major': 1,
		'minor': 0,
		'micro': 0,
		'build': 20111009,
		'release': 'BETA'
	}

}

## Development/debug settings
config['apptools.project.dev'] = {

}

## Output layer settings
config['apptools.project.output'] = { 

	# Output Configuration

	'minify': False, ## whether to minify page output or not
	'optimize': True, ## whether to use the async script loader or not
	'standalone': False, ## whether to render only the current template, or the whole context (ignores "extends")

	'appcache': { ## HTML5 appcaching
		'enable': False, ## whether to enable
		'manifest': 'scaffolding-v1.appcache' ## manifest to link to
	},

	'assets':{
		'minified': False, ## whether to switch to minified assets or not
		'serving_mode': 'local', ## 'local' or 'cdn' (CDN prefixes all assets with an absolute URL)
		'cdn_prefix': [] ## CDN prefix/prefixes - a string is used globally, a list of hostnames is selected from randomly for each asset
	}

}

## Caching
config['apptools.project.cache'] = {

	# Caching Configuration

	'key_seperator': '::',
	'prefix': 'dev',
	'prefix_mode': 'explicit',
	'prefix_namespace': False,
	'namespace_seperator': '::',
	
	'adapters': {

		# Instance Memory
		'fastcache': {

			'default_ttl': 600
	
		},
		
		# Memcache API
		'memcache': {

			'default_ttl': 10800
		
		}, 
		
		# Backend Instance Memory
		'backend': {

			'default_ttl': 10800

		},
		
		# Datastore Caching
		'datastore': {

			'default_ttl': 86400
		
		}
			
	}

}

config['apptools.project.output.template_loader'] = {

	# Template Loader Config

	'force': True, ## Force enable template loader even on Dev server
	'debug': False,  ## Enable dev logging
	'use_memory_cache': False, ## Use handler in-memory cache for template source
	'use_memcache': False, ## Use Memcache API for template source

}

# Pipelines Configuration
config['apptools.project.pipelines'] = {

    'debug': False, # Enable basic serverlogs
	'logging': {
	
		'enable': False, # Enable the pipeline logging subsystem
		'mode': 'serverlogs', # 'serverlogs', 'xmpp' or 'channel'
		'channel': '', # Default channel to send to (admin channels are their email addresses, this can be overridden on a per-pipeline basis in the dev console)
		'jid': '', # Default XMPP JID to send to (this can be overridden on a per-pipeline basis in the dev console)
	
	}

}