# py_sp_api.generated.vendorShipments.VendorShippingApi

All URIs are relative to *https://sellingpartnerapi-na.amazon.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_shipment_details**](VendorShippingApi.md#get_shipment_details) | **GET** /vendor/shipping/v1/shipments | GetShipmentDetails
[**get_shipment_labels**](VendorShippingApi.md#get_shipment_labels) | **GET** /vendor/shipping/v1/transportLabels | 
[**submit_shipment_confirmations**](VendorShippingApi.md#submit_shipment_confirmations) | **POST** /vendor/shipping/v1/shipmentConfirmations | SubmitShipmentConfirmations
[**submit_shipments**](VendorShippingApi.md#submit_shipments) | **POST** /vendor/shipping/v1/shipments | SubmitShipments


# **get_shipment_details**
> GetShipmentDetailsResponse get_shipment_details(limit=limit, sort_order=sort_order, next_token=next_token, created_after=created_after, created_before=created_before, shipment_confirmed_before=shipment_confirmed_before, shipment_confirmed_after=shipment_confirmed_after, package_label_created_before=package_label_created_before, package_label_created_after=package_label_created_after, shipped_before=shipped_before, shipped_after=shipped_after, estimated_delivery_before=estimated_delivery_before, estimated_delivery_after=estimated_delivery_after, shipment_delivery_before=shipment_delivery_before, shipment_delivery_after=shipment_delivery_after, requested_pick_up_before=requested_pick_up_before, requested_pick_up_after=requested_pick_up_after, scheduled_pick_up_before=scheduled_pick_up_before, scheduled_pick_up_after=scheduled_pick_up_after, current_shipment_status=current_shipment_status, vendor_shipment_identifier=vendor_shipment_identifier, buyer_reference_number=buyer_reference_number, buyer_warehouse_code=buyer_warehouse_code, seller_warehouse_code=seller_warehouse_code)

GetShipmentDetails

Returns the Details about Shipment, Carrier Details,  status of the shipment, container details and other details related to shipment based on the filter parameters value that you specify.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 10 | 10 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.vendorShipments
from py_sp_api.generated.vendorShipments.models.get_shipment_details_response import GetShipmentDetailsResponse
from py_sp_api.generated.vendorShipments.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.vendorShipments.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.vendorShipments.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.vendorShipments.VendorShippingApi(api_client)
    limit = 56 # int | The limit to the number of records returned. Default value is 50 records. (optional)
    sort_order = 'sort_order_example' # str | Sort in ascending or descending order by purchase order creation date. (optional)
    next_token = 'next_token_example' # str | Used for pagination when there are more shipments than the specified result size limit. (optional)
    created_after = '2013-10-20T19:20:30+01:00' # datetime | Get Shipment Details that became available after this timestamp will be included in the result. Must be in <a href='https://developer-docs.amazon.com/sp-api/docs/iso-8601'>ISO 8601</a> format. (optional)
    created_before = '2013-10-20T19:20:30+01:00' # datetime | Get Shipment Details that became available before this timestamp will be included in the result. Must be in <a href='https://developer-docs.amazon.com/sp-api/docs/iso-8601'>ISO 8601</a> format. (optional)
    shipment_confirmed_before = '2013-10-20T19:20:30+01:00' # datetime | Get Shipment Details by passing Shipment confirmed create Date Before. Must be in <a href='https://developer-docs.amazon.com/sp-api/docs/iso-8601'>ISO 8601</a> format. (optional)
    shipment_confirmed_after = '2013-10-20T19:20:30+01:00' # datetime | Get Shipment Details by passing Shipment confirmed create Date After. Must be in <a href='https://developer-docs.amazon.com/sp-api/docs/iso-8601'>ISO 8601</a> format. (optional)
    package_label_created_before = '2013-10-20T19:20:30+01:00' # datetime | Get Shipment Details by passing Package label create Date by buyer. Must be in <a href='https://developer-docs.amazon.com/sp-api/docs/iso-8601'>ISO 8601</a> format. (optional)
    package_label_created_after = '2013-10-20T19:20:30+01:00' # datetime | Get Shipment Details by passing Package label create Date After by buyer. Must be in <a href='https://developer-docs.amazon.com/sp-api/docs/iso-8601'>ISO 8601</a> format. (optional)
    shipped_before = '2013-10-20T19:20:30+01:00' # datetime | Get Shipment Details by passing Shipped Date Before. Must be in <a href='https://developer-docs.amazon.com/sp-api/docs/iso-8601'>ISO 8601</a> format. (optional)
    shipped_after = '2013-10-20T19:20:30+01:00' # datetime | Get Shipment Details by passing Shipped Date After. Must be in <a href='https://developer-docs.amazon.com/sp-api/docs/iso-8601'>ISO 8601</a> format. (optional)
    estimated_delivery_before = '2013-10-20T19:20:30+01:00' # datetime | Get Shipment Details by passing Estimated Delivery Date Before. Must be in <a href='https://developer-docs.amazon.com/sp-api/docs/iso-8601'>ISO 8601</a> format. (optional)
    estimated_delivery_after = '2013-10-20T19:20:30+01:00' # datetime | Get Shipment Details by passing Estimated Delivery Date Before. Must be in <a href='https://developer-docs.amazon.com/sp-api/docs/iso-8601'>ISO 8601</a> format. (optional)
    shipment_delivery_before = '2013-10-20T19:20:30+01:00' # datetime | Get Shipment Details by passing Shipment Delivery Date Before. Must be in <a href='https://developer-docs.amazon.com/sp-api/docs/iso-8601'>ISO 8601</a> format. (optional)
    shipment_delivery_after = '2013-10-20T19:20:30+01:00' # datetime | Get Shipment Details by passing Shipment Delivery Date After. Must be in <a href='https://developer-docs.amazon.com/sp-api/docs/iso-8601'>ISO 8601</a> format. (optional)
    requested_pick_up_before = '2013-10-20T19:20:30+01:00' # datetime | Get Shipment Details by passing Before Requested pickup date. Must be in <a href='https://developer-docs.amazon.com/sp-api/docs/iso-8601'>ISO 8601</a> format. (optional)
    requested_pick_up_after = '2013-10-20T19:20:30+01:00' # datetime | Get Shipment Details by passing After Requested pickup date. Must be in <a href='https://developer-docs.amazon.com/sp-api/docs/iso-8601'>ISO 8601</a> format. (optional)
    scheduled_pick_up_before = '2013-10-20T19:20:30+01:00' # datetime | Get Shipment Details by passing Before scheduled pickup date. Must be in <a href='https://developer-docs.amazon.com/sp-api/docs/iso-8601'>ISO 8601</a> format. (optional)
    scheduled_pick_up_after = '2013-10-20T19:20:30+01:00' # datetime | Get Shipment Details by passing After Scheduled pickup date. Must be in <a href='https://developer-docs.amazon.com/sp-api/docs/iso-8601'>ISO 8601</a> format. (optional)
    current_shipment_status = 'current_shipment_status_example' # str | Get Shipment Details by passing Current shipment status. (optional)
    vendor_shipment_identifier = 'vendor_shipment_identifier_example' # str | Get Shipment Details by passing Vendor Shipment ID (optional)
    buyer_reference_number = 'buyer_reference_number_example' # str | Get Shipment Details by passing buyer Reference ID (optional)
    buyer_warehouse_code = 'buyer_warehouse_code_example' # str | Get Shipping Details based on buyer warehouse code. This value should be same as 'shipToParty.partyId' in the Shipment. (optional)
    seller_warehouse_code = 'seller_warehouse_code_example' # str | Get Shipping Details based on vendor warehouse code. This value should be same as 'sellingParty.partyId' in the Shipment. (optional)

    try:
        # GetShipmentDetails
        api_response = api_instance.get_shipment_details(limit=limit, sort_order=sort_order, next_token=next_token, created_after=created_after, created_before=created_before, shipment_confirmed_before=shipment_confirmed_before, shipment_confirmed_after=shipment_confirmed_after, package_label_created_before=package_label_created_before, package_label_created_after=package_label_created_after, shipped_before=shipped_before, shipped_after=shipped_after, estimated_delivery_before=estimated_delivery_before, estimated_delivery_after=estimated_delivery_after, shipment_delivery_before=shipment_delivery_before, shipment_delivery_after=shipment_delivery_after, requested_pick_up_before=requested_pick_up_before, requested_pick_up_after=requested_pick_up_after, scheduled_pick_up_before=scheduled_pick_up_before, scheduled_pick_up_after=scheduled_pick_up_after, current_shipment_status=current_shipment_status, vendor_shipment_identifier=vendor_shipment_identifier, buyer_reference_number=buyer_reference_number, buyer_warehouse_code=buyer_warehouse_code, seller_warehouse_code=seller_warehouse_code)
        print("The response of VendorShippingApi->get_shipment_details:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VendorShippingApi->get_shipment_details: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| The limit to the number of records returned. Default value is 50 records. | [optional] 
 **sort_order** | **str**| Sort in ascending or descending order by purchase order creation date. | [optional] 
 **next_token** | **str**| Used for pagination when there are more shipments than the specified result size limit. | [optional] 
 **created_after** | **datetime**| Get Shipment Details that became available after this timestamp will be included in the result. Must be in &lt;a href&#x3D;&#39;https://developer-docs.amazon.com/sp-api/docs/iso-8601&#39;&gt;ISO 8601&lt;/a&gt; format. | [optional] 
 **created_before** | **datetime**| Get Shipment Details that became available before this timestamp will be included in the result. Must be in &lt;a href&#x3D;&#39;https://developer-docs.amazon.com/sp-api/docs/iso-8601&#39;&gt;ISO 8601&lt;/a&gt; format. | [optional] 
 **shipment_confirmed_before** | **datetime**| Get Shipment Details by passing Shipment confirmed create Date Before. Must be in &lt;a href&#x3D;&#39;https://developer-docs.amazon.com/sp-api/docs/iso-8601&#39;&gt;ISO 8601&lt;/a&gt; format. | [optional] 
 **shipment_confirmed_after** | **datetime**| Get Shipment Details by passing Shipment confirmed create Date After. Must be in &lt;a href&#x3D;&#39;https://developer-docs.amazon.com/sp-api/docs/iso-8601&#39;&gt;ISO 8601&lt;/a&gt; format. | [optional] 
 **package_label_created_before** | **datetime**| Get Shipment Details by passing Package label create Date by buyer. Must be in &lt;a href&#x3D;&#39;https://developer-docs.amazon.com/sp-api/docs/iso-8601&#39;&gt;ISO 8601&lt;/a&gt; format. | [optional] 
 **package_label_created_after** | **datetime**| Get Shipment Details by passing Package label create Date After by buyer. Must be in &lt;a href&#x3D;&#39;https://developer-docs.amazon.com/sp-api/docs/iso-8601&#39;&gt;ISO 8601&lt;/a&gt; format. | [optional] 
 **shipped_before** | **datetime**| Get Shipment Details by passing Shipped Date Before. Must be in &lt;a href&#x3D;&#39;https://developer-docs.amazon.com/sp-api/docs/iso-8601&#39;&gt;ISO 8601&lt;/a&gt; format. | [optional] 
 **shipped_after** | **datetime**| Get Shipment Details by passing Shipped Date After. Must be in &lt;a href&#x3D;&#39;https://developer-docs.amazon.com/sp-api/docs/iso-8601&#39;&gt;ISO 8601&lt;/a&gt; format. | [optional] 
 **estimated_delivery_before** | **datetime**| Get Shipment Details by passing Estimated Delivery Date Before. Must be in &lt;a href&#x3D;&#39;https://developer-docs.amazon.com/sp-api/docs/iso-8601&#39;&gt;ISO 8601&lt;/a&gt; format. | [optional] 
 **estimated_delivery_after** | **datetime**| Get Shipment Details by passing Estimated Delivery Date Before. Must be in &lt;a href&#x3D;&#39;https://developer-docs.amazon.com/sp-api/docs/iso-8601&#39;&gt;ISO 8601&lt;/a&gt; format. | [optional] 
 **shipment_delivery_before** | **datetime**| Get Shipment Details by passing Shipment Delivery Date Before. Must be in &lt;a href&#x3D;&#39;https://developer-docs.amazon.com/sp-api/docs/iso-8601&#39;&gt;ISO 8601&lt;/a&gt; format. | [optional] 
 **shipment_delivery_after** | **datetime**| Get Shipment Details by passing Shipment Delivery Date After. Must be in &lt;a href&#x3D;&#39;https://developer-docs.amazon.com/sp-api/docs/iso-8601&#39;&gt;ISO 8601&lt;/a&gt; format. | [optional] 
 **requested_pick_up_before** | **datetime**| Get Shipment Details by passing Before Requested pickup date. Must be in &lt;a href&#x3D;&#39;https://developer-docs.amazon.com/sp-api/docs/iso-8601&#39;&gt;ISO 8601&lt;/a&gt; format. | [optional] 
 **requested_pick_up_after** | **datetime**| Get Shipment Details by passing After Requested pickup date. Must be in &lt;a href&#x3D;&#39;https://developer-docs.amazon.com/sp-api/docs/iso-8601&#39;&gt;ISO 8601&lt;/a&gt; format. | [optional] 
 **scheduled_pick_up_before** | **datetime**| Get Shipment Details by passing Before scheduled pickup date. Must be in &lt;a href&#x3D;&#39;https://developer-docs.amazon.com/sp-api/docs/iso-8601&#39;&gt;ISO 8601&lt;/a&gt; format. | [optional] 
 **scheduled_pick_up_after** | **datetime**| Get Shipment Details by passing After Scheduled pickup date. Must be in &lt;a href&#x3D;&#39;https://developer-docs.amazon.com/sp-api/docs/iso-8601&#39;&gt;ISO 8601&lt;/a&gt; format. | [optional] 
 **current_shipment_status** | **str**| Get Shipment Details by passing Current shipment status. | [optional] 
 **vendor_shipment_identifier** | **str**| Get Shipment Details by passing Vendor Shipment ID | [optional] 
 **buyer_reference_number** | **str**| Get Shipment Details by passing buyer Reference ID | [optional] 
 **buyer_warehouse_code** | **str**| Get Shipping Details based on buyer warehouse code. This value should be same as &#39;shipToParty.partyId&#39; in the Shipment. | [optional] 
 **seller_warehouse_code** | **str**| Get Shipping Details based on vendor warehouse code. This value should be same as &#39;sellingParty.partyId&#39; in the Shipment. | [optional] 

### Return type

[**GetShipmentDetailsResponse**](GetShipmentDetailsResponse.md)

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

# **get_shipment_labels**
> GetShipmentLabels get_shipment_labels(limit=limit, sort_order=sort_order, next_token=next_token, label_created_after=label_created_after, label_created_before=label_created_before, buyer_reference_number=buyer_reference_number, vendor_shipment_identifier=vendor_shipment_identifier, seller_warehouse_code=seller_warehouse_code)



Returns small parcel shipment labels based on the filters that you specify.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 10 | 10 |  The `x-amzn-RateLimit-Limit` response header contains the usage plan rate limits for the operation, when available. The preceding table contains the default rate and burst values for this operation. Selling partners whose business demands require higher throughput might have higher rate and burst values than those shown here. For more information, refer to [Usage Plans and Rate Limits](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.vendorShipments
from py_sp_api.generated.vendorShipments.models.get_shipment_labels import GetShipmentLabels
from py_sp_api.generated.vendorShipments.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.vendorShipments.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.vendorShipments.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.vendorShipments.VendorShippingApi(api_client)
    limit = 56 # int | The limit to the number of records returned. Default value is 50 records. (optional)
    sort_order = 'sort_order_example' # str | Sort the list by shipment label creation date in ascending or descending order. (optional)
    next_token = 'next_token_example' # str | A token that is used to retrieve the next page of results. The response includes `nextToken` when the number of results exceeds the specified `pageSize` value. To get the next page of results, call the operation with this token and include the same arguments as the call that produced the token. To get a complete list, call this operation until `nextToken` is null. Note that this operation can return empty pages. (optional)
    label_created_after = '2013-10-20T19:20:30+01:00' # datetime | Shipment labels created after this time will be included in the result. This field must be in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) datetime format. (optional)
    label_created_before = '2013-10-20T19:20:30+01:00' # datetime | Shipment labels created before this time will be included in the result. This field must be in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) datetime format. (optional)
    buyer_reference_number = 'buyer_reference_number_example' # str | Get Shipment labels by passing buyer reference number. (optional)
    vendor_shipment_identifier = 'vendor_shipment_identifier_example' # str | Get Shipment labels by passing vendor shipment identifier. (optional)
    seller_warehouse_code = 'seller_warehouse_code_example' # str | Get Shipping labels based on vendor warehouse code. This value must be same as the `sellingParty.partyId` in the shipment. (optional)

    try:
        api_response = api_instance.get_shipment_labels(limit=limit, sort_order=sort_order, next_token=next_token, label_created_after=label_created_after, label_created_before=label_created_before, buyer_reference_number=buyer_reference_number, vendor_shipment_identifier=vendor_shipment_identifier, seller_warehouse_code=seller_warehouse_code)
        print("The response of VendorShippingApi->get_shipment_labels:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VendorShippingApi->get_shipment_labels: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| The limit to the number of records returned. Default value is 50 records. | [optional] 
 **sort_order** | **str**| Sort the list by shipment label creation date in ascending or descending order. | [optional] 
 **next_token** | **str**| A token that is used to retrieve the next page of results. The response includes &#x60;nextToken&#x60; when the number of results exceeds the specified &#x60;pageSize&#x60; value. To get the next page of results, call the operation with this token and include the same arguments as the call that produced the token. To get a complete list, call this operation until &#x60;nextToken&#x60; is null. Note that this operation can return empty pages. | [optional] 
 **label_created_after** | **datetime**| Shipment labels created after this time will be included in the result. This field must be in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) datetime format. | [optional] 
 **label_created_before** | **datetime**| Shipment labels created before this time will be included in the result. This field must be in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) datetime format. | [optional] 
 **buyer_reference_number** | **str**| Get Shipment labels by passing buyer reference number. | [optional] 
 **vendor_shipment_identifier** | **str**| Get Shipment labels by passing vendor shipment identifier. | [optional] 
 **seller_warehouse_code** | **str**| Get Shipping labels based on vendor warehouse code. This value must be same as the &#x60;sellingParty.partyId&#x60; in the shipment. | [optional] 

### Return type

[**GetShipmentLabels**](GetShipmentLabels.md)

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
> SubmitShipmentConfirmationsResponse submit_shipment_confirmations(body)

SubmitShipmentConfirmations

Submits one or more shipment confirmations for vendor orders.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 10 | 10 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.vendorShipments
from py_sp_api.generated.vendorShipments.models.submit_shipment_confirmations_request import SubmitShipmentConfirmationsRequest
from py_sp_api.generated.vendorShipments.models.submit_shipment_confirmations_response import SubmitShipmentConfirmationsResponse
from py_sp_api.generated.vendorShipments.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.vendorShipments.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.vendorShipments.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.vendorShipments.VendorShippingApi(api_client)
    body = py_sp_api.generated.vendorShipments.SubmitShipmentConfirmationsRequest() # SubmitShipmentConfirmationsRequest | A request to submit shipment confirmation.

    try:
        # SubmitShipmentConfirmations
        api_response = api_instance.submit_shipment_confirmations(body)
        print("The response of VendorShippingApi->submit_shipment_confirmations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VendorShippingApi->submit_shipment_confirmations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SubmitShipmentConfirmationsRequest**](SubmitShipmentConfirmationsRequest.md)| A request to submit shipment confirmation. | 

### Return type

[**SubmitShipmentConfirmationsResponse**](SubmitShipmentConfirmationsResponse.md)

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

# **submit_shipments**
> SubmitShipmentConfirmationsResponse submit_shipments(body)

SubmitShipments

Submits one or more shipment request for vendor Orders.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 10 | 10 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.vendorShipments
from py_sp_api.generated.vendorShipments.models.submit_shipment_confirmations_response import SubmitShipmentConfirmationsResponse
from py_sp_api.generated.vendorShipments.models.submit_shipments import SubmitShipments
from py_sp_api.generated.vendorShipments.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.vendorShipments.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.vendorShipments.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.vendorShipments.VendorShippingApi(api_client)
    body = py_sp_api.generated.vendorShipments.SubmitShipments() # SubmitShipments | A request to submit shipment request.

    try:
        # SubmitShipments
        api_response = api_instance.submit_shipments(body)
        print("The response of VendorShippingApi->submit_shipments:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VendorShippingApi->submit_shipments: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SubmitShipments**](SubmitShipments.md)| A request to submit shipment request. | 

### Return type

[**SubmitShipmentConfirmationsResponse**](SubmitShipmentConfirmationsResponse.md)

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

