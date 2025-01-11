# py_sp_api.generated.feeds_2020_09_04.FeedsApi

All URIs are relative to *https://sellingpartnerapi-na.amazon.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**cancel_feed**](FeedsApi.md#cancel_feed) | **DELETE** /feeds/2020-09-04/feeds/{feedId} | 
[**create_feed**](FeedsApi.md#create_feed) | **POST** /feeds/2020-09-04/feeds | 
[**create_feed_document**](FeedsApi.md#create_feed_document) | **POST** /feeds/2020-09-04/documents | 
[**get_feed**](FeedsApi.md#get_feed) | **GET** /feeds/2020-09-04/feeds/{feedId} | 
[**get_feed_document**](FeedsApi.md#get_feed_document) | **GET** /feeds/2020-09-04/documents/{feedDocumentId} | 
[**get_feeds**](FeedsApi.md#get_feeds) | **GET** /feeds/2020-09-04/feeds | 


# **cancel_feed**
> CancelFeedResponse cancel_feed(feed_id)



Effective June 27, 2023, the `cancelFeed` operation will no longer be available in the Selling Partner API for Feeds v2020-09-04 and all calls to it will fail. Integrations that rely on this operation should migrate to [Feeds v2021-06-30](https://developer-docs.amazon.com/sp-api/docs/feeds-api-v2021-06-30-reference) to avoid service disruption.

### Example


```python
import py_sp_api.generated.feeds_2020_09_04
from py_sp_api.generated.feeds_2020_09_04.models.cancel_feed_response import CancelFeedResponse
from py_sp_api.generated.feeds_2020_09_04.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.feeds_2020_09_04.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.feeds_2020_09_04.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.feeds_2020_09_04.FeedsApi(api_client)
    feed_id = 'feed_id_example' # str | The identifier for the feed. This identifier is unique only in combination with a seller ID.

    try:
        api_response = api_instance.cancel_feed(feed_id)
        print("The response of FeedsApi->cancel_feed:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FeedsApi->cancel_feed: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **feed_id** | **str**| The identifier for the feed. This identifier is unique only in combination with a seller ID. | 

### Return type

[**CancelFeedResponse**](CancelFeedResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**401** | The request&#39;s Authorization header is not formatted correctly or does not contain a valid token. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference ID. <br>  |
**404** | The specified resource does not exist. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request&#39;s Content-Type header is invalid. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_feed**
> CreateFeedResponse create_feed(body)



Effective June 27, 2023, the `createFeed` operation will no longer be available in the Selling Partner API for Feeds v2020-09-04 and all calls to it will fail. Integrations that rely on this operation should migrate to [Feeds v2021-06-30](https://developer-docs.amazon.com/sp-api/docs/feeds-api-v2021-06-30-reference) to avoid service disruption.

### Example


```python
import py_sp_api.generated.feeds_2020_09_04
from py_sp_api.generated.feeds_2020_09_04.models.create_feed_response import CreateFeedResponse
from py_sp_api.generated.feeds_2020_09_04.models.create_feed_specification import CreateFeedSpecification
from py_sp_api.generated.feeds_2020_09_04.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.feeds_2020_09_04.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.feeds_2020_09_04.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.feeds_2020_09_04.FeedsApi(api_client)
    body = py_sp_api.generated.feeds_2020_09_04.CreateFeedSpecification() # CreateFeedSpecification | 

    try:
        api_response = api_instance.create_feed(body)
        print("The response of FeedsApi->create_feed:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FeedsApi->create_feed: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateFeedSpecification**](CreateFeedSpecification.md)|  | 

### Return type

[**CreateFeedResponse**](CreateFeedResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Success. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**401** | The request&#39;s Authorization header is not formatted correctly or does not contain a valid token. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference ID. <br>  |
**404** | The specified resource does not exist. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request&#39;s Content-Type header is invalid. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_feed_document**
> CreateFeedDocumentResponse create_feed_document(body)



Effective June 27, 2023, the `createFeedDocument` operation will no longer be available in the Selling Partner API for Feeds v2020-09-04 and all calls to it will fail. Integrations that rely on this operation should migrate to [Feeds v2021-06-30](https://developer-docs.amazon.com/sp-api/docs/feeds-api-v2021-06-30-reference) to avoid service disruption.

### Example


```python
import py_sp_api.generated.feeds_2020_09_04
from py_sp_api.generated.feeds_2020_09_04.models.create_feed_document_response import CreateFeedDocumentResponse
from py_sp_api.generated.feeds_2020_09_04.models.create_feed_document_specification import CreateFeedDocumentSpecification
from py_sp_api.generated.feeds_2020_09_04.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.feeds_2020_09_04.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.feeds_2020_09_04.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.feeds_2020_09_04.FeedsApi(api_client)
    body = py_sp_api.generated.feeds_2020_09_04.CreateFeedDocumentSpecification() # CreateFeedDocumentSpecification | 

    try:
        api_response = api_instance.create_feed_document(body)
        print("The response of FeedsApi->create_feed_document:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FeedsApi->create_feed_document: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CreateFeedDocumentSpecification**](CreateFeedDocumentSpecification.md)|  | 

### Return type

[**CreateFeedDocumentResponse**](CreateFeedDocumentResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successfully created a feed document that is ready to receive contents. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference ID. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_feed**
> GetFeedResponse get_feed(feed_id)



Effective June 27, 2023, the `getFeed` operation will no longer be available in the Selling Partner API for Feeds v2020-09-04 and all calls to it will fail. Integrations that rely on this operation should migrate to [Feeds v2021-06-30](https://developer-docs.amazon.com/sp-api/docs/feeds-api-v2021-06-30-reference) to avoid service disruption.

### Example


```python
import py_sp_api.generated.feeds_2020_09_04
from py_sp_api.generated.feeds_2020_09_04.models.get_feed_response import GetFeedResponse
from py_sp_api.generated.feeds_2020_09_04.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.feeds_2020_09_04.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.feeds_2020_09_04.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.feeds_2020_09_04.FeedsApi(api_client)
    feed_id = 'feed_id_example' # str | The identifier for the feed. This identifier is unique only in combination with a seller ID.

    try:
        api_response = api_instance.get_feed(feed_id)
        print("The response of FeedsApi->get_feed:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FeedsApi->get_feed: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **feed_id** | **str**| The identifier for the feed. This identifier is unique only in combination with a seller ID. | 

### Return type

[**GetFeedResponse**](GetFeedResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**401** | The request&#39;s Authorization header is not formatted correctly or does not contain a valid token. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference ID. <br>  |
**404** | The specified resource does not exist. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request&#39;s Content-Type header is invalid. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_feed_document**
> GetFeedDocumentResponse get_feed_document(feed_document_id)



Effective June 27, 2023, the `getFeedDocument` operation will no longer be available in the Selling Partner API for Feeds v2020-09-04 and all calls to it will fail. Integrations that rely on this operation should migrate to [Feeds v2021-06-30](https://developer-docs.amazon.com/sp-api/docs/feeds-api-v2021-06-30-reference) to avoid service disruption.

### Example


```python
import py_sp_api.generated.feeds_2020_09_04
from py_sp_api.generated.feeds_2020_09_04.models.get_feed_document_response import GetFeedDocumentResponse
from py_sp_api.generated.feeds_2020_09_04.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.feeds_2020_09_04.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.feeds_2020_09_04.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.feeds_2020_09_04.FeedsApi(api_client)
    feed_document_id = 'feed_document_id_example' # str | The identifier of the feed document.

    try:
        api_response = api_instance.get_feed_document(feed_document_id)
        print("The response of FeedsApi->get_feed_document:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FeedsApi->get_feed_document: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **feed_document_id** | **str**| The identifier of the feed document. | 

### Return type

[**GetFeedDocumentResponse**](GetFeedDocumentResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**401** | The request&#39;s Authorization header is not formatted correctly or does not contain a valid token. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference ID. <br>  |
**404** | The specified resource does not exist. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request&#39;s Content-Type header is invalid. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_feeds**
> GetFeedsResponse get_feeds(feed_types=feed_types, marketplace_ids=marketplace_ids, page_size=page_size, processing_statuses=processing_statuses, created_since=created_since, created_until=created_until, next_token=next_token)



Effective June 27, 2023, the `getFeeds` operation will no longer be available in the Selling Partner API for Feeds v2020-09-04 and all calls to it will fail. Integrations that rely on this operation should migrate to [Feeds v2021-06-30](https://developer-docs.amazon.com/sp-api/docs/feeds-api-v2021-06-30-reference) to avoid service disruption.

### Example


```python
import py_sp_api.generated.feeds_2020_09_04
from py_sp_api.generated.feeds_2020_09_04.models.get_feeds_response import GetFeedsResponse
from py_sp_api.generated.feeds_2020_09_04.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.feeds_2020_09_04.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.feeds_2020_09_04.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.feeds_2020_09_04.FeedsApi(api_client)
    feed_types = ['feed_types_example'] # List[str] | A list of feed types used to filter feeds. When feedTypes is provided, the other filter parameters (processingStatuses, marketplaceIds, createdSince, createdUntil) and pageSize may also be provided. Either feedTypes or nextToken is required. (optional)
    marketplace_ids = ['marketplace_ids_example'] # List[str] | A list of marketplace identifiers used to filter feeds. The feeds returned will match at least one of the marketplaces that you specify. (optional)
    page_size = 10 # int | The maximum number of feeds to return in a single call. (optional) (default to 10)
    processing_statuses = ['processing_statuses_example'] # List[str] | A list of processing statuses used to filter feeds. (optional)
    created_since = '2013-10-20T19:20:30+01:00' # datetime | The earliest feed creation date and time for feeds included in the response, in ISO 8601 format. The default is 90 days ago. Feeds are retained for a maximum of 90 days. (optional)
    created_until = '2013-10-20T19:20:30+01:00' # datetime | The latest feed creation date and time for feeds included in the response, in ISO 8601 format. The default is now. (optional)
    next_token = 'next_token_example' # str | A string token returned in the response to your previous request. nextToken is returned when the number of results exceeds the specified pageSize value. To get the next page of results, call the getFeeds operation and include this token as the only parameter. Specifying nextToken with any other parameters will cause the request to fail. (optional)

    try:
        api_response = api_instance.get_feeds(feed_types=feed_types, marketplace_ids=marketplace_ids, page_size=page_size, processing_statuses=processing_statuses, created_since=created_since, created_until=created_until, next_token=next_token)
        print("The response of FeedsApi->get_feeds:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FeedsApi->get_feeds: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **feed_types** | [**List[str]**](str.md)| A list of feed types used to filter feeds. When feedTypes is provided, the other filter parameters (processingStatuses, marketplaceIds, createdSince, createdUntil) and pageSize may also be provided. Either feedTypes or nextToken is required. | [optional] 
 **marketplace_ids** | [**List[str]**](str.md)| A list of marketplace identifiers used to filter feeds. The feeds returned will match at least one of the marketplaces that you specify. | [optional] 
 **page_size** | **int**| The maximum number of feeds to return in a single call. | [optional] [default to 10]
 **processing_statuses** | [**List[str]**](str.md)| A list of processing statuses used to filter feeds. | [optional] 
 **created_since** | **datetime**| The earliest feed creation date and time for feeds included in the response, in ISO 8601 format. The default is 90 days ago. Feeds are retained for a maximum of 90 days. | [optional] 
 **created_until** | **datetime**| The latest feed creation date and time for feeds included in the response, in ISO 8601 format. The default is now. | [optional] 
 **next_token** | **str**| A string token returned in the response to your previous request. nextToken is returned when the number of results exceeds the specified pageSize value. To get the next page of results, call the getFeeds operation and include this token as the only parameter. Specifying nextToken with any other parameters will cause the request to fail. | [optional] 

### Return type

[**GetFeedsResponse**](GetFeedsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**401** | The request&#39;s Authorization header is not formatted correctly or does not contain a valid token. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference ID. <br>  |
**404** | The specified resource does not exist. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request&#39;s Content-Type header is invalid. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

