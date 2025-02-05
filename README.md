mondialrelay_pyt
========

A Python library to access Mondial Relay API V2 (WEB SERVICE DUAL CARRIER), in order to create shipping labels for outbound/return parcels.

## Installation

Install it using pip. In a terminal :  

    pip install mondialrelay-pyt

## Usage 
Call make_shipping_label() function from mondialrelay_pyt giving it a dictionary.

The dictionary must contain the following keys:  

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


The dictionary can contain the following optional keys :

    "OrderNo",
    "CustomerNo",
    "SenderHouseNo",
    "SenderAdressAdd2",
    "SenderAdressAdd3",
    "SenderPhoneNo",
    "SenderEmail",
    "RecipientHouseNo",
    "RecipientAdressAdd2",
    "RecipientAdressAdd3",
    "RecipientPhoneNo",
    "RecipientEmail",

Check the Mondial Relay documentation to see the expected values.

## API Documentation  
Mondial Relay API V2 documentation :
https://www.mondialrelay.fr/media/123861/web-service-dual-carrier-v-27.pdf

## Credits:
This is a fork from initial Akretion mondialrelay_pyt, made by Sébastien BEAU and Aymeric LECOMTE, thanks for their work that helped me a lot. This fork was made by Henri DEWILDE.

## Copyright and License

mondialrelay_pyt is copyright (c) 2012 Akretion

mondialrelay_pyt is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

mondialrelay_pyt is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public
License along with mondialrelay_pyt. If not, see [GNU licenses](http://www.gnu.org/licenses/).
