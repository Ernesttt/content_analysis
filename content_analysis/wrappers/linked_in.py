from linkedin import linkedin #pip install -I linkedin
from oauthlib import *
import math
import codecs


class linkedin_Python:
    
    #Constructor
    def __init__(self,CONSUMER_KEY,CONSUMER_SECRET,USER_TOKEN,USER_SECRET,RETURN_URL):
        self.auth = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET, 
                                USER_TOKEN, USER_SECRET, 
                                RETURN_URL, 
                                permissions=linkedin.PERMISSIONS.enums.values())
        self.app = linkedin.LinkedInApplication(self.auth)
        


    def busqueda_de_industrias(self,elementosClave,archivo):

        '''
              get information about industries from Linkedin
              
              In:
                    (elementosClave, text) search topic
                    (archivo, text) name of the file to save the information about industries  
              Out:


              Company search API (busqueda de industrias)

            <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                <company-search>
                  <companies total="4493" count="10" start="0">
                    <company>
                      <id>162479</id>
                      <name>Apple Inc.</name>
                      <logo-url>http://media.linkedin.com/mpr/mpr/p/2/000/082/2e6/39570d2.png</logo-url>
                      <type>Public Company</type>
                </company>
                <company>
                      <id>1276</id>
                      <name>Apple Retail</name>
                      <logo-url>http://media.linkedin.com/mpr/mpr/p/2/000/039/353/3e84d05.png</logo-url>
                      <type>Public Company</type>
                </company>
                </company-search>


                Elementos que se pueden recuperar del perfil publico
                    *id
                    *name
                    *universal-name
                    *email-domains
                    *description
                    *specialties

                mayor referencia: http://developer.linkedin.com/documents/company-search       
        '''

        selectors=[{"companies": ['name', 'type',"website-url","email-domains","locations:(address:(city))","description","num-followers"]}]
        params={}
        params["keywords"]=elementosClave;
        params["start"]=0
        params["count"]=20
        resultadoBusqueda=self.app.search_company(selectors,params)
        numeroResultados=resultadoBusqueda["companies"]["_total"]
        # no hubo resultados de la busqueda de linkedin
        if (numeroResultados==0):
            print "no hay resultados asociados a la busqueda"
            return
        # hay resultados de la busqueda y el rango de la pagina cubre todos los valores 
        elif(numeroResultados >0 and numeroResultados <= 20):
            print "numero de resultados asociados a la consulta: "+str(numeroResultados)
            for x in  resultadoBusqueda["companies"]["values"]:
                        if "name" in x:         nombre=x["name"]
                        else:                   nombre="---"
                        if "type" in x:         tipo=x["type"]
                        else:                   tipo="---"
                        if "websiteUrl" in x:   URL=x["websiteUrl"]
                        else:                   URL="---"
                        if "description" in x:
                                                descripcion=x["description"]
                                                descripcionLimpia=(descripcion.replace("\n", "")).replace("\r","")
                        else:                   descripcionLimpia="---"
                        if "numFollowers" in x: seguidores=x["numFollowers"]
                        else:                   seguidores="---"
                        listaCorreo=[]
                        listaCiudades=[]
                        if not "emailDomains" in x: listaCorreo.append("---")
                        else:                   
                                if (x["emailDomains"]["_total"]==0):
                                    listaCorreo.append("---")
                                else:
                                     for y in x["emailDomains"]["values"]:
                                        listaCorreo.append(y)
                        if not "locations" in x: listaCiudades.append("---")
                        else:         
                                if (x["locations"]["_total"]==0):
                                    listaCiudades.append("---")
                                else:
                                        for y in x["locations"]["values"]:
                                                for v in y["address"]:
                                                    listaCiudades.append(y["address"]["city"])                      
                        try:
                            archivoEscritura=codecs.open(archivo,"a","utf8")
                            archivoEscritura.write(",".join(elementosClave)+"/|/"+nombre+"/|/"+tipo+"/|/"+URL+"/|/"+str(seguidores)+"/|/"+descripcionLimpia+"/|/"+",".join(listaCiudades)+"/|/"+",".join(listaCorreo)+"\n")
                        finally:
                            archivoEscritura.close()
            
        # hay resultados de la busqueda y el rango de la pagina no cubre todos los valores  
        else:
                # numero de veces que se cargaran paginas con resultados
                numeroPaginas= int(math.ceil(numeroResultados/float(20)))
                print "numero de resultados asociados a la consulta: "+str(numeroResultados)
                for x in range(0, numeroResultados, 20):
                    print "pagina a cargar: "+ str(x)
                    params["start"]=x
                    params["count"]=20
                    resultadoBusqueda2=self.app.search_company(selectors,params)
                    for x in  resultadoBusqueda2["companies"]["values"]:
                        if "name" in x:         nombre=x["name"]
                        else:                   nombre="---"
                        if "type" in x:         tipo=x["type"]
                        else:                   tipo="---"
                        if "websiteUrl" in x:   URL=x["websiteUrl"]
                        else:                   URL="---"
                        if "description" in x:
                                                descripcion=x["description"]
                                                descripcionLimpia=(descripcion.replace("\n", "")).replace("\r","")
                        else:                   descripcionLimpia="---"
                        if "numFollowers" in x: seguidores=x["numFollowers"]
                        else:                   seguidores="---"
                        listaCorreo=[]
                        listaCiudades=[]
                        if not "emailDomains" in x: listaCorreo.append("---")
                        else:                   
                                if (x["emailDomains"]["_total"]==0):
                                    listaCorreo.append("---")
                                else:
                                     for y in x["emailDomains"]["values"]:
                                        listaCorreo.append(y)

                        if not "locations" in x: listaCiudades.append("---")
                        else:         
                                if (x["locations"]["_total"]==0):
                                    listaCiudades.append("---")
                                else:
                                        for y in x["locations"]["values"]:
                                                for v in y["address"]:
                                                     listaCiudades.append(y["address"]["city"])                       
                        try:
                            archivoEscritura=codecs.open(archivo,"a","utf8")
                            archivoEscritura.write(",".join(elementosClave)+"/|/"+nombre+"/|/"+tipo+"/|/"+URL+"/|/"+str(seguidores)+"/|/"+descripcionLimpia+"/|/"+",".join(listaCiudades)+"/|/"+",".join(listaCorreo)+"\n")
                        finally:
                            archivoEscritura.close()                       



    def busqueda_de_trabajo(self,elementosClave,archivo):

        '''
              get information about jobs from Linkedin
              
              In:
                    (elementosClave, text) search topic
                    (archivo, text) name of the file to save the information about jobs  
              Out:

              Job Search API (busqueda de trabajo)

            <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                <job-search>
                    <jobs count="10" start="0">
                <job>
                <id>1547469</id>
              <company>
              </company>
              <compensation>
                <salary>
                    <pay-interval>
                   </pay-interval>
                </salary>
                  </compensation>
                <job-poster>
             <id>S-TTGn8IK9</id>
             <first-name>Heather</first-name>
             <last-name>Cavanagh</last-name>
             <headline>Legal Recruitment Administrator at SNR Denton
             </job-poster>
            <description-snippet>Position Description:SNR Denton US LLP is seeking an Associate for the Real Estate group for the New York office. Candidates should have 1-2 years real estate or related experience. Candidates with real estate lending experience are preferred. Who to Contact:Please submit resume, cover letter and law school transcript to heather.cavanagh@snrdenton.com</description-snippet>
            <location-description>Greater New York City Area</location-description>
        </job>
        </job-search>

        Elementos que se pueden recuperar del perfil publico
           *company-name
           *job-title
           *country-code
           *postal-code
                    
        '''
        selectors=[{"jobs": ["salary",'company','description-snippet', 'location-description',"site-job-url","position:(job-functions)"]}]
        params={}
        params["keywords"]=elementosClave;
        params["start"]=0
        params["count"]=20
        resultadoBusqueda=self.app.search_job(selectors,params)
        numeroResultados=resultadoBusqueda["jobs"]["_total"]
        # no hubo resultados de la busqueda de linkedin
        if (numeroResultados==0):
            print "no hay resultados asociados a la busqueda"
            return
        # hay resultados de la busqueda y el rango de la pagina cubre todos los valores 
        elif(numeroResultados >0 and numeroResultados <= 20):
            print "numero de resultados asociados a la consulta: "+str(numeroResultados)
            for x in  resultadoBusqueda["jobs"]["values"]:
                 if "salary" in x:               salario=x["salary"]
                 else:                           salario="---"
                 if "company" in x:              industria=x["company"]["name"]
                 else:                           industria="---"
                 if "description-snippet" in x:
                                                 descripcion=x["description-snippet"]
                                                 descripcionLimpia=(descripcion.replace("\n", "")).replace("\r","")
                 else:                           descripcionLimpia="---"
                 if "location-description" in x: locacion=x["location-description"]
                 else:                           locacion="---"
                 if "site-job-url" in x:         URL=x["site-job-url"]
                 else:                           URL="---"
                 listaFunciones=[]
                 if not "position" in x: listaFunciones.append("---")
                 else:    
                        if (x["position"]["jobFunctions"]["_total"]==0):
                                listaFunciones.append("---")
                        else:
                            for z in x["position"]["jobFunctions"]["values"]:
                                listaFunciones.append(z["name"])
                 try:
                          archivoEscritura=codecs.open(archivo,"a","utf8")
                          archivoEscritura.write(",".join(elementosClave)+"/|/"+industria+"/|/"+locacion+"/|/"+URL+"/|/"+descripcionLimpia+"/|/"+",".join(listaFunciones)+"/|/"+str(salario)+"\n")
                 finally:
                          archivoEscritura.close()
                          
        # hay resultados de la busqueda y el rango de la pagina no cubre todos los valores  
        else:
                print "numero de resultados asociados a la consulta: "+str(numeroResultados)
                for x in range(0, numeroResultados, 20):
                    print "pagina a cargar: "+ str(x)
                    params["start"]=x
                    params["count"]=20
                    resultadoBusqueda2=self.app.search_job(selectors,params)
                    for x in  resultadoBusqueda2["jobs"]["values"]:
                        
                        if "salary" in x:               salario=x["salary"]
                        else:                           salario="---"
                        if "company" in x:              industria=x["company"]["name"]
                        else:                           industria="---"
                        if "description-snippet" in x:
                                                        descripcion=x["description-snippet"]
                                                        descripcionLimpia=(descripcion.replace("\n", "")).replace("\r","")
                        else:                           descripcionLimpia="---"
                        if "location-description" in x: locacion=x["location-description"]
                        else:                           locacion="---"
                        if "site-job-url" in x:         URL=x["site-job-url"]
                        else:                           URL="---"
                        listaFunciones=[]
                        if not "position" in x: listaFunciones.append("---")
                        else:    
                                if (x["position"]["jobFunctions"]["_total"]==0):
                                    listaFunciones.append("---")
                                else:
                                    for z in x["position"]["jobFunctions"]["values"]:
                                        listaFunciones.append(z["name"])
                        try:
                                  archivoEscritura=codecs.open(archivo,"a","utf8")
                                  archivoEscritura.write(",".join(elementosClave)+"/|/"+industria+"/|/"+locacion+"/|/"+URL+"/|/"+descripcionLimpia+"/|/"+",".join(listaFunciones)+"/|/"+salario+"\n")
                        finally:
                                  archivoEscritura.close()


    def busqueda_de_personas(self,elementosClave,archivo):


        '''
              get information about users from Linkedin
              
              In:
                    (elementosClave, text) search topic
                    (archivo, text) name of the file to save the information about users 
              Out:

              People Search API(busqueda de personas)

        <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <people-search>
          <people total="100" count="10" start="0">
            <person>
              <id>tePXJ3SX1o</id>
              <first-name>Clair</first-name>
              <last-name>Standish</last-name>
            </person>
            <person>
              <id>pcfBxmL_Vv</id>
              <first-name>John</first-name>
              <last-name>Bender</last-name>
            </person>
     
          </people>
          <num-results>108</num-results>
        </people-search>


        Elementos para la busqueda:
            *keywords
            *first-name
            *last-name
            *company-name
            *current-company
            *title
            *current-title
            *school-name
            *current-school
            *country-code
            *postal-code

        Elementos que se pueden recuperar del perfil publico
            *id
            *first-name
            *last-name
            *headline
            *num-connections

        mayor referencia: http://developer.linkedin.com/documents/profile-fields  
                    
        '''
                
        selectors=[{'people': ['first-name', 'last-name',"headline","industry","location","summary","public-profile-url"]}]
        params={}
        params["keywords"]=elementosClave;
        params["start"]=0
        params["count"]=20
        resultadoBusqueda=self.app.search_profile(selectors,params)
        numeroResultados=resultadoBusqueda["people"]["_total"]  
        # no hubo resultados de la busqueda de linkedin
        if (numeroResultados==0):
            print "no hay resultados asociados a la busqueda"
            return
        # hay resultados de la busqueda y el rango de la pagina cubre todos los valores 
        elif(numeroResultados >0 and numeroResultados <= 20):
            print "numero de resultados asociados a la consulta: "+str(numeroResultados)
            for x in  resultadoBusqueda["people"]["values"]:

                 if "firstName" in x:            nombre=x["firstName"]
                 else:                           nombre="---"
                 if "lastName" in x:             apellido=x["lastName"]
                 else:                           apellido="---"
                 if "headline" in x:             titulo=x["headline"]
                 else:                           titulo="---"
                 if "industry" in x:             industria=x["industry"]
                 else:                           industria="---"
                 if "publicProfileUrl" in x:     URL=x["publicProfileUrl"]
                 else:                           URL="---"
                 if "location" in x:             localizacion=x["location"]["name"]
                 else:                           localizacion="---"
                 if "summary" in x:
                                                 descripcion=x["summary"]
                                                 descripcionLimpia=(descripcion.replace("\n", "")).replace("\r","")
                 else:                           descripcionLimpia="---"
                 

                 try:
                          archivoEscritura=codecs.open(archivo,"a","utf8")
                          archivoEscritura.write(",".join(elementosClave)+"/|/"+nombre+"/|/"+apellido+"/|/"+titulo+"/|/"+industria+"/|/"+URL+"/|/"+descripcionLimpia+"/|/"+localizacion+"\n")
                 finally:
                          archivoEscritura.close()
         # hay resultados de la busqueda y el rango de la pagina no cubre todos los valores  
        else:
                print "numero de resultados asociados a la consulta: "+str(numeroResultados)
                for x in range(0, numeroResultados, 20):
                    print "pagina a cargar: "+ str(x)
                    params["start"]=x
                    params["count"]=20
                    resultadoBusqueda2=self.app.search_profile(selectors,params)
                    for x in  resultadoBusqueda2["people"]["values"]:
                        
                         if "firstName" in x:            nombre=x["firstName"]
                         else:                           nombre="---"
                         if "lastName" in x:             apellido=x["lastName"]
                         else:                           apellido="---"
                         if "headline" in x:             titulo=x["headline"]
                         else:                           titulo="---"
                         if "industry" in x:             industria=x["industry"]
                         else:                           industria="---"
                         if "publicProfileUrl" in x:     URL=x["publicProfileUrl"]
                         else:                           URL="---"
                         if "location" in x:             localizacion=x["location"]["name"]
                         else:                           localizacion="---"
                         if "summary" in x:
                                                         descripcion=x["summary"]
                                                         descripcionLimpia=(descripcion.replace("\n", "")).replace("\r","")
                         else:                           descripcionLimpia="---"

                         try:
                                archivoEscritura=codecs.open(archivo,"a","utf8")
                                archivoEscritura.write(",".join(elementosClave)+"/|/"+nombre+"/|/"+apellido+"/|/"+titulo+"/|/"+industria+"/|/"+URL+"/|/"+descripcionLimpia+"/|/"+localizacion+"\n")
                         finally:
                                archivoEscritura.close()




'''
Caso de uso
                                          
prueba = linkedin_Python('759ddboxufrx91','Bh1H672fM2unXbeA','6bda7fe3-3858-4440-8310-19c2a4a0d62a','43e3938e-e7b7-4a2e-8f0a-a49d6c502d26','')
prueba.busqueda_de_industrias(["finanzas"],"personas.txt")

''' 
