import requests
from bs4 import BeautifulSoup
import re
import webbrowser
from time import localtime, strftime, sleep, time

print '\nSupreme Bot by @DefNotAvg\n'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
}

r = requests.get('http://www.supremenewyork.com/shop/all', headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')

categories = soup.find_all('a')
categories = [s.text.encode('utf-8') for s in categories]
categories = categories[categories.index('new') + 1:categories.index('')]
if categories == []:
	categories = ['jackets', 'shirts', 'tops/sweaters', 'sweatshirts', 'pants', 'hats', 'bags', 'accessories', 'shoes', 'skate']
choices = list(range(1,len(categories) + 1))

print 'Choose a category by entering the corresponding number\n'
for choice in choices:
	print '({}) {}'.format(choice, categories[choice - 1].title())

category = categories[int(raw_input('\nChoice: ')) - 1]
if category == 'tops/sweaters':
	category = category.replace('/', '_')
	category_link = 'http://www.supremenewyork.com/shop/all/{}'.format(category)
else:
	category_link = 'http://www.supremenewyork.com/shop/all/{}'.format(category)
print ''
new = raw_input('New Items Only? (y/n): ').lower()
keywords = raw_input('Keyword(s): ').split(', ')
browser = raw_input('Open Link(s) in Browser? (y/n): ').lower()
print ''

matching_titles = []

if new == 'y':
	r = requests.get(category_link, headers=headers)
	soup = BeautifulSoup(r.content, 'html.parser')

	initial_links = re.findall(r'class="name-link" href="(.*?)"', r.content)
	initial_links = ['http://www.supremenewyork.com{}'.format(s) for s in initial_links]
	initial_links = initial_links[::2]
	initial_titles = soup.find_all('a')
	initial_titles = [s.text.encode('utf-8') for s in initial_titles]
	initial_titles = initial_titles[initial_titles.index(''):]
	initial_titles = [s for s in initial_titles if s != '' and s != 'sold out']
	initial_titles = initial_titles[:initial_titles.index('home')]
	initial_titles = [' - '.join(x) for x in zip(initial_titles[0::2], initial_titles[1::2])]

else:
	initial_links = []
	initial_titles = []

while matching_titles == []:
	r = requests.get(category_link, headers=headers)
	soup = BeautifulSoup(r.content, 'html.parser')

	links = re.findall(r'class="name-link" href="(.*?)"', r.content)
	links = ['http://www.supremenewyork.com{}'.format(s) for s in links]
	links = links[::2]
	links = [s for s in links if s not in initial_links]
	titles = soup.find_all('a')
	titles = [s.text.encode('utf-8') for s in titles]
	titles = titles[titles.index(''):]
	titles = [s for s in titles if s != '' and s != 'sold out']
	titles = titles[:titles.index('home')]
	titles = [' - '.join(x) for x in zip(titles[0::2], titles[1::2])]
	titles = [s for s in titles if s not in initial_titles]
	for title in titles:
		if all(keyword in title.lower() for keyword in keywords):
			matching_titles.append(title)
	matching_links = [links[titles.index(s)] for s in matching_titles]
	if matching_titles != []:
		print 'Item(s) matching keywords found...\n'
		for i in range(0,len(matching_titles)):
			if i != len(matching_titles) - 1:
				print '{}\n{}\n'.format(matching_titles[i], matching_links[i])
			else:
				print '{}\n{}'.format(matching_titles[i], matching_links[i])
			if browser == 'y':
				print 'Opening link in browser...'
				webbrowser.open(matching_links[i])
	else:
		print 'No items matching keywords found. [{}]'.format(str(strftime('%m-%d-%Y %I:%M %p', localtime())))
	sleep(1)