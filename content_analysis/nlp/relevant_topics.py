import codecs
import sys
from metrics_reduced import *

metricas = Metricas()
CODIFICACION = "utf-8"

sustantivos = ['NN', 'NNS', 'NNP', 'NNPS']
verbos = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
adjetivos = ['JJ','JJR','JJS']
articulos =['DT']
conjunciones = ['IN', 'CC']
adverbios = ['RB','RBR', 'RBS']

class Topicos_Relevantes:
  
    #Constructor
    def __init__(self):   
            pass

        
    def __call__(self):
            self.__init__


    def leer_texto(self, nombre):
            '''Read a txt file 
            
            In: (nombre, str) name of the file
            Out: (texto, text) text of the readed file coded in UTF-8
            '''
            try:
                try:
                        texto = ""
                        archivo_texto = codecs.open(nombre,"r",CODIFICACION)
                        linea = archivo_texto.readline()
                        while linea:
                              texto = texto + linea
                              linea = archivo_texto.readline()
                        return texto
                finally:
                        archivo_texto.close()
            except IOError:
                    print ("IOError")
                    

    def construcciones_sintacticas_bigramas(self, texto):
            '''Obtain particular sintactic constructions for n-best bigrams
            
            In: (texto, str) name of the file
            Out: (lista, list) list of the n-best sintactic constructions
            '''
            lista = texto.split()
            if len(lista) < 1000:
                N = 50 
            else:
                N = 20
            lista = []
            bigramas  = metricas.colocaciones_bigramas_filtro_texto(texto, N, 1)
            for bigrama in bigramas:
                categoria= metricas.categoria_gramatical_texto_pattern(bigrama)
                if (categoria[0].split(':')[1] in sustantivos):
                   if ((categoria[1].split(':')[1] in (sustantivos or adjetivos))):
                      lista.append(bigrama)
                if ((categoria[0].split(':')[1] in (adjetivos)) or (categoria[1].split(':')[1] in adjetivos)):
                   if (categoria[1].split(':')[1] in sustantivos):  
                      lista.append(bigrama)
            return lista
     
     
     

    def construcciones_sintacticas_trigramas(self, texto):
            '''Obtain particular sintactic constructions for n-best trigrams
            
            In: (texto, str) name of the file
            Out: (lista, list) list of the n-best sintactic constructions
            '''
            lista = texto.split()
            if len(lista) < 1000:
                N = 100 
            else:
                N = 50
            lista = []
            trigramas  = metricas.colocaciones_trigramas_filtro_texto(texto, N, 1)
            for trigrama in trigramas:
                categoria= metricas.categoria_gramatical_texto_pattern(trigrama)
                if (categoria[0].split(':')[1] in sustantivos):
                   if (categoria[1].split(':')[1] in verbos):
                      if (categoria[2].split(':')[1] in (adverbios or sustantivos)):
                         lista.append(trigrama)
                   if (categoria[1].split(':')[1] in conjunciones):
                      if (categoria[2].split(':')[1] in sustantivos):
                         lista.append(trigrama)
                if (categoria[0].split(':')[1] in articulos):
                   if (categoria[1].split(':')[1] in sustantivos):
                      if (categoria[2].split(':')[1] in adjetivos):
                         lista.append(trigrama)
            return lista
          