import nltk
import itertools
import re
import string
import codecs
import unicodedata
import sys
from nltk.util import ingrams
from nltk.collocations import *
from nltk.corpus import stopwords
from pattern.es import parse, split
from collections import Counter


class Metricas:
    
    #Constructor
    def __init__(self):   
            pass
        
    def __call__(self):
            self.__init__


    def filtro_palabras_cerradas(self, texto):
            '''
              Removing stopwords
              
              In:
                    (texto, text) text string              
              Out:
                    (listaLimpia, list) list of strings in unicode
            '''
            listaCerradas = []
            listaLimpia = []
            if isinstance(texto, str):
                texto = unicode(texto, "utf-8", "xmlcharrefreplace")
            for x in stopwords.words('spanish'):
                listaCerradas.append(unicode(x,"utf-8"))
            lista = texto.split()
            for palabra in lista:
                if palabra not in listaCerradas:
                    listaLimpia.append(palabra)
            return listaLimpia
       
       
       

    def filtro_caracteres_especiales(self, texto):
            '''
              Removing specaial characters
              
              In:
                    (texto, text) text string               
              Out:
                    (text) text string free of special characters in unicode
            '''
            PRINTABLE = set(('Lu', 'Ll', 'Nd', 'Zs'))
            if isinstance(texto, str):
                texto = unicode(texto, "utf-8", "xmlcharrefreplace")
            resultado = []
            for c in texto:
                c = unicodedata.category(c) in PRINTABLE and c or u'#'
                resultado.append(c)
            return u''.join(resultado).replace(u'#', u' ')  
        



    def colocaciones_bigramas_filtro_texto(self,texto,N,M):
            '''
            N-Best bigrams in a text
            
            In:
                   (N, int) Number of n-best bigrams
                   (M, int) Minimum frequency for each bigram to be considered
                   (texto, str) String text
            Out:
                   (listaFinal,list) list with N-best bigrams
            '''
            if isinstance(N, int) and isinstance(M, int):
                        try:
                                listaFinal = []
                                if isinstance(texto, str):
                                   texto = unicode(texto, "utf-8", "xmlcharrefreplace")
                                texto = self.filtro_caracteres_especiales(texto)
                                lista = texto.split()
                                bigrama_medidas = nltk.collocations.BigramAssocMeasures()
                                buscador = BigramCollocationFinder.from_words(lista)
                                buscador.apply_freq_filter(M)
                                for x in buscador.nbest(bigrama_medidas.pmi, N):
                                    listaFinal.append(" ".join(x))
                                return listaFinal
                        except TypeError:
                                return []
                        except UnicodeDecodeError:
                                return [] 
                        except:
                                return [] 
            else:
                    return []
           



    def colocaciones_trigramas_filtro_texto(self,texto,N,M):
            '''
            N-Best trigrams in a text
            
            In:
                   (N,int) Number of n-best trigrams
                   (M,int) Minimum frequency for each trigram to be considered
                   (texto, str) String text
            Out:
                   (listaFinal, list) list with N-best trigrams
            '''
            if isinstance(N, int) and isinstance(M, int):
                        try:
                             listaFinal = []
                             if isinstance(texto, str):
                                texto = unicode(texto, "utf-8", "xmlcharrefreplace")
                             texto = self.filtro_caracteres_especiales(texto)
                             lista = texto.split()
                             trigrama_medidas = nltk.collocations.TrigramAssocMeasures()
                             buscador = TrigramCollocationFinder.from_words(lista)
                             buscador.apply_freq_filter(M)
                             for x in buscador.nbest(trigrama_medidas.pmi, N):
                                 listaFinal.append(" ".join(x))
                             return listaFinal
                        except TypeError:
                                    return []
                        except UnicodeDecodeError:
                                    return []       
                        except:
                                    return []             
            else:
                    return []
   


   
    def categoria_gramatical_texto_pattern(self,texto):
            '''
              Grammatical category of each word

              ej. she:PRP drove:VBD a:DT silver:NN pt:NN cruiser:NN
                    PRP: Possesive pronoun
                    VBD: Verb in past tense
                    DT: Determiner
                    NN: Noun in singular
              In:
                    (texto, text) string text               
              Out:
                    (listaCategoria, list) list with grammatical categories associated to every word
            '''
            try:
                    categorias = parse(texto)
                    listaCategoria = []
                    if isinstance(texto, str):
                        texto = unicode(texto, "utf-8", "xmlcharrefreplace")
                    for x in categorias.split():
                        for y in x:
                            listaCategoria.append(y[0]+":"+y[1])
                    return listaCategoria
            except TypeError:
                    return []
            except UnicodeDecodeError:
                    return []
            except:
                    return []    




    def n_gramas_texto(self,texto,N):
            '''
              Searching for n-grams
    
              In:
                    (texto, text) text string
                    (N, int)  size of the n-gram 2 is equal to bigram, 3 is equal to trigram and so on...
              Out:
                    (listaNgrama, list) n-gram list
            '''
            if  isinstance(N, int):
                    try:
                            if isinstance(texto, str):
                               texto = unicode(texto, "utf-8", "xmlcharrefreplace")
                            texto = self.filtro_caracteres_especiales(texto)
                            lista = self.filtro_palabras_cerradas(texto)
                            listaNgrama=[]
                            for Ngramas in ingrams(lista, N, pad_right=True):
                                    if (str(Ngramas[N-1])!= "None"):
                                            listaNgrama.append(" ".join(Ngramas))
                            return listaNgrama
                    except TypeError:
                            return []
                    except UnicodeDecodeError:
                            return []    
                    except:
                            return []
            else:
                    return []
                    
    
    

    def elementos_mas_frecuentes_texto(self,texto,N):
            '''
              Searching for most common words in a text
              
              In:
                    (texto, text) text string
                    (N, int) top N elements
              Out:
                    (listaFinal, list) n-most common words
            '''
            if isinstance(N, int) and N>0:
                try:
                     listaFinal = []
                     if isinstance(texto, str):
                        texto = unicode(texto, "utf-8", "xmlcharrefreplace")
                     texto = self.filtro_caracteres_especiales(texto)
                     lista = self.filtro_palabras_cerradas(texto)
                     for x in Counter(lista).most_common(N):
                                listaFinal.append(x[0]+":"+str(x[1]))
                     return listaFinal
                except TypeError:
                          return []
                except UnicodeDecodeError:
                          return []  
                except:
                          return []
            else:
                    return []
                    



    def elementos_mas_frecuentes_lista(self,lista,N):
            '''
              Searching most common elements (words) in a list
              
              In:
                    (lista,list) list of words
                    (N,int) top N elements
              Out:
                    (lista,list) n-most common words
            '''
            if isinstance(lista, list) and isinstance(N, int) and N>0:
                try:
                        listaFinal = []
                        for x in Counter(lista).most_common(N):
                            listaFinal.append(x[0]+":"+str(x[1]))
                        listaFinal = [i.decode('utf-8') if isinstance(i, str) else i for i in listaFinal]
                        return listaFinal
                except TypeError:
                          return []
                except UnicodeDecodeError:
                          return []  
                except:
                          return []
            else:
                    return []   




    def elementos_mas_frecuentes_diccionario(self,diccionario,N):
            '''
              Searching most common elements (words) in a dictionary
              
              In:
                    (diccionario,dict) dictionary of words
                    (N,int) top N elements
              Out:
                    (lista,list) n-most common words
            '''
            if  isinstance(diccionario, dict) and isinstance(N, int) and N>0:
                try:
                     listaFinal = [] 
                     for x in Counter(diccionario).most_common(N):
                         listaFinal.append(x[0]+":"+str(x[1]))
                     listaFinal = [i.decode('utf-8') if isinstance(i, str) else i for i in listaFinal]
                     return listaFinal
                except TypeError:
                          return []
                except UnicodeDecodeError:
                          return []  
                except:
                          return []
            else:
                    return []
        
        
        
                 
                 
    def elementos_menos_frecuentes_texto(self,texto,N):
            '''
              Searching for least common words in a text
              
              In:
                    (texto, text) text string
                    (N, int) top N elements
              Out:
                    (listaFinal, list) n-most common words
            '''
            if isinstance(N, int) and N>0:
                try:
                     listaFinal = []
                     if isinstance(texto, str):
                        texto = unicode(texto, "utf-8", "xmlcharrefreplace")
                     texto = self.filtro_caracteres_especiales(texto)
                     lista = self.filtro_palabras_cerradas(texto)
                     for x in list(reversed(Counter(lista).most_common()[-N:])):
                                listaFinal.append(x[0]+":"+str(x[1]))
                     return listaFinal
                except TypeError:
                          return []
                except UnicodeDecodeError:
                          return []  
                except:
                          return []
            else:
                    return []
                    



    def elementos_menos_frecuentes_lista(self,lista,N):
            '''
              Searching most common elements (words) in a list
              
              In:
                    (lista,list) list of words
                    (N,int) top N elements
              Out:
                    (lista,list) n-most common words
            '''
            if isinstance(lista, list) and isinstance(N, int) and N>0:
                try:
                        listaFinal = []
                        for x in list(reversed(Counter(lista).most_common()[-N:])):
                            listaFinal.append(x[0]+":"+str(x[1]))
                        listaFinal = [i.decode('utf-8') if isinstance(i, str) else i for i in listaFinal]
                        return listaFinal
                except TypeError:
                          return []
                except UnicodeDecodeError:
                          return []  
                except:
                          return []
            else:
                    return []   




    def elementos_menos_frecuentes_diccionario(self,diccionario,N):
            '''
              Searching most common elements (words) in a dictionary
              
              In:
                    (diccionario,dict) dictionary of words
                    (N,int) top N elements
              Out:
                    (lista,list) n-most common words
            '''
            if  isinstance(diccionario, dict) and isinstance(N, int) and N>0:
                try:
                     listaFinal = [] 
                     for x in list(reversed(Counter(diccionario).most_common()[-N:])):
                         listaFinal.append(x[0]+":"+str(x[1]))
                     listaFinal = [i.decode('utf-8') if isinstance(i, str) else i for i in listaFinal]
                     return listaFinal
                except TypeError:
                          return []
                except UnicodeDecodeError:
                          return []  
                except:
                          return []
            else:
                    return []
                    
                    
                    
                    
    def vocabulario_texto(self,texto):
            '''
              vocabulary in a text
              
              In:
                    (texto,text) text string 
              Out:
                    (vocabulario,dict) dictionary with every word and its frequency
            '''
            if  isinstance(texto, str):
                texto = unicode(texto, "utf-8", "xmlcharrefreplace")
            try:
                    vocabulario={}
                    texto = self.filtro_caracteres_especiales(texto)
                    lista = self.filtro_palabras_cerradas(texto)
                    for x in  lista:
                        if x in vocabulario:
                                vocabulario[x]+=1
                        else:
                                vocabulario[x]=1
                    return vocabulario

            except TypeError:
                        return {}
            except UnicodeDecodeError:
                        return {}      
            except:
                        return {}  
                        