# py_sp_api.generated.definitionsProductTypes_2020_09_01.DefinitionsApi

All URIs are relative to *https://sellingpartnerapi-na.amazon.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_definitions_product_type**](DefinitionsApi.md#get_definitions_product_type) | **GET** /definitions/2020-09-01/productTypes/{productType} | 
[**search_definitions_product_types**](DefinitionsApi.md#search_definitions_product_types) | **GET** /definitions/2020-09-01/productTypes | 


# **get_definitions_product_type**
> ProductTypeDefinition get_definitions_product_type(product_type, marketplace_ids, seller_id=seller_id, product_type_version=product_type_version, requirements=requirements, requirements_enforced=requirements_enforced, locale=locale)



Retrieve an Amazon product type definition.  **Usage Plans:**  | Plan type | Rate (requests per second) | Burst | | ---- | ---- | ---- | |Default| 5 | 10 | |Selling partner specific| Variable | Variable |  The x-amzn-RateLimit-Limit response header returns the usage plan rate limits that were applied to the requested operation. Rate limits for some selling partners will vary from the default rate and burst shown in the table above. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.definitionsProductTypes_2020_09_01
from py_sp_api.generated.definitionsProductTypes_2020_09_01.models.product_type_definition import ProductTypeDefinition
from py_sp_api.generated.definitionsProductTypes_2020_09_01.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.definitionsProductTypes_2020_09_01.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.definitionsProductTypes_2020_09_01.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.definitionsProductTypes_2020_09_01.DefinitionsApi(api_client)
    product_type = 'LUGGAGE' # str | The Amazon product type name.
    marketplace_ids = ['ATVPDKIKX0DER'] # List[str] | A comma-delimited list of Amazon marketplace identifiers for the request. Note: This parameter is limited to one marketplaceId at this time.
    seller_id = 'seller_id_example' # str | A selling partner identifier. When provided, seller-specific requirements and values are populated within the product type definition schema, such as brand names associated with the selling partner. (optional)
    product_type_version = 'LATEST' # str | The version of the Amazon product type to retrieve. Defaults to \"LATEST\",. Prerelease versions of product type definitions may be retrieved with \"RELEASE_CANDIDATE\". If no prerelease version is currently available, the \"LATEST\" live version will be provided. (optional) (default to 'LATEST')
    requirements = LISTING # str | The name of the requirements set to retrieve requirements for. (optional) (default to LISTING)
    requirements_enforced = ENFORCED # str | Identifies if the required attributes for a requirements set are enforced by the product type definition schema. Non-enforced requirements enable structural validation of individual attributes without all the required attributes being present (such as for partial updates). (optional) (default to ENFORCED)
    locale = DEFAULT # str | Locale for retrieving display labels and other presentation details. Defaults to the default language of the first marketplace in the request. (optional) (default to DEFAULT)

    try:
        api_response = api_instance.get_definitions_product_type(product_type, marketplace_ids, seller_id=seller_id, product_type_version=product_type_version, requirements=requirements, requirements_enforced=requirements_enforced, locale=locale)
        print("The response of DefinitionsApi->get_definitions_product_type:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefinitionsApi->get_definitions_product_type: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **product_type** | **str**| The Amazon product type name. | 
 **marketplace_ids** | [**List[str]**](str.md)| A comma-delimited list of Amazon marketplace identifiers for the request. Note: This parameter is limited to one marketplaceId at this time. | 
 **seller_id** | **str**| A selling partner identifier. When provided, seller-specific requirements and values are populated within the product type definition schema, such as brand names associated with the selling partner. | [optional] 
 **product_type_version** | **str**| The version of the Amazon product type to retrieve. Defaults to \&quot;LATEST\&quot;,. Prerelease versions of product type definitions may be retrieved with \&quot;RELEASE_CANDIDATE\&quot;. If no prerelease version is currently available, the \&quot;LATEST\&quot; live version will be provided. | [optional] [default to &#39;LATEST&#39;]
 **requirements** | **str**| The name of the requirements set to retrieve requirements for. | [optional] [default to LISTING]
 **requirements_enforced** | **str**| Identifies if the required attributes for a requirements set are enforced by the product type definition schema. Non-enforced requirements enable structural validation of individual attributes without all the required attributes being present (such as for partial updates). | [optional] [default to ENFORCED]
 **locale** | **str**| Locale for retrieving display labels and other presentation details. Defaults to the default language of the first marketplace in the request. | [optional] [default to DEFAULT]

### Return type

[**ProductTypeDefinition**](ProductTypeDefinition.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved an Amazon product type definition. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search_definitions_product_types**
> ProductTypeList search_definitions_product_types(marketplace_ids, keywords=keywords, item_name=item_name, locale=locale, search_locale=search_locale)



Search for and return a list of Amazon product types that have definitions available.  **Usage Plans:**  | Plan type | Rate (requests per second) | Burst | | ---- | ---- | ---- | |Default| 5 | 10 | |Selling partner specific| Variable | Variable |  The x-amzn-RateLimit-Limit response header returns the usage plan rate limits that were applied to the requested operation. Rate limits for some selling partners will vary from the default rate and burst shown in the table above. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.definitionsProductTypes_2020_09_01
from py_sp_api.generated.definitionsProductTypes_2020_09_01.models.product_type_list import ProductTypeList
from py_sp_api.generated.definitionsProductTypes_2020_09_01.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.definitionsProductTypes_2020_09_01.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.definitionsProductTypes_2020_09_01.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.definitionsProductTypes_2020_09_01.DefinitionsApi(api_client)
    marketplace_ids = ['ATVPDKIKX0DER'] # List[str] | A comma-delimited list of Amazon marketplace identifiers for the request.
    keywords = ['LUGGAGE'] # List[str] | A comma-delimited list of keywords to search product types. **Note:** Cannot be used with `itemName`. (optional)
    item_name = 'Running shoes' # str | The title of the ASIN to get the product type recommendation. **Note:** Cannot be used with `keywords`. (optional)
    locale = 'en_US' # str | The locale for the display names in the response. Defaults to the primary locale of the marketplace. (optional)
    search_locale = 'en_US' # str | The locale used for the `keywords` and `itemName` parameters. Defaults to the primary locale of the marketplace. (optional)

    try:
        api_response = api_instance.search_definitions_product_types(marketplace_ids, keywords=keywords, item_name=item_name, locale=locale, search_locale=search_locale)
        print("The response of DefinitionsApi->search_definitions_product_types:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefinitionsApi->search_definitions_product_types: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **marketplace_ids** | [**List[str]**](str.md)| A comma-delimited list of Amazon marketplace identifiers for the request. | 
 **keywords** | [**List[str]**](str.md)| A comma-delimited list of keywords to search product types. **Note:** Cannot be used with &#x60;itemName&#x60;. | [optional] 
 **item_name** | **str**| The title of the ASIN to get the product type recommendation. **Note:** Cannot be used with &#x60;keywords&#x60;. | [optional] 
 **locale** | **str**| The locale for the display names in the response. Defaults to the primary locale of the marketplace. | [optional] 
 **search_locale** | **str**| The locale used for the &#x60;keywords&#x60; and &#x60;itemName&#x60; parameters. Defaults to the primary locale of the marketplace. | [optional] 

### Return type

[**ProductTypeList**](ProductTypeList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved a list of Amazon product types that have definitions available. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

