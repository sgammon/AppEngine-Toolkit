fs = require 'fs'
path = require 'path'
util = require 'util'
{exec} = require 'child_process'

defaults =
	
	output: '~/WorkspaceTest'
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

	say: (module, message) ->
		util.log '['+@flags.wrap(module, @flags.blue)+']: '+message

	shout: (module, message, loud=false) ->
		util.log '' if shout
		util.log @flags.wrap('[############### ===== '+message+' ===== ###############]', @flags.yellow)
		util.log '' if shout
		
	error: (module, message, warning=true) ->
		if warning
			util.log @flags.wrap('[############### WARNING: '+module+' ###############]', @flags.red)
			util.log message
		else
			util.log '\n'
			util.log @flags.wrap('[############### ERROR: '+module+' ###############]', @flags.red) if warning
			util.log message
			util.log '\n'
			util.log ''
		
	spawn: (name, command, flags, callback, stdout=false, stderr=false) ->

		if not command?
			command = name
		else
			if typeof command == 'function'
				command = name
				callback = command

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
option 'w', '--watch', 'watch assets (SASS and CoffeeScript) that need compilation, and compile when they are modified'
option 'c', '--config [STR]', 'path to project feature/skeleton config (defaults to \''+defaults.config+'\')'


######### =======  Utils  ========== #########
f_escape = (path) =>
	reg = new RegExp(' ','gi')
	return path.replace(reg, '\\ ')
	
getpath = (options) =>
	## Choose whether or not to wrap
	bare = options.bare || defaults.bare
	if not bare
		## If wrap, create a project directory
		out.say 'skeleton', 'Creating project directory...'
		project_dir = (options.output || defaults.output)
		if project_dir[-1] != '/'
			project_dir += '/'
	
		project_dir = project_dir+(options.project || defaults.project)
		out.exec 'mkdir -p '+project_dir
	else
		## Else just use it
		out.say 'skeleton', 'Entering project directory...'
		project_dir = (options.output || defaults.output)
	return project_dir


######### =======  Project Tools  ========== #########	
task 'init', 'start a new project', (options) =>

	out.shout 'install', 'Starting Installation', true


task 'install:skeleton', 'download a skeleton from git and install it', (options) =>
	
	## 1: Copy skeleton over first
	install_skeleton = (callback) =>
		out.say 'skeleton', 'Copying project skeleton...'

		project_dir = getpath(options)
		skeleton_dir = __dirname+'/app')
		try
			sk = fs.readdirSync skeleton_dir

		catch error
			out.spawn('git clone --bare -b '+(options.skeleton || defaults.skeleton)+' '+(options.gitsource.skeleton || defaults.gitsource.skeleton)+' app/')

		out.exec 'chmod -R 755 app/'
		out.say 'install', 'Installation complete at: app/'
			
	install_skeleton()
	out.shout 'skeleton', 'Finished skeleton ops.'
	


task 'install:bootstrap', 'generate a buildout executable', (options) =>

	bootstrap_buildout = (project_dir) =>
	
		## 2: Run bootstrap		
		out.shout 'install', 'Running bootstrap...', true
		out.spawn 'bootstrap', '/usr/local/bin/python', [project_dir+'/bootstrap.py'], () =>
			out.say 'install', out.flags.wrap('Bootstrap complete.', out.flags.green)+' From now on, you can use `'+out.flags.wrap('cake make', out.flags.green)+'` to update dependencies.'
			out.say 'install', 'Running buildout...'
			invoke 'project:buildout'
				
	project_dir = getpath(options)
	bootstrap_buildout(project_dir)
	
	
task 'install:coffeescript', 'enable coffeescript integration in target project', (options) =>
	
	
task 'install:compass', 'enable compass integration in target project', (options) =>
	
		
task 'project:buildout', 'download and install GAE environment, supporting libraries, etc', (options) =>

	out.spawn 'buildout', 'sh', [project_dir+'/bin/buildout'], () =>
		out.say 'install', out.flags.wrap('Buildout complete.', out.flags.green)+' Installation is complete.'
		out.shout 'install', 'Installation complete.', true


######### =======  Platform Tools  ========== #########
## App ID's
app_options =

	development: 'fatcatmap'
	staging: 'momentum-labs'
	production: 'fat-cat-map'	

task 'install', 'run me on first install!', (options) ->

	out.shout 'install', 'Starting Installation'

	out.say 'install', 'Running bootstrap...'
	out.spawn 'python bootstrap.py --distribute'

	out.say 'install', 'From now on, you can use `cake make` to update dependencies. Happy coding!'
	out.shout 'install', 'Installation complete.'

	invoke 'make'


task 'make', 'download dependencies and prepare dev environment', (options) ->

	out.shout 'make', 'Starting Envrionment Setup'

	out.say 'make', 'Running buildout...'
	out.spawn 'bin/buildout'

	out.say 'make', 'Updating core libraries...'
	out.spawn 'bin/update_libraries'

	out.shout 'make', 'Environment setup complete.'


task 'bake', 'compile and minify all js, templates, and coffeescript', (options) ->

	out.shout 'bake', 'Starting Compilation'

	## 1) Compile everything first
	out.say 'bake', 'Compiling JS codebase (CoffeeScript)...'
	invoke 'compile:codebase'

	out.say 'bake', 'Compiling JS templates (mustasche)...'
	invoke 'compile:jstemplates'

	out.say 'bake', 'Compiling Jinja2 templates...'
	invoke 'compile:templates'

	out.say 'bake', 'Compiling SASS...'
	invoke 'compile:sass'


	## 2) Bundle things
	out.say 'bake', 'Bundling JS dependencies...'
	invoke 'bundle:dependencies'

	out.say 'bake', 'Bundling JS templates...'
	invoke 'bundle:jstemplates'

	## 3) Minify things
	out.say 'bake', 'Minifying JS codebase...'
	invoke 'minify:codebase'

	out.say 'bake', 'Minifying JS dependencies...'
	invoke 'minify:dependencies'

	out.say 'bake', 'Minifying JS templates...'
	invoke 'minify:jstemplates'

	out.say 'bake', 'Minifying CSS...'
	invoke 'minify:sass'


task 'slice', 'run fatcatmap\'s local dev server', (options) ->
	out.spawn 'bin/dev_appserver'

task 'serve', 'deploy fatcatmap to appengine', (options) ->
	out.spawn 'bin/appcfg upload app'


######## =======  Stylesheets/SASS  ========== ########
task 'compile:sass', 'compile SASS to CSS', (options) ->
	out.spawn 'compass compile'

task 'minify:sass', 'minify SASS into production-ready CSS', (options) ->
	out.spawn 'compass compile --output-style compressed'



########## =======  CoffeeScript  ========== ##########
task 'compile:codebase', 'compile js codebase', (options) ->
	out.spawn 'bin/coffee2'

task 'minify:codebase', 'minify js codebase', (options) ->
	out.spawn 'bin/uglify'



########## =======  JS Libraries  ========== ##########
task 'minify:dependencies', 'minify js dependencies', (options) ->


task 'bundle:dependencies', 'bundle js dependencies for production', (options) ->	



############ =======  Templates  ========== ############
task 'compile:templates', 'compile jinja2 templates', (options) ->


task 'compile:jstemplates', 'compile mustasche templates', (options) ->


task 'minify: jstemplates', 'minify mustasche templates', (options) ->