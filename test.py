from mondialrelay_pyt import make_shipping_label

with open("api_pw.token") as f:
            api_pw=f.read().strip('\n')

dico = {
        "Login": "BDTEST@business-api.mondialrelay.com",
        "Password": api_pw,
        "CustomerId": "BDTEST",
        "Culture": "fr-FR",
        "OutputFormat": "10x15",
        "OrderNo": "test01",
        "CustomerNo": "cust01",
        "DeliveryMode": "24R",
        "DeliveryLocation": "FR-33105",
        "CollectionMode": "REL",
        "ParcelWeight": 350,
        "SenderStreetname": "rue des Ajoncs",
        "SenderHouseNo": 21,
        "SenderCountryCode": "FR",
        "SenderPostCode": "59000",
        "SenderCity": "Lille",
        "SenderAddressAdd1": "Jean Voimoncolis",
        # "SenderAddressAdd2": "",
        # "SenderAddressAdd3": "",
        "SenderPhoneNo": "+33687654321",
        "SenderEmail": "jv@email.com",
        "RecipientStreetname": "rue des acacias",
        "RecipientHouseNo": 3,
        "RecipientCountryCode": "FR",
        "RecipientPostCode": "14000",
        "RecipientCity": "Caen",
        "RecipientAddressAdd1": "Jean Michmuch",
        #RecipientAddressAdd2": "",
        # "RecipientAddressAdd3": "",
        "RecipientPhoneNo": "0033612345678",
        "RecipientEmail": "jeanmichmuch@email.com",

}

#print dico

reqst = make_shipping_label(dico)

print (reqst)
