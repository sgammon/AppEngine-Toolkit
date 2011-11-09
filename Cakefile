fs = require 'fs'
path = require 'path'
util = require 'util'
wrench = require 'wrench'
{exec, spawn} = require 'child_process'

defaults =
	
	output: '~/WorkspaceTest'
	colorize: true
	compass: true
	coffee: false
	python: '/usr/bin/python2.7' ## python interpreter to use for buildout/bootstrap	
	skeleton: 'py27-base' ## skeleton we're using (this should be the name of a branch available at gitsource.skeleton...)
	gitsource:
		apptools: 'git@github.com:sgammon/apptools.git' ## the core apptools library, with webapp/protorpc/ndb abstractions + utils
		toolkit: 'git@github.com:sgammon/AppEngine-Toolkit.git' ## the whole and complete toolkit, with tools for project management + workflow
		skeleton: 'git@github.com:sgammon/AppEngine-Toolkit-Skeleton.git' ## the app skeleton (the stuff that's actually deployed to GAE)

out =

	flags:
		header: '\033[95m'
		blue: '\033[94m'
		green: '\033[92m'
		yellow: '\033[93m'
		red: '\033[91m'
		end: '\033[0m'
	
		wrap: (message, flag) ->
			return flag+message+@end

	whisper: (message) ->
		if message?
			console.log message.toString().replace('\n', "")

	say: (module, message) ->
		if message?
			console.log '['+@flags.wrap(module.toString(), @flags.blue)+']: '+message.toString()
		else
			console.log module.toString()

	shout: (module, message, loud=false) ->
		if loud
			console.log ''
			console.log @flags.wrap('[############### ===== '+message.toString()+' ===== ###############]', @flags.yellow)
			console.log ''
		else
			console.log '['+@flags.wrap(module.toString(), @flags.blue)+']: '+@flags.wrap(message.toString(), @flags.green)
			console.log ''
		
	error: (module, message, warning=true) ->
		console.log ''
		if warning
			console.log out.flags.wrap '[############### WARNING: '+module.toString()+' ###############]', out.flags.red
			console.log message.toString()
		else
			console.log out.flags.wrap('[############### ERROR: '+module.toString()+' ###############]', out.flags.red)
			console.log message.toString()
		console.log ''
		
	spawn: (name, command, flags, callback, stdout=false, stderr=false) ->

		if not command?
			command = name
		else
			if typeof command == 'function'
				callback = command
				command = name	

		if not flags?
			flags = []
		else
			if typeof flags == 'function'
				callback = flags
				flags = []

		op = spawn command, flags || []

		if stderr
			op.stderr.on 'data', stderr
		else
			op.stderr.on 'data', (data) =>
				out.error name, data.toString(), false

		if stdout
			op.stdout.on 'data', stdout
		else
			op.stdout.on 'data', (data) =>
				out.say name, data.toString()

		op.on 'exit', (code) =>
			callback?() if code is 0

	exec: (command, callback) ->
		return exec command, (error, stdout, stderr) =>
			if error is null
				callback?(stdout)
			else
				@error('execute', 'Problem encountered executing the command: "'+command+'". Error details: '+error)
	
	
## Script Options
option 'v', '--verbose', 'be loud about what\'s going on'
option 'f', '--force', 'force dangerous operations to succeed'
option 'c', '--config [STR]', 'path to project feature/skeleton config (defaults to \''+defaults.config+'\')'
option 's', '--skeleton [STR]', 'different skeleton branch to install (defaults to \'py27-base\')'
option 'cm', '--compass', 'enable compass support, if it\'s set to off by default'
option 'cs', '--coffee', 'enable coffeescript support, if it\'s set to off by default'


######### =======  Project Tools  ========== #########	
task 'init', 'start a new project and run the dev server', (options) =>

	out.shout 'install', 'Starting Project Init', true
	
	out.say 'install', 'Downloading project scaffolding...'
	invoke 'scaffold'


