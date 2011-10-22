# -*- coding: utf-8 -*-
import webapp2


class DynamicAssetHandler(webapp2.RequestHandler):
	
	def get(self):
		return self.response.out.write('Dynamic assets are not yet supported.')
		
		
DynamicAsset = webapp2.WSGIApplication([webapp2.Route('/.*', DynamicAssetHandler, name='retrieve-asset')])


def main():
	DynamicAsset.run()
	

## Run in CGI-mode...
if __name__ == '__main__':
	main()