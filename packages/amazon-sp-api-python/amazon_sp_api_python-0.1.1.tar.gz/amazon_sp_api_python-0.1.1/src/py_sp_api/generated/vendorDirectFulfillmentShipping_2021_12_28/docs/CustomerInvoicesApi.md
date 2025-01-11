# py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.CustomerInvoicesApi

All URIs are relative to *https://sellingpartnerapi-na.amazon.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_customer_invoice**](CustomerInvoicesApi.md#get_customer_invoice) | **GET** /vendor/directFulfillment/shipping/2021-12-28/customerInvoices/{purchaseOrderNumber} | getCustomerInvoice
[**get_customer_invoices**](CustomerInvoicesApi.md#get_customer_invoices) | **GET** /vendor/directFulfillment/shipping/2021-12-28/customerInvoices | getCustomerInvoices


# **get_customer_invoice**
> CustomerInvoice get_customer_invoice(purchase_order_number)

getCustomerInvoice

Returns a customer invoice based on the purchaseOrderNumber that you specify.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 10 | 10 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The preceding table indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may have higher rate and burst values then those shown here. For more information, refer to [Usage Plans and Rate Limits in the Selling Partner API](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits).

### Example


```python
import py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.models.customer_invoice import CustomerInvoice
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
    api_instance = py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.CustomerInvoicesApi(api_client)
    purchase_order_number = 'purchase_order_number_example' # str | Purchase order number of the shipment for which to return the invoice.

    try:
        # getCustomerInvoice
        api_response = api_instance.get_customer_invoice(purchase_order_number)
        print("The response of CustomerInvoicesApi->get_customer_invoice:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CustomerInvoicesApi->get_customer_invoice: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **purchase_order_number** | **str**| Purchase order number of the shipment for which to return the invoice. | 

### Return type

[**CustomerInvoice**](CustomerInvoice.md)

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

# **get_customer_invoices**
> CustomerInvoiceList get_customer_invoices(created_after, created_before, ship_from_party_id=ship_from_party_id, limit=limit, sort_order=sort_order, next_token=next_token)

getCustomerInvoices

Returns a list of customer invoices created during a time frame that you specify. You define the time frame using the createdAfter and createdBefore parameters. You must use both of these parameters. The date range to search must be no more than 7 days.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 10 | 10 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The preceding table indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may have higher rate and burst values then those shown here. For more information, refer to [Usage Plans and Rate Limits in the Selling Partner API](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits).

### Example


```python
import py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.models.customer_invoice_list import CustomerInvoiceList
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
    api_instance = py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.CustomerInvoicesApi(api_client)
    created_after = '2013-10-20T19:20:30+01:00' # datetime | Orders that became available after this date and time will be included in the result. Values are in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date-time format.
    created_before = '2013-10-20T19:20:30+01:00' # datetime | Orders that became available before this date and time will be included in the result. Values are in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date-time format.
    ship_from_party_id = 'ship_from_party_id_example' # str | The vendor warehouseId for order fulfillment. If not specified, the result will contain orders for all warehouses. (optional)
    limit = 56 # int | The limit to the number of records returned (optional)
    sort_order = 'sort_order_example' # str | Sort ASC or DESC by order creation date. (optional)
    next_token = 'next_token_example' # str | Used for pagination when there are more orders than the specified result size limit. The token value is returned in the previous API call. (optional)

    try:
        # getCustomerInvoices
        api_response = api_instance.get_customer_invoices(created_after, created_before, ship_from_party_id=ship_from_party_id, limit=limit, sort_order=sort_order, next_token=next_token)
        print("The response of CustomerInvoicesApi->get_customer_invoices:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CustomerInvoicesApi->get_customer_invoices: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **created_after** | **datetime**| Orders that became available after this date and time will be included in the result. Values are in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date-time format. | 
 **created_before** | **datetime**| Orders that became available before this date and time will be included in the result. Values are in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date-time format. | 
 **ship_from_party_id** | **str**| The vendor warehouseId for order fulfillment. If not specified, the result will contain orders for all warehouses. | [optional] 
 **limit** | **int**| The limit to the number of records returned | [optional] 
 **sort_order** | **str**| Sort ASC or DESC by order creation date. | [optional] 
 **next_token** | **str**| Used for pagination when there are more orders than the specified result size limit. The token value is returned in the previous API call. | [optional] 

### Return type

[**CustomerInvoiceList**](CustomerInvoiceList.md)

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

