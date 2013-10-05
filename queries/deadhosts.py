#!/usr/bin/env python

import json,urllib2,os,sys,pycurl,cStringIO,time

# You really can use anything here that exists on any system
collectd_metric = "*.df-root.df_complex-free"

def last_valid(dataset):
  points = dataset['datapoints']
  nocount = 0
  for m in points:
    if not m[0]:
      nocount +=1
  return nocount
    
if __name__ == "__main__":
  if 'GRAPHITE_URL' in os.environ :
    if len(sys.argv) == 2:
      query_string = "%s/render/?target=%s&from=-%smin&format=json" % (os.environ["GRAPHITE_URL"], collectd_metric, sys.argv[1])
      print "Connecting to", query_string

      response = cStringIO.StringIO()
      pc = pycurl.Curl()
      pc.setopt(pc.URL,query_string)
      pc.setopt(pc.WRITEFUNCTION,response.write)
      pc.perform()

      metrics = json.loads(response.getvalue())

      for h in metrics:
        if h:
          if last_valid(h) == len(h['datapoints']):
            print h['target'].split('.')[0], "is dead"

      response.close()

    else:
      print "Usage\n\tdeadhosts.py <time in minutes>"
  else:
    print "Did not set GRAPHITE_URL"
