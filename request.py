#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
sortOrder = 1
#lucky us for less security atm, simple cookie usage from browser login is possible
cookies = dict(XTCsid='cookie here')
#domain no trailing slash
domain = 'http://domain here'

def setPropertySettings(prop_id):
    global domain
    url = domain + '/admin/request_port.php?module=PropertiesCombisAdmin&action=save&type=combis_settings'
    payload = {
        'properties_dropdown_mode': 'dropdown_mode_1',
        'properties_show_price': 'true',
        'use_properties_combis_weight': 0,
        'use_properties_combis_quantity': 3,
        'use_properties_combis_shipping_time': 0,
        'products_id': prop_id
    }
    r = requests.post(url, allow_redirects=True, cookies=cookies, data=payload)
    print r.text
    return;

def createPropertiesValue (prop, ele, silverP):
    global domain
    url = domain + '/admin/request_port.php?module=PropertiesAdmin&action=save&type=properties_values'
    payload = {
        'values_name[de]': ele['name'],
        'values_name[en]': ele['name_en'],
        'sort_order': ele['sort'],
        'value_model': ele['abr'],
        'value_price': 0.00,
        'properties_id': prop,
        'properties_values_id': 0
    }
    if  (silverP > 0):
        payload['value_price'] = silverP
    r = requests.post(url, allow_redirects=True, cookies=cookies, data=payload)
    ret = json.loads(r.text)['properties_values_id']['properties_values_id']
    return ret
    
def presetProperties (prod_id, props):
    global domain
    url = domain + '/admin/request_port.php?module=PropertiesCombisAdmin&action=save&type=admin_select'
    payload = {
        'products_id': prod_id,
        #'properties_values_ids_array[2][]':[33, 34, 35, 36, 37, 38, 39, 40],
        #'properties_values_ids_array[50][]':[125, 126, 127],
    }
    for prop in props:
        sendlist = []
        for i in prop[1]:
            sendlist.append(i)
            pass
        payload['properties_values_ids_array['+ str(prop[0]) +'][]'] = sendlist
        pass
    requests.post(url, allow_redirects=True, cookies=cookies, data=payload)
    return;

def createProperties (name, silverP):
    propval = []
    global domain
    url = domain + '/admin/request_port.php?module=PropertiesAdmin&action=save&type=properties'
    payload = {
        'properties_name[de]': 'Material',
        'properties_admin_name[de]': 'M_' + name,
        'properties_name[en]': 'material',
        'properties_admin_name[en]': 'M_' + name,
        'sort_order': '2',
        'properties_id': '0'
    }
    r = requests.post(url, allow_redirects=True, cookies=cookies, data=payload)
    prop = json.loads(r.text)['properties_id']
    print "Property: " + str(prop)
    propval.append(createPropertiesValue(prop, {'name': 'Aluminium', 'name_en': 'aluminium', 'sort': 1, 'abr': 'Al'}, 0))
    propval.append(createPropertiesValue(prop, {'name': 'Edelstahl', 'name_en': 'stainless steel', 'sort': 2, 'abr': 'Es'}, 0))
    propval.append(createPropertiesValue(prop, {'name': 'Silber', 'name_en': 'silver', 'sort': 3, 'abr': 'Si'}, silverP))
    print "Values: " + str(propval)
    return [prop, propval];

def sendPost (properties, prod_id):
    global cookies
    global sortOrder
    print properties
    global domain
    url = domain + '/admin/request_port.php?module=PropertiesCombisAdmin&action=save&type=combis'
    payload = {
        'sort_order':sortOrder,
        'combi_quantity':0,
        'combi_price':0.00,
        'vpe_value':0.00,
        'properties_values[]':properties,
        'combi_price_type':'calc',
        'products_vpe_id':0,
        'combi_shipping_status_id':0,
        'products_id':prod_id,
        'products_properties_combis_id':0
    }
    r = requests.post(url, allow_redirects=True, cookies=cookies, data=payload)
    print r.text
    sortOrder += 1
    return;

