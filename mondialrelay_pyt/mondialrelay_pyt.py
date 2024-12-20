#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
#
#    mondialrelaiy_pyt
#    (Mondial Relay Python)
#
#    Copyright (C) 2012 Akretion
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
"""

    mondialrelay_pyt is a Python library made to interact with
    the Mondial Relay's Web Service API : WSI2_CreationEtiquette
    (http://www.mondialrelay.fr/webservice/WSI2_CreationEtiquette)

    It takes a dictionnary of values required and the format of label wanted
    and gives the tracking number, and the url to donwload the label in pdf.

"""

__author__ = "Sébastien BEAU / Aymeric LECOMTE"
__version__ = "0.1.0"
__date__ = "2012-12-06"

from unidecode import unidecode # Debian package python-unidecode


#-----------------------------------------#
#               LIBRARIES                 #
#-----------------------------------------#

from lxml import etree, objectify
from hashlib import md5
from requests.auth import HTTPBasicAuth
import requests
import re
import collections


#-----------------------------------------#
#               CONSTANTS                 #
#-----------------------------------------#

HOST= 'api.mondialrelay.com'
ENCODE = b'<?xml version="1.0" encoding="utf-8"?>'

#TODO add error code after the regex to use it in the raise
#('Enseigne',{"^[0-9A-Z]{2}[0-9A-Z]{6}$" : 30}),

MR_KEYS = collections.OrderedDict([
    ('Enseigne',"^[0-9A-Z]{2}[0-9A-Z]{6}$"),
    ('ModeCol',"^(CCC|CDR|CDS|REL)$"),
    ('ModeLiv',"^(LCC|LD1|LDS|24R|ESP|DRI)$"),
    ('NDossier',"^(|[0-9A-Z_ -]{0,15})$"),
    ('NClient',"^(|[0-9A-Z]{0,9})$"),
    ('Expe_Langage',"^[A-Z]{2}$"),
    ('Expe_Ad1',"^.{2,32}$"),
    ('Expe_Ad2',"^.{0,32}$"),
    ('Expe_Ad3',"^.{2,32}$"),
    ('Expe_Ad4',"^.{0,32}$"),
    ('Expe_Ville',"^[A-Z_\-' ]{2,26}$"),
    ('Expe_CP',"^[0-9]{5}$"),
    ('Expe_Pays',"^[A-Z]{2}$"),
    ('Expe_Tel1',"^((00|\+)33|0)[0-9][0-9]{8}$"),
    ('Expe_Tel2',"^((00|\+)33|0)[0-9][0-9]{8}$"),
    ('Expe_Mail',"^[\w\-\.\@_]{7,70}$"),
    ('Dest_Langage',"^[A-Z]{2}$"),
    ('Dest_Ad1',"^.{2,32}$"),
    ('Dest_Ad2',"^.{0,32}$"),
    ('Dest_Ad3',"^.{2,32}$"),
    ('Dest_Ad4',"^.{0,32}$"),
    ('Dest_Ville',"^[0-9A-Z_\-'., /]{0,32}$"),
    ('Dest_CP',"^[0-9]{5}$"),
    ('Dest_Pays',"^[A-Z]{2}$"),
    ('Dest_Tel1',"^((00|\+)33|0)[0-9][0-9]{8}$"),
    ('Dest_Tel2',"^((00|\+)33|0)[0-9][0-9]{8}$"),
    ('Dest_Mail',"^[\w\-\.\@_]{7,70}$"),
    ('Poids',"^[0-9]{3,7}$"),
    ('Longueur',"^[0-9]{0,3}$"),
    ('Taille',"^{0}$"),
    ('NbColis',"^[0-9]{1,2}$"),
    ('CRT_Valeur',"^[0-9]{1,7}$"),
    ('CRT_Devise',"^(|EUR)$"),
    ('EXP_Valeur',"^[0-9]{0,7}$"),
    ('EXP_Devise',"^(|EUR)$"),
    ('COL_Rel_Pays',"^[A-Z]{2}$"),
    ('COL_Rel',"^(|[0-9]{6})$"),
    ('LIV_Rel_Pays',"^[A-Z]{2}$"),
    ('LIV_Rel',"^(|[0-9]{6})$"),
    ('TAvisage',"^(|O|N)$"),
    ('TReprise',"^(|O|N)$"),
    ('Montage',"^(|[0-9]{1,3})$"),
    ('TRDV',"^(|O|N)$"),
    ('Assurance',"^(|[0-9A-Z]{1})$"),
    ('Instructions',"^[0-9A-Z_\-'., /]{0,31}"),
    ('Texte',"^([^<>&']{3,30})(\(cr\)[^<>&']{0,30})")
    ])

