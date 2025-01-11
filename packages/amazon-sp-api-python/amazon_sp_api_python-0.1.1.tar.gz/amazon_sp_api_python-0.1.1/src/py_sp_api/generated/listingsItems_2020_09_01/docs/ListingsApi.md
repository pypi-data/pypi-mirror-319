# py_sp_api.generated.listingsItems_2020_09_01.ListingsApi

All URIs are relative to *https://sellingpartnerapi-na.amazon.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_listings_item**](ListingsApi.md#delete_listings_item) | **DELETE** /listings/2020-09-01/items/{sellerId}/{sku} | 
[**patch_listings_item**](ListingsApi.md#patch_listings_item) | **PATCH** /listings/2020-09-01/items/{sellerId}/{sku} | 
[**put_listings_item**](ListingsApi.md#put_listings_item) | **PUT** /listings/2020-09-01/items/{sellerId}/{sku} | 


# **delete_listings_item**
> ListingsItemSubmissionResponse delete_listings_item(seller_id, sku, marketplace_ids, issue_locale=issue_locale)



Delete a listings item for a selling partner.  **Note:** The parameters associated with this operation may contain special characters that must be encoded to successfully call the API. To avoid errors with SKUs when encoding URLs, refer to [URL Encoding](https://developer-docs.amazon.com/sp-api/docs/url-encoding).  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 5 | 10 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.listingsItems_2020_09_01
from py_sp_api.generated.listingsItems_2020_09_01.models.listings_item_submission_response import ListingsItemSubmissionResponse
from py_sp_api.generated.listingsItems_2020_09_01.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.listingsItems_2020_09_01.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.listingsItems_2020_09_01.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.listingsItems_2020_09_01.ListingsApi(api_client)
    seller_id = 'seller_id_example' # str | A selling partner identifier, such as a merchant account or vendor code.
    sku = 'sku_example' # str | A selling partner provided identifier for an Amazon listing.
    marketplace_ids = ['ATVPDKIKX0DER'] # List[str] | A comma-delimited list of Amazon marketplace identifiers for the request.
    issue_locale = 'en_US' # str | A locale for localization of issues. When not provided, the default language code of the first marketplace is used. Examples: \"en_US\", \"fr_CA\", \"fr_FR\". Localized messages default to \"en_US\" when a localization is not available in the specified locale. (optional)

    try:
        api_response = api_instance.delete_listings_item(seller_id, sku, marketplace_ids, issue_locale=issue_locale)
        print("The response of ListingsApi->delete_listings_item:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ListingsApi->delete_listings_item: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **seller_id** | **str**| A selling partner identifier, such as a merchant account or vendor code. | 
 **sku** | **str**| A selling partner provided identifier for an Amazon listing. | 
 **marketplace_ids** | [**List[str]**](str.md)| A comma-delimited list of Amazon marketplace identifiers for the request. | 
 **issue_locale** | **str**| A locale for localization of issues. When not provided, the default language code of the first marketplace is used. Examples: \&quot;en_US\&quot;, \&quot;fr_CA\&quot;, \&quot;fr_FR\&quot;. Localized messages default to \&quot;en_US\&quot; when a localization is not available in the specified locale. | [optional] 

### Return type

[**ListingsItemSubmissionResponse**](ListingsItemSubmissionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully understood the listings item delete request. See the response to determine whether the submission has been accepted. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_listings_item**
> ListingsItemSubmissionResponse patch_listings_item(seller_id, sku, marketplace_ids, body, issue_locale=issue_locale)



Partially update (patch) a listings item for a selling partner. Only top-level listings item attributes can be patched. Patching nested attributes is not supported.  **Note:** The parameters associated with this operation may contain special characters that must be encoded to successfully call the API. To avoid errors with SKUs when encoding URLs, refer to [URL Encoding](https://developer-docs.amazon.com/sp-api/docs/url-encoding).  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 5 | 10 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.listingsItems_2020_09_01
from py_sp_api.generated.listingsItems_2020_09_01.models.listings_item_patch_request import ListingsItemPatchRequest
from py_sp_api.generated.listingsItems_2020_09_01.models.listings_item_submission_response import ListingsItemSubmissionResponse
from py_sp_api.generated.listingsItems_2020_09_01.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.listingsItems_2020_09_01.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.listingsItems_2020_09_01.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.listingsItems_2020_09_01.ListingsApi(api_client)
    seller_id = 'seller_id_example' # str | A selling partner identifier, such as a merchant account or vendor code.
    sku = 'sku_example' # str | A selling partner provided identifier for an Amazon listing.
    marketplace_ids = ['ATVPDKIKX0DER'] # List[str] | A comma-delimited list of Amazon marketplace identifiers for the request.
    body = py_sp_api.generated.listingsItems_2020_09_01.ListingsItemPatchRequest() # ListingsItemPatchRequest | The request body schema for the patchListingsItem operation.
    issue_locale = 'en_US' # str | A locale for localization of issues. When not provided, the default language code of the first marketplace is used. Examples: \"en_US\", \"fr_CA\", \"fr_FR\". Localized messages default to \"en_US\" when a localization is not available in the specified locale. (optional)

    try:
        api_response = api_instance.patch_listings_item(seller_id, sku, marketplace_ids, body, issue_locale=issue_locale)
        print("The response of ListingsApi->patch_listings_item:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ListingsApi->patch_listings_item: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **seller_id** | **str**| A selling partner identifier, such as a merchant account or vendor code. | 
 **sku** | **str**| A selling partner provided identifier for an Amazon listing. | 
 **marketplace_ids** | [**List[str]**](str.md)| A comma-delimited list of Amazon marketplace identifiers for the request. | 
 **body** | [**ListingsItemPatchRequest**](ListingsItemPatchRequest.md)| The request body schema for the patchListingsItem operation. | 
 **issue_locale** | **str**| A locale for localization of issues. When not provided, the default language code of the first marketplace is used. Examples: \&quot;en_US\&quot;, \&quot;fr_CA\&quot;, \&quot;fr_FR\&quot;. Localized messages default to \&quot;en_US\&quot; when a localization is not available in the specified locale. | [optional] 

### Return type

[**ListingsItemSubmissionResponse**](ListingsItemSubmissionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully understood the listings item patch request. See the response to determine if the submission was accepted. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_listings_item**
> ListingsItemSubmissionResponse put_listings_item(seller_id, sku, marketplace_ids, body, issue_locale=issue_locale)



Creates a new or fully-updates an existing listings item for a selling partner.  **Note:** The parameters associated with this operation may contain special characters that must be encoded to successfully call the API. To avoid errors with SKUs when encoding URLs, refer to [URL Encoding](https://developer-docs.amazon.com/sp-api/docs/url-encoding).  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 5 | 10 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.listingsItems_2020_09_01
from py_sp_api.generated.listingsItems_2020_09_01.models.listings_item_put_request import ListingsItemPutRequest
from py_sp_api.generated.listingsItems_2020_09_01.models.listings_item_submission_response import ListingsItemSubmissionResponse
from py_sp_api.generated.listingsItems_2020_09_01.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.listingsItems_2020_09_01.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.listingsItems_2020_09_01.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.listingsItems_2020_09_01.ListingsApi(api_client)
    seller_id = 'seller_id_example' # str | A selling partner identifier, such as a merchant account or vendor code.
    sku = 'sku_example' # str | A selling partner provided identifier for an Amazon listing.
    marketplace_ids = ['ATVPDKIKX0DER'] # List[str] | A comma-delimited list of Amazon marketplace identifiers for the request.
    body = py_sp_api.generated.listingsItems_2020_09_01.ListingsItemPutRequest() # ListingsItemPutRequest | The request body schema for the putListingsItem operation.
    issue_locale = 'en_US' # str | A locale for localization of issues. When not provided, the default language code of the first marketplace is used. Examples: \"en_US\", \"fr_CA\", \"fr_FR\". Localized messages default to \"en_US\" when a localization is not available in the specified locale. (optional)

    try:
        api_response = api_instance.put_listings_item(seller_id, sku, marketplace_ids, body, issue_locale=issue_locale)
        print("The response of ListingsApi->put_listings_item:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ListingsApi->put_listings_item: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **seller_id** | **str**| A selling partner identifier, such as a merchant account or vendor code. | 
 **sku** | **str**| A selling partner provided identifier for an Amazon listing. | 
 **marketplace_ids** | [**List[str]**](str.md)| A comma-delimited list of Amazon marketplace identifiers for the request. | 
 **body** | [**ListingsItemPutRequest**](ListingsItemPutRequest.md)| The request body schema for the putListingsItem operation. | 
 **issue_locale** | **str**| A locale for localization of issues. When not provided, the default language code of the first marketplace is used. Examples: \&quot;en_US\&quot;, \&quot;fr_CA\&quot;, \&quot;fr_FR\&quot;. Localized messages default to \&quot;en_US\&quot; when a localization is not available in the specified locale. | [optional] 

### Return type

[**ListingsItemSubmissionResponse**](ListingsItemSubmissionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully understood the request to create or fully-update a listings item. See the response to determine if the submission has been accepted. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