task 'make', 'download dependencies and prepare dev environment', (options) ->

	out.shout 'make', 'Starting Envrionment Setup'

	out.say 'install', 'Running bootstrap...'
	invoke 'project:bootstrap'
	
	out.say 'install', 'Updating GAE libs...'
	invoke 'clean:gaelibs'
	invoke 'update:gaelibs'
	out.shout 'install', 'GAE libs updated.'
	
	out.say 'install', 'Installing apptools...'
	invoke 'update:apptools'
	out.shout 'install', 'AppTools udpated.'

	out.say 'make', 'Running buildout...'
	invoke 'project:buildout'
	
	out.say 'make', 'Compiling SASS...'
	invoke 'compile:sass'
	
	out.say 'make', 'Compiling CoffeeScript...'
	invoke 'compile:coffee'

	out.shout 'make', 'Environment setup complete.'


task 'bake', 'compile and minify all js, templates, and coffeescript', (options) ->

	out.shout 'bake', 'Starting Compilation'

	## 1) Compile/minify SASS
	if defaults.compass or options.compass
		out.say 'bake', 'Compiling SASS...'
		invoke 'compile:sass'

		out.say 'bake', 'Minifying SASS...'
		invoke 'minify:sass'

	## 2) Compile/minify Coffee
	if defaults.coffee or options.coffee
		out.say 'bake', 'Compiling CoffeeScript...'
		invoke 'compile:coffee'

		out.say 'bake', 'Minifying CoffeeScript...'
		invoke 'minify:coffee'
	
	## 3) Jinja2 Templates
	out.say 'bake', 'Compiling Jinja2 templates...'
	invoke 'compile:templates'
	

task 'run', 'run fatcatmap\'s local dev server', (options) ->

	devserver_done = (code) =>
		out.shout 'devserver', 'Server exited with code '+code+'.'
		
	compass_done = (code) =>
		out.shout 'compass', 'Compass exited with code '+code+'.'
		
	compass_data = (data) =>
		data = data.toString().split(' ')

		line = []
		for i in data
			if /.css/.test(i.toString())
				line.push(i.toString())
				out.whisper line.join(' ')
				line = []
			else
				line.push(i.toString())
				
	compass_err = (data) =>
		
	devserver_data = (data) =>

		if defaults.colorize and not options.boring
			data = data.toString().split(' ')
			
			go = (chunks, output, flag) =>
				logline = []
				endline = []
				prefixfinish = false	

				## Piece together output logline from split chunks
				for chunk in chunks
					chunk = chunk.toString()
					if chunk in ['DEBUG', 'INFO', 'WARNING']
						if flag isnt null
							logline.push('['+out.flags.wrap(chunk, flag))
						else
							logline.push('['+chunk+']')
					
					else if chunk.length == 10 and chunk.split('-').length == 3
						continue ## filter out today's date... people own clocks
						
					else if chunk.length == 12 and chunk.split(':').length == 3
						continue ## filter out the timestamp for regular log messages
						
					else if /.py:/i.test(chunk) and chunk.split(':').length == 2
						logline.push(out.flags.wrap(chunk, flag).replace(']', '')+']')
						prefixfinish = true
					
					else if chunk in [' ', '', "\n"]
						if prefixfinish
							logline.push(chunk)
						else
							continue ## skip multiple spaces in the prefix
					else
						logline.push(chunk)
				
				## Assemble back into a string and output
				output([logline.join(' '), endline.join(' ')].join(' '))
			
			goerror = (chunks, output) =>
				output 'Runtime Error', chunks.join(' ')
			
			
			switch data[0] ## should be log level severity, for log messages
				when "DEBUG" then go data, out.whisper, out.flags.blue
				when "INFO" then go data, out.whisper, out.flags.green
				when "WARNING" then go data, out.whisper, out.flags.yellow
				when "ERROR" then goerror data, out.error
				when "CRITICAL" then goerror data, out.error
				else out.whisper data
		else
			out.whisper data
					
	devserver_err = (data) =>
		devserver_data data

	out.spawn 'devserver', (options.python || defaults.python), ['tools/bin/dev_appserver', 'app/'], devserver_done, devserver_data, devserver_err
	if options.compass or defaults.compass
		out.say 'compass', 'Compass support enabled. Watching.'
		out.spawn 'compass', 'compass', ['watch'], compass_done, compass_data, compass_err


