#!/usr/bin/env python

import urllib2
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import NavigableString
from BeautifulSoup import Tag
import re

class PokeyBot:
    """
    PokeyBlog is a simple little class that gets a Pokey The Penguin! post.
    """


    # entryNumber is the comic number. None to get most recent.
    entryNumber = int()

    # PokeyUrl is the url path to a Pokey blog post
    PokeyUrl = "http://www.yellow5.com/pokey/archive/index^ENTRYNUM^"

    PokeyUrlNone = "http://www.yellow5.com/pokey/"

    # urlFile is the result from urllib.urlopen() action, which
    # is a file-like object.
    urlFile = None

    # wholeBody is the body of the blog post, in Unicode
    wholeBody = None

    # entryBodyHtml is the content part of the blog post - that is, pictures
    # and text (complete with markup)
    entryBodyHtml = None

    # entryTitle is the tile of the blog post
    entryTitle = None

    # soup is the BeauitfulSoup object created out of the post.
    soup = None

    def __init__(self, entryNumber = None):
        self.entryNumber = entryNumber
        self.__constructPokeyUrl()
        self.__getUrl()
        #self.__readBody()
        #self.soup = BeautifulSoup(self.wholeBody)
        #self.__findContent()
        #self.__setTitle()
        return

    def __constructPokeyUrl(self):
        if (self.entryNumber == None):
            self.PokeyUrl = self.PokeyUrlNone
        else:
            self.PokeyUrl = self.PokeyUrl.replace('^ENTRYNUM^', str(self.entryNumber))

    def __getUrl(self):
        """
        Gets the url and stores it in a urllib2 object
        """
        try:
            self.urlFile = urllib2.urlopen(self.PokeyUrl)
        except HTTPError:
            self.urlFile = None
        return

    def __readBody(self):
        """
        Takes the entire body, converts it to Unicode, and 
        stores it in self.wholeBody
        """
        body = self.urlFile.read()
        self.wholeBody = unicode(body, self.__ENCODING)
        return

    def __findContent(self):
        """
        Finds the exciting content in the blog post.
        """
        self.entryBodyHtml = self.soup.find('div', {'class':'entry_body'})
        return

    def __setTitle(self):
        """
        Sets the title of the blog post.
        """
        try:
            self.entryTitle = self.soup.find('div', {'class':'entry_title'}).a.getText()
        except AttributeError:
            self.entryTitle = None
        return

    def ircContent(self):
        """
        Returns a string of the content, properly formatted for posting an in IRC channel. 
        """
        # This could be interesting. The blog posts are messes of <br /> 
        # tags, and not using something HTML-aware could be painful.
        # This will most likely be accomplished using parts of Beautiful
        # Soup.

        # There are a few tags that seem to be used in fc2 blogs, at least
        # this one in particular.
        #  * br tags are abused for formatting
        #  * img tags contain pictures
        #    and are stored within a tags.
        #  * Text is just placed outside of everything.
        #    Text is of type BeautifulSoup.NavigableString.

        ircString = unicode()
        try:
            for item in self.entryBodyHtml:
                if (type(item) == Tag):
                            if(item.getText() != ''):
                                # Some link text
                                ircString = ircString.rstrip('\n')
                                ircString += item.getText() + u" "
                                ircString += u"< " + item.get("href") + u" >"
                if (item.find('img') != None):
                    # Image.
                    ircString += item.find('img')['src'] + u"\n"
                elif (item.find('embed') != None):
                    # Youtube video.
                    ircString += item.find('embed')['src'] + u"\n"

                # Text:
                if (type(item) == NavigableString):
                    ircString += item + u"\n"
        except TypeError:
            ircString = u"No blog post found."
            
        return ircString

    def latestPost(self):
        """
        Returns the integer number of the most recent blog post.
        """
        allLinks = self.soup.findAll('a')
        for link in allLinks:
            url = link.get("href")
            result = re.match("http://sisinPokey.blog17.fc2.com/blog-entry-....html", url)
            if (result != None):
                pos = re.search("[0-9][0-9][0-9]", url)
                start = pos.start()
                end = pos.end()
                return int(url[start:end])
        return None

# vim: set swiftwidth=4 tabstop=4
