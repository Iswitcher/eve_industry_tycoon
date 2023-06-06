import requests

from log import log

class web:

    def get_sde_checksum(url):
        try:    
            # log.info(f'Checksum URL: {url}')
            response = requests.get(url, allow_redirects=True)
            if response.status_code == 200:
                return response.text
            else:
                log.warning(f'HTTP response code not 200: {response.status_code}', 'w')
                return ''
        except Exception as e:
            log.critical(f'Failed to get new SDE checksum: {e}')