task 'serve', 'deploy fatcatmap to appengine', (options) ->

	appcfg_done = (code) =>
		out.shout 'serve', 'Appcfg exited with code '+code+'.'
		
	appcfg_data = (data) =>
		out.whisper data
	
	appcfg_err = (data) =>
		out.whisper data

	invoke 'compile:sass'
	invoke 'compile:coffee'
	invoke 'compile:templates'
	
	invoke 'minify:sass'
	invoke 'minify:coffee'
	
	out.spawn 'appcfg', 'tools/bin/appcfg', ['upload', 'app'], appcfg_done, appcfg_data, appcfg_err
	

task 'clean', 'remove managed libraries (ndb, mapreduce, pipeline, everything in lib/dist), delete cached files (*.py[c|o], sass-cache, etc)', (option) ->
	
	out.say 'clean', 'Cleaning libraries...'
	
	invoke 'clean:gaelibs'
	invoke 'clean:distlibs'
	invoke 'clean:templates'
	invoke 'clean:apptools'


task 'scaffold', 'download a skeleton from git and install it', (options) =>
	
	## 1: Copy skeleton over first
	skeleton_dir = __dirname+'/app'	
	out.say 'skeleton', 'Cloning project skeleton...'
	out.say 'skeleton', 'Target directory: "'+skeleton_dir+'".'
	
	gitfinish = () =>
		wrench.chmodSyncRecursive(skeleton_dir, 0755);
		out.say 'install', 'Installation complete at: app/'
		out.shout 'skeleton', 'Finished skeleton installation.'

		invoke 'update:gaelibs'
		invoke 'update:apptools'
		invoke 'project:bootstrap'
	
	gitdata = (data) =>
	giterr = (data) =>
	
	gitclone = out.spawn 'gitclone', 'git', ['clone', '-b', options.skeleton || defaults.skeleton, defaults.gitsource.skeleton, './app'], gitfinish, gitdata, giterr
	
	gitclone.on 'exit', (code) =>
		if code == 128
			out.error 'skeleton', 'The app/ directory already exists and is not empty. Please remove the directory if you wish to clone a new skeleton.'
		else
			out.shout 'skeleton:gitclone', 'Gitclone complete. Exited with code '+code+'.'
			

######## =======  Project Tools  ========== ########
task 'project:bootstrap', 'generate a buildout executable', (options) =>

	bootstrap_done = () =>
		out.say 'bootstrap', out.flags.wrap('Bootstrap complete.', out.flags.green)+' From now on, you can use `'+out.flags.wrap('cake make', out.flags.green)+'` to update dependencies.'
		out.say 'bootstrap', 'Kicking off first buildout...'
		invoke 'project:buildout'
		
	bootstrap_data = (data) =>
		out.whisper data
		
	bootstrap_err = (data) =>
		out.error 'bootstrap', data

	## Run bootstrap
	out.say 'bootstrap', 'Executing bootstrap...'
	out.spawn 'bootstrap', options.python || defaults.python, [__dirname+'/tools/bootstrap.py', '-c', __dirname+'/buildout.cfg', '--eggs', __dirname+'/var/eggs'], bootstrap_done, bootstrap_data, bootstrap_err


task 'project:buildout', 'download and install GAE environment, supporting libraries, etc', (options) =>

	buildout_done = (code) =>
		out.shout 'buildout', 'Buildout complete. Exited with code '+code+'.'
		
	buildout_data = (data) =>
		out.whisper data
		
	buildout_err = (data) =>
		out.error 'Buildout Error', data

	out.spawn 'buildout', options.python || defaults.python, [__dirname+'/tools/bin/buildout', '-c', __dirname+'/buildout.cfg'], buildout_done, buildout_data, buildout_err


