

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
    text_content = [urwid.Text(title.text.encode('utf8','ignore'),wrap='clip') for title in soup.find_all('a')][9:]
    return urwid.SimpleListWalker([urwid.AttrMap(w, None, 'reveal focus') for w in text_content])

#the frame widget

def get_rows():
    return urwid.raw_display.Screen().get_cols_rows()[1]

def hot_keys(key):
    if key in ('q', 'Q'):
	raise urwid.ExitMainLoop()
    if key in ('r', 'R'):
        news_titles[:] = load() 

news_titles = load()
Header = urwid.Filler(urwid.Text(u'Welcome to BBS Reader, %s threads' % str(len(news_titles))),'top')

Body = urwid.ListBox(news_titles)

Frame = urwid.Frame(Header, urwid.BoxAdapter(Body,get_rows()))

loop = urwid.MainLoop(Frame,unhandled_input=hot_keys)

loop.run()

