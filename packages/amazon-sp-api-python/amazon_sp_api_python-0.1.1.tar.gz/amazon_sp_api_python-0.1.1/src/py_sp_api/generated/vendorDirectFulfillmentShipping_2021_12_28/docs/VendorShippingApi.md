# py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.VendorShippingApi

All URIs are relative to *https://sellingpartnerapi-na.amazon.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_packing_slip**](VendorShippingApi.md#get_packing_slip) | **GET** /vendor/directFulfillment/shipping/2021-12-28/packingSlips/{purchaseOrderNumber} | getPackingSlip
[**get_packing_slips**](VendorShippingApi.md#get_packing_slips) | **GET** /vendor/directFulfillment/shipping/2021-12-28/packingSlips | getPackingSlips
[**submit_shipment_confirmations**](VendorShippingApi.md#submit_shipment_confirmations) | **POST** /vendor/directFulfillment/shipping/2021-12-28/shipmentConfirmations | submitShipmentConfirmations
[**submit_shipment_status_updates**](VendorShippingApi.md#submit_shipment_status_updates) | **POST** /vendor/directFulfillment/shipping/2021-12-28/shipmentStatusUpdates | submitShipmentStatusUpdates


# **get_packing_slip**
> PackingSlip get_packing_slip(purchase_order_number)

getPackingSlip

Returns a packing slip based on the purchaseOrderNumber that you specify.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 10 | 10 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The preceding table indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may have higher rate and burst values then those shown here. For more information, refer to [Usage Plans and Rate Limits in the Selling Partner API](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits).

### Example


```python
import py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.models.packing_slip import PackingSlip
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.VendorShippingApi(api_client)
    purchase_order_number = 'purchase_order_number_example' # str | The `purchaseOrderNumber` for the packing slip that you want.

    try:
        # getPackingSlip
        api_response = api_instance.get_packing_slip(purchase_order_number)
        print("The response of VendorShippingApi->get_packing_slip:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VendorShippingApi->get_packing_slip: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **purchase_order_number** | **str**| The &#x60;purchaseOrderNumber&#x60; for the packing slip that you want. | 

### Return type

[**PackingSlip**](PackingSlip.md)

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

# **get_packing_slips**
> PackingSlipList get_packing_slips(created_after, created_before, ship_from_party_id=ship_from_party_id, limit=limit, sort_order=sort_order, next_token=next_token)

getPackingSlips

Returns a list of packing slips for the purchase orders that match the criteria specified. Date range to search must not be more than 7 days.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 10 | 10 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The preceding table indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may have higher rate and burst values then those shown here. For more information, refer to [Usage Plans and Rate Limits in the Selling Partner API](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits).

### Example


```python
import py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.models.packing_slip_list import PackingSlipList
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.VendorShippingApi(api_client)
    created_after = '2013-10-20T19:20:30+01:00' # datetime | Packing slips that become available after this date and time will be included in the result. Values are in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date-time format.
    created_before = '2013-10-20T19:20:30+01:00' # datetime | Packing slips that became available before this date and time will be included in the result. Values are in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date-time format.
    ship_from_party_id = 'ship_from_party_id_example' # str | The vendor `warehouseId` for order fulfillment. If not specified, the result contains orders for all warehouses. (optional)
    limit = 56 # int | The maximum number of records to return. (optional)
    sort_order = ASC # str | The packing slip creation dates, which are sorted by ascending or descending order. (optional) (default to ASC)
    next_token = 'next_token_example' # str | Used for pagination when there are more packing slips than the specified result size limit. The token value is returned in the previous API call. (optional)

    try:
        # getPackingSlips
        api_response = api_instance.get_packing_slips(created_after, created_before, ship_from_party_id=ship_from_party_id, limit=limit, sort_order=sort_order, next_token=next_token)
        print("The response of VendorShippingApi->get_packing_slips:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VendorShippingApi->get_packing_slips: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **created_after** | **datetime**| Packing slips that become available after this date and time will be included in the result. Values are in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date-time format. | 
 **created_before** | **datetime**| Packing slips that became available before this date and time will be included in the result. Values are in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date-time format. | 
 **ship_from_party_id** | **str**| The vendor &#x60;warehouseId&#x60; for order fulfillment. If not specified, the result contains orders for all warehouses. | [optional] 
 **limit** | **int**| The maximum number of records to return. | [optional] 
 **sort_order** | **str**| The packing slip creation dates, which are sorted by ascending or descending order. | [optional] [default to ASC]
 **next_token** | **str**| Used for pagination when there are more packing slips than the specified result size limit. The token value is returned in the previous API call. | [optional] 

### Return type

[**PackingSlipList**](PackingSlipList.md)

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

# **submit_shipment_confirmations**
> TransactionReference submit_shipment_confirmations(body)

submitShipmentConfirmations

Submits one or more shipment confirmations for vendor orders.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 10 | 10 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The preceding table indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may have higher rate and burst values then those shown here. For more information, refer to [Usage Plans and Rate Limits in the Selling Partner API](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits).

### Example


```python
import py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.models.submit_shipment_confirmations_request import SubmitShipmentConfirmationsRequest
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.models.transaction_reference import TransactionReference
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.VendorShippingApi(api_client)
    body = py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.SubmitShipmentConfirmationsRequest() # SubmitShipmentConfirmationsRequest | Request body containing the shipment confirmations data.

    try:
        # submitShipmentConfirmations
        api_response = api_instance.submit_shipment_confirmations(body)
        print("The response of VendorShippingApi->submit_shipment_confirmations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VendorShippingApi->submit_shipment_confirmations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SubmitShipmentConfirmationsRequest**](SubmitShipmentConfirmationsRequest.md)| Request body containing the shipment confirmations data. | 

### Return type

[**TransactionReference**](TransactionReference.md)

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

# **submit_shipment_status_updates**
> TransactionReference submit_shipment_status_updates(body)

submitShipmentStatusUpdates

This operation is only to be used by Vendor-Own-Carrier (VOC) vendors. Calling this API submits a shipment status update for the package that a vendor has shipped. It will provide the Amazon customer visibility on their order, when the package is outside of Amazon Network visibility.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 10 | 10 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The preceding table indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may have higher rate and burst values then those shown here. For more information, refer to [Usage Plans and Rate Limits in the Selling Partner API](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits).

### Example


```python
import py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.models.submit_shipment_status_updates_request import SubmitShipmentStatusUpdatesRequest
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.models.transaction_reference import TransactionReference
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.VendorShippingApi(api_client)
    body = py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.SubmitShipmentStatusUpdatesRequest() # SubmitShipmentStatusUpdatesRequest | Request body containing the shipment status update data.

    try:
        # submitShipmentStatusUpdates
        api_response = api_instance.submit_shipment_status_updates(body)
        print("The response of VendorShippingApi->submit_shipment_status_updates:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VendorShippingApi->submit_shipment_status_updates: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SubmitShipmentStatusUpdatesRequest**](SubmitShipmentStatusUpdatesRequest.md)| Request body containing the shipment status update data. | 

### Return type

[**TransactionReference**](TransactionReference.md)

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

