import json
import codecs
from apiclient.discovery import build


API_KEY = "AIzaSyAdHnvmBSL6k0vY_qJQcnAuqagSZ3LjoSM"
cx_key  = '011033102363583886669:avf3hux4mn4'
# first it is created a google custom search service at http://www.google.com/cse/
# -then configure it to search the entire web
# -obtain cx_key from code snippet
# -finally obtain API_KEY from API ACCESS in the API control panel

class Google(object):

	def __init__(self, license=None, geolocation='mx'):
	    """ license     : license key for the API
	    geolocation : default country of search is defined as Mexico
	    """
	    self.license = license or API_KEY
	    self.geolocation = geolocation

	def search(self, query, num_results=10, starting_at=1):
	    """ Returns a list (json) of results from Google for the given query.
	    - num_results: number of displayed results (from 1 to 10)
	    - starting_at: number of starting point,
	    - there is a daily limit of 100 free queries. Google Custom Search is a paid service if more queries are needed.
	    """
	    service = build("customsearch", "v1", developerKey=self.license)
	    result  = service.cse().list( q     = query, 
					  gl    = self.geolocation, 
					  num   = num_results,
					  start = starting_at,
					  cx	= cx_key,).execute()
	    return result


	def write_txt(self, result_search, file_name="google.txt"):
	    dictionary  = {}
	    result_json = json.dumps(result_search)
	    dictionary  = json.loads(result_json.encode('utf-8'))
	    try:
		try:
		    #create or open existing file
		    googleFile = codecs.open(file_name, "a", "utf-8")
                    try:
                            for res in dictionary['items']:
                                #for element in res: 
                                file_line  = dictionary['queries']['request'][0]['searchTerms']+"/|/"+res['title']+"/|/"+res['snippet']+"/|/"+res['link']+"\n"
                                file_line.replace("\n","")
                                googleFile.write(file_line)
                                print file_line
                    except KeyError, e:
                        value = 'default'
		finally:
			# closing file
			googleFile.close()
	    except IOError:
		print("IOError")
                

	def result_list(self, result_search):
	    dictionary  = {}
            list = []
	    result_json = json.dumps(result_search)
	    dictionary  = json.loads(result_json.encode('utf-8'))
	    try:
                for res in dictionary['items']:
                    line  = res['title']+", "+res['link']
                    line.replace("\n","")
                    list.append(line)
                return list
	    except KeyError, e:
		value = 'default'

