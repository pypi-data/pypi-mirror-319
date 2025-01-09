from slixmpp.xmlstream import ElementBase

class Post(ElementBase):
    name = 'post'
    namespace = 'viyu:custom:actions'
    plugin_attrib = 'post'
    interfaces = {'ev', 'response'}
    sub_interfaces = interfaces