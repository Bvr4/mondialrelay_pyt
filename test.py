#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import collections
from mondialrelay_pyt import make_shipping_label

with open("api_pw.token") as f:
            api_pw=f.read().strip('\n')

dico = collections.OrderedDict()

dico["Context"] = {
        "Login": "BDTEST@business-api.mondialrelay.com",
        "Password": api_pw,
        "CustomerId": "BDTEST",
        "Culture": "fr-FR",
        "VersionAPI": "1.0",
    }


dico["OutputOptions"] = {
        "OutputFormat": "10x15",
        "OutputType": "PdfUrl",
    }

dico["Shipment"] = {
        "ORderNo": "test01",
        "CustomerNo": "cust01",
        "ParcelCount": 1,
        "DeliveryMode": {
            "Mode": "24R",
            "Location": "78857",            
        },
        "CollectionMode": {
            "Mode": "REL",            
        },
        "Parcel": {
            "Weight": {
                "Value": 350,
            },
        },
        "DeliveryInstruction": "door code : 0000",
    }

dico["Address"] = {
        "StreetName": "rue des acacias",
        "HouseNo": 3,
        "CountryCode": "FR",
        "Postcode": "14000",
        "City": "Caen",
        "AddressAdd1": "Jean Michmuch",
        # "AdressAdd2": "",
        # "AdressAdd3": "",
        "PhoneNo": "0033612345678",
        "email": "jeanmichmuch@email.com"
    }



dico_old = {
        'Enseigne':'BDTEST13',
        'ModeCol':'CCC',
        'ModeLiv':'LCC',
        'NDossier':'1234',
        'NClient':'123456789',
        'Expe_Langage':'FR',
        'Expe_Ad1':'M.KALIF',
        #'Expe_Ad2':,
        'Expe_Ad3':'rue dailleurs',
        #'Expe_Ad4':,
        'Expe_Ville':'Machin Ville',
        'Expe_CP':'69100',
        'Expe_Pays':'FR',
        'Expe_Tel1':'0033445566778',
        #'Expe_Tel2':,
        #'Expe_Mail':,
        'Dest_Langage':'FR',
        'Dest_Ad1':'M.KALIF',
        ##'Dest_Ad2':,
        'Dest_Ad3':'414 BD DES CANUTS',
        #'Dest_Ad4':'etjebougeraipas',
        'Dest_Ville':'LYON',
        'Dest_CP':'69300',
        'Dest_Pays':'FR',
        'Dest_Tel1':'0033409887766',
        #'Dest_Tel2':,
        #'Dest_Mail':,
        'Poids':'30000',
        'Longueur':'145',
        #'Taille':,
        'NbColis':'1',
        'CRT_Valeur':'0',
        #'CRT_Devise':,
        #'EXP_Valeur':,
        #'EXP_Devise':,
        #'COL_Rel_Pays':,
        #'COL_Rel':,
        'LIV_Rel_Pays':'FR',
        'LIV_Rel':'78857',
        #'TAvisage':,
        #'TReprise':,
        #'Montage':,
        #'TRDV':,
        #'Assurance':,
        #'Instructions':,
        #'Texte':,
    }

#dico['ModeLiv'] = 'LDS'
#dico['ModeCol'] = 'CCC'

#print dico

response = '<?xml version="1.0" encoding="utf-8"?>\
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"\
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\
 xmlns:xsd="http://www.w3.org/2001/XMLSchema">\
<soap:Body><WSI2_CreationEtiquetteResponse\
 xmlns="http://www.mondialrelay.fr/webservice/">\
<WSI2_CreationEtiquetteResult><STAT>0</STAT>\
<ExpeditionNum>17193867</ExpeditionNum>\
<URL_Etiquette>/PDF/StickerMaker2.aspx?ens=BDTEST1211&amp;expedition=17193867&amp;lg=FR&amp;\
format=A4&amp;crc=9579B14BCF9FA5B894A27A952DD90CC7</URL_Etiquette>\
</WSI2_CreationEtiquetteResult></WSI2_CreationEtiquetteResponse></soap:Body></soap:Envelope>'


reqst = make_shipping_label(dico)

print (reqst)
