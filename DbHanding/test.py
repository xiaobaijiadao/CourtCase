from mongoengine import *
connect("caseTest")
# 如需验证和指定主机名
# connect('blog', host='192.168.3.1', username='root', password='1234')

class allCase(Document):
    title = StringField(required=True) #标题
    QW = StringField(required=True) #全文
    YGSCD = StringField(required=True) #原告俗称
    BGBCD = StringField(required=True) #被告辩称
    CMSSD = StringField(required=True) #查明事实段
    CUS_JANYR = StringField(required=True) #结案年月日
    FYCJM = StringField(required=True) #法院层级码


cs = allCase.objects()
print(cs)