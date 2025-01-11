# py_sp_api.generated.listingsRestrictions_2021_08_01.ListingsApi

All URIs are relative to *https://sellingpartnerapi-na.amazon.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_listings_restrictions**](ListingsApi.md#get_listings_restrictions) | **GET** /listings/2021-08-01/restrictions | 


# **get_listings_restrictions**
> RestrictionList get_listings_restrictions(asin, seller_id, marketplace_ids, condition_type=condition_type, reason_locale=reason_locale)



Returns listing restrictions for an item in the Amazon Catalog.   **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 5 | 10 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values then those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.listingsRestrictions_2021_08_01
from py_sp_api.generated.listingsRestrictions_2021_08_01.models.restriction_list import RestrictionList
from py_sp_api.generated.listingsRestrictions_2021_08_01.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.listingsRestrictions_2021_08_01.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.listingsRestrictions_2021_08_01.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.listingsRestrictions_2021_08_01.ListingsApi(api_client)
    asin = 'B0000ASIN1' # str | The Amazon Standard Identification Number (ASIN) of the item.
    seller_id = 'seller_id_example' # str | A selling partner identifier, such as a merchant account.
    marketplace_ids = ['ATVPDKIKX0DER'] # List[str] | A comma-delimited list of Amazon marketplace identifiers for the request.
    condition_type = 'used_very_good' # str | The condition used to filter restrictions. (optional)
    reason_locale = 'en_US' # str | A locale for reason text localization. When not provided, the default language code of the first marketplace is used. Examples: \"en_US\", \"fr_CA\", \"fr_FR\". Localized messages default to \"en_US\" when a localization is not available in the specified locale. (optional)

    try:
        api_response = api_instance.get_listings_restrictions(asin, seller_id, marketplace_ids, condition_type=condition_type, reason_locale=reason_locale)
        print("The response of ListingsApi->get_listings_restrictions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ListingsApi->get_listings_restrictions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asin** | **str**| The Amazon Standard Identification Number (ASIN) of the item. | 
 **seller_id** | **str**| A selling partner identifier, such as a merchant account. | 
 **marketplace_ids** | [**List[str]**](str.md)| A comma-delimited list of Amazon marketplace identifiers for the request. | 
 **condition_type** | **str**| The condition used to filter restrictions. | [optional] 
 **reason_locale** | **str**| A locale for reason text localization. When not provided, the default language code of the first marketplace is used. Examples: \&quot;en_US\&quot;, \&quot;fr_CA\&quot;, \&quot;fr_FR\&quot;. Localized messages default to \&quot;en_US\&quot; when a localization is not available in the specified locale. | [optional] 

### Return type

[**RestrictionList**](RestrictionList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved the listings restrictions. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

