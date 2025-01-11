# py_sp_api.generated.messaging.MessagingApi

All URIs are relative to *https://sellingpartnerapi-na.amazon.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**confirm_customization_details**](MessagingApi.md#confirm_customization_details) | **POST** /messaging/v1/orders/{amazonOrderId}/messages/confirmCustomizationDetails | 
[**create_amazon_motors**](MessagingApi.md#create_amazon_motors) | **POST** /messaging/v1/orders/{amazonOrderId}/messages/amazonMotors | 
[**create_confirm_delivery_details**](MessagingApi.md#create_confirm_delivery_details) | **POST** /messaging/v1/orders/{amazonOrderId}/messages/confirmDeliveryDetails | 
[**create_confirm_order_details**](MessagingApi.md#create_confirm_order_details) | **POST** /messaging/v1/orders/{amazonOrderId}/messages/confirmOrderDetails | 
[**create_confirm_service_details**](MessagingApi.md#create_confirm_service_details) | **POST** /messaging/v1/orders/{amazonOrderId}/messages/confirmServiceDetails | 
[**create_digital_access_key**](MessagingApi.md#create_digital_access_key) | **POST** /messaging/v1/orders/{amazonOrderId}/messages/digitalAccessKey | 
[**create_legal_disclosure**](MessagingApi.md#create_legal_disclosure) | **POST** /messaging/v1/orders/{amazonOrderId}/messages/legalDisclosure | 
[**create_negative_feedback_removal**](MessagingApi.md#create_negative_feedback_removal) | **POST** /messaging/v1/orders/{amazonOrderId}/messages/negativeFeedbackRemoval | 
[**create_unexpected_problem**](MessagingApi.md#create_unexpected_problem) | **POST** /messaging/v1/orders/{amazonOrderId}/messages/unexpectedProblem | 
[**create_warranty**](MessagingApi.md#create_warranty) | **POST** /messaging/v1/orders/{amazonOrderId}/messages/warranty | 
[**get_attributes**](MessagingApi.md#get_attributes) | **GET** /messaging/v1/orders/{amazonOrderId}/attributes | 
[**get_messaging_actions_for_order**](MessagingApi.md#get_messaging_actions_for_order) | **GET** /messaging/v1/orders/{amazonOrderId} | 
[**send_invoice**](MessagingApi.md#send_invoice) | **POST** /messaging/v1/orders/{amazonOrderId}/messages/invoice | 


# **confirm_customization_details**
> CreateConfirmCustomizationDetailsResponse confirm_customization_details(amazon_order_id, marketplace_ids, body)



Sends a message asking a buyer to provide or verify customization details such as name spelling, images, initials, etc.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 1 | 5 |  The `x-amzn-RateLimit-Limit` response header contains the usage plan rate limits for the operation, when available. The preceding table contains the default rate and burst values for this operation. Selling partners whose business demands require higher throughput might have higher rate and burst values than those shown here. For more information, refer to [Usage Plans and Rate Limits](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.messaging
from py_sp_api.generated.messaging.models.create_confirm_customization_details_request import CreateConfirmCustomizationDetailsRequest
from py_sp_api.generated.messaging.models.create_confirm_customization_details_response import CreateConfirmCustomizationDetailsResponse
from py_sp_api.generated.messaging.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.messaging.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.messaging.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.messaging.MessagingApi(api_client)
    amazon_order_id = 'amazon_order_id_example' # str | An Amazon order identifier. This identifies the order for which a message is sent.
    marketplace_ids = ['marketplace_ids_example'] # List[str] | A marketplace identifier. This identifies the marketplace in which the order was placed. You can only specify one marketplace.
    body = py_sp_api.generated.messaging.CreateConfirmCustomizationDetailsRequest() # CreateConfirmCustomizationDetailsRequest | This contains the message body for a message.

    try:
        api_response = api_instance.confirm_customization_details(amazon_order_id, marketplace_ids, body)
        print("The response of MessagingApi->confirm_customization_details:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MessagingApi->confirm_customization_details: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **amazon_order_id** | **str**| An Amazon order identifier. This identifies the order for which a message is sent. | 
 **marketplace_ids** | [**List[str]**](str.md)| A marketplace identifier. This identifies the marketplace in which the order was placed. You can only specify one marketplace. | 
 **body** | [**CreateConfirmCustomizationDetailsRequest**](CreateConfirmCustomizationDetailsRequest.md)| This contains the message body for a message. | 

### Return type

[**CreateConfirmCustomizationDetailsResponse**](CreateConfirmCustomizationDetailsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/hal+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | The message was created for the order. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_amazon_motors**
> CreateAmazonMotorsResponse create_amazon_motors(amazon_order_id, marketplace_ids, body)



Sends a message to a buyer to provide details about an Amazon Motors order. This message can only be sent by Amazon Motors sellers.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 1 | 5 |  The `x-amzn-RateLimit-Limit` response header contains the usage plan rate limits for the operation, when available. The preceding table contains the default rate and burst values for this operation. Selling partners whose business demands require higher throughput might have higher rate and burst values than those shown here. For more information, refer to [Usage Plans and Rate Limits](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.messaging
from py_sp_api.generated.messaging.models.create_amazon_motors_request import CreateAmazonMotorsRequest
from py_sp_api.generated.messaging.models.create_amazon_motors_response import CreateAmazonMotorsResponse
from py_sp_api.generated.messaging.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.messaging.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.messaging.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.messaging.MessagingApi(api_client)
    amazon_order_id = 'amazon_order_id_example' # str | An Amazon order identifier. This identifies the order for which a message is sent.
    marketplace_ids = ['marketplace_ids_example'] # List[str] | A marketplace identifier. This identifies the marketplace in which the order was placed. You can only specify one marketplace.
    body = py_sp_api.generated.messaging.CreateAmazonMotorsRequest() # CreateAmazonMotorsRequest | This contains the message body for a message.

    try:
        api_response = api_instance.create_amazon_motors(amazon_order_id, marketplace_ids, body)
        print("The response of MessagingApi->create_amazon_motors:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MessagingApi->create_amazon_motors: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **amazon_order_id** | **str**| An Amazon order identifier. This identifies the order for which a message is sent. | 
 **marketplace_ids** | [**List[str]**](str.md)| A marketplace identifier. This identifies the marketplace in which the order was placed. You can only specify one marketplace. | 
 **body** | [**CreateAmazonMotorsRequest**](CreateAmazonMotorsRequest.md)| This contains the message body for a message. | 

### Return type

[**CreateAmazonMotorsResponse**](CreateAmazonMotorsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/hal+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | The message was created for the order. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_confirm_delivery_details**
> CreateConfirmDeliveryDetailsResponse create_confirm_delivery_details(amazon_order_id, marketplace_ids, body)



Sends a message to a buyer to arrange a delivery or to confirm contact information for making a delivery.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 1 | 5 |  The `x-amzn-RateLimit-Limit` response header contains the usage plan rate limits for the operation, when available. The preceding table contains the default rate and burst values for this operation. Selling partners whose business demands require higher throughput might have higher rate and burst values than those shown here. For more information, refer to [Usage Plans and Rate Limits](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.messaging
from py_sp_api.generated.messaging.models.create_confirm_delivery_details_request import CreateConfirmDeliveryDetailsRequest
from py_sp_api.generated.messaging.models.create_confirm_delivery_details_response import CreateConfirmDeliveryDetailsResponse
from py_sp_api.generated.messaging.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.messaging.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.messaging.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.messaging.MessagingApi(api_client)
    amazon_order_id = 'amazon_order_id_example' # str | An Amazon order identifier. This identifies the order for which a message is sent.
    marketplace_ids = ['marketplace_ids_example'] # List[str] | A marketplace identifier. This identifies the marketplace in which the order was placed. You can only specify one marketplace.
    body = py_sp_api.generated.messaging.CreateConfirmDeliveryDetailsRequest() # CreateConfirmDeliveryDetailsRequest | This contains the message body for a message.

    try:
        api_response = api_instance.create_confirm_delivery_details(amazon_order_id, marketplace_ids, body)
        print("The response of MessagingApi->create_confirm_delivery_details:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MessagingApi->create_confirm_delivery_details: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **amazon_order_id** | **str**| An Amazon order identifier. This identifies the order for which a message is sent. | 
 **marketplace_ids** | [**List[str]**](str.md)| A marketplace identifier. This identifies the marketplace in which the order was placed. You can only specify one marketplace. | 
 **body** | [**CreateConfirmDeliveryDetailsRequest**](CreateConfirmDeliveryDetailsRequest.md)| This contains the message body for a message. | 

### Return type

[**CreateConfirmDeliveryDetailsResponse**](CreateConfirmDeliveryDetailsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/hal+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | The message was created for the order. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_confirm_order_details**
> CreateConfirmOrderDetailsResponse create_confirm_order_details(amazon_order_id, marketplace_ids, body)



Sends a message to ask a buyer an order-related question prior to shipping their order.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 1 | 5 |  The `x-amzn-RateLimit-Limit` response header contains the usage plan rate limits for the operation, when available. The preceding table contains the default rate and burst values for this operation. Selling partners whose business demands require higher throughput might have higher rate and burst values than those shown here. For more information, refer to [Usage Plans and Rate Limits](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.messaging
from py_sp_api.generated.messaging.models.create_confirm_order_details_request import CreateConfirmOrderDetailsRequest
from py_sp_api.generated.messaging.models.create_confirm_order_details_response import CreateConfirmOrderDetailsResponse
from py_sp_api.generated.messaging.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.messaging.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.messaging.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.messaging.MessagingApi(api_client)
    amazon_order_id = 'amazon_order_id_example' # str | An Amazon order identifier. This identifies the order for which a message is sent.
    marketplace_ids = ['marketplace_ids_example'] # List[str] | A marketplace identifier. This identifies the marketplace in which the order was placed. You can only specify one marketplace.
    body = py_sp_api.generated.messaging.CreateConfirmOrderDetailsRequest() # CreateConfirmOrderDetailsRequest | This contains the message body for a message.

    try:
        api_response = api_instance.create_confirm_order_details(amazon_order_id, marketplace_ids, body)
        print("The response of MessagingApi->create_confirm_order_details:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MessagingApi->create_confirm_order_details: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **amazon_order_id** | **str**| An Amazon order identifier. This identifies the order for which a message is sent. | 
 **marketplace_ids** | [**List[str]**](str.md)| A marketplace identifier. This identifies the marketplace in which the order was placed. You can only specify one marketplace. | 
 **body** | [**CreateConfirmOrderDetailsRequest**](CreateConfirmOrderDetailsRequest.md)| This contains the message body for a message. | 

### Return type

[**CreateConfirmOrderDetailsResponse**](CreateConfirmOrderDetailsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/hal+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | The message was created for the order. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_confirm_service_details**
> CreateConfirmServiceDetailsResponse create_confirm_service_details(amazon_order_id, marketplace_ids, body)



Sends a message to contact a Home Service customer to arrange a service call or to gather information prior to a service call.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 1 | 5 |  The `x-amzn-RateLimit-Limit` response header contains the usage plan rate limits for the operation, when available. The preceding table contains the default rate and burst values for this operation. Selling partners whose business demands require higher throughput might have higher rate and burst values than those shown here. For more information, refer to [Usage Plans and Rate Limits](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.messaging
from py_sp_api.generated.messaging.models.create_confirm_service_details_request import CreateConfirmServiceDetailsRequest
from py_sp_api.generated.messaging.models.create_confirm_service_details_response import CreateConfirmServiceDetailsResponse
from py_sp_api.generated.messaging.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.messaging.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.messaging.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.messaging.MessagingApi(api_client)
    amazon_order_id = 'amazon_order_id_example' # str | An Amazon order identifier. This identifies the order for which a message is sent.
    marketplace_ids = ['marketplace_ids_example'] # List[str] | A marketplace identifier. This identifies the marketplace in which the order was placed. You can only specify one marketplace.
    body = py_sp_api.generated.messaging.CreateConfirmServiceDetailsRequest() # CreateConfirmServiceDetailsRequest | This contains the message body for a message.

    try:
        api_response = api_instance.create_confirm_service_details(amazon_order_id, marketplace_ids, body)
        print("The response of MessagingApi->create_confirm_service_details:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MessagingApi->create_confirm_service_details: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **amazon_order_id** | **str**| An Amazon order identifier. This identifies the order for which a message is sent. | 
 **marketplace_ids** | [**List[str]**](str.md)| A marketplace identifier. This identifies the marketplace in which the order was placed. You can only specify one marketplace. | 
 **body** | [**CreateConfirmServiceDetailsRequest**](CreateConfirmServiceDetailsRequest.md)| This contains the message body for a message. | 

### Return type

[**CreateConfirmServiceDetailsResponse**](CreateConfirmServiceDetailsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/hal+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | The message was created for the order. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_digital_access_key**
> CreateDigitalAccessKeyResponse create_digital_access_key(amazon_order_id, marketplace_ids, body)



Sends a buyer a message to share a digital access key that is required to utilize digital content in their order.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 1 | 5 |  The `x-amzn-RateLimit-Limit` response header contains the usage plan rate limits for the operation, when available. The preceding table contains the default rate and burst values for this operation. Selling partners whose business demands require higher throughput might have higher rate and burst values than those shown here. For more information, refer to [Usage Plans and Rate Limits](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.messaging
from py_sp_api.generated.messaging.models.create_digital_access_key_request import CreateDigitalAccessKeyRequest
from py_sp_api.generated.messaging.models.create_digital_access_key_response import CreateDigitalAccessKeyResponse
from py_sp_api.generated.messaging.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.messaging.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.messaging.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.messaging.MessagingApi(api_client)
    amazon_order_id = 'amazon_order_id_example' # str | An Amazon order identifier. This identifies the order for which a message is sent.
    marketplace_ids = ['marketplace_ids_example'] # List[str] | A marketplace identifier. This identifies the marketplace in which the order was placed. You can only specify one marketplace.
    body = py_sp_api.generated.messaging.CreateDigitalAccessKeyRequest() # CreateDigitalAccessKeyRequest | This contains the message body for a message.

    try:
        api_response = api_instance.create_digital_access_key(amazon_order_id, marketplace_ids, body)
        print("The response of MessagingApi->create_digital_access_key:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MessagingApi->create_digital_access_key: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **amazon_order_id** | **str**| An Amazon order identifier. This identifies the order for which a message is sent. | 
 **marketplace_ids** | [**List[str]**](str.md)| A marketplace identifier. This identifies the marketplace in which the order was placed. You can only specify one marketplace. | 
 **body** | [**CreateDigitalAccessKeyRequest**](CreateDigitalAccessKeyRequest.md)| This contains the message body for a message. | 

### Return type

[**CreateDigitalAccessKeyResponse**](CreateDigitalAccessKeyResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/hal+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | The message was created for the order. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_legal_disclosure**
> CreateLegalDisclosureResponse create_legal_disclosure(amazon_order_id, marketplace_ids, body)



Sends a critical message that contains documents that a seller is legally obligated to provide to the buyer. This message should only be used to deliver documents that are required by law.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 1 | 5 |  The `x-amzn-RateLimit-Limit` response header contains the usage plan rate limits for the operation, when available. The preceding table contains the default rate and burst values for this operation. Selling partners whose business demands require higher throughput might have higher rate and burst values than those shown here. For more information, refer to [Usage Plans and Rate Limits](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.messaging
from py_sp_api.generated.messaging.models.create_legal_disclosure_request import CreateLegalDisclosureRequest
from py_sp_api.generated.messaging.models.create_legal_disclosure_response import CreateLegalDisclosureResponse
from py_sp_api.generated.messaging.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.messaging.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.messaging.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.messaging.MessagingApi(api_client)
    amazon_order_id = 'amazon_order_id_example' # str | An Amazon order identifier. This identifies the order for which a message is sent.
    marketplace_ids = ['marketplace_ids_example'] # List[str] | A marketplace identifier. This identifies the marketplace in which the order was placed. You can only specify one marketplace.
    body = py_sp_api.generated.messaging.CreateLegalDisclosureRequest() # CreateLegalDisclosureRequest | This contains the message body for a message.

    try:
        api_response = api_instance.create_legal_disclosure(amazon_order_id, marketplace_ids, body)
        print("The response of MessagingApi->create_legal_disclosure:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MessagingApi->create_legal_disclosure: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **amazon_order_id** | **str**| An Amazon order identifier. This identifies the order for which a message is sent. | 
 **marketplace_ids** | [**List[str]**](str.md)| A marketplace identifier. This identifies the marketplace in which the order was placed. You can only specify one marketplace. | 
 **body** | [**CreateLegalDisclosureRequest**](CreateLegalDisclosureRequest.md)| This contains the message body for a message. | 

### Return type

[**CreateLegalDisclosureResponse**](CreateLegalDisclosureResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/hal+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | The legal disclosure message was created for the order. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_negative_feedback_removal**
> CreateNegativeFeedbackRemovalResponse create_negative_feedback_removal(amazon_order_id, marketplace_ids)



Sends a non-critical message that asks a buyer to remove their negative feedback. This message should only be sent after the seller has resolved the buyer's problem.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 1 | 5 |  The `x-amzn-RateLimit-Limit` response header contains the usage plan rate limits for the operation, when available. The preceding table contains the default rate and burst values for this operation. Selling partners whose business demands require higher throughput might have higher rate and burst values than those shown here. For more information, refer to [Usage Plans and Rate Limits](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.messaging
from py_sp_api.generated.messaging.models.create_negative_feedback_removal_response import CreateNegativeFeedbackRemovalResponse
from py_sp_api.generated.messaging.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.messaging.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.messaging.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.messaging.MessagingApi(api_client)
    amazon_order_id = 'amazon_order_id_example' # str | An Amazon order identifier. This identifies the order for which a message is sent.
    marketplace_ids = ['marketplace_ids_example'] # List[str] | A marketplace identifier. This identifies the marketplace in which the order was placed. You can only specify one marketplace.

    try:
        api_response = api_instance.create_negative_feedback_removal(amazon_order_id, marketplace_ids)
        print("The response of MessagingApi->create_negative_feedback_removal:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MessagingApi->create_negative_feedback_removal: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **amazon_order_id** | **str**| An Amazon order identifier. This identifies the order for which a message is sent. | 
 **marketplace_ids** | [**List[str]**](str.md)| A marketplace identifier. This identifies the marketplace in which the order was placed. You can only specify one marketplace. | 

### Return type

[**CreateNegativeFeedbackRemovalResponse**](CreateNegativeFeedbackRemovalResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/hal+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | The negativeFeedbackRemoval message was created for the order. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_unexpected_problem**
> CreateUnexpectedProblemResponse create_unexpected_problem(amazon_order_id, marketplace_ids, body)



Sends a critical message to a buyer that an unexpected problem was encountered affecting the completion of the order.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 1 | 5 |  The `x-amzn-RateLimit-Limit` response header contains the usage plan rate limits for the operation, when available. The preceding table contains the default rate and burst values for this operation. Selling partners whose business demands require higher throughput might have higher rate and burst values than those shown here. For more information, refer to [Usage Plans and Rate Limits](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.messaging
from py_sp_api.generated.messaging.models.create_unexpected_problem_request import CreateUnexpectedProblemRequest
from py_sp_api.generated.messaging.models.create_unexpected_problem_response import CreateUnexpectedProblemResponse
from py_sp_api.generated.messaging.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.messaging.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.messaging.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.messaging.MessagingApi(api_client)
    amazon_order_id = 'amazon_order_id_example' # str | An Amazon order identifier. This identifies the order for which a message is sent.
    marketplace_ids = ['marketplace_ids_example'] # List[str] | A marketplace identifier. This identifies the marketplace in which the order was placed. You can only specify one marketplace.
    body = py_sp_api.generated.messaging.CreateUnexpectedProblemRequest() # CreateUnexpectedProblemRequest | This contains the message body for a message.

    try:
        api_response = api_instance.create_unexpected_problem(amazon_order_id, marketplace_ids, body)
        print("The response of MessagingApi->create_unexpected_problem:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MessagingApi->create_unexpected_problem: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **amazon_order_id** | **str**| An Amazon order identifier. This identifies the order for which a message is sent. | 
 **marketplace_ids** | [**List[str]**](str.md)| A marketplace identifier. This identifies the marketplace in which the order was placed. You can only specify one marketplace. | 
 **body** | [**CreateUnexpectedProblemRequest**](CreateUnexpectedProblemRequest.md)| This contains the message body for a message. | 

### Return type

[**CreateUnexpectedProblemResponse**](CreateUnexpectedProblemResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/hal+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | The message was created for the order. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_warranty**
> CreateWarrantyResponse create_warranty(amazon_order_id, marketplace_ids, body)



Sends a message to a buyer to provide details about warranty information on a purchase in their order.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 1 | 5 |  The `x-amzn-RateLimit-Limit` response header contains the usage plan rate limits for the operation, when available. The preceding table contains the default rate and burst values for this operation. Selling partners whose business demands require higher throughput might have higher rate and burst values than those shown here. For more information, refer to [Usage Plans and Rate Limits](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.messaging
from py_sp_api.generated.messaging.models.create_warranty_request import CreateWarrantyRequest
from py_sp_api.generated.messaging.models.create_warranty_response import CreateWarrantyResponse
from py_sp_api.generated.messaging.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.messaging.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.messaging.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.messaging.MessagingApi(api_client)
    amazon_order_id = 'amazon_order_id_example' # str | An Amazon order identifier. This identifies the order for which a message is sent.
    marketplace_ids = ['marketplace_ids_example'] # List[str] | A marketplace identifier. This identifies the marketplace in which the order was placed. You can only specify one marketplace.
    body = py_sp_api.generated.messaging.CreateWarrantyRequest() # CreateWarrantyRequest | This contains the message body for a message.

    try:
        api_response = api_instance.create_warranty(amazon_order_id, marketplace_ids, body)
        print("The response of MessagingApi->create_warranty:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MessagingApi->create_warranty: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **amazon_order_id** | **str**| An Amazon order identifier. This identifies the order for which a message is sent. | 
 **marketplace_ids** | [**List[str]**](str.md)| A marketplace identifier. This identifies the marketplace in which the order was placed. You can only specify one marketplace. | 
 **body** | [**CreateWarrantyRequest**](CreateWarrantyRequest.md)| This contains the message body for a message. | 

### Return type

[**CreateWarrantyResponse**](CreateWarrantyResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/hal+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | The message was created for the order. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_attributes**
> GetAttributesResponse get_attributes(amazon_order_id, marketplace_ids)



Returns a response containing attributes related to an order. This includes buyer preferences.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 1 | 5 |

### Example


```python
import py_sp_api.generated.messaging
from py_sp_api.generated.messaging.models.get_attributes_response import GetAttributesResponse
from py_sp_api.generated.messaging.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.messaging.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.messaging.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.messaging.MessagingApi(api_client)
    amazon_order_id = 'amazon_order_id_example' # str | An Amazon order identifier. This identifies the order for which a message is sent.
    marketplace_ids = ['marketplace_ids_example'] # List[str] | A marketplace identifier. This identifies the marketplace in which the order was placed. You can only specify one marketplace.

    try:
        api_response = api_instance.get_attributes(amazon_order_id, marketplace_ids)
        print("The response of MessagingApi->get_attributes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MessagingApi->get_attributes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **amazon_order_id** | **str**| An Amazon order identifier. This identifies the order for which a message is sent. | 
 **marketplace_ids** | [**List[str]**](str.md)| A marketplace identifier. This identifies the marketplace in which the order was placed. You can only specify one marketplace. | 

### Return type

[**GetAttributesResponse**](GetAttributesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/hal+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Response has successfully been returned. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_messaging_actions_for_order**
> GetMessagingActionsForOrderResponse get_messaging_actions_for_order(amazon_order_id, marketplace_ids)



Returns a list of message types that are available for an order that you specify. A message type is represented by an actions object, which contains a path and query parameter(s). You can use the path and parameter(s) to call an operation that sends a message.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 1 | 5 |  The `x-amzn-RateLimit-Limit` response header contains the usage plan rate limits for the operation, when available. The preceding table contains the default rate and burst values for this operation. Selling partners whose business demands require higher throughput might have higher rate and burst values than those shown here. For more information, refer to [Usage Plans and Rate Limits](https://developer-docs.amazon.com/sp-api/docs/usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.messaging
from py_sp_api.generated.messaging.models.get_messaging_actions_for_order_response import GetMessagingActionsForOrderResponse
from py_sp_api.generated.messaging.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.messaging.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.messaging.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.messaging.MessagingApi(api_client)
    amazon_order_id = 'amazon_order_id_example' # str | An Amazon order identifier. This specifies the order for which you want a list of available message types.
    marketplace_ids = ['marketplace_ids_example'] # List[str] | A marketplace identifier. This identifies the marketplace in which the order was placed. You can only specify one marketplace.

    try:
        api_response = api_instance.get_messaging_actions_for_order(amazon_order_id, marketplace_ids)
        print("The response of MessagingApi->get_messaging_actions_for_order:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MessagingApi->get_messaging_actions_for_order: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **amazon_order_id** | **str**| An Amazon order identifier. This specifies the order for which you want a list of available message types. | 
 **marketplace_ids** | [**List[str]**](str.md)| A marketplace identifier. This identifies the marketplace in which the order was placed. You can only specify one marketplace. | 

### Return type

[**GetMessagingActionsForOrderResponse**](GetMessagingActionsForOrderResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/hal+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returns hypermedia links under the _links.actions key that specify which messaging actions are allowed for the order. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **send_invoice**
> InvoiceResponse send_invoice(amazon_order_id, marketplace_ids, body)



Sends a message providing the buyer an invoice

### Example


```python
import py_sp_api.generated.messaging
from py_sp_api.generated.messaging.models.invoice_request import InvoiceRequest
from py_sp_api.generated.messaging.models.invoice_response import InvoiceResponse
from py_sp_api.generated.messaging.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.messaging.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.messaging.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.messaging.MessagingApi(api_client)
    amazon_order_id = 'amazon_order_id_example' # str | An Amazon order identifier. This identifies the order for which a message is sent.
    marketplace_ids = ['marketplace_ids_example'] # List[str] | A marketplace identifier. This identifies the marketplace in which the order was placed. You can only specify one marketplace.
    body = py_sp_api.generated.messaging.InvoiceRequest() # InvoiceRequest | This contains the message body for a message.

    try:
        api_response = api_instance.send_invoice(amazon_order_id, marketplace_ids, body)
        print("The response of MessagingApi->send_invoice:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MessagingApi->send_invoice: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **amazon_order_id** | **str**| An Amazon order identifier. This identifies the order for which a message is sent. | 
 **marketplace_ids** | [**List[str]**](str.md)| A marketplace identifier. This identifies the marketplace in which the order was placed. You can only specify one marketplace. | 
 **body** | [**InvoiceRequest**](InvoiceRequest.md)| This contains the message body for a message. | 

### Return type

[**InvoiceResponse**](InvoiceResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/hal+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | The message was created for the order. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | 403 can be caused for reasons like Access Denied, Unauthorized, Expired Token, Invalid Signature or Resource Not Found. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**415** | The entity of the request is in a format not supported by the requested resource. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | Encountered an unexpected condition which prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

