# py_sp_api.generated.vendorOrders.VendorOrdersApi

All URIs are relative to *https://sellingpartnerapi-na.amazon.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_purchase_order**](VendorOrdersApi.md#get_purchase_order) | **GET** /vendor/orders/v1/purchaseOrders/{purchaseOrderNumber} | 
[**get_purchase_orders**](VendorOrdersApi.md#get_purchase_orders) | **GET** /vendor/orders/v1/purchaseOrders | 
[**get_purchase_orders_status**](VendorOrdersApi.md#get_purchase_orders_status) | **GET** /vendor/orders/v1/purchaseOrdersStatus | 
[**submit_acknowledgement**](VendorOrdersApi.md#submit_acknowledgement) | **POST** /vendor/orders/v1/acknowledgements | 


# **get_purchase_order**
> GetPurchaseOrderResponse get_purchase_order(purchase_order_number)



Returns a purchase order based on the `purchaseOrderNumber` value that you specify.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 10 | 10 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The preceding table indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may have higher rate and burst values than those shown here. For more information, refer to [Usage Plans and Rate Limits in the Selling Partner API](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.vendorOrders
from py_sp_api.generated.vendorOrders.models.get_purchase_order_response import GetPurchaseOrderResponse
from py_sp_api.generated.vendorOrders.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.vendorOrders.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.vendorOrders.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.vendorOrders.VendorOrdersApi(api_client)
    purchase_order_number = 'purchase_order_number_example' # str | The purchase order identifier for the order that you want. Formatting Notes: 8-character alpha-numeric code.

    try:
        api_response = api_instance.get_purchase_order(purchase_order_number)
        print("The response of VendorOrdersApi->get_purchase_order:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VendorOrdersApi->get_purchase_order: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **purchase_order_number** | **str**| The purchase order identifier for the order that you want. Formatting Notes: 8-character alpha-numeric code. | 

### Return type

[**GetPurchaseOrderResponse**](GetPurchaseOrderResponse.md)

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

# **get_purchase_orders**
> GetPurchaseOrdersResponse get_purchase_orders(limit=limit, created_after=created_after, created_before=created_before, sort_order=sort_order, next_token=next_token, include_details=include_details, changed_after=changed_after, changed_before=changed_before, po_item_state=po_item_state, is_po_changed=is_po_changed, purchase_order_state=purchase_order_state, ordering_vendor_code=ordering_vendor_code)



Returns a list of purchase orders created or changed during the time frame that you specify. You define the time frame using the `createdAfter`, `createdBefore`, `changedAfter` and `changedBefore` parameters. The date range to search must not be more than 7 days. You can choose to get only the purchase order numbers by setting `includeDetails` to false. You can then use the `getPurchaseOrder` operation to receive details for a specific purchase order.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 10 | 10 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The preceding table indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may have higher rate and burst values than those shown here. For more information, refer to [Usage Plans and Rate Limits in the Selling Partner API](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.vendorOrders
from py_sp_api.generated.vendorOrders.models.get_purchase_orders_response import GetPurchaseOrdersResponse
from py_sp_api.generated.vendorOrders.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.vendorOrders.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.vendorOrders.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.vendorOrders.VendorOrdersApi(api_client)
    limit = 56 # int | The limit to the number of records returned. Default value is 100 records. (optional)
    created_after = '2013-10-20T19:20:30+01:00' # datetime | Purchase orders that became available after this time will be included in the result. Must be in ISO-8601 date/time format. (optional)
    created_before = '2013-10-20T19:20:30+01:00' # datetime | Purchase orders that became available before this time will be included in the result. Must be in ISO-8601 date/time format. (optional)
    sort_order = 'sort_order_example' # str | Sort in ascending or descending order by purchase order creation date. (optional)
    next_token = 'next_token_example' # str | Used for pagination when there is more purchase orders than the specified result size limit. The token value is returned in the previous API call (optional)
    include_details = True # bool | When true, returns purchase orders with complete details. Otherwise, only purchase order numbers are returned. Default value is true. (optional)
    changed_after = '2013-10-20T19:20:30+01:00' # datetime | Purchase orders that changed after this timestamp will be included in the result. Must be in ISO-8601 date/time format. (optional)
    changed_before = '2013-10-20T19:20:30+01:00' # datetime | Purchase orders that changed before this timestamp will be included in the result. Must be in ISO-8601 date/time format. (optional)
    po_item_state = 'po_item_state_example' # str | Current state of the purchase order item. If this value is Cancelled, this API will return purchase orders which have one or more items cancelled by Amazon with updated item quantity as zero. (optional)
    is_po_changed = True # bool | When true, returns purchase orders which were modified after the order was placed. Vendors are required to pull the changed purchase order and fulfill the updated purchase order and not the original one. Default value is false. (optional)
    purchase_order_state = 'purchase_order_state_example' # str | Filters purchase orders based on the purchase order state. (optional)
    ordering_vendor_code = 'ordering_vendor_code_example' # str | Filters purchase orders based on the specified ordering vendor code. This value should be same as 'sellingParty.partyId' in the purchase order. If not included in the filter, all purchase orders for all of the vendor codes that exist in the vendor group used to authorize the API client application are returned. (optional)

    try:
        api_response = api_instance.get_purchase_orders(limit=limit, created_after=created_after, created_before=created_before, sort_order=sort_order, next_token=next_token, include_details=include_details, changed_after=changed_after, changed_before=changed_before, po_item_state=po_item_state, is_po_changed=is_po_changed, purchase_order_state=purchase_order_state, ordering_vendor_code=ordering_vendor_code)
        print("The response of VendorOrdersApi->get_purchase_orders:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VendorOrdersApi->get_purchase_orders: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| The limit to the number of records returned. Default value is 100 records. | [optional] 
 **created_after** | **datetime**| Purchase orders that became available after this time will be included in the result. Must be in ISO-8601 date/time format. | [optional] 
 **created_before** | **datetime**| Purchase orders that became available before this time will be included in the result. Must be in ISO-8601 date/time format. | [optional] 
 **sort_order** | **str**| Sort in ascending or descending order by purchase order creation date. | [optional] 
 **next_token** | **str**| Used for pagination when there is more purchase orders than the specified result size limit. The token value is returned in the previous API call | [optional] 
 **include_details** | **bool**| When true, returns purchase orders with complete details. Otherwise, only purchase order numbers are returned. Default value is true. | [optional] 
 **changed_after** | **datetime**| Purchase orders that changed after this timestamp will be included in the result. Must be in ISO-8601 date/time format. | [optional] 
 **changed_before** | **datetime**| Purchase orders that changed before this timestamp will be included in the result. Must be in ISO-8601 date/time format. | [optional] 
 **po_item_state** | **str**| Current state of the purchase order item. If this value is Cancelled, this API will return purchase orders which have one or more items cancelled by Amazon with updated item quantity as zero. | [optional] 
 **is_po_changed** | **bool**| When true, returns purchase orders which were modified after the order was placed. Vendors are required to pull the changed purchase order and fulfill the updated purchase order and not the original one. Default value is false. | [optional] 
 **purchase_order_state** | **str**| Filters purchase orders based on the purchase order state. | [optional] 
 **ordering_vendor_code** | **str**| Filters purchase orders based on the specified ordering vendor code. This value should be same as &#39;sellingParty.partyId&#39; in the purchase order. If not included in the filter, all purchase orders for all of the vendor codes that exist in the vendor group used to authorize the API client application are returned. | [optional] 

### Return type

[**GetPurchaseOrdersResponse**](GetPurchaseOrdersResponse.md)

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

# **get_purchase_orders_status**
> GetPurchaseOrdersStatusResponse get_purchase_orders_status(limit=limit, sort_order=sort_order, next_token=next_token, created_after=created_after, created_before=created_before, updated_after=updated_after, updated_before=updated_before, purchase_order_number=purchase_order_number, purchase_order_status=purchase_order_status, item_confirmation_status=item_confirmation_status, item_receive_status=item_receive_status, ordering_vendor_code=ordering_vendor_code, ship_to_party_id=ship_to_party_id)



Returns purchase order statuses based on the filters that you specify. Date range to search must not be more than 7 days. You can return a list of purchase order statuses using the available filters, or a single purchase order status by providing the purchase order number.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 10 | 10 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The preceding table indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may have higher rate and burst values than those shown here. For more information, refer to [Usage Plans and Rate Limits in the Selling Partner API](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.vendorOrders
from py_sp_api.generated.vendorOrders.models.get_purchase_orders_status_response import GetPurchaseOrdersStatusResponse
from py_sp_api.generated.vendorOrders.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.vendorOrders.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.vendorOrders.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.vendorOrders.VendorOrdersApi(api_client)
    limit = 56 # int | The limit to the number of records returned. Default value is 100 records. (optional)
    sort_order = 'sort_order_example' # str | Sort in ascending or descending order by purchase order creation date. (optional)
    next_token = 'next_token_example' # str | Used for pagination when there are more purchase orders than the specified result size limit. (optional)
    created_after = '2013-10-20T19:20:30+01:00' # datetime | Purchase orders that became available after this timestamp will be included in the result. Must be in ISO-8601 date/time format. (optional)
    created_before = '2013-10-20T19:20:30+01:00' # datetime | Purchase orders that became available before this timestamp will be included in the result. Must be in ISO-8601 date/time format. (optional)
    updated_after = '2013-10-20T19:20:30+01:00' # datetime | Purchase orders for which the last purchase order update happened after this timestamp will be included in the result. Must be in ISO-8601 date/time format. (optional)
    updated_before = '2013-10-20T19:20:30+01:00' # datetime | Purchase orders for which the last purchase order update happened before this timestamp will be included in the result. Must be in ISO-8601 date/time format. (optional)
    purchase_order_number = 'purchase_order_number_example' # str | Provides purchase order status for the specified purchase order number. (optional)
    purchase_order_status = 'purchase_order_status_example' # str | Filters purchase orders based on the specified purchase order status. If not included in filter, this will return purchase orders for all statuses. (optional)
    item_confirmation_status = 'item_confirmation_status_example' # str | Filters purchase orders based on their item confirmation status. If the item confirmation status is not included in the filter, purchase orders for all confirmation statuses are included. (optional)
    item_receive_status = 'item_receive_status_example' # str | Filters purchase orders based on the purchase order's item receive status. If the item receive status is not included in the filter, purchase orders for all receive statuses are included. (optional)
    ordering_vendor_code = 'ordering_vendor_code_example' # str | Filters purchase orders based on the specified ordering vendor code. This value should be same as 'sellingParty.partyId' in the purchase order. If not included in filter, all purchase orders for all the vendor codes that exist in the vendor group used to authorize API client application are returned. (optional)
    ship_to_party_id = 'ship_to_party_id_example' # str | Filters purchase orders for a specific buyer's Fulfillment Center/warehouse by providing ship to location id here. This value should be same as 'shipToParty.partyId' in the purchase order. If not included in filter, this will return purchase orders for all the buyer's warehouses used for vendor group purchase orders. (optional)

    try:
        api_response = api_instance.get_purchase_orders_status(limit=limit, sort_order=sort_order, next_token=next_token, created_after=created_after, created_before=created_before, updated_after=updated_after, updated_before=updated_before, purchase_order_number=purchase_order_number, purchase_order_status=purchase_order_status, item_confirmation_status=item_confirmation_status, item_receive_status=item_receive_status, ordering_vendor_code=ordering_vendor_code, ship_to_party_id=ship_to_party_id)
        print("The response of VendorOrdersApi->get_purchase_orders_status:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VendorOrdersApi->get_purchase_orders_status: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| The limit to the number of records returned. Default value is 100 records. | [optional] 
 **sort_order** | **str**| Sort in ascending or descending order by purchase order creation date. | [optional] 
 **next_token** | **str**| Used for pagination when there are more purchase orders than the specified result size limit. | [optional] 
 **created_after** | **datetime**| Purchase orders that became available after this timestamp will be included in the result. Must be in ISO-8601 date/time format. | [optional] 
 **created_before** | **datetime**| Purchase orders that became available before this timestamp will be included in the result. Must be in ISO-8601 date/time format. | [optional] 
 **updated_after** | **datetime**| Purchase orders for which the last purchase order update happened after this timestamp will be included in the result. Must be in ISO-8601 date/time format. | [optional] 
 **updated_before** | **datetime**| Purchase orders for which the last purchase order update happened before this timestamp will be included in the result. Must be in ISO-8601 date/time format. | [optional] 
 **purchase_order_number** | **str**| Provides purchase order status for the specified purchase order number. | [optional] 
 **purchase_order_status** | **str**| Filters purchase orders based on the specified purchase order status. If not included in filter, this will return purchase orders for all statuses. | [optional] 
 **item_confirmation_status** | **str**| Filters purchase orders based on their item confirmation status. If the item confirmation status is not included in the filter, purchase orders for all confirmation statuses are included. | [optional] 
 **item_receive_status** | **str**| Filters purchase orders based on the purchase order&#39;s item receive status. If the item receive status is not included in the filter, purchase orders for all receive statuses are included. | [optional] 
 **ordering_vendor_code** | **str**| Filters purchase orders based on the specified ordering vendor code. This value should be same as &#39;sellingParty.partyId&#39; in the purchase order. If not included in filter, all purchase orders for all the vendor codes that exist in the vendor group used to authorize API client application are returned. | [optional] 
 **ship_to_party_id** | **str**| Filters purchase orders for a specific buyer&#39;s Fulfillment Center/warehouse by providing ship to location id here. This value should be same as &#39;shipToParty.partyId&#39; in the purchase order. If not included in filter, this will return purchase orders for all the buyer&#39;s warehouses used for vendor group purchase orders. | [optional] 

### Return type

[**GetPurchaseOrdersStatusResponse**](GetPurchaseOrdersStatusResponse.md)

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
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **submit_acknowledgement**
> SubmitAcknowledgementResponse submit_acknowledgement(body)



Submits acknowledgements for one or more purchase orders.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 10 | 10 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The preceding table indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may have higher rate and burst values than those shown here. For more information, refer to [Usage Plans and Rate Limits in the Selling Partner API](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.vendorOrders
from py_sp_api.generated.vendorOrders.models.submit_acknowledgement_request import SubmitAcknowledgementRequest
from py_sp_api.generated.vendorOrders.models.submit_acknowledgement_response import SubmitAcknowledgementResponse
from py_sp_api.generated.vendorOrders.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.vendorOrders.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.vendorOrders.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.vendorOrders.VendorOrdersApi(api_client)
    body = py_sp_api.generated.vendorOrders.SubmitAcknowledgementRequest() # SubmitAcknowledgementRequest | Submits acknowledgements for one or more purchase orders from a vendor.

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
 **body** | [**SubmitAcknowledgementRequest**](SubmitAcknowledgementRequest.md)| Submits acknowledgements for one or more purchase orders from a vendor. | 

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

