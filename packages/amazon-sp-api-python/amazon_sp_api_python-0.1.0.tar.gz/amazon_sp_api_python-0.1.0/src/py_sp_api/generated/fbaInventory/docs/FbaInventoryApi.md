# py_sp_api.generated.fbaInventory.FbaInventoryApi

All URIs are relative to *https://sellingpartnerapi-na.amazon.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_inventory**](FbaInventoryApi.md#add_inventory) | **POST** /fba/inventory/v1/items/inventory | 
[**create_inventory_item**](FbaInventoryApi.md#create_inventory_item) | **POST** /fba/inventory/v1/items | 
[**delete_inventory_item**](FbaInventoryApi.md#delete_inventory_item) | **DELETE** /fba/inventory/v1/items/{sellerSku} | 
[**get_inventory_summaries**](FbaInventoryApi.md#get_inventory_summaries) | **GET** /fba/inventory/v1/summaries | 


# **add_inventory**
> AddInventoryResponse add_inventory(x_amzn_idempotency_token, add_inventory_request_body)



Requests that Amazon add items to the Sandbox Inventory with desired amount of quantity in the sandbox environment. This is a sandbox-only operation and must be directed to a sandbox endpoint. Refer to [Selling Partner API sandbox](https://developer-docs.amazon.com/sp-api/docs/the-selling-partner-api-sandbox) for more information.

### Example


```python
import py_sp_api.generated.fbaInventory
from py_sp_api.generated.fbaInventory.models.add_inventory_request import AddInventoryRequest
from py_sp_api.generated.fbaInventory.models.add_inventory_response import AddInventoryResponse
from py_sp_api.generated.fbaInventory.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.fbaInventory.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.fbaInventory.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.fbaInventory.FbaInventoryApi(api_client)
    x_amzn_idempotency_token = 'x_amzn_idempotency_token_example' # str | A unique token/requestId provided with each call to ensure idempotency.
    add_inventory_request_body = py_sp_api.generated.fbaInventory.AddInventoryRequest() # AddInventoryRequest | List of items to add to Sandbox inventory.

    try:
        api_response = api_instance.add_inventory(x_amzn_idempotency_token, add_inventory_request_body)
        print("The response of FbaInventoryApi->add_inventory:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FbaInventoryApi->add_inventory: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_amzn_idempotency_token** | **str**| A unique token/requestId provided with each call to ensure idempotency. | 
 **add_inventory_request_body** | [**AddInventoryRequest**](AddInventoryRequest.md)| List of items to add to Sandbox inventory. | 

### Return type

[**AddInventoryResponse**](AddInventoryResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**403** | Indicates access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, Invalid Signature or Resource Not Found. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The specified resource does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_inventory_item**
> CreateInventoryItemResponse create_inventory_item(create_inventory_item_request_body)



Requests that Amazon create product-details in the Sandbox Inventory in the sandbox environment. This is a sandbox-only operation and must be directed to a sandbox endpoint. Refer to [Selling Partner API sandbox](https://developer-docs.amazon.com/sp-api/docs/the-selling-partner-api-sandbox) for more information.

### Example


```python
import py_sp_api.generated.fbaInventory
from py_sp_api.generated.fbaInventory.models.create_inventory_item_request import CreateInventoryItemRequest
from py_sp_api.generated.fbaInventory.models.create_inventory_item_response import CreateInventoryItemResponse
from py_sp_api.generated.fbaInventory.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.fbaInventory.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.fbaInventory.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.fbaInventory.FbaInventoryApi(api_client)
    create_inventory_item_request_body = py_sp_api.generated.fbaInventory.CreateInventoryItemRequest() # CreateInventoryItemRequest | CreateInventoryItem Request Body Parameter.

    try:
        api_response = api_instance.create_inventory_item(create_inventory_item_request_body)
        print("The response of FbaInventoryApi->create_inventory_item:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FbaInventoryApi->create_inventory_item: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_inventory_item_request_body** | [**CreateInventoryItemRequest**](CreateInventoryItemRequest.md)| CreateInventoryItem Request Body Parameter. | 

### Return type

[**CreateInventoryItemResponse**](CreateInventoryItemResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**403** | Indicates access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, Invalid Signature or Resource Not Found. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The specified resource does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_inventory_item**
> DeleteInventoryItemResponse delete_inventory_item(seller_sku, marketplace_id)



Requests that Amazon Deletes an item from the Sandbox Inventory in the sandbox environment. This is a sandbox-only operation and must be directed to a sandbox endpoint. Refer to [Selling Partner API sandbox](https://developer-docs.amazon.com/sp-api/docs/the-selling-partner-api-sandbox) for more information.

### Example


```python
import py_sp_api.generated.fbaInventory
from py_sp_api.generated.fbaInventory.models.delete_inventory_item_response import DeleteInventoryItemResponse
from py_sp_api.generated.fbaInventory.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.fbaInventory.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.fbaInventory.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.fbaInventory.FbaInventoryApi(api_client)
    seller_sku = 'seller_sku_example' # str | A single seller SKU used for querying the specified seller SKU inventory summaries.
    marketplace_id = 'marketplace_id_example' # str | The marketplace ID for the marketplace for which the sellerSku is to be deleted.

    try:
        api_response = api_instance.delete_inventory_item(seller_sku, marketplace_id)
        print("The response of FbaInventoryApi->delete_inventory_item:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FbaInventoryApi->delete_inventory_item: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **seller_sku** | **str**| A single seller SKU used for querying the specified seller SKU inventory summaries. | 
 **marketplace_id** | **str**| The marketplace ID for the marketplace for which the sellerSku is to be deleted. | 

### Return type

[**DeleteInventoryItemResponse**](DeleteInventoryItemResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**403** | Indicates access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, Invalid Signature or Resource Not Found. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The specified resource does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_inventory_summaries**
> GetInventorySummariesResponse get_inventory_summaries(granularity_type, granularity_id, marketplace_ids, details=details, start_date_time=start_date_time, seller_skus=seller_skus, seller_sku=seller_sku, next_token=next_token)



Returns a list of inventory summaries. The summaries returned depend on the presence or absence of the startDateTime, sellerSkus and sellerSku parameters:  - All inventory summaries with available details are returned when the startDateTime, sellerSkus and sellerSku parameters are omitted. - When startDateTime is provided, the operation returns inventory summaries that have had changes after the date and time specified. The sellerSkus and sellerSku parameters are ignored. Important: To avoid errors, use both startDateTime and nextToken to get the next page of inventory summaries that have changed after the date and time specified. - When the sellerSkus parameter is provided, the operation returns inventory summaries for only the specified sellerSkus. The sellerSku parameter is ignored. - When the sellerSku parameter is provided, the operation returns inventory summaries for only the specified sellerSku.  Note: The parameters associated with this operation may contain special characters that must be encoded to successfully call the API. To avoid errors with SKUs when encoding URLs, refer to [URL Encoding](https://developer-docs.amazon.com/sp-api/docs/url-encoding).  Usage Plan:  | Rate (requests per second) | Burst | | ---- | ---- | | 2 | 2 |  The x-amzn-RateLimit-Limit response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits).

### Example


```python
import py_sp_api.generated.fbaInventory
from py_sp_api.generated.fbaInventory.models.get_inventory_summaries_response import GetInventorySummariesResponse
from py_sp_api.generated.fbaInventory.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.fbaInventory.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.fbaInventory.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.fbaInventory.FbaInventoryApi(api_client)
    granularity_type = 'granularity_type_example' # str | The granularity type for the inventory aggregation level.
    granularity_id = 'granularity_id_example' # str | The granularity ID for the inventory aggregation level.
    marketplace_ids = ['marketplace_ids_example'] # List[str] | The marketplace ID for the marketplace for which to return inventory summaries.
    details = False # bool | true to return inventory summaries with additional summarized inventory details and quantities. Otherwise, returns inventory summaries only (default value). (optional) (default to False)
    start_date_time = '2013-10-20T19:20:30+01:00' # datetime | A start date and time in ISO8601 format. If specified, all inventory summaries that have changed since then are returned. You must specify a date and time that is no earlier than 18 months prior to the date and time when you call the API. Note: Changes in inboundWorkingQuantity, inboundShippedQuantity and inboundReceivingQuantity are not detected. (optional)
    seller_skus = ['seller_skus_example'] # List[str] | A list of seller SKUs for which to return inventory summaries. You may specify up to 50 SKUs. (optional)
    seller_sku = 'seller_sku_example' # str | A single seller SKU used for querying the specified seller SKU inventory summaries. (optional)
    next_token = 'next_token_example' # str | String token returned in the response of your previous request. The string token will expire 30 seconds after being created. (optional)

    try:
        api_response = api_instance.get_inventory_summaries(granularity_type, granularity_id, marketplace_ids, details=details, start_date_time=start_date_time, seller_skus=seller_skus, seller_sku=seller_sku, next_token=next_token)
        print("The response of FbaInventoryApi->get_inventory_summaries:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FbaInventoryApi->get_inventory_summaries: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **granularity_type** | **str**| The granularity type for the inventory aggregation level. | 
 **granularity_id** | **str**| The granularity ID for the inventory aggregation level. | 
 **marketplace_ids** | [**List[str]**](str.md)| The marketplace ID for the marketplace for which to return inventory summaries. | 
 **details** | **bool**| true to return inventory summaries with additional summarized inventory details and quantities. Otherwise, returns inventory summaries only (default value). | [optional] [default to False]
 **start_date_time** | **datetime**| A start date and time in ISO8601 format. If specified, all inventory summaries that have changed since then are returned. You must specify a date and time that is no earlier than 18 months prior to the date and time when you call the API. Note: Changes in inboundWorkingQuantity, inboundShippedQuantity and inboundReceivingQuantity are not detected. | [optional] 
 **seller_skus** | [**List[str]**](str.md)| A list of seller SKUs for which to return inventory summaries. You may specify up to 50 SKUs. | [optional] 
 **seller_sku** | **str**| A single seller SKU used for querying the specified seller SKU inventory summaries. | [optional] 
 **next_token** | **str**| String token returned in the response of your previous request. The string token will expire 30 seconds after being created. | [optional] 

### Return type

[**GetInventorySummariesResponse**](GetInventorySummariesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, Invalid Signature or Resource Not Found. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The specified resource does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

