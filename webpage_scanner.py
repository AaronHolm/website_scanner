import sqlalchemy as sa
import pandas as pd
import hashlib
import requests
import random
import time
import smtplib

def getHash(url):
  randomint = random.randint(0,7)
  user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19'
  ]

  headers = {'User-Agent' : user_agents[randomint]}
  response = requests.get(url, headers=headers)
  the_page = response.content
  return hashlib.sha224(the_page).hexdigest()

def getStoredHash(engine, site):
  query = "select name, site_link, hash from sources.source_reference where name = '" + site + "'"
  df = pd.read_sql(query, engine)
  return df

def putStoredHash(engine, hash, site):
  query = "update sources.source_reference set hash = '" + str(hash) + "' where name = '" + site + "';"
  engine.execute(query)
  return

def sendEmail(to_addr, site):
  from_addr = 'an email address'
  server = smtplib.SMTP('smtp.office365.com', 587)
  server.ehlo()
  server.starttls()
  server.login('your email address username', 'your email address password')

  subject = 'Website Change: ' + site
  body = 'A change has been detected in ' + site + '. It is time to run the ETL script.'
  msg = 'Subject: {}\n\n{}'.format(subject, body)

  server.sendmail(from_addr, to_addr, msg)
  server.close()
  return

def scan_website(site):
  engine = sa.create_engine('sql type://sql user:sql password@sql address:sql port/sql database')

  df_oldhash = getStoredHash(engine, site)

  if df_oldhash['hash'].empty:
    hash = getHash(df_oldhash['site_link'][0])
    putStoredHash(engine, hash, site)
    oldhash = hash
  else:
    oldhash = df_oldhash['hash'][0]

  newhash = getHash(df_oldhash['site_link'][0])

  if oldhash == newhash:
    pass
  else:
    putStoredHash(engine, newhash, site)
    sendEmail('an email address', site)
  return

if __name__ == '__main__':
  scan_website('name of site to check stored in your sql database')
