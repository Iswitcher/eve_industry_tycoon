import requests
import traceback

from log import log


class web:
    
    # http get and return text
    def http_get(self, url):
        try:
            response = requests.get(url, allow_redirects=True)
            if response.status_code == 200:
                return response.text
            else:
                log.warning(f'HTTP response code not 200: {response.status_code}', 'w')
                return ''
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            log.critical(f'ERROR in {method_name}: {e}')