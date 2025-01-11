# py_sp_api.generated.vendorDirectFulfillmentSandboxData_2021_10_28.VendorDFSandboxApi

All URIs are relative to *https://sandbox.sellingpartnerapi-na.amazon.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**generate_order_scenarios**](VendorDFSandboxApi.md#generate_order_scenarios) | **POST** /vendor/directFulfillment/sandbox/2021-10-28/orders | 


# **generate_order_scenarios**
> TransactionReference generate_order_scenarios(body)



Submits a request to generate test order data for Vendor Direct Fulfillment API entities.

### Example


```python
import py_sp_api.generated.vendorDirectFulfillmentSandboxData_2021_10_28
from py_sp_api.generated.vendorDirectFulfillmentSandboxData_2021_10_28.models.generate_order_scenario_request import GenerateOrderScenarioRequest
from py_sp_api.generated.vendorDirectFulfillmentSandboxData_2021_10_28.models.transaction_reference import TransactionReference
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
    api_instance = py_sp_api.generated.vendorDirectFulfillmentSandboxData_2021_10_28.VendorDFSandboxApi(api_client)
    body = py_sp_api.generated.vendorDirectFulfillmentSandboxData_2021_10_28.GenerateOrderScenarioRequest() # GenerateOrderScenarioRequest | The request payload containing parameters for generating test order data scenarios.

    try:
        api_response = api_instance.generate_order_scenarios(body)
        print("The response of VendorDFSandboxApi->generate_order_scenarios:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VendorDFSandboxApi->generate_order_scenarios: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**GenerateOrderScenarioRequest**](GenerateOrderScenarioRequest.md)| The request payload containing parameters for generating test order data scenarios. | 

### Return type

[**TransactionReference**](TransactionReference.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Success. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference identifier. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

