# py_sp_api.generated.ordersV0.OrdersApi

All URIs are relative to *https://sellingpartnerapi-na.amazon.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**confirm_shipment**](OrdersApi.md#confirm_shipment) | **POST** /orders/v0/orders/{orderId}/shipmentConfirmation | confirmShipment
[**get_order**](OrdersApi.md#get_order) | **GET** /orders/v0/orders/{orderId} | getOrder
[**get_order_address**](OrdersApi.md#get_order_address) | **GET** /orders/v0/orders/{orderId}/address | getOrderAddress
[**get_order_buyer_info**](OrdersApi.md#get_order_buyer_info) | **GET** /orders/v0/orders/{orderId}/buyerInfo | getOrderBuyerInfo
[**get_order_items**](OrdersApi.md#get_order_items) | **GET** /orders/v0/orders/{orderId}/orderItems | getOrderItems
[**get_order_items_buyer_info**](OrdersApi.md#get_order_items_buyer_info) | **GET** /orders/v0/orders/{orderId}/orderItems/buyerInfo | getOrderItemsBuyerInfo
[**get_order_regulated_info**](OrdersApi.md#get_order_regulated_info) | **GET** /orders/v0/orders/{orderId}/regulatedInfo | getOrderRegulatedInfo
[**get_orders**](OrdersApi.md#get_orders) | **GET** /orders/v0/orders | getOrders
[**update_shipment_status**](OrdersApi.md#update_shipment_status) | **POST** /orders/v0/orders/{orderId}/shipment | updateShipmentStatus
[**update_verification_status**](OrdersApi.md#update_verification_status) | **PATCH** /orders/v0/orders/{orderId}/regulatedInfo | updateVerificationStatus


# **confirm_shipment**
> confirm_shipment(order_id, payload)

confirmShipment

Updates the shipment confirmation status for a specified order.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 2 | 10 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The preceding table contains the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may receive higher rate and burst values then those shown here. For more information, refer to [Usage Plans and Rate Limits](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.ordersV0
from py_sp_api.generated.ordersV0.models.confirm_shipment_request import ConfirmShipmentRequest
from py_sp_api.generated.ordersV0.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.ordersV0.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.ordersV0.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.ordersV0.OrdersApi(api_client)
    order_id = 'order_id_example' # str | An Amazon-defined order identifier, in 3-7-7 format.
    payload = py_sp_api.generated.ordersV0.ConfirmShipmentRequest() # ConfirmShipmentRequest | Request body of `confirmShipment`.

    try:
        # confirmShipment
        api_instance.confirm_shipment(order_id, payload)
    except Exception as e:
        print("Exception when calling OrdersApi->confirm_shipment: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **order_id** | **str**| An Amazon-defined order identifier, in 3-7-7 format. | 
 **payload** | [**ConfirmShipmentRequest**](ConfirmShipmentRequest.md)| Request body of &#x60;confirmShipment&#x60;. | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Success. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**401** | The request&#39;s Authorization header is not formatted correctly or does not contain a valid token. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The specified resource does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_order**
> GetOrderResponse get_order(order_id)

getOrder

Returns the order that you specify.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 0.5 | 30 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The preceding table contains the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may receive higher rate and burst values then those shown here. For more information, refer to [Usage Plans and Rate Limits](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.ordersV0
from py_sp_api.generated.ordersV0.models.get_order_response import GetOrderResponse
from py_sp_api.generated.ordersV0.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.ordersV0.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.ordersV0.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.ordersV0.OrdersApi(api_client)
    order_id = 'order_id_example' # str | An Amazon-defined order identifier, in 3-7-7 format.

    try:
        # getOrder
        api_response = api_instance.get_order(order_id)
        print("The response of OrdersApi->get_order:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrdersApi->get_order: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **order_id** | **str**| An Amazon-defined order identifier, in 3-7-7 format. | 

### Return type

[**GetOrderResponse**](GetOrderResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_order_address**
> GetOrderAddressResponse get_order_address(order_id)

getOrderAddress

Returns the shipping address for the order that you specify.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 0.5 | 30 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The preceding table contains the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may receive higher rate and burst values then those shown here. For more information, refer to [Usage Plans and Rate Limits](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.ordersV0
from py_sp_api.generated.ordersV0.models.get_order_address_response import GetOrderAddressResponse
from py_sp_api.generated.ordersV0.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.ordersV0.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.ordersV0.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.ordersV0.OrdersApi(api_client)
    order_id = 'order_id_example' # str | An `orderId` is an Amazon-defined order identifier, in 3-7-7 format.

    try:
        # getOrderAddress
        api_response = api_instance.get_order_address(order_id)
        print("The response of OrdersApi->get_order_address:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrdersApi->get_order_address: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **order_id** | **str**| An &#x60;orderId&#x60; is an Amazon-defined order identifier, in 3-7-7 format. | 

### Return type

[**GetOrderAddressResponse**](GetOrderAddressResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_order_buyer_info**
> GetOrderBuyerInfoResponse get_order_buyer_info(order_id)

getOrderBuyerInfo

Returns buyer information for the order that you specify.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 0.5 | 30 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The preceding table contains the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may receive higher rate and burst values then those shown here. For more information, refer to [Usage Plans and Rate Limits](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.ordersV0
from py_sp_api.generated.ordersV0.models.get_order_buyer_info_response import GetOrderBuyerInfoResponse
from py_sp_api.generated.ordersV0.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.ordersV0.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.ordersV0.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.ordersV0.OrdersApi(api_client)
    order_id = 'order_id_example' # str | An `orderId` is an Amazon-defined order identifier, in 3-7-7 format.

    try:
        # getOrderBuyerInfo
        api_response = api_instance.get_order_buyer_info(order_id)
        print("The response of OrdersApi->get_order_buyer_info:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrdersApi->get_order_buyer_info: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **order_id** | **str**| An &#x60;orderId&#x60; is an Amazon-defined order identifier, in 3-7-7 format. | 

### Return type

[**GetOrderBuyerInfoResponse**](GetOrderBuyerInfoResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_order_items**
> GetOrderItemsResponse get_order_items(order_id, next_token=next_token)

getOrderItems

Returns detailed order item information for the order that you specify. If `NextToken` is provided, it's used to retrieve the next page of order items.  __Note__: When an order is in the Pending state (the order has been placed but payment has not been authorized), the getOrderItems operation does not return information about pricing, taxes, shipping charges, gift status or promotions for the order items in the order. After an order leaves the Pending state (this occurs when payment has been authorized) and enters the Unshipped, Partially Shipped, or Shipped state, the getOrderItems operation returns information about pricing, taxes, shipping charges, gift status and promotions for the order items in the order.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 0.5 | 30 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The preceding table contains the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may receive higher rate and burst values then those shown here. For more information, refer to [Usage Plans and Rate Limits](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.ordersV0
from py_sp_api.generated.ordersV0.models.get_order_items_response import GetOrderItemsResponse
from py_sp_api.generated.ordersV0.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.ordersV0.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.ordersV0.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.ordersV0.OrdersApi(api_client)
    order_id = 'order_id_example' # str | An Amazon-defined order identifier, in 3-7-7 format.
    next_token = 'next_token_example' # str | A string token returned in the response of your previous request. (optional)

    try:
        # getOrderItems
        api_response = api_instance.get_order_items(order_id, next_token=next_token)
        print("The response of OrdersApi->get_order_items:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrdersApi->get_order_items: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **order_id** | **str**| An Amazon-defined order identifier, in 3-7-7 format. | 
 **next_token** | **str**| A string token returned in the response of your previous request. | [optional] 

### Return type

[**GetOrderItemsResponse**](GetOrderItemsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_order_items_buyer_info**
> GetOrderItemsBuyerInfoResponse get_order_items_buyer_info(order_id, next_token=next_token)

getOrderItemsBuyerInfo

Returns buyer information for the order items in the order that you specify.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 0.5 | 30 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The preceding table contains the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may receive higher rate and burst values then those shown here. For more information, refer to [Usage Plans and Rate Limits](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.ordersV0
from py_sp_api.generated.ordersV0.models.get_order_items_buyer_info_response import GetOrderItemsBuyerInfoResponse
from py_sp_api.generated.ordersV0.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.ordersV0.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.ordersV0.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.ordersV0.OrdersApi(api_client)
    order_id = 'order_id_example' # str | An Amazon-defined order identifier, in 3-7-7 format.
    next_token = 'next_token_example' # str | A string token returned in the response of your previous request. (optional)

    try:
        # getOrderItemsBuyerInfo
        api_response = api_instance.get_order_items_buyer_info(order_id, next_token=next_token)
        print("The response of OrdersApi->get_order_items_buyer_info:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrdersApi->get_order_items_buyer_info: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **order_id** | **str**| An Amazon-defined order identifier, in 3-7-7 format. | 
 **next_token** | **str**| A string token returned in the response of your previous request. | [optional] 

### Return type

[**GetOrderItemsBuyerInfoResponse**](GetOrderItemsBuyerInfoResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_order_regulated_info**
> GetOrderRegulatedInfoResponse get_order_regulated_info(order_id)

getOrderRegulatedInfo

Returns regulated information for the order that you specify.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 0.5 | 30 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The preceding table contains the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may receive higher rate and burst values then those shown here. For more information, refer to [Usage Plans and Rate Limits](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.ordersV0
from py_sp_api.generated.ordersV0.models.get_order_regulated_info_response import GetOrderRegulatedInfoResponse
from py_sp_api.generated.ordersV0.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.ordersV0.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.ordersV0.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.ordersV0.OrdersApi(api_client)
    order_id = 'order_id_example' # str | An Amazon-defined order identifier, in 3-7-7 format.

    try:
        # getOrderRegulatedInfo
        api_response = api_instance.get_order_regulated_info(order_id)
        print("The response of OrdersApi->get_order_regulated_info:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrdersApi->get_order_regulated_info: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **order_id** | **str**| An Amazon-defined order identifier, in 3-7-7 format. | 

### Return type

[**GetOrderRegulatedInfoResponse**](GetOrderRegulatedInfoResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, PendingOrder, ApprovedOrder, RejectedOrder

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_orders**
> GetOrdersResponse get_orders(marketplace_ids, created_after=created_after, created_before=created_before, last_updated_after=last_updated_after, last_updated_before=last_updated_before, order_statuses=order_statuses, fulfillment_channels=fulfillment_channels, payment_methods=payment_methods, buyer_email=buyer_email, seller_order_id=seller_order_id, max_results_per_page=max_results_per_page, easy_ship_shipment_statuses=easy_ship_shipment_statuses, electronic_invoice_statuses=electronic_invoice_statuses, next_token=next_token, amazon_order_ids=amazon_order_ids, actual_fulfillment_supply_source_id=actual_fulfillment_supply_source_id, is_ispu=is_ispu, store_chain_store_id=store_chain_store_id, earliest_delivery_date_before=earliest_delivery_date_before, earliest_delivery_date_after=earliest_delivery_date_after, latest_delivery_date_before=latest_delivery_date_before, latest_delivery_date_after=latest_delivery_date_after)

getOrders

Returns orders that are created or updated during the specified time period. If you want to return specific types of orders, you can apply filters to your request. `NextToken` doesn't affect any filters that you include in your request; it only impacts the pagination for the filtered orders response.   **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 0.0167 | 20 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that are applied to the requested operation, when available. The preceding table contains the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may receive higher rate and burst values then those shown here. For more information, refer to [Usage Plans and Rate Limits](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api) in the Selling Partner API documentation.

### Example


```python
import py_sp_api.generated.ordersV0
from py_sp_api.generated.ordersV0.models.get_orders_response import GetOrdersResponse
from py_sp_api.generated.ordersV0.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.ordersV0.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.ordersV0.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.ordersV0.OrdersApi(api_client)
    marketplace_ids = ['marketplace_ids_example'] # List[str] | A list of `MarketplaceId` values. Used to select orders that were placed in the specified marketplaces.  Refer to [Marketplace IDs](https://developer-docs.amazon.com/sp-api/docs/marketplace-ids) for a complete list of `marketplaceId` values.
    created_after = 'created_after_example' # str | Use this date to select orders created after (or at) a specified time. Only orders placed after the specified time are returned. The date must be in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) format.  **Note**: Either the `CreatedAfter` parameter or the `LastUpdatedAfter` parameter is required. Both cannot be empty. `LastUpdatedAfter` and `LastUpdatedBefore` cannot be set when `CreatedAfter` is set. (optional)
    created_before = 'created_before_example' # str | Use this date to select orders created before (or at) a specified time. Only orders placed before the specified time are returned. The date must be in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) format.  **Note**: `CreatedBefore` is optional when `CreatedAfter` is set. If specified, `CreatedBefore` must be equal to or after the `CreatedAfter` date and at least two minutes before current time. (optional)
    last_updated_after = 'last_updated_after_example' # str | Use this date to select orders that were last updated after (or at) a specified time. An update is defined as any change in order status, including the creation of a new order. Includes updates made by Amazon and by the seller. The date must be in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) format.  **Note**: Either the `CreatedAfter` parameter or the `LastUpdatedAfter` parameter is required. Both cannot be empty. `CreatedAfter` or `CreatedBefore` cannot be set when `LastUpdatedAfter` is set. (optional)
    last_updated_before = 'last_updated_before_example' # str | Use this date to select orders that were last updated before (or at) a specified time. An update is defined as any change in order status, including the creation of a new order. Includes updates made by Amazon and by the seller. The date must be in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) format.  **Note**: `LastUpdatedBefore` is optional when `LastUpdatedAfter` is set. But if specified, `LastUpdatedBefore` must be equal to or after the `LastUpdatedAfter` date and at least two minutes before current time. (optional)
    order_statuses = ['order_statuses_example'] # List[str] | A list of `OrderStatus` values used to filter the results.  **Possible values:** - `PendingAvailability` (This status is available for pre-orders only. The order has been placed, payment has not been authorized, and the release date of the item is in the future.) - `Pending` (The order has been placed but payment has not been authorized.) - `Unshipped` (Payment has been authorized and the order is ready for shipment, but no items in the order have been shipped.) - `PartiallyShipped` (One or more, but not all, items in the order have been shipped.) - `Shipped` (All items in the order have been shipped.) - `InvoiceUnconfirmed` (All items in the order have been shipped. The seller has not yet given confirmation to Amazon that the invoice has been shipped to the buyer.) - `Canceled` (The order has been canceled.) - `Unfulfillable` (The order cannot be fulfilled. This state applies only to Multi-Channel Fulfillment orders.) (optional)
    fulfillment_channels = ['fulfillment_channels_example'] # List[str] | A list that indicates how an order was fulfilled. Filters the results by fulfillment channel.   **Possible values**: `AFN` (fulfilled by Amazon), `MFN` (fulfilled by seller). (optional)
    payment_methods = ['payment_methods_example'] # List[str] | A list of payment method values. Use this field to select orders that were paid with the specified payment methods.  **Possible values**: `COD` (cash on delivery), `CVS` (convenience store), `Other` (Any payment method other than COD or CVS). (optional)
    buyer_email = 'buyer_email_example' # str | The email address of a buyer. Used to select orders that contain the specified email address. (optional)
    seller_order_id = 'seller_order_id_example' # str | An order identifier that is specified by the seller. Used to select only the orders that match the order identifier. If `SellerOrderId` is specified, then `FulfillmentChannels`, `OrderStatuses`, `PaymentMethod`, `LastUpdatedAfter`, LastUpdatedBefore, and `BuyerEmail` cannot be specified. (optional)
    max_results_per_page = 56 # int | A number that indicates the maximum number of orders that can be returned per page. Value must be 1 - 100. Default 100. (optional)
    easy_ship_shipment_statuses = ['easy_ship_shipment_statuses_example'] # List[str] | A list of `EasyShipShipmentStatus` values. Used to select Easy Ship orders with statuses that match the specified values. If `EasyShipShipmentStatus` is specified, only Amazon Easy Ship orders are returned.  **Possible values:** - `PendingSchedule` (The package is awaiting the schedule for pick-up.) - `PendingPickUp` (Amazon has not yet picked up the package from the seller.) - `PendingDropOff` (The seller will deliver the package to the carrier.) - `LabelCanceled` (The seller canceled the pickup.) - `PickedUp` (Amazon has picked up the package from the seller.) - `DroppedOff` (The package is delivered to the carrier by the seller.) - `AtOriginFC` (The packaged is at the origin fulfillment center.) - `AtDestinationFC` (The package is at the destination fulfillment center.) - `Delivered` (The package has been delivered.) - `RejectedByBuyer` (The package has been rejected by the buyer.) - `Undeliverable` (The package cannot be delivered.) - `ReturningToSeller` (The package was not delivered and is being returned to the seller.) - `ReturnedToSeller` (The package was not delivered and was returned to the seller.) - `Lost` (The package is lost.) - `OutForDelivery` (The package is out for delivery.) - `Damaged` (The package was damaged by the carrier.) (optional)
    electronic_invoice_statuses = ['electronic_invoice_statuses_example'] # List[str] | A list of `ElectronicInvoiceStatus` values. Used to select orders with electronic invoice statuses that match the specified values.  **Possible values:** - `NotRequired` (Electronic invoice submission is not required for this order.) - `NotFound` (The electronic invoice was not submitted for this order.) - `Processing` (The electronic invoice is being processed for this order.) - `Errored` (The last submitted electronic invoice was rejected for this order.) - `Accepted` (The last submitted electronic invoice was submitted and accepted.) (optional)
    next_token = 'next_token_example' # str | A string token returned in the response of your previous request. (optional)
    amazon_order_ids = ['amazon_order_ids_example'] # List[str] | A list of `AmazonOrderId` values. An `AmazonOrderId` is an Amazon-defined order identifier, in 3-7-7 format. (optional)
    actual_fulfillment_supply_source_id = 'actual_fulfillment_supply_source_id_example' # str | The `sourceId` of the location from where you want the order fulfilled. (optional)
    is_ispu = True # bool | When true, this order is marked to be picked up from a store rather than delivered. (optional)
    store_chain_store_id = 'store_chain_store_id_example' # str | The store chain store identifier. Linked to a specific store in a store chain. (optional)
    earliest_delivery_date_before = 'earliest_delivery_date_before_example' # str | Use this date to select orders with a earliest delivery date before (or at) a specified time. The date must be in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) format. (optional)
    earliest_delivery_date_after = 'earliest_delivery_date_after_example' # str | Use this date to select orders with a earliest delivery date after (or at) a specified time. The date must be in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) format. (optional)
    latest_delivery_date_before = 'latest_delivery_date_before_example' # str | Use this date to select orders with a latest delivery date before (or at) a specified time. The date must be in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) format. (optional)
    latest_delivery_date_after = 'latest_delivery_date_after_example' # str | Use this date to select orders with a latest delivery date after (or at) a specified time. The date must be in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) format. (optional)

    try:
        # getOrders
        api_response = api_instance.get_orders(marketplace_ids, created_after=created_after, created_before=created_before, last_updated_after=last_updated_after, last_updated_before=last_updated_before, order_statuses=order_statuses, fulfillment_channels=fulfillment_channels, payment_methods=payment_methods, buyer_email=buyer_email, seller_order_id=seller_order_id, max_results_per_page=max_results_per_page, easy_ship_shipment_statuses=easy_ship_shipment_statuses, electronic_invoice_statuses=electronic_invoice_statuses, next_token=next_token, amazon_order_ids=amazon_order_ids, actual_fulfillment_supply_source_id=actual_fulfillment_supply_source_id, is_ispu=is_ispu, store_chain_store_id=store_chain_store_id, earliest_delivery_date_before=earliest_delivery_date_before, earliest_delivery_date_after=earliest_delivery_date_after, latest_delivery_date_before=latest_delivery_date_before, latest_delivery_date_after=latest_delivery_date_after)
        print("The response of OrdersApi->get_orders:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrdersApi->get_orders: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **marketplace_ids** | [**List[str]**](str.md)| A list of &#x60;MarketplaceId&#x60; values. Used to select orders that were placed in the specified marketplaces.  Refer to [Marketplace IDs](https://developer-docs.amazon.com/sp-api/docs/marketplace-ids) for a complete list of &#x60;marketplaceId&#x60; values. | 
 **created_after** | **str**| Use this date to select orders created after (or at) a specified time. Only orders placed after the specified time are returned. The date must be in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) format.  **Note**: Either the &#x60;CreatedAfter&#x60; parameter or the &#x60;LastUpdatedAfter&#x60; parameter is required. Both cannot be empty. &#x60;LastUpdatedAfter&#x60; and &#x60;LastUpdatedBefore&#x60; cannot be set when &#x60;CreatedAfter&#x60; is set. | [optional] 
 **created_before** | **str**| Use this date to select orders created before (or at) a specified time. Only orders placed before the specified time are returned. The date must be in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) format.  **Note**: &#x60;CreatedBefore&#x60; is optional when &#x60;CreatedAfter&#x60; is set. If specified, &#x60;CreatedBefore&#x60; must be equal to or after the &#x60;CreatedAfter&#x60; date and at least two minutes before current time. | [optional] 
 **last_updated_after** | **str**| Use this date to select orders that were last updated after (or at) a specified time. An update is defined as any change in order status, including the creation of a new order. Includes updates made by Amazon and by the seller. The date must be in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) format.  **Note**: Either the &#x60;CreatedAfter&#x60; parameter or the &#x60;LastUpdatedAfter&#x60; parameter is required. Both cannot be empty. &#x60;CreatedAfter&#x60; or &#x60;CreatedBefore&#x60; cannot be set when &#x60;LastUpdatedAfter&#x60; is set. | [optional] 
 **last_updated_before** | **str**| Use this date to select orders that were last updated before (or at) a specified time. An update is defined as any change in order status, including the creation of a new order. Includes updates made by Amazon and by the seller. The date must be in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) format.  **Note**: &#x60;LastUpdatedBefore&#x60; is optional when &#x60;LastUpdatedAfter&#x60; is set. But if specified, &#x60;LastUpdatedBefore&#x60; must be equal to or after the &#x60;LastUpdatedAfter&#x60; date and at least two minutes before current time. | [optional] 
 **order_statuses** | [**List[str]**](str.md)| A list of &#x60;OrderStatus&#x60; values used to filter the results.  **Possible values:** - &#x60;PendingAvailability&#x60; (This status is available for pre-orders only. The order has been placed, payment has not been authorized, and the release date of the item is in the future.) - &#x60;Pending&#x60; (The order has been placed but payment has not been authorized.) - &#x60;Unshipped&#x60; (Payment has been authorized and the order is ready for shipment, but no items in the order have been shipped.) - &#x60;PartiallyShipped&#x60; (One or more, but not all, items in the order have been shipped.) - &#x60;Shipped&#x60; (All items in the order have been shipped.) - &#x60;InvoiceUnconfirmed&#x60; (All items in the order have been shipped. The seller has not yet given confirmation to Amazon that the invoice has been shipped to the buyer.) - &#x60;Canceled&#x60; (The order has been canceled.) - &#x60;Unfulfillable&#x60; (The order cannot be fulfilled. This state applies only to Multi-Channel Fulfillment orders.) | [optional] 
 **fulfillment_channels** | [**List[str]**](str.md)| A list that indicates how an order was fulfilled. Filters the results by fulfillment channel.   **Possible values**: &#x60;AFN&#x60; (fulfilled by Amazon), &#x60;MFN&#x60; (fulfilled by seller). | [optional] 
 **payment_methods** | [**List[str]**](str.md)| A list of payment method values. Use this field to select orders that were paid with the specified payment methods.  **Possible values**: &#x60;COD&#x60; (cash on delivery), &#x60;CVS&#x60; (convenience store), &#x60;Other&#x60; (Any payment method other than COD or CVS). | [optional] 
 **buyer_email** | **str**| The email address of a buyer. Used to select orders that contain the specified email address. | [optional] 
 **seller_order_id** | **str**| An order identifier that is specified by the seller. Used to select only the orders that match the order identifier. If &#x60;SellerOrderId&#x60; is specified, then &#x60;FulfillmentChannels&#x60;, &#x60;OrderStatuses&#x60;, &#x60;PaymentMethod&#x60;, &#x60;LastUpdatedAfter&#x60;, LastUpdatedBefore, and &#x60;BuyerEmail&#x60; cannot be specified. | [optional] 
 **max_results_per_page** | **int**| A number that indicates the maximum number of orders that can be returned per page. Value must be 1 - 100. Default 100. | [optional] 
 **easy_ship_shipment_statuses** | [**List[str]**](str.md)| A list of &#x60;EasyShipShipmentStatus&#x60; values. Used to select Easy Ship orders with statuses that match the specified values. If &#x60;EasyShipShipmentStatus&#x60; is specified, only Amazon Easy Ship orders are returned.  **Possible values:** - &#x60;PendingSchedule&#x60; (The package is awaiting the schedule for pick-up.) - &#x60;PendingPickUp&#x60; (Amazon has not yet picked up the package from the seller.) - &#x60;PendingDropOff&#x60; (The seller will deliver the package to the carrier.) - &#x60;LabelCanceled&#x60; (The seller canceled the pickup.) - &#x60;PickedUp&#x60; (Amazon has picked up the package from the seller.) - &#x60;DroppedOff&#x60; (The package is delivered to the carrier by the seller.) - &#x60;AtOriginFC&#x60; (The packaged is at the origin fulfillment center.) - &#x60;AtDestinationFC&#x60; (The package is at the destination fulfillment center.) - &#x60;Delivered&#x60; (The package has been delivered.) - &#x60;RejectedByBuyer&#x60; (The package has been rejected by the buyer.) - &#x60;Undeliverable&#x60; (The package cannot be delivered.) - &#x60;ReturningToSeller&#x60; (The package was not delivered and is being returned to the seller.) - &#x60;ReturnedToSeller&#x60; (The package was not delivered and was returned to the seller.) - &#x60;Lost&#x60; (The package is lost.) - &#x60;OutForDelivery&#x60; (The package is out for delivery.) - &#x60;Damaged&#x60; (The package was damaged by the carrier.) | [optional] 
 **electronic_invoice_statuses** | [**List[str]**](str.md)| A list of &#x60;ElectronicInvoiceStatus&#x60; values. Used to select orders with electronic invoice statuses that match the specified values.  **Possible values:** - &#x60;NotRequired&#x60; (Electronic invoice submission is not required for this order.) - &#x60;NotFound&#x60; (The electronic invoice was not submitted for this order.) - &#x60;Processing&#x60; (The electronic invoice is being processed for this order.) - &#x60;Errored&#x60; (The last submitted electronic invoice was rejected for this order.) - &#x60;Accepted&#x60; (The last submitted electronic invoice was submitted and accepted.) | [optional] 
 **next_token** | **str**| A string token returned in the response of your previous request. | [optional] 
 **amazon_order_ids** | [**List[str]**](str.md)| A list of &#x60;AmazonOrderId&#x60; values. An &#x60;AmazonOrderId&#x60; is an Amazon-defined order identifier, in 3-7-7 format. | [optional] 
 **actual_fulfillment_supply_source_id** | **str**| The &#x60;sourceId&#x60; of the location from where you want the order fulfilled. | [optional] 
 **is_ispu** | **bool**| When true, this order is marked to be picked up from a store rather than delivered. | [optional] 
 **store_chain_store_id** | **str**| The store chain store identifier. Linked to a specific store in a store chain. | [optional] 
 **earliest_delivery_date_before** | **str**| Use this date to select orders with a earliest delivery date before (or at) a specified time. The date must be in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) format. | [optional] 
 **earliest_delivery_date_after** | **str**| Use this date to select orders with a earliest delivery date after (or at) a specified time. The date must be in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) format. | [optional] 
 **latest_delivery_date_before** | **str**| Use this date to select orders with a latest delivery date before (or at) a specified time. The date must be in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) format. | [optional] 
 **latest_delivery_date_after** | **str**| Use this date to select orders with a latest delivery date after (or at) a specified time. The date must be in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) format. | [optional] 

### Return type

[**GetOrdersResponse**](GetOrdersResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_shipment_status**
> update_shipment_status(order_id, payload)

updateShipmentStatus

Update the shipment status for an order that you specify.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 5 | 15 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The preceding table contains the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may receive higher rate and burst values then those shown here. For more information, refer to [Usage Plans and Rate Limits](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.ordersV0
from py_sp_api.generated.ordersV0.models.update_shipment_status_request import UpdateShipmentStatusRequest
from py_sp_api.generated.ordersV0.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.ordersV0.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.ordersV0.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.ordersV0.OrdersApi(api_client)
    order_id = 'order_id_example' # str | An Amazon-defined order identifier, in 3-7-7 format.
    payload = py_sp_api.generated.ordersV0.UpdateShipmentStatusRequest() # UpdateShipmentStatusRequest | The request body for the `updateShipmentStatus` operation.

    try:
        # updateShipmentStatus
        api_instance.update_shipment_status(order_id, payload)
    except Exception as e:
        print("Exception when calling OrdersApi->update_shipment_status: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **order_id** | **str**| An Amazon-defined order identifier, in 3-7-7 format. | 
 **payload** | [**UpdateShipmentStatusRequest**](UpdateShipmentStatusRequest.md)| The request body for the &#x60;updateShipmentStatus&#x60; operation. | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Success. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_verification_status**
> update_verification_status(order_id, payload)

updateVerificationStatus

Updates (approves or rejects) the verification status of an order containing regulated products.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 0.5 | 30 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The preceding table contains the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may receive higher rate and burst values then those shown here. For more information, refer to [Usage Plans and Rate Limits](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.ordersV0
from py_sp_api.generated.ordersV0.models.update_verification_status_request import UpdateVerificationStatusRequest
from py_sp_api.generated.ordersV0.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.ordersV0.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.ordersV0.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.ordersV0.OrdersApi(api_client)
    order_id = 'order_id_example' # str | An Amazon-defined order identifier, in 3-7-7 format.
    payload = py_sp_api.generated.ordersV0.UpdateVerificationStatusRequest() # UpdateVerificationStatusRequest | The request body for the `updateVerificationStatus` operation.

    try:
        # updateVerificationStatus
        api_instance.update_verification_status(order_id, payload)
    except Exception as e:
        print("Exception when calling OrdersApi->update_verification_status: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **order_id** | **str**| An Amazon-defined order identifier, in 3-7-7 format. | 
 **payload** | [**UpdateVerificationStatusRequest**](UpdateVerificationStatusRequest.md)| The request body for the &#x60;updateVerificationStatus&#x60; operation. | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Success. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

