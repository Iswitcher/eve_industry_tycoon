import requests

class rest:
  def get(self, url: str, params: dict) -> str:
    if url == "":
      return ""
    resp = requests.get(url=url, params=params)
    if resp.status_code != 200:
      # TODO: check other status codes
      return ""
    return resp.text

  def post(self, url: str, params: dict, body: str) -> str:
    if url == "":
      return ""
    resp = requests.post(url=url, json=body, data=params)
    if resp.status_code != 200:
      # TODO: check other status codes
      return ""
    return resp.text

  def put(self, url: str, params: dict) -> str:
    if url == "":
      return ""
    resp = requests.put(url=url, params=params)
    if resp.status_code != 200:
      # TODO: check other status codes
      return ""
    return resp.text

  def delete(self, url: str) -> str:
    if url == "":
      return ""
    resp = requests.delete(url)
    if resp.status_code != 200:
      # TODO: check other status codes
      return ""
    return resp.text
