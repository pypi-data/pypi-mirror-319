# py_sp_api.generated.vendorDirectFulfillmentTransactions_2021_12_28.VendorTransactionApi

All URIs are relative to *https://sellingpartnerapi-na.amazon.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_transaction_status**](VendorTransactionApi.md#get_transaction_status) | **GET** /vendor/directFulfillment/transactions/2021-12-28/transactions/{transactionId} | 


# **get_transaction_status**
> TransactionStatus get_transaction_status(transaction_id)



Returns the status of the transaction indicated by the specified transactionId.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 10 | 10 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values then those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.vendorDirectFulfillmentTransactions_2021_12_28
from py_sp_api.generated.vendorDirectFulfillmentTransactions_2021_12_28.models.transaction_status import TransactionStatus
from py_sp_api.generated.vendorDirectFulfillmentTransactions_2021_12_28.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.vendorDirectFulfillmentTransactions_2021_12_28.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.vendorDirectFulfillmentTransactions_2021_12_28.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.vendorDirectFulfillmentTransactions_2021_12_28.VendorTransactionApi(api_client)
    transaction_id = 'transaction_id_example' # str | Previously returned in the response to the POST request of a specific transaction.

    try:
        api_response = api_instance.get_transaction_status(transaction_id)
        print("The response of VendorTransactionApi->get_transaction_status:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VendorTransactionApi->get_transaction_status: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **transaction_id** | **str**| Previously returned in the response to the POST request of a specific transaction. | 

### Return type

[**TransactionStatus**](TransactionStatus.md)

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

