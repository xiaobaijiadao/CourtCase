from mongoengine import *
connect("testmongo")
# 如需验证和指定主机名
# connect('blog', host='192.168.3.1', username='root', password='1234')

class User(Document):
    username = StringField(required=True)
    website = URLField()
    tags = ListField(StringField(max_length=16))

class Test(Document):
    name = StringField(required=True)