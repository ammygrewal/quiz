import csv
import requests
import json
session=requests.session()
def CheckStatus():
    try:
        reader=csv.reader(open('input.csv','r'),delimiter=',')
        wr=open('output.csv','w',encoding='utf=8')
        writer=csv.writer(wr)
        header=next(reader)
        header.append('Is_Valid')
        writer.writerow(header)
        payload=dict()
        for ln in reader:
            payload['companyName']=ln[0]
            payload['address1']=ln[1]
            payload['address2']=''
            payload['city']=ln[2]
            payload['state']=ln[3]
            payload['urbanCode']=''
            payload['zip']=ln[4]
            ln.append(json.loads(session.post('https://tools.usps.com/tools/app/ziplookup/zipByAddress',data=payload,headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}).content.decode())['resultStatus'])
            writer.writerow(ln)
        wr.close()
        print('[+] output.csv Generated')
    except Exception as err:
        print('[-] Error:',err)
def download_file(url):
    resp=session.get(url)
    if resp.status_code==200:
        f=open('input.csv','wb')
        f.write(resp.content)
        f.close()
        print('[+] File Downloaded')
        return True
    else:
        print('[-] Failed To Download File')
        return False
print('*** Please Enter File URL Within 5 Seconds To Avoid Link Expiration ***')
if download_file(input('Enter csv file url: ')):
    print('*** Address Validation Start ***')
    CheckStatus()