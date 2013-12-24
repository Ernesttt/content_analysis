import tweepy
import json
import codecs
import sys

busqueda=""
    
class Twitter_tiempo_real:

    #Constructor
    def __init__(self,consumer_key,consumer_secret,access_token_key,access_token_secret):
         self.consumer_key = consumer_key
         self.consumer_secret =consumer_secret 
         self.access_token_key = access_token_key
         self.access_token_secret = access_token_secret
         try:
             self.auth1 = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
             self.auth1.set_access_token(self.access_token_key, self.access_token_secret)
         except ValueError:
                return ""
         except TypeError:
                return ""     
         except UnicodeDecodeError:
                return ""    
         except:
                return ""
            
    def obtencion_de_tweets(self,lista):
           '''
              Gets Tweets about a specific topic from the stream
              
              In:
                    (lista, list) list of topics              
              Out:
                    (listaLimpia, list) Create a file called tweet.txt with the tweets
           '''
           try: 
                self.l = StreamListener()
                streamer = tweepy.Stream(auth=self.auth1, listener=self.l, timeout=60)
                streamer.filter(track = lista, languages=['es'])
           except ValueError:
                return ""
           except TypeError:
                return ""     
           except UnicodeDecodeError:
                return ""    
           except:
                return ""     



class StreamListener(tweepy.StreamListener):
    #archivo donde se almacenara la informacion
    archivoEscritura=codecs.open("tweet.txt","a","utf-8")
    numero_tweets=1000
    #variable
    contador = 1
    def on_status(self, tweet):
        '''
              status from the stream
              
              In:
                    (tweet, text) text string              
              Out:
                    
        '''
        print "------------------"
        
    def on_error(self, status_code):
        '''
              errors from the stream
              
              In:
                    (status_code, text) text string with the error code             
              Out:
                    
        '''
        print 'Error: ' + repr(status_code)
        return False

    def on_data(self, data):
        '''
              data from the stream(tweets about a topic)
              
              In:
                    (data, JSON format) JSON with the tweets from the stream             
              Out:
                    
        '''
        if (self.contador <= self.numero_tweets):
            diccionario={}
            print "encontrando tweet numero "+str(self.contador)
            diccionario=json.loads(data)
            tweet=(diccionario["text"]).replace("\n", "")
            cadena=','.join(busqueda) +"/|/"+diccionario["created_at"]+"/|/"+diccionario["lang"]+"/|/"+diccionario["user"]["name"]+"/|/"+tweet+"/|/"+str(diccionario["user"]["friends_count"])+"/|/"+str(diccionario["user"]["followers_count"])+"\n"  
            self.archivoEscritura.write(cadena);
            self.contador += 1
        else:
            self.archivoEscritura.close();
            return False
        
    def on_timeout(self):
        '''
              cheks if the timeout limit is reach
            
              In:            
              Out:
                    
        '''
        print 'Tiempo fuera, no se encontro mas informacion en el tiempo establecido como limite...'
        archivoEscritura.close();
        return False

'''
caso de uso

consumer_key = 'tPTSY5fz1l8jTBamlsg'          
consumer_secret = 'IkGZgb7RXY6hlINW4yXDDo078LfikNqYnybMeAwkhI'
access_token_key = '2255882202-OQWZ7gz3HZipE7Cas0oeJKRPA8vF8HJT4edyNgq'
access_token_secret = '6JpyzfF18GGMEFToWVvvkxz0Zv8SeTM99Eoxnchz67PS0'
prueba=Twitter_tiempo_real(consumer_key,consumer_secret,access_token_key,access_token_secret)
busqueda=["mujeres","emprendedoras"]
prueba.obtencion_de_tweets(busqueda)

'''


