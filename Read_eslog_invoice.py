# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 12:29:15 2022

@author: tomazk

eSlog 2.0 računi: https://www.epos.si/eslog

"""

        
"""
BG-25	INVOICE LINE

    BT-126	Invoice line identifier                    /Invoice/M_INVOIC/G_SG26/S_LIN/D_1082
    BT-127	Invoice line note	                       /Invoice/M_INVOIC/G_SG26/S_FTX[D_4451='ACB']/C_C108/D_4440
    BT-129	Invoiced quantity	                       /Invoice/M_INVOIC/G_SG26/S_QTY[C_C186/D_6063='47']/C_C186/D_6060
    BT-130	Invoiced quantity unit of measure	       /Invoice/M_INVOIC/G_SG26/S_QTY[C_C186/D_6063='47']/C_C186/D_6411
    BT-131	Invoice line net amount	                   /Invoice/M_INVOIC/G_SG26/G_SG27[S_MOA/C_C516/D_5025='203']/S_MOA/C_C516/D_5004
    BT-133	Invoice line Buyer accounting reference	   /Invoice/M_INVOIC/G_SG26/G_SG30[S_RFF/C_C506/D_1153='AWQ']/S_RFF/C_C506/D_1154


NBG-03  INVOICE LINE NATIONAL EXTENSION

    NBT-031	Invoice line net amount including VAT	    /Invoice/M_INVOIC/G_SG26/G_SG27[S_MOA/C_C516/D_5025='38']/S_MOA/C_C516/D_5004
    NBT-032	Invoice line VAT category taxable amount	/Invoice/M_INVOIC/G_SG26/G_SG34[S_TAX/D_5283='7' and S_TAX/C_C241/D_5153='VAT']/S_MOA[C_C516/D_5025='125']/C_C516/D_5004
    NBT-033	Invoice line VAT category tax amount	    /Invoice/M_INVOIC/G_SG26/G_SG34[S_TAX/D_5283='7' and S_TAX/C_C241/D_5153='VAT']/S_MOA[C_C516/D_5025='124']/C_C516/D_5004


BG-31	ITEM INFORMATION

    BT-153	Item name	 	              /Invoice/M_INVOIC/G_SG26/S_IMD[D_7077='F']/C_C273/D_7008
    BT-155	Item Seller's identifier	  /Invoice/M_INVOIC/G_SG26/S_PIA[D_4347='5']/C_C212[D_7143='SA']/D_7140
    BT-156	Item Buyer's identifier	 	 /Invoice/M_INVOIC/G_SG26/S_PIA[D_4347='5']/C_C212[D_7143='IN']/D_7140
    BT-157	Item standard identifier	 /Invoice/M_INVOIC/G_SG26/S_LIN/C_C212/D_7140



