# use requests and beautiful soup libraries
import requests, bs4, csv

scores = [] # list to hold scores
baseUrl = 'http://film-quiz.com/'
out = './scores.csv'
months = range(1, 13)
years = range(2012, 2016)

def extractRows(url, year, month, venue):
  '''
  Given a url and year/month/venue parameters
  extract the teams and scores
  '''

  rows = 0
  prev_score = 0
  rank = 1
  # get the url contents
  page = requests.get(url)
  # not all combinations are possible, so ignore 404s
  if page.status_code == 404:
    print ('{0} [Not Found]'.format(url))
  else:
    soup = bs4.BeautifulSoup(page.text, 'html.parser')

    # assume scores are held in a table, with 1 header row
    for tr in soup.find_all('tr')[1:]:
      rows += 1 # count of rows and ordinal position within table
      tds = tr.find_all('td')
      team  = tds[0].get_text().replace('\t', '')
      score = tds[1].get_text().replace('\t', '')
       # rank is same as position, unless the scores are the same
      if score != prev_score: 
        rank = rows
      prev_score = score
      scores.append([year, month, venue, team, score, rows, rank])

    print ('{0} [{1} rows]'.format(url, rows))

'''
2012/2013 formats /yyyy/yy[01-12]x.html
2014/2015 formats /yyyy/xx[01-12].html
N London = b | ah
S London = r | ur
E London = h | ha
'''

# dicts for venue codes
new_venues = {'ah': 1, 'ur': 2, 'ha': 3}
old_venues = {'b': 1, 'r': 2, 'h': 3}

# loop through months, years, and venues
for month in months:

  pad_month = "%02d" % month # url needs 2-digit month nums
  for year in years:

    if year < 2014: # old url format
      for k, v in old_venues.items():
        url = '{0}{1}/{2}{3}{4}.html'.format(baseUrl, str(year), str(year)[2:], pad_month, k)
        extractRows(url, year, pad_month, v)
    else: # new url format
      for k, v in new_venues.items():
        url = '{0}{1}/{2}{3}.html'.format(baseUrl, str(year), k, pad_month)
        extractRows(url, year, pad_month, v)

# write the responses out to a file
myfile = open(out, 'w', newline='\n')
wr = csv.writer(myfile, dialect="excel", delimiter=',')
for score in scores:
  wr.writerow(score)