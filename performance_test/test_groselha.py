from groselha import Grosa
from datetime import datetime
from time import time

import json
import pystache


quantidade = 1000


with open("news.json") as example_file:
    context = json.loads(example_file.read())


template = Grosa("""
    <div repeat="item news">
        <h2>
            <a attr:href="item.url" content="item.title"></a>
        </h2>
        <p content="item.descrition"></p>
    </div>
""")



init = time()
for i in xrange(quantidade):
    template.render(context)
print (time() - init)/quantidade


init = time()
for i in xrange(quantidade):
    pystache.render("""
    {{#news}}
        <div>
            <h2><a href="{{url}}">{{title}}</a></h2>
            <p content="{{descrition}}"></p>
        </div>
    {{/news}}
    """, context)
print (time() - init)/quantidade
