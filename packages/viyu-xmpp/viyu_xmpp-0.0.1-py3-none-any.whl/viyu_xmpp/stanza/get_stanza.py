from slixmpp.xmlstream import ElementBase

class Get(ElementBase):
    name = 'get'
    namespace = 'viyu:custom:actions'
    plugin_attrib = 'get'
    interfaces = {'ev', 'response'}
    sub_interfaces = interfaces