######## =======  Libraries  ========== ########
task 'update:gaelibs', 'download and install GAE libraries, directly from source control (ndb, pipelines, mapreduce & protorpc)', (options) ->

	update_say = (data) =>
		out.whisper data
	update_err = (data) =>
		out.error 'Update Error', data, false
	
	out.shout 'update', 'Updating GAE libs...', true
	
	out.say 'update', 'Updating NDB...'
	out.spawn('ndbclone', 'hg', ['clone', 'https://appengine-ndb-experiment.googlecode.com/hg/', __dirname+'/var/parts/ndb'], (code) =>
		
		out.say 'update:ndb', 'Download complete. Copying NDB to project.'
		
		wrench.copyDirSyncRecursive __dirname+'/var/parts/ndb/ndb', __dirname+'/app/ndb'
		
		out.shout 'update:ndb', 'NDB update complete.'
		
				
		out.say 'update', 'Updating Map/Reduce...'
		
		out.spawn('mrclone', 'svn', ['checkout', 'http://appengine-mapreduce.googlecode.com/svn/trunk/python/src', __dirname+'/var/parts/mapreduce', '--force'], (code) =>

			## Copy to project
			out.say 'update:mapreduce', 'Download complete. Copying Map/Reduce to project.'
			wrench.copyDirSyncRecursive __dirname+'/var/parts/mapreduce/mapreduce', __dirname+'/app/mapreduce'

			out.shout 'update:mapreduce', 'Map/Reduce update complete.'

			out.say 'update', 'Updating Pipelines...'
			out.spawn('pipelineclone', 'svn', ['checkout', 'http://appengine-pipeline.googlecode.com/svn/trunk/src', __dirname+'/var/parts/pipelines', '--force'], (code) =>
				
				## Copy to project
				out.say 'update:pipelines', 'Download complete. Copying Pipelines to project.'
				wrench.copyDirSyncRecursive __dirname+'/var/parts/pipelines/pipeline', __dirname+'/app/pipeline'
				
				out.shout 'update:pipelines', 'Pipelines update complete.'
				
				
				out.say 'update', 'Cleaning downloaded update parts...'
				wrench.rmdirSyncRecursive __dirname+'/var/parts/ndb'
				wrench.rmdirSyncRecursive __dirname+'/var/parts/mapreduce'
				wrench.rmdirSyncRecursive __dirname+'/var/parts/pipelines'
				
				out.shout 'update', 'Update complete.', true
				
				
			, update_say, update_err)
		, update_say, update_err)
	, update_say, update_err)
	

task 'update:apptools', 'download and install apptools library', (options) ->

	## 1: Copy skeleton over first
	apptools_dir = __dirname+'/app/lib/apptools'
	out.say 'apptools', 'Cloning apptools from git...'
	out.say 'apptools', 'Target directory: "'+apptools_dir+'".'

	gitfinish = () =>
		wrench.chmodSyncRecursive(apptools_dir, 0755);
		out.say 'apptools', 'Apptools installation complete at: app/lib/apptools'
		out.shout 'apptools', 'Finished skeleton installation.'

	gitdata = (data) =>
		out.whisper data
	
	giterr = (data) =>
		out.whisper data

	gitclone = out.spawn 'gitclone', 'git', ['clone' , defaults.gitsource.apptools, './app/lib/apptools'], gitfinish, gitdata, giterr

	gitclone.on 'exit', (code) =>
		if code == 128
			out.error 'apptools', 'The app/lib/apptools directory already exists and is not empty. Please remove the directory if you wish to clone a new copy of the apptools core library.'
		else
			out.shout 'apptools:gitclone', 'Gitclone complete. Exited with code '+code+'.'
	