API_ERRORS_MESSAGE = {  
    -1: "Critical Error Severe System Error. Please, contact the Service Center.",
    10000: "Critical Error 10001 Critical Error Invalid user and/or password. Check the authentication information.",
    10002: "Critical Error A general error occurred while checking configuration."
        "Check that the customerId field is correctly filled.",
    10003: "Critical Error A general error occurred while checking configuration." 
        "Check that the culture field is correctly filled.",
    10004: "Critical Error A general error occurred while checking configuration." 
        "Check that the VersionAPI field is correctly filled.",
    10005: "Critical Error A general error occurred while checking configuration. Unknown customer Id.",
    10006: "Critical Error A general error occurred while checking configuration. Unknown culture.",
    10007: "Critical Error A general error occurred while checking configuration. Unknown VersionAPI.",
    10008: "Warning Unknown outputFormat. Statement ignored.",
    10009: "Error No output type defined in the output options.",
    10010: "Error Invalid output type defined in the output options.",
    10011: "Error A general error occurred while checking shipments List."
        "No shipment entity defined in the request."
        "A request must contain at least one return element.",
    10012: "Error No sender information defined in the shipment request.",
    10013: "Error No receiver information defined in the shipment request.",
    10014: "Warning Invalid order number. Statement ignored. A general error occurred during authentication." 
        "Check that the login or/and password are correctly filled.Error",
    10015: "Warning Invalid customer reference defined in the shipment entity. Statement ignored.",
    10016: "Error No parcel count defined in the shipment entity.",
    10017: "Error Invalid parcel count.",
    10018: "Warning Invalid amount defined in the shipment. Statement ignored.",
    10019: "Warning Invalid shipmentValue defined in the shipment. Statement ignored.",
    10020: "Warning Invalid currency. Statement ignored.",
    10021: "Warning Invalid option key. Statement ignored.",
    10022: "Warning Invalid option value. Statement ignored.",
    10023: "Error No delivery mode defined in the request.",
    10024: "Error Invalid delivery mode defined in the request.",
    10025: "Warning Invalid location for the delivery mode. Statement ignored.",
    10026: "Error No Collection Mode defined in the request.",
    10027: "Error Invalid Collection Mode defined in the request.",
    10028: "Warning Invalid location for the collection mode. Statement ignored.",
    10029: "Warning Invalid content. Statement ignored.",
    10030: "Warning Invalid length. Statement ignored.",
    10031: "Warning Invalid width. Statement ignored.",
    10032: "Warning Invalid depth. Statement ignored.",
    10033: "Error No weight defined in the parcel element.",
    10034: "Error Invalid weight.",
    10035: "Warning Invalid delivery Instruction. Statement ignored.",
    10036: "Warning Invalid Title defined in the address. Statement ignored.",
    10037: "Warning Invalid first name defined in the address. Statement ignored.",
    10038: "Warning Invalid last name defined in the address. Statement ignored.",
    10039: "Error Invalid street name defined in the address.",
    10040: "Error No street name defined in the address.",
    10041: "Warning Invalid house Number defined in the address. Statement ignored.",
    10042: "Error Invalid country code defined in the address.",
    10043: "Error No country code defined in the address.",
    10044: "Error Invalid postcode defined in the address.",
    10045: "Error No postcode defined in the address.",
    10046: "Error Invalid city defined in the address.",
    10047: "Error No city defined in the address.",
    10048: "Warning Invalid Additional address field 1 defined in the address. Statement ignored.",
    10049: "Warning Invalid Additional address field 2 defined in the address. Statement ignored.",
    10050: "Warning Invalid Additional address field 3 defined in the address. Statement ignored.",
    10051: "Warning Invalid phone number defined in the address. Statement ignored.",
    10052: "Warning Invalid mobile number defined in the address. Statement ignored.",
    10053: "Warning Invalid email defined in the address. Statement ignored.",
    10054: "Error Unknown address.",
    10055: "Error Unable to determine transportation plan for this sender address.",
    10056: "Error Unable to determine transportation plan for this receiver address.",
    10057: "Error Routing is not needed. No routing will be created.",
    10058: "Error Routing not completed.",
    10059: "Error Routing denied.",
    10060: "Error Label could not be generated for this request.",
    10061: "Error Not Well-formed XML request.",
    10062: "Warning Title + FirstName + LastName should not be greater than 30 characters.",
    10063: "Error HouseNo + StreetName should not be greater than 30 characters.Error",
    10065: "Error The number of parcel elements is different from the parcelCount defined in the shipment.",
    10066: "Error A general error occurred while checking configuration. No access right.",
    10067: "Error No configuration for your business.",
    10068: "Error Unable to get the partner barcode.",
    10069: "Warning Postal code modified by the partner for routing purpose.",
    10070: "Error Multi parcels forbidden for this product code.",
    10071: "Error Collection location not found.",
    10072: "Error Location not allowed for your business. Please refer to your binding agreement.",
    10073: "Error Location not allowed for this shipment.",
    10074: "Error No allowed location for this product code.",
    10075: "Error Llocation not allowed for this product code.",
    10076: "Error Unauthorized option for this product code.",
    10077: "Error No compatible label for this printer.",
    10078: "Error No available label for this shipment.",
    10079: "Error Invalid country code for your customer settings.",
    10080: "Error PDF File unavailable.",
    10081: "Error Unable to join the partner.",
    99998: "Error XML Parse error. This error will return the specific reason of the reject."
        "You can check your XML request via the XML validator link specify in the policy part.",
    99999: "Critical Error An error occurred. Please contact the Service Center.",
}

