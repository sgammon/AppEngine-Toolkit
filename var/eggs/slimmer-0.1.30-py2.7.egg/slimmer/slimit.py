#!/usr/bin/python

"""
A command line program wrapper to slimmer
"""

from slimmer import *
from slimmer import run
import CommandLineApp

class slimit(CommandLineApp.CommandLineApp):
    """ whitespace trip HTML, XHTML, Javascript and CSS """
    
    EXAMPLES_DESCRIPTION = """
To slim a html file:

    $ slimit /home/peter/big.html xhtml

To slim a Javascript file:
    
    $ slimit library.js js
      
Most of the time you don't need specify the format since it's guessed:
    
    $ slimit screen.css
      
To save to a particular file other than stdout:
    
    $ slimit --output=library.slimmed.js library.js
    
    """
    
    def optionHandler_version(self):
        """Prints version and exits"""
        print __version__
        
        
    speedtest = 0
    def optionHandler_test(self):
        """Perform a speed and compression test"""
        self.speedtest = 1
    optionHandler_t = optionHandler_test
    
    outputfile = None
    def optionHandler_output(self, path):
        """ Save result to file """
        self.outputfile = path
        
    hardcore = False
    def optionHandler_hardcore(self):
        """Tries really hard but potentially slower. Default is not to do it hardcore."""
        self.hardcore = True
        
    def showVerboseHelp(self):
        CommandLineApp.CommandLineApp.showVerboseHelp(self)
        
        
    def main(self, filename, syntax=None):
        """
        Run the slimmer
        """
        if syntax is None:
            print "guess for", repr(filename),
            syntax = guessSyntax(filename)
            print repr(syntax)
        print syntax
        run(filename, syntax, self.speedtest, self.outputfile, hardcore=self.hardcore)
        
        
                
        
if __name__ == '__main__':
    slimit().run()
        