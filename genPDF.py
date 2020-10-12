import pandas as pd
import numpy as np
def readFile(fileName):
    data = pd.read_csv(fileName)
    return(data)

def createFile(downPayment, interestRate,cap,comps):

    #read file and remove listings with no cap rate or
    df = readFile("output.csv")
    df['CapRate'].replace('nan', np.nan, inplace=True)
    df.dropna(subset=['CapRate'], inplace=True)

    #drop rows with no tax data
    df = df[df.TaxMonthlyTotal != 0.0]

    #drop rows with low cap rate
    df = df[df.CapRate >= cap]
    df = df[df.CapRate <= 15]

    #drop rows with only 1 comp
    df = df[df.NumComps >= comps]

    #rounding numbers to look nice
    df['CapRate'] = df['CapRate'].apply(lambda x: round(x, 2))
    df['MonthlyProfit'] = df['MonthlyProfit'].apply(lambda x: round(x, 2))
    df['TaxMonthlyTotal'] = df['TaxMonthlyTotal'].apply(lambda x: round(x, 2))
    df['CompAvgRentRevenue'] = df['CompAvgRentRevenue'].apply(lambda x: round(x, 2))
    df['CompAvgSqFt'] = df['CompAvgSqFt'].apply(lambda x: round(x, 2))


    #sort by cap rate high to low
    df.sort_values("CapRate", inplace=True, ascending=False)

    #title
    payload = "<center><h1>---------- Search 07/01/20 ----------</h1>Copyright Paytape Inc.<br><hr><h3>Invested Amount: $"+str(downPayment)+"</h3><h3>Interest Rate: "+str(interestRate)+"%</h3><hr></center>"
    a = 'FILTERS: <b>CapRate >'+str(cap)+'%</b>   -   <b>Min '+str(comps)+' Comps</b>   -   <b>Omit Listings With Incomplete Information</b><hr>'
    payload = payload+a

    #create HTML object per listing
    def createObject(MLSNumber, city, price, age, size,bedroom,bathroom,hoa,mortgage,tax,rev,profit,cap,compsize, compage, yearbuilt,numComps):
        a = "<h2>MLS Listing ID: "+MLSNumber+"</h2>"
        aa = "<a href=https://www.altarealtyco.com/pages/403986/prop_search/mlsid_"+MLSNumber+">View Property</a><br><br>"
        bb = "<b>Location: </b>"+city+" ,VA<br>"
        b = "<h3>Listing Price: $"+str(price)+"</h3>"
        c = "<b>On Market For: </b>"+str(age)+"<br>"
        d = "<b>Size: </b>"+str(size)+" Sq Ft<br>"
        e = "<b>Rooms: </b>"+str(bedroom)+" Br "+str(bathroom)+" Ba<br>"
        ee = "<b>Year Built: </b>"+str(yearbuilt)
        f = "<h2>Financials:</h2>"
        g = "<table><tbody><tr><td>Monthly HOA Fee</td><td>$"+str(hoa)+"</td></tr><tr><td>Monthly Mortgage Payment</td><td>$"+str(mortgage)+"</td></tr><tr><td>Monthly Taxes</td><td>$"+str(tax)+"</td></tr><tr><td>Monthly Revenue</td><td>$"+str(rev)+"</td></tr><tr><td>Monthly Profit</td><td>$"+str(profit)+"</td></tr>  <tr><td><b>Cap Rate</b></td><td><b>"+str(cap)+"%</b></td></tr></tbody></table><br>"
        h = "This information is based on "+str(int(numComps))+" successfully rented properties in the same neighborhood with the following averages:<br>"
        i = "- Avg Size (sq ft): "+str(compsize)+"<br> - Avg Year Built: "+str(int(compage))+"<br>"
        payload = a+aa+b+bb+c+d+e+ee+f+g+h+i
        return(payload)

    #make object per item
    for index,row in df.iterrows():
        payload = payload+createObject(row['MLSNumber'],row['City'],row['List Price'],row['DOM'],row['InteriorSqFt'],row['Bedrooms'],row['BathsFull'],row['hoaTotalFee'],row['MonthlyMortgage'],row['TaxMonthlyTotal'],row['CompAvgRentRevenue'],row['MonthlyProfit'],row['CapRate'],row['CompAvgSqFt'],row['CompAvgAge'],row['Age'], row['NumComps'])

        payload = payload + '<hr><br>'


    #write to file
    Html_file= open("listings.html","w")
    Html_file.write(payload)
    Html_file.close()
