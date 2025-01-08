import asyncio,httpx,logging
from .utils import *
from abstract_apis import get_headers,get_response
def safe_json_dumps(obj):
    if isinstance(obj,dict):
        obj = json.dumps(obj)
    return obj   
async def make_request(url, payload, headers=None):
        async with httpx.AsyncClient(timeout=1000) as client:
            response = await client.post(url, data=safe_json_dumps(payload), headers=headers)
            response.raise_for_status()  # Raise exception for non-2xx status codes
            return response.json()       # or just return response if you want the full object



def get_solcatcherSettings(getApi=False,**kwargs):
    solcatcherSettings = kwargs.get('solcatcherSettings')
    if 'solcatcherSettings' in kwargs:
        del kwargs['solcatcherSettings']
    headers = kwargs.get('headers')
    if 'headers' in kwargs:
        del kwargs['headers']
    headers = headers or get_headers()
    apiKey = kwargs.get('solcatcherApiKey')
    if 'solcatcherApiKey' in kwargs:
        del kwargs['solcatcherApiKey']
    if apiKey or getApi:
        apiKey = apiKey or getApi
        if isinstance(apiKey,bool):
            apiKey=None
        headers = get_db_header(headers=headers,api_key=apiKey)
    headers = headers or  get_headers()
    return kwargs,solcatcherSettings,headers
def runSolcatcherSettings(response,solcatcherSettings):
    usedKeys = []
    if solcatcherSettings:
        for key,value in solcatcherSettings.items():
            if key == 'getResponse':
                response = get_response(response)
                usedKeys.append(key)
            if key == 'getResult':
                result = response
                values = ['result',value] 
                if 'getResponse' not in usedKeys:
                    response = get_response(result)
                for value in values:
                    if result and isinstance(result,dict) and value in result:
                        result = result.get(value)
                response = result
                usedKeys.append(key)
    return response

async def async_call_solcatcher_ts(endpoint,*args,**kwargs):
    kwargs,solcatcherSettings,headers = get_solcatcherSettings(**kwargs)
    payload = get_payload(*args,**kwargs)
    url = getSolcatcherTsUrl(endpoint=endpoint)
    response = await  make_request(url, payload,headers=headers)
    result = runSolcatcherSettings(response,solcatcherSettings)
    return result

async def async_call_solcatcher_py(endpoint,*args,**kwargs):
    kwargs,solcatcherSettings,headers = get_solcatcherSettings(**kwargs)
    payload = get_payload(*args,**kwargs)
    url = getSolcatcherPairCatchUrl(endpoint=endpoint)
    response = await  make_request(url, payload,headers=headers)
    result = runSolcatcherSettings(response,solcatcherSettings)
    return result

async def async_call_solcatcher_db(endpoint,*args,**kwargs):
    kwargs,solcatcherSettings,headers = get_solcatcherSettings(True,**kwargs)
    payload = get_payload(*args,**kwargs)
    url = getSolcatcherDbCalls(endpoint=endpoint)
    response = await  make_request(url, payload,headers=headers)
    result = runSolcatcherSettings(response,solcatcherSettings)
    return result

async def async_call_rate_limiter(method, params=None, url_1_only=None, url_2_only=None,**kwargs):
    """
    A rate-limited caller that funnels into makeLimitedRpcCall.
    """
    params = params or []
    url_1_only = True if url_1_only is None else url_1_only
    url_2_only = False if url_2_only is None else url_2_only
    unique_item = params[0] if params else params
    try:
        logging.debug(f"Fetching transaction for signature={unique_item}")
        response = await makeLimitedRpcCall(method=method, params=params,
                                            url_1_only=url_1_only,
                                            url_2_only=url_2_only,
                                            **kwargs)
        logging.debug(f"Raw response from {method} for {unique_item}.")
        return response
    except Exception as e:
        logging.error(f"Error fetching {method}: {e}")
        return []

async def async_make_rate_limited_call(method, params, url_1_only=True, url_2_only=False,**kwargs):
    """
    Attempt up to 3 times. After the 2nd attempt, set url_2_only=True.
    After the 1st attempt, set url_1_only=False.
    """
    kwargs,solcatcherSettings,headers = get_solcatcherSettings(**kwargs)
    for attempt in range(3):  # Retry logic
        if attempt == 2:
            url_2_only = True
        if attempt == 1:
            url_1_only = False
        
        response = await async_call_solcatcher_py(
            'make_limited_rpc_call',
            method=method,
            params=params,
            url_1_only=url_1_only,
            url_2_only=url_2_only,
            solcatcherSettings=solcatcherSettings,
            headers = headers,
            **kwargs
        )
        if response:
            return response
    # If no response after all attempts, return empty or raise an exception
    return []

def call_rate_limiter(method, params, url_1_only=True, url_2_only=False,**kwargs):
    return asyncio.run(async_call_rate_limiter(method=method, params=params, url_1_only=url_1_only, url_2_only=url_2_only,**kwargs))

def make_rate_limited_call(method, params, url_1_only=True, url_2_only=False,**kwargs):
    return asyncio.run(async_make_rate_limited_call(method=method, params=params, url_1_only=url_1_only, url_2_only=url_2_only,**kwargs))

def call_solcatcher_py(endpoint,*args,**kwargs):
    return asyncio.run(async_call_solcatcher_py(endpoint,*args,**kwargs))

def call_solcatcher_ts(endpoint,*args,**kwargs):
    return asyncio.run(async_call_solcatcher_ts(endpoint,*args,**kwargs))

def call_solcatcher_db(endpoint,*args, **kwargs):
    return asyncio.run(async_call_solcatcher_db(endpoint,*args,**kwargs))

