# use requests and beautiful soup libraries
import requests, bs4, csv, datetime

weeks = [] # list to hold scores
baseUrl = 'http://officialcharts.com/charts/uk-top-40-singles-chart/'
out = './weeks.csv'
startdate = datetime.date(1960, 3, 10) # first week with a top 40
enddate = datetime.date(2016, 3, 18)

myfile = open(out, 'w', newline='\n')
# write the responses out to a file
wr = csv.writer(myfile, dialect="excel", delimiter=',')

def extractWoC(date):
  '''
  Given a date string,
  Scrape the top 40 WoC figures and aggregate them

  the chart data is in the main table on the page,
  the individual tracks are in the <tr> _without_ a class attribute
  '''
  url = baseUrl + date + '/750140/'
  page = requests.get(url)

  if (page.status_code == 404):
    print ('{0} [Not found]'.format(url))
  else:
    soup = bs4.BeautifulSoup(page.text, 'html5lib')
    rows = soup.find_all('tr', attrs={'class': None})

  s = 0
  for row in rows:
    try:
      # the number of weeks on chart is the 5th column
      s += int(row.find_all('td')[4].get_text())
    except:
      # ignore rows with no data (adverts)
      pass
  
  print(date, s)
  wr.writerow([date, s])

dt = startdate
# loop through each week
while (dt <= enddate):
  dt = dt + datetime.timedelta(days = 7)
  extractWoC(dt.strftime('%Y%m%d'))



