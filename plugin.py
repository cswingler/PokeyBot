###
# Copyright (c) 2010, Chris Swingler
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import supybot.ircmsgs as ircmsgs
import PokeyBot as pb
from random import randint


class PokeyBot(callbacks.Plugin):
    """
    This plugin gets a Pokey the Penguin comic.
    Simlpy call say "pokey postnumber" and the comic will
    be returned to the channel. Omitting the postnumber
    will get a strip at random.
    """
    pass

    def pokey(self, irc, msg, args, channel, num=None):
        """[comic number]

        Prints a pokey the penguin comic to the channel. If no post number is
        given, returns a strip at random.
        """
        if (num == None):
            self.log.info("Randomly getting a Pokey the Pengiun Panel:")
            latestP = pb.PokeyBot()
            r = latestP.randomPanel()
            irc.queueMsg(ircmsgs.privmsg(channel, r))
            irc.noReply
            return
        else:
            postNum = num
        self.log.info("Getting pokey strip number: " + str(postNum))
        p = PokeyBot.PokeyBot(postNum)
        r = p.ircContent()
        self.log.debug("Pokeying %q in %s due to %s.",
                       r, channel, msg.prefix)
        self.log.debug("Type :%s ", type(r))
        irc.queueMsg(ircmsgs.privmsg(channel, r))
        irc.noReply()
        
    pokey = wrap(pokey, ['inChannel',optional('int')])

    def randpokey(self, irc, msg, args, channel):
        """
        Prints a pokey the penguin comic to the channel. If no post number is
        given, returns a strip at random.
        """

        postNum = randint(1,latestP.LatestPost())
        self.log.info("Getting pokey strip number: " + str(postNum))
        p = PokeyBot.PokeyBot(postNum)
        r = p.ircContent()
        self.log.debug("Pokeying %q in %s due to %s.",
                       r, channel, msg.prefix)
        self.log.debug("Type :%s ", type(r))
        irc.queueMsg(ircmsgs.privmsg(channel, r))
        irc.noReply()
    randpokey = wrap(randpokey, ['inChannel'])

    def hug(self, irc, msg, args, channel):
        """
        Huuuuuuuuuuuuuuuugs!
        """
        irc.queueMsg(ircmsgs.privmsg(channel,
        "http://lakupo.com/qu/ghacks/userpics/philippe-hugs.jpg"))
        irc.noReply()
        return
    hug = wrap(hug, ['inChannel'])

Class = PokeyBot

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
