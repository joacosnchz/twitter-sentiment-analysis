import os
import random
import re
import logging as log

class CustomProxyMiddleware(object):

    def process_request(self, request, spider):
        if 'PROXIES' in os.environ:
            proxies = os.environ['PROXIES'].split(' ')
            proxy_id = int(random.uniform(0, len(proxies)-1))

            if len(proxies) > 0:
                try:
                    proxy_addr = proxies[proxy_id]
                    pattern = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+")
                    if pattern.match(proxy_addr):
                        log.info('Using proxy: %s' % proxy_addr)
                        request.meta["proxy"] = "http://" + proxy_addr
                except IndexError:
                    log.error('Selection of random proxy failed, running without proxy')
            else:
                log.info('List of proxies empty, running without proxy')
        else:
            log.error('Proxies not set on environment, running without proxy')
