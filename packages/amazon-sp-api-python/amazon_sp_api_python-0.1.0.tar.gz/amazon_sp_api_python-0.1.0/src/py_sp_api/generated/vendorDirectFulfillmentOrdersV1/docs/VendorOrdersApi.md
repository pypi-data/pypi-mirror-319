# py_sp_api.generated.vendorDirectFulfillmentOrdersV1.VendorOrdersApi

All URIs are relative to *https://sellingpartnerapi-na.amazon.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_order**](VendorOrdersApi.md#get_order) | **GET** /vendor/directFulfillment/orders/v1/purchaseOrders/{purchaseOrderNumber} | 
[**get_orders**](VendorOrdersApi.md#get_orders) | **GET** /vendor/directFulfillment/orders/v1/purchaseOrders | 
[**submit_acknowledgement**](VendorOrdersApi.md#submit_acknowledgement) | **POST** /vendor/directFulfillment/orders/v1/acknowledgements | 


# **get_order**
> GetOrderResponse get_order(purchase_order_number)



Returns purchase order information for the purchaseOrderNumber that you specify.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 10 | 10 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.vendorDirectFulfillmentOrdersV1
from py_sp_api.generated.vendorDirectFulfillmentOrdersV1.models.get_order_response import GetOrderResponse
from py_sp_api.generated.vendorDirectFulfillmentOrdersV1.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.vendorDirectFulfillmentOrdersV1.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.vendorDirectFulfillmentOrdersV1.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.vendorDirectFulfillmentOrdersV1.VendorOrdersApi(api_client)
    purchase_order_number = 'purchase_order_number_example' # str | The order identifier for the purchase order that you want. Formatting Notes: alpha-numeric code.

    try:
        api_response = api_instance.get_order(purchase_order_number)
        print("The response of VendorOrdersApi->get_order:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VendorOrdersApi->get_order: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **purchase_order_number** | **str**| The order identifier for the purchase order that you want. Formatting Notes: alpha-numeric code. | 

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
**401** | The request&#39;s Authorization header is not formatted correctly or does not contain a valid token. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_orders**
> GetOrdersResponse get_orders(created_after, created_before, ship_from_party_id=ship_from_party_id, status=status, limit=limit, sort_order=sort_order, next_token=next_token, include_details=include_details)



Returns a list of purchase orders created during the time frame that you specify. You define the time frame using the createdAfter and createdBefore parameters. You must use both parameters. You can choose to get only the purchase order numbers by setting the includeDetails parameter to false. In that case, the operation returns a list of purchase order numbers. You can then call the getOrder operation to return the details of a specific order.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 10 | 10 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.vendorDirectFulfillmentOrdersV1
from py_sp_api.generated.vendorDirectFulfillmentOrdersV1.models.get_orders_response import GetOrdersResponse
from py_sp_api.generated.vendorDirectFulfillmentOrdersV1.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.vendorDirectFulfillmentOrdersV1.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.vendorDirectFulfillmentOrdersV1.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.vendorDirectFulfillmentOrdersV1.VendorOrdersApi(api_client)
    created_after = '2013-10-20T19:20:30+01:00' # datetime | Purchase orders that became available after this date and time will be included in the result. Must be in ISO-8601 date/time format.
    created_before = '2013-10-20T19:20:30+01:00' # datetime | Purchase orders that became available before this date and time will be included in the result. Must be in ISO-8601 date/time format.
    ship_from_party_id = 'ship_from_party_id_example' # str | The vendor warehouse identifier for the fulfillment warehouse. If not specified, the result will contain orders for all warehouses. (optional)
    status = 'status_example' # str | Returns only the purchase orders that match the specified status. If not specified, the result will contain orders that match any status. (optional)
    limit = 56 # int | The limit to the number of purchase orders returned. (optional)
    sort_order = 'sort_order_example' # str | Sort the list in ascending or descending order by order creation date. (optional)
    next_token = 'next_token_example' # str | Used for pagination when there are more orders than the specified result size limit. The token value is returned in the previous API call. (optional)
    include_details = 'true' # bool | When true, returns the complete purchase order details. Otherwise, only purchase order numbers are returned. (optional) (default to 'true')

    try:
        api_response = api_instance.get_orders(created_after, created_before, ship_from_party_id=ship_from_party_id, status=status, limit=limit, sort_order=sort_order, next_token=next_token, include_details=include_details)
        print("The response of VendorOrdersApi->get_orders:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VendorOrdersApi->get_orders: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **created_after** | **datetime**| Purchase orders that became available after this date and time will be included in the result. Must be in ISO-8601 date/time format. | 
 **created_before** | **datetime**| Purchase orders that became available before this date and time will be included in the result. Must be in ISO-8601 date/time format. | 
 **ship_from_party_id** | **str**| The vendor warehouse identifier for the fulfillment warehouse. If not specified, the result will contain orders for all warehouses. | [optional] 
 **status** | **str**| Returns only the purchase orders that match the specified status. If not specified, the result will contain orders that match any status. | [optional] 
 **limit** | **int**| The limit to the number of purchase orders returned. | [optional] 
 **sort_order** | **str**| Sort the list in ascending or descending order by order creation date. | [optional] 
 **next_token** | **str**| Used for pagination when there are more orders than the specified result size limit. The token value is returned in the previous API call. | [optional] 
 **include_details** | **bool**| When true, returns the complete purchase order details. Otherwise, only purchase order numbers are returned. | [optional] [default to &#39;true&#39;]

### Return type

[**GetOrdersResponse**](GetOrdersResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, payload

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **submit_acknowledgement**
> SubmitAcknowledgementResponse submit_acknowledgement(body)



Submits acknowledgements for one or more purchase orders.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 10 | 10 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.vendorDirectFulfillmentOrdersV1
from py_sp_api.generated.vendorDirectFulfillmentOrdersV1.models.submit_acknowledgement_request import SubmitAcknowledgementRequest
from py_sp_api.generated.vendorDirectFulfillmentOrdersV1.models.submit_acknowledgement_response import SubmitAcknowledgementResponse
from py_sp_api.generated.vendorDirectFulfillmentOrdersV1.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.vendorDirectFulfillmentOrdersV1.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.vendorDirectFulfillmentOrdersV1.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.vendorDirectFulfillmentOrdersV1.VendorOrdersApi(api_client)
    body = py_sp_api.generated.vendorDirectFulfillmentOrdersV1.SubmitAcknowledgementRequest() # SubmitAcknowledgementRequest | The request body containing the acknowledgement to an order.

    try:
        api_response = api_instance.submit_acknowledgement(body)
        print("The response of VendorOrdersApi->submit_acknowledgement:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VendorOrdersApi->submit_acknowledgement: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SubmitAcknowledgementRequest**](SubmitAcknowledgementRequest.md)| The request body containing the acknowledgement to an order. | 

### Return type

[**SubmitAcknowledgementResponse**](SubmitAcknowledgementResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Success. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

