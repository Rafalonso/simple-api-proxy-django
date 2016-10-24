from simpleapi.settings import REQUESTHEADERS, CACHE_TIME, RESPONSEPARAMS, RESPONSEHEADERS, STATUS_MESSAGES
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from django.core.cache import cache
import pycurl
from StringIO import StringIO
import json
from simpleapi.logger import logger
class FetchAPI():

	def __init__(self, url, headers=REQUESTHEADERS):
		self.fetch(url, headers)

	def getfield(self, func):
		return func(self.response)

	def fetch(self, url, headers):
		buffer = StringIO()
		c = pycurl.Curl()
		c.setopt(c.URL, url)
		c.setopt(pycurl.HTTPHEADER, headers)
		c.setopt(c.WRITEDATA, buffer)
		c.perform()
		self.statuscode = c.getinfo(c.RESPONSE_CODE)
		c.close()
		self.response = json.loads(buffer.getvalue())

def main_page(request):
	return JsonResponse({"status code": 404, 'message': 'Page not found'}, status=404)

# Needs to be logged in as an admin user to get a response
@api_view(['GET'])
@permission_classes((IsAdminUser, ))
def event_detail(request, pk):
    if request.method != 'GET': HttpResponse(status=404)
    returninfo = cache.get(pk)
    if not returninfo:
    	event = FetchAPI('https://demo.calendar42.com/api/v2/events/%s/' % pk)
    	if event.statuscode<200 or event.statuscode>=300:
    		return JsonResponse({'status code': event.statuscode, 'message': STATUS_MESSAGES[event.statuscode]}, 
    			json_dumps_params=RESPONSEPARAMS, status=event.statuscode)

    	returninfo = {'event_id': pk}
    	title = lambda x: x['data'][0]['title']
    	returninfo.update({'title': event.getfield(title)})

    	eventsubscribers = FetchAPI('https://demo.calendar42.com/api/v2/event-subscriptions/?event_ids=[%s]'% pk)
    	names = []
    	for d in eventsubscribers.response.get('data'):
    		if d.get('event_id') != pk : continue
    		name = d.get('subscriber').get('first_name')
    		if name: names.append(name)
    	returninfo.update({"names": names})
    	cache.set(pk, returninfo, timeout=CACHE_TIME)
    return JsonResponse(returninfo, json_dumps_params=RESPONSEPARAMS)
