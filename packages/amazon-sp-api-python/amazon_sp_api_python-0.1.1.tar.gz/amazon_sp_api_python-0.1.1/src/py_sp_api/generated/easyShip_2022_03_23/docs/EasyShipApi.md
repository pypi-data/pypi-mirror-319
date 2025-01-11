# py_sp_api.generated.easyShip_2022_03_23.EasyShipApi

All URIs are relative to *https://sellingpartnerapi-na.amazon.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_scheduled_package**](EasyShipApi.md#create_scheduled_package) | **POST** /easyShip/2022-03-23/package | 
[**create_scheduled_package_bulk**](EasyShipApi.md#create_scheduled_package_bulk) | **POST** /easyShip/2022-03-23/packages/bulk | 
[**get_scheduled_package**](EasyShipApi.md#get_scheduled_package) | **GET** /easyShip/2022-03-23/package | 
[**list_handover_slots**](EasyShipApi.md#list_handover_slots) | **POST** /easyShip/2022-03-23/timeSlot | 
[**update_scheduled_packages**](EasyShipApi.md#update_scheduled_packages) | **PATCH** /easyShip/2022-03-23/package | 


# **create_scheduled_package**
> Package create_scheduled_package(create_scheduled_package_request)



Schedules an Easy Ship order and returns the scheduled package information.  This operation does the following:  *  Specifies the time slot and handover method for the order to be scheduled for delivery.  * Updates the Easy Ship order status.  * Generates a shipping label and an invoice. Calling `createScheduledPackage` also generates a warranty document if you specify a `SerialNumber` value. To get these documents, see [How to get invoice, shipping label, and warranty documents](doc:easyship-api-v2022-03-23-use-case-guide).  * Shows the status of Easy Ship orders when you call the `getOrders` operation of the Selling Partner API for Orders and examine the `EasyShipShipmentStatus` property in the response body.  See the **Shipping Label**, **Invoice**, and **Warranty** columns in the [Marketplace Support Table](doc:easyship-api-v2022-03-23-use-case-guide#marketplace-support-table) to see which documents are supported in each marketplace.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 1 | 5 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.easyShip_2022_03_23
from py_sp_api.generated.easyShip_2022_03_23.models.create_scheduled_package_request import CreateScheduledPackageRequest
from py_sp_api.generated.easyShip_2022_03_23.models.package import Package
from py_sp_api.generated.easyShip_2022_03_23.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.easyShip_2022_03_23.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.easyShip_2022_03_23.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.easyShip_2022_03_23.EasyShipApi(api_client)
    create_scheduled_package_request = py_sp_api.generated.easyShip_2022_03_23.CreateScheduledPackageRequest() # CreateScheduledPackageRequest | The request schema for the `createScheduledPackage` operation.

    try:
        api_response = api_instance.create_scheduled_package(create_scheduled_package_request)
        print("The response of EasyShipApi->create_scheduled_package:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EasyShipApi->create_scheduled_package: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_scheduled_package_request** | [**CreateScheduledPackageRequest**](CreateScheduledPackageRequest.md)| The request schema for the &#x60;createScheduledPackage&#x60; operation. | 

### Return type

[**Package**](Package.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**401** | The request&#39;s Authorization header is not formatted correctly or does not contain a valid token. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_scheduled_package_bulk**
> CreateScheduledPackagesResponse create_scheduled_package_bulk(create_scheduled_packages_request)



This operation automatically schedules a time slot for all specified `amazonOrderId` values and generates the associated shipping labels and compliance documents based on the marketplace. For more information, refer to the [marketplace support table](https://developer-docs.amazon.com/sp-api/docs/easyship-api-v2022-03-23-use-case-guide#marketplace-support-table).  You can optionally assign a `packageDetails` object to input a preferred time slot for each order in your request. In such cases, Amazon schedules the respective packages using the specified optional settings. If you don't specify a time slot, Amazon assigns the earliest available time slot.   You can choose PDF or ZPL for your shipping label's file format and Amazon creates the label accordingly.  This operation returns an array that contains the scheduled packages, and a temporary URL that you can use to access a ZIP file. The ZIP file includes the generated shipping labels and any other documents that are required for your marketplace. If an order can't be scheduled, Amazon adds the `rejectedOrders` list in the response. The response contains an entry for each order that could not be processed. Each entry contains an error message that describes the reason for the failure.  The following table contains the supported request and burst maximum rates:  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 1 | 5 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that are applied to the requested operation, when available. The preceding table contains the default rate and burst values for this operation. Selling partners whose business demands require higher throughput might have higher rate and burst values than those shown here. For more information, refer to [Usage Plans and Rate Limits in the Selling Partner API](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.easyShip_2022_03_23
from py_sp_api.generated.easyShip_2022_03_23.models.create_scheduled_packages_request import CreateScheduledPackagesRequest
from py_sp_api.generated.easyShip_2022_03_23.models.create_scheduled_packages_response import CreateScheduledPackagesResponse
from py_sp_api.generated.easyShip_2022_03_23.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.easyShip_2022_03_23.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.easyShip_2022_03_23.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.easyShip_2022_03_23.EasyShipApi(api_client)
    create_scheduled_packages_request = py_sp_api.generated.easyShip_2022_03_23.CreateScheduledPackagesRequest() # CreateScheduledPackagesRequest | The request schema for the `createScheduledPackageBulk` operation.

    try:
        api_response = api_instance.create_scheduled_package_bulk(create_scheduled_packages_request)
        print("The response of EasyShipApi->create_scheduled_package_bulk:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EasyShipApi->create_scheduled_package_bulk: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_scheduled_packages_request** | [**CreateScheduledPackagesRequest**](CreateScheduledPackagesRequest.md)| The request schema for the &#x60;createScheduledPackageBulk&#x60; operation. | 

### Return type

[**CreateScheduledPackagesResponse**](CreateScheduledPackagesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**401** | The request&#39;s Authorization header is not formatted correctly or does not contain a valid token. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_scheduled_package**
> Package get_scheduled_package(amazon_order_id, marketplace_id)



Returns information about a package, including dimensions, weight, time slot information for handover, invoice and item information, and status.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 1 | 5 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.easyShip_2022_03_23
from py_sp_api.generated.easyShip_2022_03_23.models.package import Package
from py_sp_api.generated.easyShip_2022_03_23.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.easyShip_2022_03_23.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.easyShip_2022_03_23.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.easyShip_2022_03_23.EasyShipApi(api_client)
    amazon_order_id = 'amazon_order_id_example' # str | An Amazon-defined order identifier. Identifies the order that the seller wants to deliver using Amazon Easy Ship.
    marketplace_id = 'marketplace_id_example' # str | An identifier for the marketplace in which the seller is selling.

    try:
        api_response = api_instance.get_scheduled_package(amazon_order_id, marketplace_id)
        print("The response of EasyShipApi->get_scheduled_package:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EasyShipApi->get_scheduled_package: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **amazon_order_id** | **str**| An Amazon-defined order identifier. Identifies the order that the seller wants to deliver using Amazon Easy Ship. | 
 **marketplace_id** | **str**| An identifier for the marketplace in which the seller is selling. | 

### Return type

[**Package**](Package.md)

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
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_handover_slots**
> ListHandoverSlotsResponse list_handover_slots(list_handover_slots_request=list_handover_slots_request)



Returns time slots available for Easy Ship orders to be scheduled based on the package weight and dimensions that the seller specifies.  This operation is available for scheduled and unscheduled orders based on marketplace support. See **Get Time Slots** in the [Marketplace Support Table](doc:easyship-api-v2022-03-23-use-case-guide#marketplace-support-table).  This operation can return time slots that have either pickup or drop-off handover methods - see **Supported Handover Methods** in the [Marketplace Support Table](doc:easyship-api-v2022-03-23-use-case-guide#marketplace-support-table).  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 1 | 5 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.easyShip_2022_03_23
from py_sp_api.generated.easyShip_2022_03_23.models.list_handover_slots_request import ListHandoverSlotsRequest
from py_sp_api.generated.easyShip_2022_03_23.models.list_handover_slots_response import ListHandoverSlotsResponse
from py_sp_api.generated.easyShip_2022_03_23.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.easyShip_2022_03_23.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.easyShip_2022_03_23.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.easyShip_2022_03_23.EasyShipApi(api_client)
    list_handover_slots_request = py_sp_api.generated.easyShip_2022_03_23.ListHandoverSlotsRequest() # ListHandoverSlotsRequest | The request schema for the `listHandoverSlots` operation. (optional)

    try:
        api_response = api_instance.list_handover_slots(list_handover_slots_request=list_handover_slots_request)
        print("The response of EasyShipApi->list_handover_slots:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EasyShipApi->list_handover_slots: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **list_handover_slots_request** | [**ListHandoverSlotsRequest**](ListHandoverSlotsRequest.md)| The request schema for the &#x60;listHandoverSlots&#x60; operation. | [optional] 

### Return type

[**ListHandoverSlotsResponse**](ListHandoverSlotsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**401** | The request&#39;s Authorization header is not formatted correctly or does not contain a valid token. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_scheduled_packages**
> Packages update_scheduled_packages(update_scheduled_packages_request=update_scheduled_packages_request)



Updates the time slot for handing over the package indicated by the specified `scheduledPackageId`. You can get the new `slotId` value for the time slot by calling the `listHandoverSlots` operation before making another `patch` call.  See the **Update Package** column in the [Marketplace Support Table](doc:easyship-api-v2022-03-23-use-case-guide#marketplace-support-table) to see which marketplaces this operation is supported in.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 1 | 5 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.easyShip_2022_03_23
from py_sp_api.generated.easyShip_2022_03_23.models.packages import Packages
from py_sp_api.generated.easyShip_2022_03_23.models.update_scheduled_packages_request import UpdateScheduledPackagesRequest
from py_sp_api.generated.easyShip_2022_03_23.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.easyShip_2022_03_23.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.easyShip_2022_03_23.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.easyShip_2022_03_23.EasyShipApi(api_client)
    update_scheduled_packages_request = py_sp_api.generated.easyShip_2022_03_23.UpdateScheduledPackagesRequest() # UpdateScheduledPackagesRequest | The request schema for the `updateScheduledPackages` operation. (optional)

    try:
        api_response = api_instance.update_scheduled_packages(update_scheduled_packages_request=update_scheduled_packages_request)
        print("The response of EasyShipApi->update_scheduled_packages:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EasyShipApi->update_scheduled_packages: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **update_scheduled_packages_request** | [**UpdateScheduledPackagesRequest**](UpdateScheduledPackagesRequest.md)| The request schema for the &#x60;updateScheduledPackages&#x60; operation. | [optional] 

### Return type

[**Packages**](Packages.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**401** | The request&#39;s Authorization header is not formatted correctly or does not contain a valid token. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

