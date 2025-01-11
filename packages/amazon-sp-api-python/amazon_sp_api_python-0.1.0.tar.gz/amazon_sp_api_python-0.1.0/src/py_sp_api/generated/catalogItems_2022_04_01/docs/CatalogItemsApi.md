# py_sp_api.generated.catalogItems_2022_04_01.CatalogItemsApi

All URIs are relative to *https://sellingpartnerapi-na.amazon.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_catalog_item**](CatalogItemsApi.md#get_catalog_item) | **GET** /catalog/2022-04-01/items/{asin} | getCatalogItem
[**search_catalog_items**](CatalogItemsApi.md#search_catalog_items) | **GET** /catalog/2022-04-01/items | searchCatalogItems


# **get_catalog_item**
> Item get_catalog_item(asin, marketplace_ids, included_data=included_data, locale=locale)

getCatalogItem

Retrieves details for an item in the Amazon catalog.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 2 | 2 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may observe higher rate and burst values than those shown here. For more information, refer to the [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.catalogItems_2022_04_01
from py_sp_api.generated.catalogItems_2022_04_01.models.item import Item
from py_sp_api.generated.catalogItems_2022_04_01.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.catalogItems_2022_04_01.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.catalogItems_2022_04_01.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.catalogItems_2022_04_01.CatalogItemsApi(api_client)
    asin = 'asin_example' # str | The Amazon Standard Identification Number (ASIN) of the item.
    marketplace_ids = ['ATVPDKIKX0DER'] # List[str] | A comma-delimited list of Amazon marketplace identifiers. Data sets in the response contain data only for the specified marketplaces.
    included_data = ["summaries"] # List[str] | A comma-delimited list of data sets to include in the response. Default: `summaries`. (optional) (default to ["summaries"])
    locale = 'en_US' # str | Locale for retrieving localized summaries. Defaults to the primary locale of the marketplace. (optional)

    try:
        # getCatalogItem
        api_response = api_instance.get_catalog_item(asin, marketplace_ids, included_data=included_data, locale=locale)
        print("The response of CatalogItemsApi->get_catalog_item:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CatalogItemsApi->get_catalog_item: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asin** | **str**| The Amazon Standard Identification Number (ASIN) of the item. | 
 **marketplace_ids** | [**List[str]**](str.md)| A comma-delimited list of Amazon marketplace identifiers. Data sets in the response contain data only for the specified marketplaces. | 
 **included_data** | [**List[str]**](str.md)| A comma-delimited list of data sets to include in the response. Default: &#x60;summaries&#x60;. | [optional] [default to [&quot;summaries&quot;]]
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
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search_catalog_items**
> ItemSearchResults search_catalog_items(marketplace_ids, identifiers=identifiers, identifiers_type=identifiers_type, included_data=included_data, locale=locale, seller_id=seller_id, keywords=keywords, brand_names=brand_names, classification_ids=classification_ids, page_size=page_size, page_token=page_token, keywords_locale=keywords_locale)

searchCatalogItems

Search for and return a list of Amazon catalog items and associated information either by identifier or by keywords.  **Usage Plans:**  | Rate (requests per second) | Burst | | ---- | ---- | | 2 | 2 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may observe higher rate and burst values than those shown here. For more information, refer to the [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.catalogItems_2022_04_01
from py_sp_api.generated.catalogItems_2022_04_01.models.item_search_results import ItemSearchResults
from py_sp_api.generated.catalogItems_2022_04_01.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.catalogItems_2022_04_01.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.catalogItems_2022_04_01.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.catalogItems_2022_04_01.CatalogItemsApi(api_client)
    marketplace_ids = ['ATVPDKIKX0DER'] # List[str] | A comma-delimited list of Amazon marketplace identifiers for the request.
    identifiers = ['shoes'] # List[str] | A comma-delimited list of product identifiers to search the Amazon catalog for. **Note:** Cannot be used with `keywords`. (optional)
    identifiers_type = 'ASIN' # str | Type of product identifiers to search the Amazon catalog for. **Note:** Required when `identifiers` are provided. (optional)
    included_data = ["summaries"] # List[str] | A comma-delimited list of data sets to include in the response. Default: `summaries`. (optional) (default to ["summaries"])
    locale = 'en_US' # str | Locale for retrieving localized summaries. Defaults to the primary locale of the marketplace. (optional)
    seller_id = 'seller_id_example' # str | A selling partner identifier, such as a seller account or vendor code. **Note:** Required when `identifiersType` is `SKU`. (optional)
    keywords = ['shoes'] # List[str] | A comma-delimited list of words to search the Amazon catalog for. **Note:** Cannot be used with `identifiers`. (optional)
    brand_names = ['Beautiful Boats'] # List[str] | A comma-delimited list of brand names to limit the search for `keywords`-based queries. **Note:** Cannot be used with `identifiers`. (optional)
    classification_ids = ['12345678'] # List[str] | A comma-delimited list of classification identifiers to limit the search for `keywords`-based queries. **Note:** Cannot be used with `identifiers`. (optional)
    page_size = 10 # int | Number of results to be returned per page. (optional) (default to 10)
    page_token = 'sdlkj234lkj234lksjdflkjwdflkjsfdlkj234234234234' # str | A token to fetch a certain page when there are multiple pages worth of results. (optional)
    keywords_locale = 'en_US' # str | The language of the keywords provided for `keywords`-based queries. Defaults to the primary locale of the marketplace. **Note:** Cannot be used with `identifiers`. (optional)

    try:
        # searchCatalogItems
        api_response = api_instance.search_catalog_items(marketplace_ids, identifiers=identifiers, identifiers_type=identifiers_type, included_data=included_data, locale=locale, seller_id=seller_id, keywords=keywords, brand_names=brand_names, classification_ids=classification_ids, page_size=page_size, page_token=page_token, keywords_locale=keywords_locale)
        print("The response of CatalogItemsApi->search_catalog_items:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CatalogItemsApi->search_catalog_items: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **marketplace_ids** | [**List[str]**](str.md)| A comma-delimited list of Amazon marketplace identifiers for the request. | 
 **identifiers** | [**List[str]**](str.md)| A comma-delimited list of product identifiers to search the Amazon catalog for. **Note:** Cannot be used with &#x60;keywords&#x60;. | [optional] 
 **identifiers_type** | **str**| Type of product identifiers to search the Amazon catalog for. **Note:** Required when &#x60;identifiers&#x60; are provided. | [optional] 
 **included_data** | [**List[str]**](str.md)| A comma-delimited list of data sets to include in the response. Default: &#x60;summaries&#x60;. | [optional] [default to [&quot;summaries&quot;]]
 **locale** | **str**| Locale for retrieving localized summaries. Defaults to the primary locale of the marketplace. | [optional] 
 **seller_id** | **str**| A selling partner identifier, such as a seller account or vendor code. **Note:** Required when &#x60;identifiersType&#x60; is &#x60;SKU&#x60;. | [optional] 
 **keywords** | [**List[str]**](str.md)| A comma-delimited list of words to search the Amazon catalog for. **Note:** Cannot be used with &#x60;identifiers&#x60;. | [optional] 
 **brand_names** | [**List[str]**](str.md)| A comma-delimited list of brand names to limit the search for &#x60;keywords&#x60;-based queries. **Note:** Cannot be used with &#x60;identifiers&#x60;. | [optional] 
 **classification_ids** | [**List[str]**](str.md)| A comma-delimited list of classification identifiers to limit the search for &#x60;keywords&#x60;-based queries. **Note:** Cannot be used with &#x60;identifiers&#x60;. | [optional] 
 **page_size** | **int**| Number of results to be returned per page. | [optional] [default to 10]
 **page_token** | **str**| A token to fetch a certain page when there are multiple pages worth of results. | [optional] 
 **keywords_locale** | **str**| The language of the keywords provided for &#x60;keywords&#x60;-based queries. Defaults to the primary locale of the marketplace. **Note:** Cannot be used with &#x60;identifiers&#x60;. | [optional] 

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
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

