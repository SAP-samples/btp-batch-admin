from mitmproxy import ctx
import gzip
import zlib
import re
import io
import base64
import csv
import os
import datetime

def dump(obj):
    for attr in dir(obj):
        if hasattr( obj, attr ):
            #print( "obj.%s = %s" % (attr, getattr(obj, attr)))
            ctx.log.info( "obj.%s = %s" % (attr, getattr(obj, attr)))

class PreserveXCRSF:
    def __init__(self):
        self.num = 0
        self.token = ""

    def request(self, flow):
        self.num = self.num + 1
        #ctx.log.info("We've seen %d flowz" % self.num)
        ctx.log.info("url: %s" % flow.request.url)
        if "Host" in flow.request.headers:
            #ctx.log.info("host: %s" % flow.request.headers["Host"])
            if flow.request.headers["Host"] == "hana-cockpit.cfapps.us21.hana.ondemand.com":
                #ctx.log.info("RescueTime API!")
                if "x-csrf-token" in flow.request.headers:
                    #ctx.log.info("Content-Type Exists!")
                    x_csrf_token = flow.request.headers["x-csrf-token"]
                    ctx.log.info("x_csrf_token: %s" % x_csrf_token)
                    #Save the header in our class variable
                    self.token = x_csrf_token
                else:
                    ctx.log.info("No x-csrf-token Exists!")
                    if self.token != "":
                        ctx.log.info("Saved token Exists! %s" % self.token)
                        flow.request.headers["x-csrf-token"] = self.token
                    else:
                        ctx.log.info("No saved token!")
            else:
                ctx.log.info("Not Hana Cockpit!")
        else:
            ctx.log.info("No Host Header.")

    def response(self, flow):
        self.num = self.num + 1
        flow.response.headers["count"] = str(self.num)
        if flow.request.url == "https://hana-cockpit.cfapps.us21.hana.ondemand.com":
            #ctx.log.info("rt_post_type: %s" % "config")
            content = flow.response.content.decode("utf-8")
            #ctx.log.info("content: %s" % content)
            tweeked = content
            #tweeked = re.sub(r'.*push_interval: (.*)\n', r'  push_interval: 120\n', tweeked)
            tweeked = re.sub(r'.*push_interval: (.*)\n', r'  push_interval: 60\n', tweeked)
            tweeked = re.sub(r'.*pull_interval: (.*)\n', r'  pull_interval: 30\n', tweeked)
            tweeked = re.sub(r'.*premium_enabled: (.*)\n', r'  premium_enabled: true\n', tweeked)
            tweeked = re.sub(r'.*timepie_enabled: (.*)\n', r'  timepie_enabled: true\n', tweeked)
            ctx.log.info("tweeked: %s" % tweeked)
            flow.response.text = tweeked
        #else: 
            #ctx.log.info("rt_post_type: %s" % "unknown")

addons = [
    PreserveXCRSF()
]