#Kette
def setComb(prod_id, length, colours, name, silverP):
    global sortOrder
    sortOrder = 1
    prop = createProperties(name, silverP)
    presetProperties(prod_id, [prop, [1, length], [2, colours]])
    for l in length:
        sendPost([prop[1][0],64,l], prod_id) # Alu Blank
        for c in colours:
            sendPost([prop[1][0],c,l], prod_id)
            pass
        sendPost([prop[1][1],64,l], prod_id) #Edelstahl Ohne
        sendPost([prop[1][1],34,l], prod_id) #Edelstahl Bronze
        sendPost([prop[1][2],64,l], prod_id) #Silber Ohne
        pass
    setPropertySettings(prod_id)

def setCombNoLength(prod_id, colours, name, silverP):
    global sortOrder
    sortOrder = 1
    prop = createProperties(name, silverP)
    presetProperties(prod_id, [prop, [2, colours]])
    sendPost([prop[1][0],64], prod_id) # Alu Blank
    for c in colours:
        sendPost([prop[1][0],c], prod_id)
        pass
    sendPost([prop[1][1],64], prod_id) #Edelstahl Ohne
    sendPost([prop[1][1],34], prod_id) #Edelstahl Bronze
    sendPost([prop[1][2],64], prod_id) #Silber Ohne
    setPropertySettings(prod_id)

def setCombNoLengthNoColour(prod_id, name, silverP):
    global sortOrder
    sortOrder = 1
    prop = createProperties(name, silverP)
    presetProperties(prod_id, [prop])
    sendPost([prop[1][0],64], prod_id) # Alu Blank
    sendPost([prop[1][1],64], prod_id) #Edelstahl Ohne
    sendPost([prop[1][1],34], prod_id) #Edelstahl Bronze
    sendPost([prop[1][2],64], prod_id) #Silber Ohne
    setPropertySettings(prod_id)

#size: 11-24
#Mat: 61-63
#col: 33-40, 64
#Hals alle Farben
setComb(29, xrange(11,25), xrange(33,41), 'Back_and_Forth', 45 ) #all colour
#setComb(8, xrange(11,25), xrange(33,41) ) #all colour
#setComb(9, xrange(11,25), xrange(33,41) ) #all colour
#setComb(14, xrange(11,25), xrange(33,41) ) #all colour
#setComb(30, xrange(11,25), xrange(33,41) ) #all colour
#setComb(4, xrange(11,25), xrange(33,41) ) #all colour
#setComb(5, xrange(11,25), xrange(33,41) ) #all colour
#setComb(13, xrange(11,25), xrange(33,41) ) #all colour
#setComb(6, xrange(11,25), xrange(33,41) ) #all colour
#setComb(2, xrange(11,25), xrange(33,41) ) #all colour
#setComb(31, xrange(11,25), xrange(33,41) ) #all colour

#Hals begrenzte Farben
#setComb(12, xrange(33,41), [33, 35, 36, 38, 40]) #some colour
#setComb(11, xrange(33,41), [33, 35, 36, 38, 40]) #some colour
#setComb(7, xrange(33,41), [33, 35, 36, 38, 40]) #some colour
#setComb(10, xrange(33,41), [33, 35, 36, 38, 40]) #some colour
#setComb(3, xrange(33,41), [33, 35, 36, 38, 40]) #some colour

#Armband alle Farben
#setComb(21, xrange(25,32), xrange(33,41) ) #all colour
#setComb(20, xrange(25,32), xrange(33,41) ) #all colour
#setComb(19, xrange(25,32), xrange(33,41) ) #all colour

#Ohrringe alle Farben
#setCombNoLengthNoColour(16, xrange(33,41) ) #all colour
#setCombNoLengthNoColour(17, xrange(33,41) ) #all colour
#setCombNoLengthNoColour(18, xrange(33,41) ) #all colour
#setCombNoLength(15, range(33,41), 'Barrel_drop' ) #all colour

#Schlüsselanhänger alle Farben
###setCombNoLengthNoColour(25, [7,8,10] ) #all colour // kein Silber
###setCombNoLengthNoColour(26, [7,8,10] ) #all colour // kein Silber
###setCombNoLengthNoColour(28, [7,8,10] ) #all colour // kein Silber
###setCombNoLengthNoColour(27, [7,8,10] ) #all colour // kein Silber