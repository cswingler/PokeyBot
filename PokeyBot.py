#!/usr/bin/env python

import urllib2
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import NavigableString
from BeautifulSoup import Tag
import re
from random import randint

class PokeyBot:
    """
    PokeyBot t is a simple little class that gets a Pokey The Penguin! post.
    """


    # entryNumber is the comic number. None to get most recent.
    entryNumber = int()

    # PokeyUrl is the url path to a Pokey blog post
    PokeyUrl = "http://www.yellow5.com/pokey/archive/index^ENTRYNUM^.html"

    PokeyUrlNone = "http://www.yellow5.com/pokey/"
    PokeyArchive = "http://www.yellow5.com/pokey/archive/"


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
        self.__readBody()
        self.soup = BeautifulSoup(self.wholeBody)
        self.__setTitle()
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
        except urllib2.HTTPError:
            self.urlFile = None
        return

    def __readBody(self):
        """
        Takes the entire body, converts it to Unicode, and 
        stores it in self.wholeBody
        """
        body = self.urlFile.read()
        self.wholeBody = body
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
        if (self.entryNumber == None):
            self.entryTitle = "Latest comic" # Latest comic is untitled.
        else:
            urlFile = urllib2.urlopen(self.PokeyArchive)
            body = urlFile.read()
            latestSoup = BeautifulSoup(body)
            allLinks = latestSoup.findAll('a')
            pageName = "index%s.html" % self.entryNumber
            for link in allLinks:
                try:
                    if (link.get('href') == pageName):
                        self.entryTitle = link.text
                except:
                    self.entryTitle = "Unknown"
        return

    def randomPanel(self):
        """
        Returns a string of a randomly chosen panel.
        """
        latestPost = self.latestPost()
        randomStripNum = randint(1,latestPost)
        pb = PokeyBot(randomStripNum)
        ircString = unicode()
        images = pb.soup.findAll('img')
        randomPanel = images[randint(1,len(images))]
        imgUrlPath = "http://www.yellow5.com/pokey/archive/"
        ircString = (imgUrlPath + randomPanel.get('src'))
        return ircString

    def ircContent(self):
        """
        Returns a string of the content, properly formatted for posting an in IRC channel. 
        """
        ircString = unicode()
        ircString = "%s: " % self.entryTitle
        imgUrlPath = self.PokeyUrl
        if imgUrlPath.find('html') > 0:
            # Kick to Archive.
            imgUrlPath = "http://www.yellow5.com/pokey/archive/"

        for image in self.soup.findAll('img'):
            ircString += (imgUrlPath + image.get('src') + u" ")
            
        return ircString

    def latestPost(self):
        """
        Returns the integer number of the most recent comic in the archive.
        """
        urlFile = urllib2.urlopen(self.PokeyArchive)
        body = urlFile.read()
        latestSoup = BeautifulSoup(body)
        allLinks = latestSoup.findAll('a')
        for link in allLinks:
            try:
                largest = int(link.get('href').split('.')[0].split('x')[1])
            except:
                pass
        return largest

# vim: set swiftwidth=4 tabstop=4
