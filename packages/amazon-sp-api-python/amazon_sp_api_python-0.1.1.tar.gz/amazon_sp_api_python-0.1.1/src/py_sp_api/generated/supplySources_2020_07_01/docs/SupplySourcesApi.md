# py_sp_api.generated.supplySources_2020_07_01.SupplySourcesApi

All URIs are relative to *https://sellingpartnerapi-na.amazon.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**archive_supply_source**](SupplySourcesApi.md#archive_supply_source) | **DELETE** /supplySources/2020-07-01/supplySources/{supplySourceId} | 
[**create_supply_source**](SupplySourcesApi.md#create_supply_source) | **POST** /supplySources/2020-07-01/supplySources | 
[**get_supply_source**](SupplySourcesApi.md#get_supply_source) | **GET** /supplySources/2020-07-01/supplySources/{supplySourceId} | 
[**get_supply_sources**](SupplySourcesApi.md#get_supply_sources) | **GET** /supplySources/2020-07-01/supplySources | 
[**update_supply_source**](SupplySourcesApi.md#update_supply_source) | **PUT** /supplySources/2020-07-01/supplySources/{supplySourceId} | 
[**update_supply_source_status**](SupplySourcesApi.md#update_supply_source_status) | **PUT** /supplySources/2020-07-01/supplySources/{supplySourceId}/status | 


# **archive_supply_source**
> ErrorList archive_supply_source(supply_source_id)



Archive a supply source, making it inactive. Cannot be undone.

### Example


```python
import py_sp_api.generated.supplySources_2020_07_01
from py_sp_api.generated.supplySources_2020_07_01.models.error_list import ErrorList
from py_sp_api.generated.supplySources_2020_07_01.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.supplySources_2020_07_01.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.supplySources_2020_07_01.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.supplySources_2020_07_01.SupplySourcesApi(api_client)
    supply_source_id = 'supply_source_id_example' # str | The unique identifier of a supply source.

    try:
        api_response = api_instance.archive_supply_source(supply_source_id)
        print("The response of SupplySourcesApi->archive_supply_source:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SupplySourcesApi->archive_supply_source: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **supply_source_id** | **str**| The unique identifier of a supply source. | 

### Return type

[**ErrorList**](ErrorList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Success. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | The request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - The unique request reference ID. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | The temporary overloading or maintenance of the server. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_supply_source**
> CreateSupplySourceResponse create_supply_source(payload)



Create a new supply source.

### Example


```python
import py_sp_api.generated.supplySources_2020_07_01
from py_sp_api.generated.supplySources_2020_07_01.models.create_supply_source_request import CreateSupplySourceRequest
from py_sp_api.generated.supplySources_2020_07_01.models.create_supply_source_response import CreateSupplySourceResponse
from py_sp_api.generated.supplySources_2020_07_01.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.supplySources_2020_07_01.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.supplySources_2020_07_01.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.supplySources_2020_07_01.SupplySourcesApi(api_client)
    payload = py_sp_api.generated.supplySources_2020_07_01.CreateSupplySourceRequest() # CreateSupplySourceRequest | A request to create a supply source.

    try:
        api_response = api_instance.create_supply_source(payload)
        print("The response of SupplySourcesApi->create_supply_source:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SupplySourcesApi->create_supply_source: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **payload** | [**CreateSupplySourceRequest**](CreateSupplySourceRequest.md)| A request to create a supply source. | 

### Return type

[**CreateSupplySourceResponse**](CreateSupplySourceResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | The request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | An error that indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - The unique request reference ID. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | The temporary overloading or maintenance of the server. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_supply_source**
> SupplySource get_supply_source(supply_source_id)



Retrieve a supply source.

### Example


```python
import py_sp_api.generated.supplySources_2020_07_01
from py_sp_api.generated.supplySources_2020_07_01.models.supply_source import SupplySource
from py_sp_api.generated.supplySources_2020_07_01.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.supplySources_2020_07_01.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.supplySources_2020_07_01.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.supplySources_2020_07_01.SupplySourcesApi(api_client)
    supply_source_id = 'supply_source_id_example' # str | The unique identifier of a supply source.

    try:
        api_response = api_instance.get_supply_source(supply_source_id)
        print("The response of SupplySourcesApi->get_supply_source:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SupplySourcesApi->get_supply_source: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **supply_source_id** | **str**| The unique identifier of a supply source. | 

### Return type

[**SupplySource**](SupplySource.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | The request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | An error that indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - The unique request reference ID. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | The temporary overloading or maintenance of the server. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_supply_sources**
> GetSupplySourcesResponse get_supply_sources(next_page_token=next_page_token, page_size=page_size)



The path to retrieve paginated supply sources.

### Example


```python
import py_sp_api.generated.supplySources_2020_07_01
from py_sp_api.generated.supplySources_2020_07_01.models.get_supply_sources_response import GetSupplySourcesResponse
from py_sp_api.generated.supplySources_2020_07_01.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.supplySources_2020_07_01.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.supplySources_2020_07_01.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.supplySources_2020_07_01.SupplySourcesApi(api_client)
    next_page_token = 'next_page_token_example' # str | The pagination token to retrieve a specific page of results. (optional)
    page_size = 10.0 # float | The number of supply sources to return per paginated request. (optional) (default to 10.0)

    try:
        api_response = api_instance.get_supply_sources(next_page_token=next_page_token, page_size=page_size)
        print("The response of SupplySourcesApi->get_supply_sources:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SupplySourcesApi->get_supply_sources: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **next_page_token** | **str**| The pagination token to retrieve a specific page of results. | [optional] 
 **page_size** | **float**| The number of supply sources to return per paginated request. | [optional] [default to 10.0]

### Return type

[**GetSupplySourcesResponse**](GetSupplySourcesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | The request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | An error that indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - The unique request reference ID. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | The temporary overloading or maintenance of the server. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_supply_source**
> ErrorList update_supply_source(supply_source_id, payload=payload)



Update the configuration and capabilities of a supply source.

### Example


```python
import py_sp_api.generated.supplySources_2020_07_01
from py_sp_api.generated.supplySources_2020_07_01.models.error_list import ErrorList
from py_sp_api.generated.supplySources_2020_07_01.models.update_supply_source_request import UpdateSupplySourceRequest
from py_sp_api.generated.supplySources_2020_07_01.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.supplySources_2020_07_01.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.supplySources_2020_07_01.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.supplySources_2020_07_01.SupplySourcesApi(api_client)
    supply_source_id = 'supply_source_id_example' # str | The unique identitier of a supply source.
    payload = py_sp_api.generated.supplySources_2020_07_01.UpdateSupplySourceRequest() # UpdateSupplySourceRequest |  (optional)

    try:
        api_response = api_instance.update_supply_source(supply_source_id, payload=payload)
        print("The response of SupplySourcesApi->update_supply_source:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SupplySourcesApi->update_supply_source: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **supply_source_id** | **str**| The unique identitier of a supply source. | 
 **payload** | [**UpdateSupplySourceRequest**](UpdateSupplySourceRequest.md)|  | [optional] 

### Return type

[**ErrorList**](ErrorList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Success. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | The request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | An error that indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - The unique request reference ID. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | The temporary overloading or maintenance of the server. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_supply_source_status**
> ErrorList update_supply_source_status(supply_source_id, payload=payload)



Update the status of a supply source.

### Example


```python
import py_sp_api.generated.supplySources_2020_07_01
from py_sp_api.generated.supplySources_2020_07_01.models.error_list import ErrorList
from py_sp_api.generated.supplySources_2020_07_01.models.update_supply_source_status_request import UpdateSupplySourceStatusRequest
from py_sp_api.generated.supplySources_2020_07_01.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.supplySources_2020_07_01.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.supplySources_2020_07_01.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.supplySources_2020_07_01.SupplySourcesApi(api_client)
    supply_source_id = 'supply_source_id_example' # str | The unique identifier of a supply source.
    payload = py_sp_api.generated.supplySources_2020_07_01.UpdateSupplySourceStatusRequest() # UpdateSupplySourceStatusRequest |  (optional)

    try:
        api_response = api_instance.update_supply_source_status(supply_source_id, payload=payload)
        print("The response of SupplySourcesApi->update_supply_source_status:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SupplySourcesApi->update_supply_source_status: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **supply_source_id** | **str**| The unique identifier of a supply source. | 
 **payload** | [**UpdateSupplySourceStatusRequest**](UpdateSupplySourceStatusRequest.md)|  | [optional] 

### Return type

[**ErrorList**](ErrorList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Success. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | The request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - The unique request reference ID. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | The temporary overloading or maintenance of the server. |  * x-amzn-RequestId - The unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

