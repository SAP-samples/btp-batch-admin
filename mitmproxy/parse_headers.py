def response(context, flow):
  request_headers = [{"name": k, "value": v} for k, v in flow.request.headers.iteritems()]
  response_headers = [{"name": k, "value": v} for k, v in flow.response.headers.iteritems()]
  print("################################")
  print("FOR: " + flow.request.url)
  print(flow.request.method + " " + flow.request.path + " " + flow.request.http_version)
  print("HTTP REQUEST HEADERS")
  print(request_headers)
  print("HTTP RESPONSE HEADERS")
  print(response_headers)
  print("")
