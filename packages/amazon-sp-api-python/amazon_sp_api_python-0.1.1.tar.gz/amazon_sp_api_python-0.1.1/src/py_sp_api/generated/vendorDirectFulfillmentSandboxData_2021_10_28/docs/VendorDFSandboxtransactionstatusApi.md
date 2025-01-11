# py_sp_api.generated.vendorDirectFulfillmentSandboxData_2021_10_28.VendorDFSandboxtransactionstatusApi

All URIs are relative to *https://sandbox.sellingpartnerapi-na.amazon.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_order_scenarios**](VendorDFSandboxtransactionstatusApi.md#get_order_scenarios) | **GET** /vendor/directFulfillment/sandbox/2021-10-28/transactions/{transactionId} | 


# **get_order_scenarios**
> TransactionStatus get_order_scenarios(transaction_id)



Returns the status of the transaction indicated by the specified transactionId. If the transaction was successful, also returns the requested test order data.

### Example


```python
import py_sp_api.generated.vendorDirectFulfillmentSandboxData_2021_10_28
from py_sp_api.generated.vendorDirectFulfillmentSandboxData_2021_10_28.models.transaction_status import TransactionStatus
from py_sp_api.generated.vendorDirectFulfillmentSandboxData_2021_10_28.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sandbox.sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.vendorDirectFulfillmentSandboxData_2021_10_28.Configuration(
    host = "https://sandbox.sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.vendorDirectFulfillmentSandboxData_2021_10_28.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.vendorDirectFulfillmentSandboxData_2021_10_28.VendorDFSandboxtransactionstatusApi(api_client)
    transaction_id = 'transaction_id_example' # str | The transaction identifier returned in the response to the generateOrderScenarios operation.

    try:
        api_response = api_instance.get_order_scenarios(transaction_id)
        print("The response of VendorDFSandboxtransactionstatusApi->get_order_scenarios:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VendorDFSandboxtransactionstatusApi->get_order_scenarios: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **transaction_id** | **str**| The transaction identifier returned in the response to the generateOrderScenarios operation. | 

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
**200** | Success. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**401** | The request&#39;s Authorization header is not formatted correctly or does not contain a valid token. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