## Clean Tasks
task 'clean:gaelibs', 'clean GAE libraries (ndb, pipelines, mapreduce & protorpc)', (options) ->

	out.shout 'clean', 'Cleaning GAE libs...', true

	libs =
		ndb: 'NDB'
		mapreduce: 'Map/Reduce'
		pipeline: 'Pipelines'
		
	gaelibs_dir = __dirname+'/app'
	
	for lib of libs
		
		out.say 'clean', 'Cleaning '+libs[lib]+'...'
		
		lib_dir = gaelibs_dir+'/'+lib
		
		try
			sk = fs.readdirSync lib_dir
			for file in sk
				if file != 'README.md'
					try
						fs.unlinkSync lib_dir+'/'+file
						out.say 'clean', 'Removed file "'+lib_dir+'/'+file+'".' if options.verbose

					catch error
						try
							wrench.rmdirSyncRecursive lib_dir+'/'+file, (status) =>
							out.say 'clean', 'Removed folder "'+lib_dir+'/'+file+'".' if options.verbose
						catch error
							throw error

		catch error
			wrench.mkdirSyncRecursive lib_dir, 0777
			out.say 'clean', 'Library "'+libs[lib]+'" not found. Creating empty lib directory.'
			continue
	
	out.shout 'clean', 'GAE libs cleaned.'
	

task 'clean:distlibs', 'clean buildout-managed libs from lib/dist', (options) ->

	out.shout 'clean', 'Cleaning distlibs.', true
	
	out.say 'clean', 'Removing lib/dist...'
	try
		wrench.rmdirSyncRecursive __dirname+'/app/lib/dist'	
		out.say 'clean', 'Creating empty lib/dist...'
		wrench.mkdirSyncRecursive __dirname+'/app/lib/dist'		
	catch error
		out.say 'clean', 'Clean error: '+error
		out.error 'clean', 'There was an error removing the current lib/dist. It probably doesn\'t exist.'
	
	out.shout 'clean', 'Distlib clean finished.'


task 'clean:apptools', 'clean the currently installed version of the apptools library', (options) ->
	
	out.shout 'clean', 'Cleaning AppTools...', true
	
	out.say 'clean', 'Removing lib/apptools...'
	try
		wrench.rmdirSyncRecursive __dirname+'/app/lib/apptools'
	catch error
		out.say 'clean', 'Clean error: '+error
		out.error 'clean', 'There was an error removing the current lib/apptools. It probably doesn\'t exist.'
		
	out.shout 'clean', 'AppTools clean complete.'


task 'clean:templates', 'clean compiled templates from app/templates/compiled', (options) ->

	out.shout 'clean', 'Cleaning compiled templates.', true
	
	out.say 'clean', 'Removing app/templates/compiled...'
	try
		sk = fs.readdirSync __dirname+'/app/templates/compiled'
		for file in sk
			out.say 'clean', 'Cleaning ...compiled/'+file
			try		
				wrench.rmdirSyncRecursive __dirname+'/app/templates/compiled/'+file
			catch error
				try
					fs.unlinkSync __dirname+'/app/templates/compiled/'+file
				catch error
					out.say 'clean', 'Clean error: '+error
					out.error 'clean', 'There was an error removing: '+file
				
	catch error
		out.say 'clean', 'Clean error: '+error
		out.error 'clean', 'There was an error removing the current app/templates/compiled. It probably doesn\'t exist.'
		
	out.shout 'clean', 'Template clean finished.'


######## =======  Stylesheets/SASS & CoffeeScript  ========== ########
task 'compile:sass', 'compile SASS to CSS', (options) ->

	out.shout 'compass', 'Compiling SASS', true
	out.say 'compass', 'Compiling SASS to CSS...'
	
	compass_done = (code) =>
		out.shout 'compass', 'SASS compilation complete.'
		
	compass_data = (data) =>
		data = data.toString().split(' ')
		
		line = []
		for i in data
			if /.css/.test(i.toString())
				line.push(i.toString())
				out.whisper line.join(' ')
				line = []
			else
				line.push(i.toString())
		
	compass_err = (data) =>
	
	out.spawn 'sass2css', 'compass', ['compile', '--force'], compass_done, compass_data, compass_err
	

