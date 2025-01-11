# py_sp_api.generated.vendorDirectFulfillmentShippingV1.VendorShippingLabelsApi

All URIs are relative to *https://sellingpartnerapi-na.amazon.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_shipping_label**](VendorShippingLabelsApi.md#get_shipping_label) | **GET** /vendor/directFulfillment/shipping/v1/shippingLabels/{purchaseOrderNumber} | 
[**get_shipping_labels**](VendorShippingLabelsApi.md#get_shipping_labels) | **GET** /vendor/directFulfillment/shipping/v1/shippingLabels | 
[**submit_shipping_label_request**](VendorShippingLabelsApi.md#submit_shipping_label_request) | **POST** /vendor/directFulfillment/shipping/v1/shippingLabels | 


# **get_shipping_label**
> GetShippingLabelResponse get_shipping_label(purchase_order_number)



Returns a shipping label for the purchaseOrderNumber that you specify.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 10 | 10 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.vendorDirectFulfillmentShippingV1
from py_sp_api.generated.vendorDirectFulfillmentShippingV1.models.get_shipping_label_response import GetShippingLabelResponse
from py_sp_api.generated.vendorDirectFulfillmentShippingV1.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.vendorDirectFulfillmentShippingV1.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.vendorDirectFulfillmentShippingV1.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.vendorDirectFulfillmentShippingV1.VendorShippingLabelsApi(api_client)
    purchase_order_number = 'purchase_order_number_example' # str | The purchase order number for which you want to return the shipping label. It should be the same purchaseOrderNumber as received in the order.

    try:
        api_response = api_instance.get_shipping_label(purchase_order_number)
        print("The response of VendorShippingLabelsApi->get_shipping_label:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VendorShippingLabelsApi->get_shipping_label: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **purchase_order_number** | **str**| The purchase order number for which you want to return the shipping label. It should be the same purchaseOrderNumber as received in the order. | 

### Return type

[**GetShippingLabelResponse**](GetShippingLabelResponse.md)

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
**500** | Encountered an unexpected condition which prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_shipping_labels**
> GetShippingLabelListResponse get_shipping_labels(created_after, created_before, ship_from_party_id=ship_from_party_id, limit=limit, sort_order=sort_order, next_token=next_token)



Returns a list of shipping labels created during the time frame that you specify. You define that time frame using the createdAfter and createdBefore parameters. You must use both of these parameters. The date range to search must not be more than 7 days.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 10 | 10 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.vendorDirectFulfillmentShippingV1
from py_sp_api.generated.vendorDirectFulfillmentShippingV1.models.get_shipping_label_list_response import GetShippingLabelListResponse
from py_sp_api.generated.vendorDirectFulfillmentShippingV1.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.vendorDirectFulfillmentShippingV1.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.vendorDirectFulfillmentShippingV1.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.vendorDirectFulfillmentShippingV1.VendorShippingLabelsApi(api_client)
    created_after = '2013-10-20T19:20:30+01:00' # datetime | Shipping labels that became available after this date and time will be included in the result. Must be in ISO-8601 date/time format.
    created_before = '2013-10-20T19:20:30+01:00' # datetime | Shipping labels that became available before this date and time will be included in the result. Must be in ISO-8601 date/time format.
    ship_from_party_id = 'ship_from_party_id_example' # str | The vendor warehouseId for order fulfillment. If not specified, the result will contain orders for all warehouses. (optional)
    limit = 56 # int | The limit to the number of records returned. (optional)
    sort_order = ASC # str | Sort ASC or DESC by order creation date. (optional) (default to ASC)
    next_token = 'next_token_example' # str | Used for pagination when there are more ship labels than the specified result size limit. The token value is returned in the previous API call. (optional)

    try:
        api_response = api_instance.get_shipping_labels(created_after, created_before, ship_from_party_id=ship_from_party_id, limit=limit, sort_order=sort_order, next_token=next_token)
        print("The response of VendorShippingLabelsApi->get_shipping_labels:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VendorShippingLabelsApi->get_shipping_labels: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **created_after** | **datetime**| Shipping labels that became available after this date and time will be included in the result. Must be in ISO-8601 date/time format. | 
 **created_before** | **datetime**| Shipping labels that became available before this date and time will be included in the result. Must be in ISO-8601 date/time format. | 
 **ship_from_party_id** | **str**| The vendor warehouseId for order fulfillment. If not specified, the result will contain orders for all warehouses. | [optional] 
 **limit** | **int**| The limit to the number of records returned. | [optional] 
 **sort_order** | **str**| Sort ASC or DESC by order creation date. | [optional] [default to ASC]
 **next_token** | **str**| Used for pagination when there are more ship labels than the specified result size limit. The token value is returned in the previous API call. | [optional] 

### Return type

[**GetShippingLabelListResponse**](GetShippingLabelListResponse.md)

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
**500** | Encountered an unexpected condition which prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **submit_shipping_label_request**
> SubmitShippingLabelsResponse submit_shipping_label_request(body)



Creates a shipping label for a purchase order and returns a transactionId for reference.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 10 | 10 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.vendorDirectFulfillmentShippingV1
from py_sp_api.generated.vendorDirectFulfillmentShippingV1.models.submit_shipping_labels_request import SubmitShippingLabelsRequest
from py_sp_api.generated.vendorDirectFulfillmentShippingV1.models.submit_shipping_labels_response import SubmitShippingLabelsResponse
from py_sp_api.generated.vendorDirectFulfillmentShippingV1.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.vendorDirectFulfillmentShippingV1.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.vendorDirectFulfillmentShippingV1.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.vendorDirectFulfillmentShippingV1.VendorShippingLabelsApi(api_client)
    body = py_sp_api.generated.vendorDirectFulfillmentShippingV1.SubmitShippingLabelsRequest() # SubmitShippingLabelsRequest | Request body containing one or more shipping labels data.

    try:
        api_response = api_instance.submit_shipping_label_request(body)
        print("The response of VendorShippingLabelsApi->submit_shipping_label_request:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VendorShippingLabelsApi->submit_shipping_label_request: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SubmitShippingLabelsRequest**](SubmitShippingLabelsRequest.md)| Request body containing one or more shipping labels data. | 

### Return type

[**SubmitShippingLabelsResponse**](SubmitShippingLabelsResponse.md)

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
**500** | Encountered an unexpected condition which prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

