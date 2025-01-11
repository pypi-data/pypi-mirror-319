# py_sp_api.generated.shipping.ShippingApi

All URIs are relative to *https://sellingpartnerapi-na.amazon.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**cancel_shipment**](ShippingApi.md#cancel_shipment) | **POST** /shipping/v1/shipments/{shipmentId}/cancel | 
[**create_shipment**](ShippingApi.md#create_shipment) | **POST** /shipping/v1/shipments | 
[**get_account**](ShippingApi.md#get_account) | **GET** /shipping/v1/account | 
[**get_rates**](ShippingApi.md#get_rates) | **POST** /shipping/v1/rates | 
[**get_shipment**](ShippingApi.md#get_shipment) | **GET** /shipping/v1/shipments/{shipmentId} | 
[**get_tracking_information**](ShippingApi.md#get_tracking_information) | **GET** /shipping/v1/tracking/{trackingId} | 
[**purchase_labels**](ShippingApi.md#purchase_labels) | **POST** /shipping/v1/shipments/{shipmentId}/purchaseLabels | 
[**purchase_shipment**](ShippingApi.md#purchase_shipment) | **POST** /shipping/v1/purchaseShipment | 
[**retrieve_shipping_label**](ShippingApi.md#retrieve_shipping_label) | **POST** /shipping/v1/shipments/{shipmentId}/containers/{trackingId}/label | 


# **cancel_shipment**
> CancelShipmentResponse cancel_shipment(shipment_id)



Cancel a shipment by the given shipmentId.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 5 | 15 |  For more information, see \"Usage Plans and Rate Limits\" in the Selling Partner API documentation.

### Example


```python
import py_sp_api.generated.shipping
from py_sp_api.generated.shipping.models.cancel_shipment_response import CancelShipmentResponse
from py_sp_api.generated.shipping.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.shipping.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.shipping.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.shipping.ShippingApi(api_client)
    shipment_id = 'shipment_id_example' # str | 

    try:
        api_response = api_instance.cancel_shipment(shipment_id)
        print("The response of ShippingApi->cancel_shipment:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ShippingApi->cancel_shipment: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **shipment_id** | **str**|  | 

### Return type

[**CancelShipmentResponse**](CancelShipmentResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**401** | The request&#39;s Authorization header is not formatted correctly or does not contain a valid token. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | 403 can be caused for reasons like Access Denied, Unauthorized, Expired Token, Invalid Signature or Resource Not Found. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | Encountered an unexpected condition which prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_shipment**
> CreateShipmentResponse create_shipment(body)



Create a new shipment.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 5 | 15 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.shipping
from py_sp_api.generated.shipping.models.create_shipment_request import CreateShipmentRequest
from py_sp_api.generated.shipping.models.create_shipment_response import CreateShipmentResponse
from py_sp_api.generated.shipping.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.shipping.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.shipping.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.shipping.ShippingApi(api_client)
    body = py_sp_api.generated.shipping.CreateShipmentRequest() # CreateShipmentRequest | 

    try:
        api_response = api_instance.create_shipment(body)
        print("The response of ShippingApi->create_shipment:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ShippingApi->create_shipment: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateShipmentRequest**](CreateShipmentRequest.md)|  | 

### Return type

[**CreateShipmentResponse**](CreateShipmentResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**401** | The request&#39;s Authorization header is not formatted correctly or does not contain a valid token. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | 403 can be caused for reasons like Access Denied, Unauthorized, Expired Token, Invalid Signature or Resource Not Found. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | Encountered an unexpected condition which prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_account**
> GetAccountResponse get_account()



Verify if the current account is valid.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 5 | 15 |  For more information, see \"Usage Plans and Rate Limits\" in the Selling Partner API documentation.

### Example


```python
import py_sp_api.generated.shipping
from py_sp_api.generated.shipping.models.get_account_response import GetAccountResponse
from py_sp_api.generated.shipping.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.shipping.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.shipping.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.shipping.ShippingApi(api_client)

    try:
        api_response = api_instance.get_account()
        print("The response of ShippingApi->get_account:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ShippingApi->get_account: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GetAccountResponse**](GetAccountResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The account was valid. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**401** | The request&#39;s Authorization header is not formatted correctly or does not contain a valid token. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | 403 can be caused for reasons like Access Denied, Unauthorized, Expired Token, Invalid Signature or Resource Not Found. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | Encountered an unexpected condition which prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_rates**
> GetRatesResponse get_rates(body)



Get service rates.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 5 | 15 |  For more information, see \"Usage Plans and Rate Limits\" in the Selling Partner API documentation.

### Example


```python
import py_sp_api.generated.shipping
from py_sp_api.generated.shipping.models.get_rates_request import GetRatesRequest
from py_sp_api.generated.shipping.models.get_rates_response import GetRatesResponse
from py_sp_api.generated.shipping.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.shipping.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.shipping.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.shipping.ShippingApi(api_client)
    body = py_sp_api.generated.shipping.GetRatesRequest() # GetRatesRequest | 

    try:
        api_response = api_instance.get_rates(body)
        print("The response of ShippingApi->get_rates:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ShippingApi->get_rates: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**GetRatesRequest**](GetRatesRequest.md)|  | 

### Return type

[**GetRatesResponse**](GetRatesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request is missing or has invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**401** | The request&#39;s Authorization header is not formatted correctly or does not contain a valid token. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | 403 can be caused for reasons like Access Denied, Unauthorized, Expired Token, Invalid Signature or Resource Not Found. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | Encountered an unexpected condition which prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_shipment**
> GetShipmentResponse get_shipment(shipment_id)



Return the entire shipment object for the shipmentId.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 5 | 15 |  For more information, see \"Usage Plans and Rate Limits\" in the Selling Partner API documentation.

### Example


```python
import py_sp_api.generated.shipping
from py_sp_api.generated.shipping.models.get_shipment_response import GetShipmentResponse
from py_sp_api.generated.shipping.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.shipping.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.shipping.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.shipping.ShippingApi(api_client)
    shipment_id = 'shipment_id_example' # str | 

    try:
        api_response = api_instance.get_shipment(shipment_id)
        print("The response of ShippingApi->get_shipment:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ShippingApi->get_shipment: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **shipment_id** | **str**|  | 

### Return type

[**GetShipmentResponse**](GetShipmentResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**401** | The request&#39;s Authorization header is not formatted correctly or does not contain a valid token. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | 403 can be caused for reasons like Access Denied, Unauthorized, Expired Token, Invalid Signature or Resource Not Found. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | Encountered an unexpected condition which prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_tracking_information**
> GetTrackingInformationResponse get_tracking_information(tracking_id)



Return the tracking information of a shipment.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 1 | 1 |  For more information, see \"Usage Plans and Rate Limits\" in the Selling Partner API documentation.

### Example


```python
import py_sp_api.generated.shipping
from py_sp_api.generated.shipping.models.get_tracking_information_response import GetTrackingInformationResponse
from py_sp_api.generated.shipping.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.shipping.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.shipping.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.shipping.ShippingApi(api_client)
    tracking_id = 'tracking_id_example' # str | 

    try:
        api_response = api_instance.get_tracking_information(tracking_id)
        print("The response of ShippingApi->get_tracking_information:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ShippingApi->get_tracking_information: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tracking_id** | **str**|  | 

### Return type

[**GetTrackingInformationResponse**](GetTrackingInformationResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**401** | The request&#39;s Authorization header is not formatted correctly or does not contain a valid token. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | 403 can be caused for reasons like Access Denied, Unauthorized, Expired Token, Invalid Signature or Resource Not Found. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | Encountered an unexpected condition which prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **purchase_labels**
> PurchaseLabelsResponse purchase_labels(shipment_id, body)



Purchase shipping labels based on a given rate.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 5 | 15 |  For more information, see \"Usage Plans and Rate Limits\" in the Selling Partner API documentation.

### Example


```python
import py_sp_api.generated.shipping
from py_sp_api.generated.shipping.models.purchase_labels_request import PurchaseLabelsRequest
from py_sp_api.generated.shipping.models.purchase_labels_response import PurchaseLabelsResponse
from py_sp_api.generated.shipping.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.shipping.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.shipping.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.shipping.ShippingApi(api_client)
    shipment_id = 'shipment_id_example' # str | 
    body = py_sp_api.generated.shipping.PurchaseLabelsRequest() # PurchaseLabelsRequest | 

    try:
        api_response = api_instance.purchase_labels(shipment_id, body)
        print("The response of ShippingApi->purchase_labels:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ShippingApi->purchase_labels: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **shipment_id** | **str**|  | 
 **body** | [**PurchaseLabelsRequest**](PurchaseLabelsRequest.md)|  | 

### Return type

[**PurchaseLabelsResponse**](PurchaseLabelsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**401** | The request&#39;s Authorization header is not formatted correctly or does not contain a valid token. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | 403 can be caused for reasons like Access Denied, Unauthorized, Expired Token, Invalid Signature or Resource Not Found. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | Encountered an unexpected condition which prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **purchase_shipment**
> PurchaseShipmentResponse purchase_shipment(body)



Purchase shipping labels.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 5 | 15 |  For more information, see \"Usage Plans and Rate Limits\" in the Selling Partner API documentation.

### Example


```python
import py_sp_api.generated.shipping
from py_sp_api.generated.shipping.models.purchase_shipment_request import PurchaseShipmentRequest
from py_sp_api.generated.shipping.models.purchase_shipment_response import PurchaseShipmentResponse
from py_sp_api.generated.shipping.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.shipping.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.shipping.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.shipping.ShippingApi(api_client)
    body = py_sp_api.generated.shipping.PurchaseShipmentRequest() # PurchaseShipmentRequest | 

    try:
        api_response = api_instance.purchase_shipment(body)
        print("The response of ShippingApi->purchase_shipment:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ShippingApi->purchase_shipment: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**PurchaseShipmentRequest**](PurchaseShipmentRequest.md)|  | 

### Return type

[**PurchaseShipmentResponse**](PurchaseShipmentResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**401** | The request&#39;s Authorization header is not formatted correctly or does not contain a valid token. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | 403 can be caused for reasons like Access Denied, Unauthorized, Expired Token, Invalid Signature or Resource Not Found. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | Encountered an unexpected condition which prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_shipping_label**
> RetrieveShippingLabelResponse retrieve_shipping_label(shipment_id, tracking_id, body)



Retrieve shipping label based on the shipment id and tracking id.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 5 | 15 |  For more information, see \"Usage Plans and Rate Limits\" in the Selling Partner API documentation.

### Example


```python
import py_sp_api.generated.shipping
from py_sp_api.generated.shipping.models.retrieve_shipping_label_request import RetrieveShippingLabelRequest
from py_sp_api.generated.shipping.models.retrieve_shipping_label_response import RetrieveShippingLabelResponse
from py_sp_api.generated.shipping.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.shipping.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.shipping.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.shipping.ShippingApi(api_client)
    shipment_id = 'shipment_id_example' # str | 
    tracking_id = 'tracking_id_example' # str | 
    body = py_sp_api.generated.shipping.RetrieveShippingLabelRequest() # RetrieveShippingLabelRequest | 

    try:
        api_response = api_instance.retrieve_shipping_label(shipment_id, tracking_id, body)
        print("The response of ShippingApi->retrieve_shipping_label:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ShippingApi->retrieve_shipping_label: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **shipment_id** | **str**|  | 
 **tracking_id** | **str**|  | 
 **body** | [**RetrieveShippingLabelRequest**](RetrieveShippingLabelRequest.md)|  | 

### Return type

[**RetrieveShippingLabelResponse**](RetrieveShippingLabelResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**401** | The request&#39;s Authorization header is not formatted correctly or does not contain a valid token. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | 403 can be caused for reasons like Access Denied, Unauthorized, Expired Token, Invalid Signature or Resource Not Found. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | Encountered an unexpected condition which prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

