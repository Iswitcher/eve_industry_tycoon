import requests
import io

from log import log

class web:

    # get checksum to decide if SDE update is needed
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
            
            
    # get the SDE zip archive
    def get_sde_zip(url):
        try:
            log.info('Fetching zip')
            response = requests.get(url, stream=True)
            if response.status_code != 200:
                raise Exception(f'HTTP code: {response.status_code}')
            return io.BytesIO(response.content) 
        except Exception as e:
            log.critical(f'Failed to write new SDE checksum: {e}')  
            
