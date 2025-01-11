# py_sp_api.generated.catalogItems_2020_12_01.CatalogApi

All URIs are relative to *https://sellingpartnerapi-na.amazon.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_catalog_item**](CatalogApi.md#get_catalog_item) | **GET** /catalog/2020-12-01/items/{asin} | 
[**search_catalog_items**](CatalogApi.md#search_catalog_items) | **GET** /catalog/2020-12-01/items | 


# **get_catalog_item**
> Item get_catalog_item(asin, marketplace_ids, included_data=included_data, locale=locale)



Retrieves details for an item in the Amazon catalog.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 2 | 2 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.catalogItems_2020_12_01
from py_sp_api.generated.catalogItems_2020_12_01.models.item import Item
from py_sp_api.generated.catalogItems_2020_12_01.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.catalogItems_2020_12_01.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.catalogItems_2020_12_01.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.catalogItems_2020_12_01.CatalogApi(api_client)
    asin = 'asin_example' # str | The Amazon Standard Identification Number (ASIN) of the item.
    marketplace_ids = ['ATVPDKIKX0DER'] # List[str] | A comma-delimited list of Amazon marketplace identifiers. Data sets in the response contain data only for the specified marketplaces.
    included_data = ['summaries'] # List[str] | A comma-delimited list of data sets to include in the response. Default: summaries. (optional)
    locale = 'en_US' # str | Locale for retrieving localized summaries. Defaults to the primary locale of the marketplace. (optional)

    try:
        api_response = api_instance.get_catalog_item(asin, marketplace_ids, included_data=included_data, locale=locale)
        print("The response of CatalogApi->get_catalog_item:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CatalogApi->get_catalog_item: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asin** | **str**| The Amazon Standard Identification Number (ASIN) of the item. | 
 **marketplace_ids** | [**List[str]**](str.md)| A comma-delimited list of Amazon marketplace identifiers. Data sets in the response contain data only for the specified marketplaces. | 
 **included_data** | [**List[str]**](str.md)| A comma-delimited list of data sets to include in the response. Default: summaries. | [optional] 
 **locale** | **str**| Locale for retrieving localized summaries. Defaults to the primary locale of the marketplace. | [optional] 

### Return type

[**Item**](Item.md)

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
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search_catalog_items**
> ItemSearchResults search_catalog_items(keywords, marketplace_ids, included_data=included_data, brand_names=brand_names, classification_ids=classification_ids, page_size=page_size, page_token=page_token, keywords_locale=keywords_locale, locale=locale)



Search for and return a list of Amazon catalog items and associated information.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 2 | 2 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.catalogItems_2020_12_01
from py_sp_api.generated.catalogItems_2020_12_01.models.item_search_results import ItemSearchResults
from py_sp_api.generated.catalogItems_2020_12_01.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.catalogItems_2020_12_01.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.catalogItems_2020_12_01.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.catalogItems_2020_12_01.CatalogApi(api_client)
    keywords = ['shoes'] # List[str] | A comma-delimited list of words or item identifiers to search the Amazon catalog for.
    marketplace_ids = ['ATVPDKIKX0DER'] # List[str] | A comma-delimited list of Amazon marketplace identifiers for the request.
    included_data = ['summaries'] # List[str] | A comma-delimited list of data sets to include in the response. Default: summaries. (optional)
    brand_names = ['Beautiful Boats'] # List[str] | A comma-delimited list of brand names to limit the search to. (optional)
    classification_ids = ['12345678'] # List[str] | A comma-delimited list of classification identifiers to limit the search to. (optional)
    page_size = 10 # int | Number of results to be returned per page. (optional) (default to 10)
    page_token = 'sdlkj234lkj234lksjdflkjwdflkjsfdlkj234234234234' # str | A token to fetch a certain page when there are multiple pages worth of results. (optional)
    keywords_locale = 'en_US' # str | The language the keywords are provided in. Defaults to the primary locale of the marketplace. (optional)
    locale = 'en_US' # str | Locale for retrieving localized summaries. Defaults to the primary locale of the marketplace. (optional)

    try:
        api_response = api_instance.search_catalog_items(keywords, marketplace_ids, included_data=included_data, brand_names=brand_names, classification_ids=classification_ids, page_size=page_size, page_token=page_token, keywords_locale=keywords_locale, locale=locale)
        print("The response of CatalogApi->search_catalog_items:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CatalogApi->search_catalog_items: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **keywords** | [**List[str]**](str.md)| A comma-delimited list of words or item identifiers to search the Amazon catalog for. | 
 **marketplace_ids** | [**List[str]**](str.md)| A comma-delimited list of Amazon marketplace identifiers for the request. | 
 **included_data** | [**List[str]**](str.md)| A comma-delimited list of data sets to include in the response. Default: summaries. | [optional] 
 **brand_names** | [**List[str]**](str.md)| A comma-delimited list of brand names to limit the search to. | [optional] 
 **classification_ids** | [**List[str]**](str.md)| A comma-delimited list of classification identifiers to limit the search to. | [optional] 
 **page_size** | **int**| Number of results to be returned per page. | [optional] [default to 10]
 **page_token** | **str**| A token to fetch a certain page when there are multiple pages worth of results. | [optional] 
 **keywords_locale** | **str**| The language the keywords are provided in. Defaults to the primary locale of the marketplace. | [optional] 
 **locale** | **str**| Locale for retrieving localized summaries. Defaults to the primary locale of the marketplace. | [optional] 

### Return type

[**ItemSearchResults**](ItemSearchResults.md)

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
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

