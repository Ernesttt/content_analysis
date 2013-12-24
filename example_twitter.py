#se importa el paquetes necesarios para la aplicacion
import re
import codecs
import json
import sys
import os
import string
import unicodedata
from nltk.corpus import stopwords
from content_analysis.nlp.metrics_all import all

#Constante que toma la codificacion de la computadora donde se ejecute python
codificacion=sys.stdout.encoding


class Twitter_Caso_Uso:
    
    #Constructor
    def __init__(self,archivo):
         if  isinstance(archivo, str):
                self.archivo=archivo
         else:
                self.archivo="default"

              
    def obtencion_de_elementos(self,tipo):

        '''
              Get hashtags or users or urls from a topic
              
              In:
                    (tipo, hashtag or user or url)              
              Out:
                    (data, JSON format) JSON with the hashtags or users or urls 
                    
        '''
        if  isinstance(tipo, str):
                try:         
                    archivoLectura=codecs.open(os.path.abspath("Tweets/"+self.archivo+".txt"),"r","utf8")
                    try:
                            prueba=metricas()
                            listaFinal=[]
                            lineaLecturaTweet = archivoLectura.readline()
                            regex = re.compile(r"#(\w+)", flags=re.IGNORECASE)
                            regex1 = re.compile(r"@(\w+)", flags=re.IGNORECASE)
                            regex2 = re.compile(r"^https?:\/\/.*[\r\n]*", flags=re.IGNORECASE)
                            while lineaLecturaTweet:
                                  listaTemporal=[]
                                  listaElementos= lineaLecturaTweet.split("/|/");
                                  if(tipo=="hashtag"):
                                      listaTemporal= [re.sub(r'[^#\w]', '', i)  for i in listaElementos[4].split() if i.startswith("#") if regex.match(i)]
                                  elif(tipo=="usuario"):
                                      listaTemporal= [re.sub(r'[^@\w]', '', i)  for i in listaElementos[4].split() if i.startswith("@") if regex1.match(i)]
                                  elif(tipo=="url"):
                                      listaTemporal= [i for i in listaElementos[4].split() if regex2.match(i)]                             
                                  else:
                                       listaTemporal=[]
                                       
                                  listaFinal.extend(listaTemporal)
                                  lineaLecturaTweet = archivoLectura.readline()    
                            informacion_json =json.dumps(list(set(listaFinal)))
                            return informacion_json
                    except ValueError:
                           return ""
                    except TypeError:
                           return ""     
                    except UnicodeDecodeError:
                           return ""    
                    except:
                           return ""
                    finally:
                       archivoLectura.close()
                except IOError:
                       return ""
        else:
                return ""            





    def obtencion_de_elementos_mas_frecuentes(self,tipo,N):

        '''
              Get the most frecuents hashtags or users from a topic
              
              In:
                    (tipo, hashtag or user or url)              
              Out:
                    (data, JSON format) JSON with the hashtags or urls 
                    
        '''
        if  isinstance(tipo, str) and isinstance(N, int):
                try:         
                    archivoLectura=codecs.open(os.path.abspath("Tweets/"+self.archivo+".txt"),"r","utf8")
                    try:
                            listaFinal=[]
                            simbolo=""
                            if(tipo=="hashtag"):   simbolo="#"
                            elif(tipo=="usuario"): simbolo="@"
                            else:                  simbolo=""
                            lineaLecturaTweet = archivoLectura.readline()
                            regex = re.compile(r"#(\w+)", flags=re.IGNORECASE)
                            regex1 = re.compile(r"@(\w+)", flags=re.IGNORECASE)
                            while lineaLecturaTweet:
                                  listaTemporal=[];
                                  listaElementos= lineaLecturaTweet.split("/|/");
                                  if(tipo=="hashtag"):
                                      listaTemporal= [re.sub(r'[^#\w]', '', i)  for i in listaElementos[4].split() if i.startswith("#") if regex.match(i)]
                                  elif(tipo=="usuario"):
                                      listaTemporal= [re.sub(r'[^@\w]', '', i)  for i in listaElementos[4].split() if i.startswith("@") if regex1.match(i)]
                                  else:
                                       listaTemporal=[]                  
                                  listaFinal.extend(listaTemporal)
                                  lineaLecturaTweet = archivoLectura.readline()   
                            prueba=metricas()
                            informacion_json =json.dumps([simbolo+s for s in  prueba.elementos_mas_frecuentes_lista(listaFinal,N)])
                            return informacion_json
                    except ValueError:
                           return ""
                    except TypeError:
                           return ""     
                    except UnicodeDecodeError:
                           return ""    
                    except:
                           return ""
                    finally:
                       archivoLectura.close()
                except IOError:
                      return ""
        else:
                return ""
            

    def obtencion_de_elementos_menos_frecuentes(self,tipo,N):

        '''
              Get the less frecuent hashtags or users from a topic
              
              In:
                    (N, number of hashtag or users)              
              Out:
                    (data, JSON format) JSON with the hashtags or urls 
                    
        '''
        if  isinstance(tipo, str) and isinstance(N, int):
                try:         
                    archivoLectura=codecs.open(os.path.abspath("Tweets/"+self.archivo+".txt"),"r","utf8")
                    try:
                            listaFinal=[]
                            simbolo=""
                            if(tipo=="hashtag"):   simbolo="#"
                            elif(tipo=="usuario"): simbolo="@"
                            else:                  simbolo=""
                            lineaLecturaTweet = archivoLectura.readline()
                            regex = re.compile(r"#(\w+)", flags=re.IGNORECASE)
                            regex1 = re.compile(r"@(\w+)", flags=re.IGNORECASE)
                            while lineaLecturaTweet:
                                  listaTemporal=[];
                                  listaElementos= lineaLecturaTweet.split("/|/");
                                  if(tipo=="hashtag"):
                                      listaTemporal= [re.sub(r'[^#\w]', '', i)  for i in listaElementos[4].split() if i.startswith("#") if regex.match(i)]
                                  elif(tipo=="usuario"):
                                      listaTemporal= [re.sub(r'[^@\w]', '', i)  for i in listaElementos[4].split() if i.startswith("@") if regex1.match(i)]
                                  else:
                                       listaTemporal=[]                  
                                  listaFinal.extend(listaTemporal)
                                  lineaLecturaTweet = archivoLectura.readline()
                            prueba=metricas()
                            informacion_json =json.dumps([simbolo+s for s in  prueba.elementos_menos_frecuentes_lista(listaFinal,N)])
                            return informacion_json
                    except ValueError:
                           return ""
                    except TypeError:
                           return ""     
                    except UnicodeDecodeError:
                           return ""    
                    except:
                           return ""
                    finally:
                       archivoLectura.close()
                except IOError:
                       return ""
        else:
                return ""



    def obtencion_de_vocabulario_mas_frecuente(self,N):

        '''
              Get the most frecuent vocabulary from a topic
              
              In:
                    (N, Number of most frecuente words)              
              Out:
                    (data, JSON format) JSON with the vocabulary 
                    
        '''
        if  isinstance(N, int):
                try:         
                    archivoLectura=codecs.open(os.path.abspath("Tweets/"+self.archivo+".txt"),"r","utf-8")
                    try:
                            prueba=metricas()
                            listaFinal=[]
                            listaCerradas=[]
                            lineaLecturaTweet = archivoLectura.readline()
                            regex = re.compile(r"#(\w+)", flags=re.IGNORECASE)
                            regex1 = re.compile(r"@(\w+)", flags=re.IGNORECASE)
                            regex2 = re.compile(r"^https?:\/\/.*[\r\n]*", flags=re.IGNORECASE)
                            while lineaLecturaTweet:
                                  listaTemporal=[]
                                  listaElementos= lineaLecturaTweet.split("/|/")
                                  cadena=listaElementos[4].replace("\n", "")         
                                  cadena.rstrip()
                                  listaTemporal=cadena.split()
                                  listaTemporal= [i for i in listaTemporal if not(regex.match(i)) and not(regex1.match(i)) and not(regex2.match(i))]            
                                  listaFinal.extend(listaTemporal)
                                  lineaLecturaTweet = archivoLectura.readline()
                            informacion_json =json.dumps(prueba.elementos_mas_frecuentes_lista(listaFinal,N))
                            return informacion_json
                    except ValueError:
                           return ""
                    except TypeError:
                           return ""     
                    except UnicodeDecodeError:
                           return ""    
                    except:
                           return ""
                    finally:
                       archivoLectura.close()
                except IOError:
                       return ""
        else:
                return ""           
        

    def obtencion_de_vocabulario_menos_frecuente(self,N):

        '''
              Get the less frecuent vocabulary from a topic
              
              In:
                    (N, Number of less frecuente words)              
              Out:
                    (data, JSON format) JSON with the vocabulary 
                    
        '''
        if  isinstance(N, int):
                try:         
                    archivoLectura=codecs.open(os.path.abspath("Tweets/"+self.archivo+".txt"),"r","utf-8")
                    try:
                            prueba=metricas()
                            listaFinal=[]
                            listaCerradas=[]
                            lineaLecturaTweet = archivoLectura.readline()
                            regex = re.compile(r"#(\w+)", flags=re.IGNORECASE)
                            regex1 = re.compile(r"@(\w+)", flags=re.IGNORECASE)
                            regex2 = re.compile(r"^https?:\/\/.*[\r\n]*", flags=re.IGNORECASE)
                            while lineaLecturaTweet:
                                  listaTemporal=[]
                                  listaElementos= lineaLecturaTweet.split("/|/")
                                  cadena=listaElementos[4].replace("\n", "")         
                                  cadena.rstrip()
                                  listaTemporal=cadena.split()
                                  listaTemporal= [i for i in listaTemporal if not(regex.match(i)) and not(regex1.match(i)) and not(regex2.match(i))]            
                                  listaFinal.extend(listaTemporal)
                                  lineaLecturaTweet = archivoLectura.readline()
                            informacion_json =json.dumps(prueba.elementos_menos_frecuentes_lista(listaFinal,N))
                            return informacion_json
                    except ValueError:
                           return ""
                    except TypeError:
                           return ""     
                    except UnicodeDecodeError:
                           return ""    
                    except:
                           return ""
                    finally:
                       archivoLectura.close()
                except IOError:
                       return ""
        else:
                return ""    




'''
caso de uso

prueba=Twitter_Caso_Uso("tweet")
prueba.obtencion_de_elementos_menos_frecuentes("hashtag",10):
'''            
      
        





