import requests
import io
import traceback

from log import log
from tqdm import tqdm

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
            method_name = traceback.extract_stack(None, 2)[0][2]
            log.critical(f'ERROR in {method_name}: {e}')
            
            
    # get the SDE zip archive
    def get_sde_zip(url):
        try:
            log.info('Fetching zip')
            response = requests.get(url, stream=True)
            if response.status_code != 200:
                raise Exception(f'HTTP code: {response.status_code}')
            
            total_size = int(response.headers.get("Content-Length", 0))
            progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)
            
            output = io.BytesIO()
            for data in response.iter_content(chunk_size=int(total_size/100)):
                progress_bar.update(len(data))
                output.write(data)
            progress_bar.close()
            
            return output
            # return io.BytesIO(response.content) 
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            log.critical(f'ERROR in {method_name}: {e}') 
            