"""


import xmltodict
import pandas as pd
import os
# import pypyodbc

path = r"/Users/tomazkastrun/Documents/01-work/Eslog/invoices"


col_name = ['Invoice_num','Invoice_date', 'Invoice_pay_date','Invoice_line', 
            'Invoiced_quantity', 'Invoice_unit_measure','Item_name', 'Invoice_line_net_amount',
            'Invoice_line_buyer_ref','Invoice_lineVat_Tax',
            'Invoice_Date_from','Invoice_date_to','Invoice_line_net_price','Invoice_line_tax_perc'] 
 
df = pd.DataFrame(columns = col_name)

for filename in os.listdir(path):
    #print(filename)
    pot = path + "/" + filename
    with open(pot) as fd:
        podatki = xmltodict.parse(fd.read())
        dx = podatki['Invoice']['M_INVOIC']
        
        Invoice_number = dx['S_BGM']['C_C106']['D_1004']

        a = dx['S_DTM']
        for dictionary in a:
            if dictionary['C_C507']['D_2005'] == '137':
                Invoice_issue_date = dictionary['C_C507']['D_2380']
    
        a = dx['G_SG8']
        if (a['S_PAT']['D_4279'] == '1' and a['S_DTM']['C_C507']['D_2005'] == '13' ):
            Invoice_payment_duedate = a['S_DTM']['C_C507']['D_2380']
          
        a = dx['G_SG26']
        
        for dictionary in a:
            #line identifier
            line_identifier = dictionary['S_LIN']['D_1082']
     
            #Invoiced quantity
            if (dictionary['S_QTY']['C_C186']['D_6063'] == '47'):
                Invoiced_quantity = dictionary['S_QTY']['C_C186']['D_6060']
 
            #Invoiced unit of measure
            if (dictionary['S_QTY']['C_C186']['D_6063'] == '47'):
                invoice_unit_measure = dictionary['S_QTY']['C_C186']['D_6411']

            # Invoice line net amount
           # if (dictionary['G_SG27']['S_MOA']['C_C516']['D_5025'] == '203'):
           #     Invoice_line_net_amount = dictionary['G_SG27']['S_MOA']['C_C516']['D_5004']
        
    		  if len(dictionary['G_SG27']) > 1:
                for key in dictionary['G_SG27']:
                   if (key['S_MOA']['C_C516']['D_5025'] == '203'):
                      Invoice_line_net_amount = key['S_MOA']['C_C516']['D_5004']
    
        
            # Invoice line Buyer accounting reference	
            if (dictionary['G_SG30']['S_RFF']['C_C506']['D_1153'] == 'AVE'): #AWQ
                invoice_line_buyer_ref = dictionary['G_SG30']['S_RFF']['C_C506']['D_1154']
        
            # Invoice line net amount including VAT        
            # if (dictionary['G_SG27']['S_MOA']['C_C516']['D_5025'] =='38'):
            #     Invoice_line_net_amountVAT = dictionary['G_SG27']['S_MOA']['C_C516']['D_5004']
        
            # Invoice line VAT category taxable amount 
            if (dictionary['G_SG34']['S_TAX']['D_5283'] =='7' and dictionary['G_SG34']['S_TAX']['C_C241']['D_5153'] == 'VAT' ):
                invoice_lineVat_Tax = dictionary['G_SG27']['S_MOA']['C_C516']['D_5004']
        
            # Item name 
            if (dictionary['S_IMD']['D_7077'] =='F'):
                item_name = dictionary['S_IMD']['C_C273']['D_7008']
        
            # Datum od
            if (dictionary['S_DTM'][0]['C_C507']['D_2005'] == '167'):
                Invoice_Date_from  = dictionary['S_DTM'][0]['C_C507']['D_2380']
        
            # datum do
            if (dictionary['S_DTM'][1]['C_C507']['D_2005'] == '168'):
                Invoice_date_to = dictionary['S_DTM'][1]['C_C507']['D_2380']
        
        # neto cena postavke
            if(dictionary['G_SG29']['S_PRI']['C_C509']['D_5125'] == 'AAA'):
                Invoice_line_net_price = dictionary['G_SG29']['S_PRI']['C_C509']['D_5118']
        
        # Stopnja DDV zaračunane postavke
        # /Invoice/M_INVOIC/G_SG26/G_SG34[S_TAX/D_5283='7' and  S_TAX/C_C241/D_5153='VAT']/S_TAX/C_C243/D_5278
            if (dictionary['G_SG34']['S_TAX']['D_5283'] =='7' and dictionary['G_SG34']['S_TAX']['C_C241']['D_5153'] == 'VAT' ):
                Invoice_line_tax_perc = dictionary['G_SG34']['S_TAX']['C_C243']['D_5278']
                
                
            df = df.append({'Invoice_num': Invoice_number, 'Invoice_date': Invoice_issue_date,
                        'Invoice_pay_date': Invoice_payment_duedate, 'Invoice_line': line_identifier,
                        'Invoiced_quantity': Invoiced_quantity, 'Invoice_unit_measure': invoice_unit_measure,
                        'Item_name': item_name, 'Invoice_line_net_amount': Invoice_line_net_amount,
                        'Invoice_line_buyer_ref': invoice_line_buyer_ref,
                        'Invoice_lineVat_Tax': invoice_lineVat_Tax, 'Invoice_Date_from': Invoice_Date_from,
                        'Invoice_date_to': Invoice_date_to, 'Invoice_line_net_price': Invoice_line_net_price,
                        'Invoice_line_tax_perc': Invoice_line_tax_perc}, ignore_index=True)
         
                
