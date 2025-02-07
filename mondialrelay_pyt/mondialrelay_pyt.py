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
    the Mondial Relay's Web Service API V2: WEB SERVICE DUAL CARRIER
    (https://connect-api.mondialrelay.com/api/shipment)

    It takes a dictionnary of values required and the format of label wanted
    and gives the tracking number, and the url to donwload the label in pdf.

"""

__author__ = "Sébastien BEAU / Aymeric LECOMTE / Henri DEWILDE"
__version__ = "0.2.2"
__date__ = "2025-02-05"


#-----------------------------------------#
#               LIBRARIES                 #
#-----------------------------------------#

import requests
import xmltodict


#-----------------------------------------#
#               CONSTANTS                 #
#-----------------------------------------#

# HOST= 'connect-api-sandbox.mondialrelay.com'
HOST= 'connect-api.mondialrelay.com'
ENCODE = b'<?xml version="1.0" encoding="utf-8"?>'

#TODO add error code after the regex to use it in the raise
#('Enseigne',{"^[0-9A-Z]{2}[0-9A-Z]{6}$" : 30}),

MR_KEYS = {
    "Login": "",
    "Password": "",
    "CustomerId": "^[0-9A-Z]{2}[0-9A-Z ]{6}$",
    "Culture": "^[a-z]{2}-[A-Z]{2}$",
    "OutputFormat": "^(10x15|A4|A5)$",
    "OrderNo": "^(|[0-9A-Z_-]{0,15})$",
    "CustomerNo": "^(|[0-9A-Z]{0,9})$",
    "DeliveryMode": "^(LCC|HOM|HOC|LD1|LDS|24R|24L|HOX)$",
    "DeliveryLocation": "^[0-9A-Z]{0,10}$",
    "CollectionMode": "^(CCC|CDR|CDS|REL)$",
    "ParcelWeight": "^[0-9]{0,10}$",
    "SenderStreetname": "^[0-9A-Z_\-'., /]{0,30}$",
    "SenderHouseNo": "^[0-9A-Z_\-'., /]{0,10}$",
    "SenderCountryCode": "^[A-Z]{2}$",
    "SenderPostCode": "^[A-Za-z_\-' ]{2,25}$",
    "SenderCity": "^[A-Za-z_\-' ]{2,30}$",
    "SenderAddressAdd1": "^[0-9A-Z_\-'., /]{0,30}$",
    "SenderAddressAdd2": "^[0-9A-Z_\-'., /]{0,30}$",
    "SenderAddressAdd3": "^[0-9A-Z_\-'., /]{0,30}$",
    "SenderPhoneNo": "^((00|\+)33|0)[0-9][0-9]{8}$",
    "SenderEmail": "^[\w\-\.\@_]{7,70}$",
    "RecipientStreetname": "^[0-9A-Z_\-'., /]{0,30}$",
    "RecipientHouseNo": "^[0-9A-Z_\-'., /]{0,10}$",
    "RecipientCountryCode": "^[A-Z]{2}$",
    "RecipientPostCode": "^[A-Za-z_\-' ]{2,25}$",
    "RecipientCity": "^[A-Za-z_\-' ]{2,30}$",
    "RecipientAddressAdd1": "^[0-9A-Z_\-'., /]{0,30}$",
    "RecipientAddressAdd2": "^[0-9A-Z_\-'., /]{0,30}$",
    "RecipientAddressAdd3": "^[0-9A-Z_\-'., /]{0,30}$",
    "RecipientPhoneNo": "^((00|\+)33|0)[0-9][0-9]{8}$",
    "RecipientEmail": "j^[\w\-\.\@_]{7,70}$",
}


#------------------------------------------#
#       Mondial Relay WEBService           #
#------------------------------------------#
def valid_dict(input_dict):
    """ Get a dictionnary, check if all required fields are provided.
    Return a valid dictionnary, formated to the Mondial Relay standards.
    """

    mandatory_keys = (
        "Login", 
        "Password", 
        "CustomerId", 
        "Culture", 
        "OutputFormat",
        "DeliveryMode", 
        "DeliveryLocation", 
        "CollectionMode", 
        "ParcelWeight",
        "SenderStreetname",
        "SenderPostCode",
        "SenderCity",
        "SenderAddressAdd1",
        "SenderCountryCode",
        "RecipientStreetname",
        "RecipientPostCode",
        "RecipientCity",
        "RecipientAddressAdd1",
        "RecipientCountryCode",
    )

    optional_shipment_keys = (
        "OrderNo",
        "CustomerNo",
    )

    optional_sender_keys = (
        "SenderHouseNo",
        "SenderAdressAdd2",
        "SenderAdressAdd3",
        "SenderPhoneNo",
        "SenderEmail",
    )

    optional_recipient_keys = (
        "RecipientHouseNo",
        "RecipientAdressAdd2",
        "RecipientAdressAdd3",
        "RecipientPhoneNo",
        "RecipientEmail",
    )

    for key in mandatory_keys:
            if key not in input_dict:
                raise Exception('Mandatory key %s not given in the dictionnary' %key)
            
    formated_dict = {
        "ShipmentCreationRequest": {
            "Context": {
                "Login": input_dict["Login"],
                "Password": input_dict["Password"],
                "CustomerId": input_dict["CustomerId"],
                "Culture": input_dict["Culture"],
                "VersionAPI": "1.0",
            },
            "OutputOptions": {
                "OutputFormat": input_dict["OutputFormat"],
                "OutputType": "PdfUrl",
            },
            "ShipmentsList": {
                "Shipment": {
                    "ParcelCount": 1,
                    "DeliveryMode": {   
                        "@Mode": input_dict["DeliveryMode"],
                        "@Location": input_dict["DeliveryLocation"],            
                    },
                    "CollectionMode": {
                        "@Mode": input_dict["CollectionMode"],            
                    },
                    "Parcels": {                       
                        "Parcel": {
                            "Weight": {
                                "@Value": input_dict["ParcelWeight"],
                                "@Unit": "gr"
                            },
                        },
                    },
                    "Sender": {
                        "Address": {
                            "Streetname": input_dict["SenderStreetname"],
                            "CountryCode": input_dict["SenderCountryCode"],
                            "PostCode": input_dict["SenderPostCode"],
                            "City": input_dict["SenderCity"],
                            "AddressAdd1": input_dict["SenderAddressAdd1"],
                        },
                    },
                    "Recipient": {
                        "Address": {
                            "Streetname": input_dict["RecipientStreetname"],
                            "CountryCode": input_dict["RecipientCountryCode"],
                            "PostCode": input_dict["RecipientPostCode"],
                            "City": input_dict["RecipientCity"],
                            "AddressAdd1": input_dict["RecipientAddressAdd1"],
                        },
                    },
                },
            },
        },
    }

    # Check if optional keys are given
    for input_key, input_value in input_dict.items():
        if input_key in optional_shipment_keys:
            formated_dict["ShipmentCreationRequest"]["ShipmentsList"]["Shipment"][input_key] = input_value

        if input_key in optional_sender_keys:
            formated_dict["ShipmentCreationRequest"]["ShipmentsList"]["Shipment"]["Sender"]["Address"][input_key] = input_value

        if input_key in optional_recipient_keys:
            formated_dict["ShipmentCreationRequest"]["ShipmentsList"]["Shipment"]["Recipient"]["Address"][input_key] = input_value
            
    return formated_dict


#------------------------------------#
#      functions to clean the xml    #
#------------------------------------#

def clean_xmlrequest(xml_string):
    """ [XML REQUEST]
    Ugly hardcode to get ride of specifics headers declarations or namespaces instances.
    Used in the xml before sending the request.
    See http://lxml.de/tutorial.html#namespaces or http://effbot.org/zone/element-namespaces.htm
    to improve the library and manage namespaces properly 
    """

    env='<ShipmentCreationRequest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://www.example.org/Request">'
    
    return xml_string.replace('<ShipmentCreationRequest>',env)


#------------------------------------#
#    functions to manage the xml     #
#------------------------------------#

def sendxmlrequest(xml_string):
    """ Send the POST request to the Web Service.
    IN = proper xml-string
    OUT = response from the Web Service, in an xml-string utf-8
    """

    header = {
        'Content-Type': 'text/xml',
        'charset': 'utf-8',
        'Accept': 'application/xml',
    }
    
    url="https://" + HOST + "/api/shipment"

    response=requests.post(url, headers=header, data=xml_string)

    return response.content


def parsexmlresponse(response):
    """ Parse the response given by the WebService.
    Extract and returns all fields' datas.
    IN = xml-string utf-8 returned by Mondial Relay
    OUT : Dictionnary or Error
    """

    result_dict = xmltodict.parse(response, process_namespaces=True, namespaces={'http://www.example.org/Response': None})

    print(result_dict)

    # If the server returned an error
    if result_dict["ShipmentCreationResponse"]["StatusList"] is not None and "Status" in result_dict["ShipmentCreationResponse"]["StatusList"]:
        status_data = result_dict["ShipmentCreationResponse"]["StatusList"]["Status"]
        if isinstance(status_data, dict):  # If a sigle status is returned as a dict, we transform it in a list to uniform the data treatment
            status_data = [status_data] 

        for status in status_data:
            if status["@Level"] == "Error":
                error_code = status["@Code"]
                error_message = status["@Message"]
                raise Exception(f"The server returned error {error_code} : {error_message}")

    final_dict = {
        "ShipmentNumber": result_dict["ShipmentCreationResponse"]["ShipmentsList"]["Shipment"]["@ShipmentNumber"],
        "Url": result_dict["ShipmentCreationResponse"]["ShipmentsList"]["Shipment"]["LabelList"]["Label"]["Output"],
    }

    return final_dict


#------------------------------------#
#       FUNCTION TO CALL             #
#------------------------------------#
def make_shipping_label(dictionnary):
    """ FUNCTION TO CALL TO GET DATAS WANTED FROM THE WEB SERVICE
    IN = Dictionnary with corresponding keys (see MR_Keys or Mondial Relay's Documentation)
    OUT = Raise an error with indications 
    or Expedition Number and URL to PDF
    """

    dictionnary = valid_dict(dictionnary)

    xmlstring = xmltodict.unparse(dictionnary, pretty=True)

    xmlstring = clean_xmlrequest(xmlstring)

    response = sendxmlrequest(xmlstring)

    result = parsexmlresponse(response)

    return result
