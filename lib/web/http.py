import requests
import io
import traceback

from lib.logger import logger

class http:
    
    def __init__(self, url=None):
        self.log = logger()
        self.url = url
        
    
    # http get and return text
    def http_get(self, url):
        try:
            response = requests.get(url, allow_redirects=True)
            if response.status_code == 200:
                return response.text
            else:
                self.log.warning(f'HTTP response code not 200: {response.status_code}', 'w')
                return ''
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
            

    def http_get_bytes(self, url):
        try:
            response = requests.get(url, stream=True, allow_redirects=True)
            if response.status_code == 200:
                total_size = int(response.headers.get("Content-Length", 0))
                output = io.BytesIO()
                for data in response.iter_content(chunk_size=int(total_size/100)):
                    output.write(data)
                return output
            else:
                self.log.warning(f'HTTP response code not 200: {response.status_code}', 'w')
                return ''
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')