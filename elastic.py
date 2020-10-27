import ssl
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch.connection import create_ssl_context

ssl_context = create_ssl_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

es = Elasticsearch('https://elastic:J4XayCYey1pXX3vJuF6v@49.247.19.124:9200', verify_certs=False, connection_class=RequestsHttpConnection)
es.info()
