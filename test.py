for filename in os.listdir(path):
    #print(filename)
    pot = path + "\\" + filename
    with open(pot) as fd:
        if filename.endswith('xml'):
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
    
            # prodajalec
            a = dx['G_SG2']
            for dictionary in a:
                if (dictionary['S_NAD']['D_3035'] == 'SE'):
                    Name_seller = dictionary['S_NAD']['C_C080']['D_3036']
            
            
            a = dx['G_SG26']
            #line identifies
            try:
                b = a['S_LIN']
                b = 1
            except:
                b = 2    
            if (b == 1):
                line_identifier = a['S_LIN']['D_1082']
                
                if (a['S_QTY']['C_C186']['D_6063'] == '47'):
                    Invoiced_quantity = a['S_QTY']['C_C186']['D_6060']
                
                if (a['S_QTY']['C_C186']['D_6063'] == '47'):
                    invoice_unit_measure = a['S_QTY']['C_C186']['D_6411']
                    
            else:
                for dictionary in a:
                    line_identifier = dictionary['S_LIN']['D_1082']
                    
    
                    #Invoiced quantity
                    if (dictionary['S_QTY']['C_C186']['D_6063'] == '47'):
                        Invoiced_quantity = dictionary['S_QTY']['C_C186']['D_6060']
                        
                        
                    #Invoiced unit of measure
                    if (dictionary['S_QTY']['C_C186']['D_6063'] == '47'):
                        invoice_unit_measure = dictionary['S_QTY']['C_C186']['D_6411']
    
            df = df.append({'Invoice_num': Invoice_number, 'pot': pot, 
                           'Invoice_issue_date':Invoice_issue_date ,'Invoice_payment_duedate':Invoice_payment_duedate, 
                           'Name_seller':Name_seller, 'line_identifier':line_identifier,
                           'Invoiced_quantity':Invoiced_quantity,'invoice_unit_measure':invoice_unit_measure}, ignore_index=True)
