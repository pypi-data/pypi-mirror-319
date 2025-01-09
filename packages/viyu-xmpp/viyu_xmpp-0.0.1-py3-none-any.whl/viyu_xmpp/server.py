import json
import logging
from getpass import getpass
from argparse import ArgumentParser
import ssl
import slixmpp
from slixmpp import ClientXMPP, Iq
from slixmpp.xmlstream import register_stanza_plugin
from slixmpp.xmlstream.handler import Callback
from slixmpp.xmlstream.matcher import StanzaPath
from viyu_xmpp.stanza.get_stanza import Get
from viyu_xmpp.stanza.post_stanza import Post

class ViyuXmppServer(slixmpp.ClientXMPP):
    
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.allGetEventsList = {}
        self.allPostEventsList = {}

        # Disable SSL certificate verification
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0004')  # Data Forms
        self.register_plugin('xep_0050')  # Adhoc Commands
        self.register_plugin('xep_0199', {'keepalive': True, 'frequency': 15})

        self.add_event_handler("session_start", self._start)

        # Register the handler for custom IQ with action stanza
        self.register_handler(
            Callback('Custom Get IQ handler', StanzaPath('iq@type=set/get'),
                     self._handle_get_action))

        self.register_handler(
            Callback('Custom Post IQ handler', StanzaPath('iq@type=set/post'),
                     self._handle_post_action))             

        # Register custom event to handle the action
        self.add_event_handler('viyu_client_get', self._handle_client_get)
        self.add_event_handler('viyu_client_post', self._handle_client_post)

        # Register the custom stanza plugin
        register_stanza_plugin(Iq, Get)
        register_stanza_plugin(Iq, Post)

    async def _start(self, event):
        print('XMPP started')

    def add_get(self, event, view):
        if event in self.allGetEventsList:
            raise ValueError(f"GET event '{event}' already exists.")
        self.allGetEventsList[event] = view

    def add_post(self, event, view):
        if event in self.allPostEventsList:
            raise ValueError(f"POST event '{event}' already exists.")
        self.allPostEventsList[event] = view    

    def not_event():
        return 'Not an event'

    
    def _handle_get_action(self, iq):
        self.event('viyu_client_get', iq)

    def _handle_post_action(self, iq):
        self.event('viyu_client_post', iq)    

    async def _handle_client_get(self, iq):
        ev = iq['get']['ev']
        if ev in self.allGetEventsList:
            print("Got bounded event: %s" % iq)
            resp = self.allGetEventsList.get(ev)()
            rep = iq.reply()
            rep['get']['response'] = json.dumps(resp)
            await rep.send()

    async def _handle_client_post(self, iq):
        ev = iq['post']['ev']
        if ev in self.allPostEventsList:
            print("Got bounded event: %s" % iq)
            resp = self.allPostEventsList.get(ev)()
            rep = iq.reply()
            rep['get']['response'] = json.dumps(resp)
            await rep.send()