task 'compile:coffee', 'compile js codebase', (options) ->
	
	total_ops = 0
	total_done = 0
	coffee_done = (code) =>
		total_done = total_done + 1
		if total_done == total_ops
			out.shout 'coffee', 'CoffeeScript compilation complete.'

	coffee_data = (data) =>
		out.whisper data
		
	coffee_err = (data) =>
		out.whisper data
	
	out.shout 'coffee', 'Compiling CoffeeScript...', true
	out.say 'coffee', 'Compiling AppTools base...'

	total_ops = total_ops + 1
	out.spawn 'coffee', 'coffee', [ '--join', __dirname+'/app/assets/js/static/apptools/base.js',
									'--compile', __dirname+'/app/assets/js/source/apptools/_core.coffee',
									__dirname+'/app/assets/js/source/apptools/agent.coffee',
									__dirname+'/app/assets/js/source/apptools/events.coffee',
									__dirname+'/app/assets/js/source/apptools/storage.coffee',
									__dirname+'/app/assets/js/source/apptools/rpc.coffee',
									__dirname+'/app/assets/js/source/apptools/user.coffee',
									__dirname+'/app/assets/js/source/apptools/_init.coffee'], coffee_done, coffee_data, coffee_err
									
												
	## ADD YER COFFEESCRIPTS HERE
	

task 'minify:sass', 'minify SASS into production-ready CSS', (options) ->

	out.shout 'compass', 'Minifying CSS...', true
	out.say 'compass', 'Recompiling SASS...'

	compass_done = (code) =>
		out.shout 'compass', 'CSS minification complete.'
		
	compass_data = (data) =>
		data = data.toString().split(' ')
		
		line = []
		for i in data
			if /.css/.test(i.toString())
				line.push(i.toString())
				out.whisper line.join(' ')
				line = []
			else
				line.push(i.toString())
		
	compass_err = (data) =>
	
	out.spawn 'sass2css', 'compass', ['compile', '--force', '--config', 'tools/config/compass_production.rb'], compass_done, compass_data, compass_err
	

task 'minify:coffee', 'minify js codebase', (options) ->

	total_ops = 0
	total_done = 0
	minify_done = (code) =>
		total_done = total_done + 1
		if total_done == total_ops
			out.shout 'uglifyjs', 'JS minification complete.'
	
	minify_data = (data) =>
		out.whisper data
	
	minify_err = (data) =>
		coffee_data(data)

	out.shout 'uglifyjs', 'Minifying JS...', true

	files_to_minify = [
	
		["AppTools Base", __dirname+'/app/assets/js/static/apptools/base.min.js', __dirname+'/app/assets/js/static/apptools/base.js'],
		["AppTools RPC", __dirname+'/app/assets/js/static/apptools/rpc.min.js', __dirname+'/app/assets/js/static/apptools/rpc.js'],
		["AmplifyJS", __dirname+'/app/assets/js/static/core/amplify.min.js', __dirname+'/app/assets/js/static/core/amplify.js'],
		["BackboneJS", __dirname+'/app/assets/js/static/core/backbone.min.js', __dirname+'/app/assets/js/static/core/backbone.js'],
		["jQuery", __dirname+'/app/assets/js/static/core/jquery.min.js', __dirname+'/app/assets/js/static/core/jquery.js'],
		["Lawnchair", __dirname+'/app/assets/js/static/core/lawnchair.min.js', __dirname+'/app/assets/js/static/core/lawnchair.js'],
		["Modernizr", __dirname+'/app/assets/js/static/core/modernizr.min.js', __dirname+'/app/assets/js/static/core/modernizr.js']

		## PUT YER FILES HERE FOR MINIFICATION

	]

	out.say 'uglifyjs', 'Minifying AppTools...'

	for file in files_to_minify
		total_ops = total_ops + 1
		out.say 'uglifyjs', 'Minifying '+file[0]
		out.spawn 'uglify', 'uglifyjs', ['-o', file[1], file[2]], minify_done, minify_data, minify_err
	

######## =======  Templates  ========== ########
task 'compile:templates', 'compile jinja2 templates to python modules', (options) ->

	out.say 'templates', 'Compiling Jinja2 templates...'
	
	compile_done = (code) =>
		out.shout 'templates', 'Template compilation complete. Exited with code '+code+'.'
		
	compile_data = (data) =>
		out.whisper data
		
	compile_err = (data) =>
		compile_data(data)
		
	out.spawn 'jinja2compile', defaults.python || options.python, ['tools/bin/compile_templates'], compile_done, compile_data, compile_err