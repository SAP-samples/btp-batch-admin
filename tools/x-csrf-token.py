from mitmproxy import ctx

class PreserveXCRSF:
    def __init__(self):
        self.num = 0
        self.token = ""
        self.cookies = ""

    def request(self, flow):
        self.num = self.num + 1
        if "Host" in flow.request.headers:
            #ctx.log.info("host: %s" % flow.request.headers["Host"])
            if flow.request.headers["Host"] == "hana-cockpit.cfapps.us21.hana.ondemand.com":
                ctx.log.info("We've seen %d flowz" % self.num)
                ctx.log.info("url: %s" % flow.request.url)
                ctx.log.info("token: %s" % self.token)
                ctx.log.info("cookies: %s" % self.cookies)
                #if ("Cookie" in flow.request.headers) or ("cookie" in flow.request.headers):
                #for hdr in flow.request.headers:
                #    ctx.log.info("hdr: %s" % hdr)
                if "Cookie" in flow.request.headers:
                    #if "Cookie" in flow.request.headers:
                    cookies = flow.request.headers["Cookie"]
                    #else:
                    #ctx.log.info("cookies: %s" % cookies)
                    self.cookies = cookies

                else:
                    if self.cookies != "":
                        flow.request.headers["Cookie"] = self.cookies
                        ctx.log.info("Using my Cookies!")
                        cookies = self.cookies

                if cookies != "":
                    cookie = cookies.split(';')
                    found = False
                    for eachcookie in cookie:
                        jsesskey, jsessval = eachcookie.split('=')
                        if jsesskey == "JSESSIONID":
                            found = True
                    if found:
                        ctx.log.info("Found JSESSIONID: %s" % jsessval)
                        if "x-csrf-token" in flow.request.headers:
                            x_csrf_token = flow.request.headers["x-csrf-token"]
                            ctx.log.info("x_csrf_token: %s" % x_csrf_token)
                            #Save the header in our class variable
                            if x_csrf_token != "fetch":
                                self.token = x_csrf_token
                                ctx.log.info("Ready for Batch Operations!")

                        else:
                            ctx.log.info("No x-csrf-token Header!")
                            if self.token != "":
                                ctx.log.info("Saved token Exists! %s" % self.token)
                                flow.request.headers["x-csrf-token"] = self.token
                                flow.request.headers["X-Csrf-Token"] = self.token
                            else:
                                ctx.log.info("No saved token! Requesting Fetch!")
                                flow.request.headers["x-csrf-token"] = "fetch"
                    else:
                        ctx.log.info("No logged in session.  Please relogin!")
                else:
                    ctx.log.info("No Cookies! Please relogin!")
            else:
                ctx.log.info("Not Hana Cockpit!")
        else:
            ctx.log.info("No Host Header.")

    def response(self, flow):
        self.num = self.num + 1
        flow.response.headers["count"] = str(self.num)
        #ctx.log.info("Response: %s" % flow.request.url)
        if flow.request.url == "https://hana-cockpit.cfapps.us21.hana.ondemand.com":
            if "X-Csrf-Token" in flow.response.headers:
                self.token = flow.response.headers["X-Csrf-Token"]
                ctx.log.info("Fetched token is %s" % self.token)

addons = [
    PreserveXCRSF()
]

