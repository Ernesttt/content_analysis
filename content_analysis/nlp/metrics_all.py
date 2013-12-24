import nltk
import itertools
import re
import string
import codecs
import unicodedata
import sys
from nltk.util import ingrams
from nltk.collocations import *
from pattern.es import parse, split
from collections import Counter

#Constante que toma la codificacion de la computadora donde se ejecute python
codificacion=sys.stdout.encoding

class Metricas_All:
    
    #Constructor
    def __init__(self):   
            pass

    '''
      Eliminacion de los acentos de las palabras

      Entrada:
            (s,unicode) cadena de texto en formato unicode               
      Salida:
            (s,unicode) cadena de texto sin acentos en formato unicode
    '''


    def elimina_tildes(self,s):
            try:
                 return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
            except TypeError:
                 return ""     
            except UnicodeDecodeError:
                 return ""
            except:
                 return ""    
        

    
    def colocaciones_bigramas_lista(self,lista,N):
            '''
               Collocations are sets of words bi, tri, n means 2,3, n number of words 
            '''
            
            '''
            Find all bigrams in a list
            Entrada:
                   (N,int) El numero de mejores colocaciones a obtener
                   (lista,list) lista con palabras
            Salida:
                   (lista,list) lista con palabras(colocaciones)
            '''
            if  isinstance(lista, list) and isinstance(N, int) and N>0:
                    if (all(type(x) is str for x in lista)):
                        try:
                                listaFinal=[]
                                remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
                                lista=[unicode(s,codificacion) for s in lista]
                                lista=[s.translate(remove_punctuation_map).lower() for s in lista]
                                lista=[str(self.elimina_tildes(s)) for s in lista]
                                lista= filter(None,lista)
                                lista= filter(str.strip, lista)
                                bigrama_medidas = nltk.collocations.BigramAssocMeasures()
                                buscador = BigramCollocationFinder.from_words(lista)
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
            else:
                 return []




    '''
    Encontrar las N mejores colocaciones de bigramas en un texto
    Entrada:
           (entero,int) El numero de mejores colocaciones a obtener
           (texto,str)  lista con palabras
    Salida:
           (lista,list) lista con palabras(colocaciones)
    '''

    def colocaciones_bigramas_texto(self,texto,N):
            if  isinstance(texto, str) and isinstance(N, int) and N>0:
                    try:
                            listaFinal=[]
                            remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
                            lista=[s.translate(remove_punctuation_map).lower() for s in nltk.word_tokenize(unicode(texto,codificacion))]
                            lista=[str(self.elimina_tildes(s)) for s in lista]
                            lista= filter(None,lista)
                            lista= filter(str.strip, lista)
                            bigrama_medidas = nltk.collocations.BigramAssocMeasures()
                            buscador = BigramCollocationFinder.from_words(lista)
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





    '''
    Encontrar las N mejores colocaciones de trigramas de una lista
    Entrada:
            (N,int) El numero de mejores colocaciones a obtener
            (lista,list) lista con palabras
    Salida:
            (lista,list) lista de python con palabras(colocaciones)
    '''

    def colocaciones_trigramas_lista(self,lista,N):
            if  isinstance(lista, list) and isinstance(N, int) and N>0:
                    if (all(type(x) is str for x in lista)):
                           try:
                                   listaFinal=[]
                                   remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
                                   lista=[unicode(s,codificacion) for s in lista]
                                   lista=[s.translate(remove_punctuation_map).lower() for s in lista]
                                   lista=[str(self.elimina_tildes(s)) for s in lista]
                                   lista= filter(None,lista)
                                   lista= filter(str.strip, lista)
                                   trigrama_medidas = nltk.collocations.TrigramAssocMeasures()
                                   buscador = TrigramCollocationFinder.from_words(lista)
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
            else:
                    return []





    '''
    Encontrar las N mejores colocaciones de trigramas de una lista
    Entrada:
            (N,int) El numero de mejores colocaciones a obtener
            (texto,str) lista con palabras
    Salida:
            (lista,list) lista de python con palabras(colocaciones)
    '''

    def colocaciones_trigramas_texto(self,texto,N):
            if  isinstance(texto, str) and isinstance(N, int) and N>0:
                        try:
                                listaFinal=[]
                                remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
                                lista=[s.translate(remove_punctuation_map).lower() for s in nltk.word_tokenize(unicode(texto,codificacion))]
                                lista=[str(self.elimina_tildes(s)) for s in lista]
                                lista= filter(None,lista)
                                lista= filter(str.strip, lista)
                                trigrama_medidas = nltk.collocations.TrigramAssocMeasures()
                                buscador = TrigramCollocationFinder.from_words(lista)
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

    '''
    Para elementos con alto grado de colocacion, pero que son poco frecuentes, es util la
    aplicacion de filtros, tales como haciendo caso omiso de todos los bigramas/trigramas
    que se producen menos de N veces en el texto:
    '''

    def colocaciones_bigramas_filtro_texto(self,texto,N,M):
            if  isinstance(texto, str) and isinstance(N, int) and isinstance(M, int) and N>0 and M>0:
                        try:
                                listaFinal=[]
                                remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
                                lista=[s.translate(remove_punctuation_map).lower() for s in nltk.word_tokenize(unicode(texto,codificacion))]
                                lista=[str(self.elimina_tildes(s)) for s in lista]
                                lista= filter(None,lista)
                                lista= filter(str.strip, lista)
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
           

    '''
    Encontrar las N mejores colocaciones de bigramas de una lista aplicando un filtro
    Entrada:
            (N,int) El numero de mejores colocaciones a obtener
            (M,int) El numero de veces que deben de aparecer en el texto(frecuencia)
            (lista,list) lista con palabras
    Salida:
            (lista,list) lista con palabras(colocaciones)
    '''
    def colocaciones_bigramas_filtro_lista(self,lista,N,M):
            if  isinstance(lista, list) and isinstance(N, int) and isinstance(M, int) and N>0 and M>0:
                    if (all(type(x) is str for x in lista)):
                           try:
                                   listaFinal=[]
                                   remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
                                   lista=[unicode(s,codificacion) for s in lista]
                                   lista=[s.translate(remove_punctuation_map).lower() for s in lista]
                                   lista=[str(self.elimina_tildes(s)) for s in lista]
                                   lista= filter(None,lista)
                                   lista= filter(str.strip, lista)
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
            else:
                    return []

    '''
    Encontrar las N mejores colocaciones de trigramas de un texto aplicando un filtro
    Entrada:
            (N,int) El numero de mejores colocaciones a obtener
            (M,int) El numero de veces que deben de aparecer en el texto(frecuencia)
            (lista,list) lista con palabras
    Salida:
            (lista,list) lista con palabras(colocaciones)
    '''          
    def colocaciones_trigramas_filtro_texto(self,texto,N,M):
            if  isinstance(texto, str) and isinstance(N, int) and isinstance(M, int) and N>0 and M>0:
                        try:
                             listaFinal=[]
                             remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
                             lista=[s.translate(remove_punctuation_map).lower() for s in nltk.word_tokenize(unicode(texto,codificacion))]
                             lista=[str(self.elimina_tildes(s)) for s in lista]
                             lista= filter(None,lista)
                             lista= filter(str.strip, lista)
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
   

    '''
    Encontrar las N mejores colocaciones de trigramas de una lista aplicando un filtro
    Entrada:
            (N,int) El numero de mejores colocaciones a obtener
            (M,int) El numero de veces que deben de aparecer en el texto(frecuencia)
            (lista,list) lista con palabras
    Salida:
            (lista,list) lista con palabras(colocaciones)
    '''          
    def colocaciones_trigramas_filtro_lista(self,lista,N,M):
            if  isinstance(lista, list) and isinstance(N, int) and isinstance(M, int) and N>0 and M>0:
                    if (all(type(x) is str for x in lista)):
                           try:
                                   listaFinal=[]
                                   remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
                                   lista=[unicode(s,codificacion) for s in lista]
                                   lista=[s.translate(remove_punctuation_map).lower() for s in lista]
                                   lista=[str(self.elimina_tildes(s)) for s in lista]
                                   lista= filter(None,lista)
                                   lista= filter(str.strip, lista)
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
            else:
                    return []

    '''
     En la permutacion de vocales se elimina de cada palabra las consonantes y se
     consideran todas las combinaciones de vocales, cada combinacion como una
     caracteristica.

     Entrada:
            (N,int) El numero de elementos en la permutacion
            ej. influential - iueia N=5
            ej. internet - iee      N=3
            ej. transport - ao      N=2
     Salida:
            (lista,list) lista con las caracteristicas de la permutacion
    '''
    def permutacion_vocales(self,N):
            if  isinstance(N, int):
                    try:
                            lista_vocales=[]
                            for x in range(1,(N+1)):
                                for y in itertools.permutations(["a","e","i","o","u"],x):
                                    lista_vocales.append("".join(y))
                            return lista_vocales
                    except:
                            return []
            else:
                    return []
    ''' 
     Se elimina de cada palabra las consonantes y se considera la combinacion de
     vocales restantes como una caracteristica (se unen todas las vocales repetidas en
     cada combinacion).

     Entrada:
            (N,int) El numero de elementos en la combinacion
            ej. influential - iueia - iuea N=4
            ej. internet - iee - ie        N=2
            ej. transport - ao - ao        N=2
     Salida:
            (lista,list) lista con las caracteristicas de la combinacion
    '''

    def combinacion_vocales(self,N):
            if  isinstance(N, int):
                    try:
                            lista_vocales=[]
                            for x in range(1,(N+1)):
                                for y in itertools.combinations(["a","e","i","o","u"],x):
                                    lista_vocales.append("".join(y))
                            return lista_vocales
                    except:
                            return []     
            else:
                    return []
            
    '''
    Todas aquellas palabras formadas con N letras(con repeticion de letras).

    Entrada:
            (N,int) N. El numero de letras en la palabra
            (lista,list) lista con palabras

            ej. {fcommercial; difference; comforting; assistanceg} N=10
                        
     Salida:
            (lista,list) lista con las palabras de longitud definida
    '''
    def busqueda_palabra_tam_fijo(self,lista,N):
            if  isinstance(lista, list) and isinstance(N, int):
                    if (all(type(x) is str for x in lista)):
                            try:
                                    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
                                    lista=[unicode(s,codificacion) for s in lista]
                                    lista=[s.translate(remove_punctuation_map).lower() for s in lista]
                                    lista=[str(self.elimina_tildes(s)) for s in lista]
                                    lista= filter(None,lista)
                                    lista= filter(str.strip, lista)
                                    vocabulario = set(lista)
                                    palabras = [x for x in vocabulario if len(x) == N]
                                    return list(sorted(set(palabras)))
                            except TypeError:
                                    return []
                            except UnicodeDecodeError:
                                    return []        
                            except:
                                    return [] 
                    else:
                            return [] 
            else:
                    return []            

    '''
    Todas aquellas palabras formadas entre N Y m letras(con repeticion de letras).

    Entrada:
            (N,int) El numero de letras en la palabra intervalo
            (M,int) El numero de letras en la palabra intervalo
            (lista,list) lista con palabras
                        
     Salida:
            (lista,list) lista con las palabras de longitud en el intervalo
    '''

    def busqueda_palabra_tam_intervalo(self,lista,N,M):
            if  isinstance(lista, list) and isinstance(N, int) and isinstance(M, int):
                    if (all(type(x) is str for x in lista)):
                            try:
                                    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
                                    lista=[unicode(s,codificacion) for s in lista]
                                    lista=[s.translate(remove_punctuation_map).lower() for s in lista]
                                    lista=[str(self.elimina_tildes(s)) for s in lista]
                                    lista= filter(None,lista)
                                    lista= filter(str.strip, lista)
                                    vocabulario = set(lista)
                                    palabras = [x for x in vocabulario if len(x) >= N if len(x) <= M]
                                    return list(sorted(set(palabras)))
                            except TypeError:
                                    return []
                            except UnicodeDecodeError:
                                    return []     
                            except:
                                    return []     
                    else:
                            return []
            else:
                    return []

    '''
      La subcadena que precede a la base lexica de una palabra.
      ej. est - ffinest; toughest; biggestg  N=3
      ej. tion - fconfiguration; considerationg n=4

     Entrada:
            (N,int) El numero de letras que conforman al sufijo
            (lista,list) lista con palabras
                        
     Salida:
            (lista,list) lista con los sufijos encontrados en la lista
    '''
    def sufijo(self,lista,N):
            if  isinstance(lista, list) and isinstance(N, int) and N>0:
                    if (all(type(x) is str for x in lista)):
                            try:
                                    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
                                    lista=[unicode(s,codificacion) for s in lista]
                                    lista=[s.translate(remove_punctuation_map).lower() for s in lista]
                                    lista=[str(self.elimina_tildes(s)) for s in lista]
                                    lista= filter(None,lista)
                                    lista= filter(str.strip, lista)
                                    bandera=0
                                    for x in lista:
                                        if(len(x)>= N):
                                               bandera=1
                                               break
                                    if(bandera==1):
                                           resultado=[x[-N:] for x in lista if str(x[-N:])!="" if len(str(x[-N:]))== N]
                                           return list(sorted(set(resultado)))
                                    else:
                                           return []
                            except TypeError:
                                    return []
                            except UnicodeDecodeError:
                                    return []                
                            except:
                                    return []            
                    else:
                            return []
            else:
                    return []


    '''
      La subcadena que antecede a la base lexica.
      ej. ad - advance; adjunct; adulterateg N=2
      ej. de - descend; despair; dependg     N=2

      Entrada:
            (N,int) El numero de letras que conforman al prefijo
            (lista,list) lista con palabras
                        
      Salida:
            (lista,list) lista con los prefijos encontrados en la lista 
    '''

    def prefijo(self,lista,N):
            if  isinstance(lista, list) and isinstance(N, int) and N>0:
                    if (all(type(x) is str for x in lista)): 
                            try:
                                    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
                                    lista=[unicode(s,codificacion) for s in lista]
                                    lista=[s.translate(remove_punctuation_map).lower() for s in lista]
                                    lista=[str(self.elimina_tildes(s)) for s in lista]
                                    lista= filter(None,lista)
                                    lista= filter(str.strip, lista)
                                    bandera=0
                                    for x in lista:
                                        if(len(x)>= N):
                                               bandera=1
                                               break
                                    if(bandera==1):
                                           resultado=[x[:N] for x in lista if str(x[:N])!="" if len(str(x[:N]))== N ]
                                           return list(sorted(set(resultado)))
                                    else:
                                           return []

                            except TypeError:
                                    return []
                            except UnicodeDecodeError:
                                    return []             
                            except:
                                    return []        
                                    
                    else:
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
            if  isinstance(texto, basestr):
                    try:
                            vocabulario={}
                            if isinstance(texto, str):
                                texto = unicode(texto, "utf-8", "xmlcharrefreplace")
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
            else:
                    return {}


    '''
      conjunto de palabras distintivas de un texto o documento
      
      Entrada:
            (lista,list) una lista de palabras               
      Salida:
            (diccionario,dict) diccionario con las palabras y su frecuencia de
            aparicion
    '''


    def vocabulario_lista(self,lista):
            if  isinstance(lista, list):
                    if (all(type(x) is str for x in lista)):
                        try:
                               vocabulario={}
                               remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
                               lista=[unicode(s,codificacion) for s in lista]
                               lista=[s.translate(remove_punctuation_map).lower() for s in lista]
                               lista=[str(self.elimina_tildes(s)) for s in lista]
                               lista= filter(None,lista)
                               lista= filter(str.strip, lista)
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
                    else:
                           return {} 
            else:
                  return {}



    '''
      Categoria gramatical asociada a las palabras

      ej. she:PRP drove:VBD a:DT silver:NN pt:NN cruiser:NN
            PRP: Pronombre posesivo
            VBD: Verbo en pasado
            DT: Determinante
            NN: Sustantivo
      
      Entrada:
            (texto,str) cadena con las palabras a categorizar                
      Salida:
            (lista,list) lista con pares de palabra-categoria gramatical de
            todas las palabras pasadas a la funcion
    '''

    def categoria_gramatical_texto_nltk(self,texto):
            if  isinstance(texto, str):
                    try:      
                            remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
                            lista=[s.translate(remove_punctuation_map).lower() for s in nltk.word_tokenize(unicode(texto,codificacion))]
                            lista=[str(self.elimina_tildes(s)) for s in lista]
                            lista= filter(None,lista)
                            lista= filter(str.strip, lista)
                            categoria=nltk.pos_tag(lista)
                            return categoria
                    except TypeError:
                            return []
                    except UnicodeDecodeError:
                            return []    
                    except:
                            return []    
            else:
                  return []   



    '''
      Categoria gramatical asociada a las palabras

        ej. she:PRP drove:VBD a:DT silver:NN pt:NN cruiser:NN
            PRP: Pronombre posesivo
            VBD: Verbo en pasado
            DT: Determinante
            NN: Sustantivo
      
      Entrada:
            (lista,list) cadena con las palabras a categorizar                
      Salida:
            (lista,list) lista con pares de palabra-categoria gramatical de
            todas las palabras pasadas a la funcion
   '''
    def categoria_gramatical_lista_nltk(self,lista):
            if  isinstance(lista, list):
                    if (all(type(x) is str for x in lista)):
                          try:
                                  remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
                                  lista=[unicode(s,codificacion) for s in lista]
                                  lista=[s.translate(remove_punctuation_map).lower() for s in lista]
                                  lista=[str(self.elimina_tildes(s)) for s in lista]
                                  lista= filter(None,lista)
                                  lista= filter(str.strip, lista)    
                                  categoria=nltk.pos_tag(lista)
                                  return categoria
                          except TypeError:
                                    return []
                          except UnicodeDecodeError:
                                    return []       
                          except:
                                    return []
                    else:
                           return []  
            else:
                    return []



    '''
      Categoria gramatical asociada a las palabras

      ej. she:PRP drove:VBD a:DT silver:NN pt:NN cruiser:NN
            PRP: Pronombre posesivo
            VBD: Verbo en pasado
            DT: Determinante
            NN: Sustantivo
      
      Entrada:
            (cadena,str) texto. cadena con las palabras a categorizar                
      Salida:
            (lista,list) lista con pares de palabra-categoria gramatical de
            todas las palabras pasadas a la funcion
    '''
   
    def categoria_gramatical_texto_pattern(self,texto):
            if  isinstance(texto, str):
                    try:
                            remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
                            lista=[s.translate(remove_punctuation_map).lower() for s in nltk.word_tokenize(unicode(texto,codificacion))]
                            lista=[str(self.elimina_tildes(s)) for s in lista]
                            lista= filter(None,lista)
                            lista= filter(str.strip, lista)
                            textoLimpio=" ".join(lista) 
                            categorias =parse(textoLimpio)
                            listaCategoria=[]
                            for x in categorias.split():
                                for y in x:
                                        listaCategoria.append(y[0].encode('ascii','ignore')+":"+y[1].encode('ascii','ignore'))
                            return listaCategoria
                    except TypeError:
                            return []
                    except UnicodeDecodeError:
                            return []
                    except:
                            return []    
            else:
                  return []
   
    '''
      Categoria gramatical asociada a las palabras

        ej. she:PRP drove:VBD a:DT silver:NN pt:NN cruiser:NN
            PRP: Pronombre posesivo
            VBD: Verbo en pasado
            DT: Determinante
            NN: Sustantivo
      
      Entrada:
            (lista,list) lista. cadena con las palabras a categorizar                
      Salida:
            (lista,list) lista con pares de palabra-categoria gramatical de
            todas las palabras pasadas a la funcion
   '''
    def categoria_gramatical_lista_pattern(self,lista):
            if  isinstance(lista, list):
                    if (all(type(x) is str for x in lista)):
                          try:
                                  remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
                                  lista=[unicode(s,codificacion) for s in lista]
                                  lista=[s.translate(remove_punctuation_map).lower() for s in lista]
                                  lista=[str(self.elimina_tildes(s)) for s in lista]
                                  lista= filter(None,lista)
                                  lista= filter(str.strip, lista)    
                                  textoLimpio=" ".join(lista) 
                                  categorias =parse(textoLimpio)
                                  listaCategoria=[]
                                  for x in categorias.split():
                                        for y in x:
                                             listaCategoria.append(y[0].encode('ascii','ignore')+":"+y[1].encode('ascii','ignore'))
                                  return listaCategoria
                          except TypeError:
                               return []
                          except UnicodeDecodeError:
                               return []      
                          except:
                               return []
                    else:
                           return []  
            else:
                    return []

    '''
      Todas las secuencias de 3 palabras que aparecen a lo largo
      de todo el documento.

        ej. secjuencias de 3 palabras sobre el siguiente texto:

            esta es una prueba de los ngramas de palabras

            1. esta es una
            2. es una prueba
            3. una prueba de
            4. prueba de los
            5. de los ngramas
            6. los ngramas de
            7. ngramas de palabras
        
      Entrada:
            (lista,list) lista con las palabras de una oracion o texto largo
            (N,int)  numero que determina el tam del ngrama
      Salida:
            (lista,list) lista con los ngramas de tam N
   '''

    def N_gramas_texto(self,texto,N):
            if  isinstance(texto, str) and isinstance(N, int):
                    try:
                            remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
                            lista=[s.translate(remove_punctuation_map).lower() for s in nltk.word_tokenize(unicode(texto,codificacion))]
                            lista=[str(self.elimina_tildes(s)) for s in lista]
                            lista= filter(None,lista)
                            lista= filter(str.strip, lista)
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

    '''
      Todas las secuencias de 3 palabras que aparecen a lo largo
      de todo el documento.

        ej. secjuencias de 3 palabras sobre el siguiente texto:

            esta es una prueba de los ngramas de palabras

            1. esta es una
            2. es una prueba
            3. una prueba de
            4. prueba de los
            5. de los ngramas
            6. los ngramas de
            7. ngramas de palabras
        
      Entrada:
            (lista,list) lista con las palabras de una oracion o texto largo
            (N,int)  numero que determina el tam del ngrama
      Salida:
            (lista,list) lista con los ngramas de tam N
   '''

    def N_gramas_lista(self,lista,N):
            if  isinstance(lista, list) and isinstance(N, int):
                    if (all(type(x) is str for x in lista)):
                          try:
                                    listaNgrama=[]
                                    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
                                    lista=[unicode(s,codificacion) for s in lista]
                                    lista=[s.translate(remove_punctuation_map).lower() for s in lista]
                                    lista=[str(self.elimina_tildes(s)) for s in lista]
                                    lista= filter(None,lista)
                                    lista= filter(str.strip, lista)    
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
            else:
                    return []



    '''
      elementos mas frecuenctes en una cadena de texto(utilizando la frecuencia de aparicion)
      
      Entrada:
            (cadena,str) texto. cadena con las palabras 
            (N,int) numero de palabras mas frecuentes a obtener
      Salida:
            (lista,list) lista con las N palabras mas frecuentes
    '''

    def elementos_mas_frecuentes_texto(self,texto,N):
            if  isinstance(texto, str) and isinstance(N, int) and N>0:
                try:
                     listaFinal=[]
                     remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
                     lista=[s.translate(remove_punctuation_map).lower() for s in nltk.word_tokenize(unicode(texto,codificacion))]
                     lista=[str(self.elimina_tildes(s)) for s in lista]
                     lista= filter(None,lista)
                     lista= filter(str.strip, lista)
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


    '''
      elementos mas frecuenctes en una lista(utilizando la frecuencia de aparicion)
      
      Entrada:
            (lista,list) lista con las palabras de una oracion o texto largo
            (N,int) numero de palabras mas frecuentes a obtener
      Salida:
            (lista,list) lista con las N palabras mas frecuentes
    '''

    def elementos_mas_frecuentes_lista(self,lista,N):
            if  isinstance(lista, list) and isinstance(N, int) and N>0:
                try:
                     listaFinal=[]
                     remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
                     lista=[unicode(s,codificacion) for s in lista]
                     lista=[s.translate(remove_punctuation_map).lower() for s in lista]
                     lista=[str(self.elimina_tildes(s)) for s in lista]
                     lista= filter(None,lista)
                     lista= filter(str.strip, lista)
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


    '''
      elementos mas frecuenctes en un diccionario(utilizando la frecuencia de aparicion)
      
      Entrada:
            (diccionario,dict) diccionario con las palabras de una oracion o texto largo y su frecuencia de aparicion
            (N,int) numero de palabras mas frecuentes a obtener
      Salida:
            (lista,list) lista con las N palabras mas frecuentes
    '''

    def elementos_mas_frecuentes_diccionario(self,diccionario,N):
            if  isinstance(diccionario, dict) and isinstance(N, int) and N>0:
                try:
                     listaFinal=[]
                     remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
                     diccionario_llave=[unicode(k,codificacion) for k,v in diccionario.items()]
                     diccionario_llave=[s.translate(remove_punctuation_map).lower() for s in diccionario_llave]
                     diccionario_llave=[str(self.elimina_tildes(s)) for s in diccionario_llave]
                     diccionario_llave= filter(None,diccionario_llave)
                     diccionario_llave= filter(str.strip, diccionario_llave)
                     diccionario_valores=[str(v) for k,v in diccionario.items()]
                     diccionario_limpio=dict(zip(diccionario_llave,diccionario_valores ))
                     for x in Counter(diccionario_limpio).most_common(N):
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


    '''
      elementos menos frecuenctes en una cadena de texto(utilizando la frecuencia de aparicion)
      
      Entrada:
            (cadena,str) texto. cadena con las palabras 
            (N,int) numero de palabras mas frecuentes a obtener
      Salida:
            (lista,list) lista con las N palabras mas frecuentes
    '''

    def elementos_menos_frecuentes_texto(self,texto,N):
            if  isinstance(texto, str) and isinstance(N, int) and N>0:
                try:
                     listaFinal=[]
                     remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
                     lista=[s.translate(remove_punctuation_map).lower() for s in nltk.word_tokenize(unicode(texto,codificacion))]
                     lista=[str(self.elimina_tildes(s)) for s in lista]
                     lista= filter(None,lista)
                     lista= filter(str.strip, lista)
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

    '''
      elementos menos frecuenctes en una lista(utilizando la frecuencia de aparicion)
      
      Entrada:
            (lista,list) lista con las palabras de una oracion o texto largo
            (N,int) numero de palabras mas frecuentes a obtener
      Salida:
            (lista,list) lista con las N palabras mas frecuentes
    '''

    def elementos_menos_frecuentes_lista(self,lista,N):
            if  isinstance(lista, list) and isinstance(N, int) and N>0:
                try:
                     listaFinal=[]
                     remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
                     lista=[unicode(s,codificacion) for s in lista]
                     lista=[s.translate(remove_punctuation_map).lower() for s in lista]
                     lista=[str(self.elimina_tildes(s)) for s in lista]
                     lista= filter(None,lista)
                     lista= filter(str.strip, lista)
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

                
    '''
      elementos menos frecuenctes en un diccionario(utilizando la frecuencia de aparicion)
      
      Entrada:
            (diccionario,dict) diccionario con las palabras de una oracion o texto largo y su frecuencia de aparicion
            (N,int) numero de palabras mas frecuentes a obtener
      Salida:
            (lista,list) lista con las N palabras mas frecuentes
    '''

    def elementos_menos_frecuentes_diccionario(self,diccionario,N):
            if  isinstance(diccionario, dict) and isinstance(N, int) and N>0:
                try:
                     listaFinal=[]
                     remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
                     diccionario_llave=[unicode(k,codificacion) for k,v in diccionario.items()]
                     diccionario_llave=[s.translate(remove_punctuation_map).lower() for s in diccionario_llave]
                     diccionario_llave=[str(self.elimina_tildes(s)) for s in diccionario_llave]
                     diccionario_llave= filter(None,diccionario_llave)
                     diccionario_llave= filter(str.strip, diccionario_llave)
                     diccionario_valores=[str(v) for k,v in diccionario.items()]
                     diccionario_limpio=dict(zip(diccionario_llave,diccionario_valores ))
                     for x in list(reversed(Counter(diccionario_limpio).most_common()[-N:])):
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

