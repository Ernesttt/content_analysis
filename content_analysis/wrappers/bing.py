import urllib
import urllib2
import json
import codecs

API_KEY = '502vtbYXjzGEGFwI7uIEOD8i1PNlPFJYccGVNubkxaw'
# Create an API key in https://datamarket.azure.com/account/keys
# then- select Bing Search API in http://www.bing.com/dev/en-us/dev-center
 
def main():
    query = "mujeres emprendedoras pdf"
    result = bing_search(query, 'Web')
    write_txt(query, result)

 
def bing_search(query, search_type):
    #search_type: Web, Image, News, Video
    query = urllib.quote(query)
    # create credential for authentication
    user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)'
    credentials = (':%s' % API_KEY).encode('base64')[:-1]
    auth = 'Basic %s' % credentials
    url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/'+search_type+'?Query=%27'+query+'%27&$top=10&$format=json'
    request = urllib2.Request(url)
    request.add_header('Authorization', auth)
    request.add_header('User-Agent', user_agent)
    request_opener = urllib2.build_opener()
    response = request_opener.open(request) 
    response_data = response.read()
    json_result = json.loads(response_data)
    result_list = json_result['d']['results']
    #print json.dumps(result_list, sort_keys=False, indent=5)
    return result_list

def write_txt(query,result_search):
    dictionary  = {}
    result_json = json.dumps(result_search)
    dictionary  = json.loads(result_json.encode('utf-8'))
    try:
        try:
            #create or open existing file
            bingFile = codecs.open("Bing.txt", "a", "utf-8")
            for res in dictionary:
                file_line  = query +"/|/"+res['Title']+"/|/"+res['Description']+"/|/"+res['DisplayUrl']+"\n"
                bingFile.write(file_line)
                print file_line
        finally:
            # closing file
            bingFile.close()
    except IOError:
        print("IOError")
 
if __name__ == "__main__":
    main()