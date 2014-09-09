

import mechanize
import cookielib
from bs4 import BeautifulSoup
import urwid

br = mechanize.Browser()

cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(True)

br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'),('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'),('Accept-Encoding', 'none'),('Accept-Language', 'en-US,en;q=0.8'),('Connection','keep-alive'),]

target = 'http://headline.2ch.net/bbynews/'

def load():
	res = br.open(target).read().decode('shiftjis','ignore')

	soup = BeautifulSoup(res)

	return [urwid.Text(title.text.encode('utf8','ignore'),wrap='clip') for title in soup.find_all('a')][9:]

#the frame widget

def hot_keys(key):
	if key in ('q', 'Q'):
		raise urwid.ExitMainLoop()
	if key in ('r', 'R'):
		news_titles = load()
		loop.draw_screen()
			

news_titles = load()
Header = urwid.Filler(urwid.Text(u'Welcome to BBS Reader, %s threads' % str(len(news_titles))),'top')

Body = urwid.Pile(news_titles)

Frame = urwid.Frame(Header,Body)

loop = urwid.MainLoop(Frame,unhandled_input=hot_keys)

loop.run()