#------------------------------------------#
#       Mondial Relay WEBService           #
#        WSI2_CreationEtiquette            #
#------------------------------------------#

class MRWebService(object):

    def __init__(self, security_key):
        self.security_key = security_key

    def valid_dict(self, dico):
        ''' Get a dictionnary, check if all required fields are provided,
        and if the values correpond to the required format.'''

        mandatory = [
            'Enseigne',
            'ModeCol',
            'ModeLiv',
            'Expe_Langage',
            'Expe_Ad1',
            'Expe_Ad3',
            'Expe_Ville',
            'Expe_CP',
            'Expe_Pays',
            'Expe_Tel1',
            'Dest_Langage',
            'Dest_Ad1',
            'Dest_Ad3',
            'Dest_Ville',
            'Dest_CP',
            'Dest_Pays',
            'Poids',
            'NbColis',
            'CRT_Valeur',
            ]


        if ('ModeLiv' or 'ModeCol') not in dico:
            raise Exception('The given dictionnary is not valid.')

        for element in dico:
            if element not in MR_KEYS:
                raise Exception('Key %s not valid in given dictionnary' %element)
            formt = MR_KEYS[element]
            #if dico[element] and re.match(formt, dico[element].upper()) == None:
            #    raise Exception('Value %s not valid in given dictionary, key %s, expected format %s' %(dico[element],element, MR_KEYS[element]))

        if dico['ModeLiv'] == "24R":
            mandatory.insert(19,'LIV_Rel')
            mandatory.insert(19,'LIV_Rel_Pays')
        if dico['ModeCol'] == "REL":
            mandatory.insert(19,'COL_Rel')
            mandatory.insert(19,'COL_Rel_Pays')
        if dico['ModeLiv'] == "LDS":
            mandatory.insert(16,'Dest_Tel1')

        for mandatkey in mandatory:
            if mandatkey not in dico:
                raise Exception('Mandatory key %s not given in the dictionnary' %mandatkey)

        return True

    #------------------------------------#
    #      functions to clean the xml    #
    #------------------------------------#

    def clean_xmlrequest(self, xml_string):
        ''' [XML REQUEST]
        Ugly hardcode to get ride of specifics headers declarations or namespaces instances.
        Used in the xml before sending the request.
        See http://lxml.de/tutorial.html#namespaces or http://effbot.org/zone/element-namespaces.htm
        to improve the library and manage namespaces properly '''

        env=b'<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'+b' xmlns:xsd="http://www.w3.org/2001/XMLSchema"'+b' xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
        wsietiq=b'<WSI2_CreationEtiquette xmlns="http://www.mondialrelay.fr/webservice/">'

        str1 = xml_string.replace(b'soapBody',b'soap:Body').replace(b'soapEnvelope',b'soap:Envelope')
        str2 = str1.replace(b'<soap:Envelope>',env)
        str3 = str2.replace(b'<WSI2_CreationEtiquette>',wsietiq)

        return str3

    def clean_xmlresponse(self, xml_string):
        ''' [XML RESPONSE]
        Ugly hardcode to get ride of specifics headers declarations or namespaces instances.
        Used in the xml after receiving the response.
        See http://lxml.de/tutorial.html#namespaces or http://effbot.org/zone/element-namespaces.htm
        to improve the library and manage namespaces properly '''

        head = b' xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"'
        env = b'soap:Envelope'
        body= b'soap:Body'
        xmlns=b' xmlns="http://www.mondialrelay.fr/webservice/"'

        str1 = xml_string.replace(head,b'').replace(env,b'soapEnvelope').replace(body,b'soapBody').replace(xmlns,b'')
        str2 = str1.replace(ENCODE,b'')

        return str2

    #------------------------------------#
    #    functions to manage the xml     #
    #------------------------------------#

    def create_xmlrequest(self, vals):
        '''[XML REQUEST]
        Creates an xml tree fitted to the soap request to WSI2_CreationEtiquette,
        from the given dictionnary. All dictionnary's keys must correspond to a field to pass.

        IN = Dictionnary
        OUT = XML (as an utf-8 encoded string) ready to send a request '''

        #check if the given dictionnary is correct to make an xml
        mandat_dic = MRWebService.valid_dict(self, vals)

        #initialisation of future md5key
        security = ""

        # beginning of the xml tree, to be modified later with soapclean_xml()
        envl = etree.Element('soapEnvelope')
        body = etree.SubElement(envl, 'soapBody')
        wsi2_crea = etree.SubElement(body,'WSI2_CreationEtiquette')

        # xml elements creation
        for key in MR_KEYS:
           if key != 'Texte':
                xml_element = etree.SubElement(wsi2_crea,key)
                xml_element.text = vals.get(key, '')
                security += vals.get(key,'')

        # generates <Security/> xml element
        security+=self.security_key
        md5secu = md5(security.encode('utf-8')).hexdigest().upper()

        xml_security = etree.SubElement(wsi2_crea, "Security" )
        xml_security.text = md5secu

        # add <Text/> last xml element if present, not included in security key
        if 'Texte' in vals:
            xml_element = etree.SubElement(wsi2_crea,"Texte")
            xml_element.text = vals['Texte']

        # generates and modifies the xml tree to obtain an apropriate xml soap string
        xmltostring = etree.tostring(envl, encoding='utf-8', pretty_print=True)
        xmlrequest = MRWebService.clean_xmlrequest(self,xmltostring)
        return xmlrequest

    def sendsoaprequest(self, xml_string, store):
        ''' Send the POST request to the Web Service.
        IN = proper xml-string
        OUT = response from the Web Service, in an xml-string utf-8'''

        header = {
            'POST': '/Web_Services.asmx',
            'Host': HOST,
            'Content-Type': 'text/xml',
            'charset': 'utf-8',
            'Content-Lenght': 'Lenght',
            'SOAPAction': 'http://www.mondialrelay.fr/webservice/WSI2_CreationEtiquette',
        }
        
        url="https://api.mondialrelay.com/Web_Services.asmx"
        response=requests.post(url,headers=header, data=xml_string, auth=(store,self.security_key))

        return response.content

    def parsexmlresponse(self,soap_response):
        ''' Parse the response given by the WebService.
        Extract and returns all fields' datas.
        IN = xml-string utf-8 returned by Mondial Relay
        OUT : Dictionnary or Error'''

        strresp = soap_response
        strresp = strresp.replace(ENCODE,b'')
        tree= etree.fromstring(strresp)
        string = etree.tostring(tree, pretty_print=True, encoding='utf-8')

        response =  MRWebService.clean_xmlresponse(self, soap_response)
        soapEnvelope = objectify.fromstring(response)

        #---------------Parsing---------------#
        stat = soapEnvelope.soapBody.WSI2_CreationEtiquetteResponse.WSI2_CreationEtiquetteResult.STAT

        if stat == 0:
            NumExpe = soapEnvelope.soapBody.WSI2_CreationEtiquetteResponse.WSI2_CreationEtiquetteResult.ExpeditionNum
            urlpdf = 'https://' + HOST.replace('api', 'www') + str(soapEnvelope.soapBody.WSI2_CreationEtiquetteResponse.WSI2_CreationEtiquetteResult.URL_Etiquette)
            resultat={'STAT':stat,'ExpeditionNum':NumExpe,'URL_Etiquette':urlpdf}
        else:
            resultat={'STAT':stat}
            explanation = API_ERRORS_MESSAGE.get(stat)
            raise Exception('The server returned %s . The mondial relay documentation says %s' % (stat,explanation))

        return resultat
        #TOFIX ?
        return True

    #------------------------------------#
    #       FUNCTION TO CALL             #
    #------------------------------------#
    def make_shipping_label(self, dictionnary, labelformat="A4"):
        ''' FUNCTION TO CALL TO GET DATAS WANTED FROM THE WEB SERVICE
        IN = Dictionnary with corresponding keys (see MR_Keys or Mondial Relay's Documentation)
        OUT = Raise an error with indications (see MR Doc for numbers correspondances)
        or Expedition Number and URL to PDF'''

        #MondialRelay api required only ascii in uppercase
        for key in dictionnary:
            dictionnary[key] = unidecode(dictionnary[key]).upper()

        xmlstring = MRWebService.create_xmlrequest(self, dictionnary)

        storename=dictionnary['Enseigne']
        resp = MRWebService.sendsoaprequest(self,xmlstring, storename)

        result = MRWebService.parsexmlresponse(self,resp)
        url = result['URL_Etiquette']

        #switch url if default format is not A4
        if labelformat == 'A5':
            url = url.replace('format=A4','format=A5')
        if labelformat == '10x15':
            url = url.replace('format=A4','format=10x15')

        final = {
                'ExpeditionNum': result['ExpeditionNum'],
                'URL_Etiquette': url,
                'format':labelformat,
                }

        return final

