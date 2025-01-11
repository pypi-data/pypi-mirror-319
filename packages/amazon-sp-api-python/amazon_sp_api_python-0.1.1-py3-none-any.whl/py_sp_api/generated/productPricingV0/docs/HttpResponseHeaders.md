# HttpResponseHeaders

A mapping of additional HTTP headers to send/receive for the individual batch request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_date** | **str** | The timestamp that the API request was received.  For more information, consult [RFC 2616 Section 14](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html). | [optional] 
**x_amzn_request_id** | **str** | Unique request reference ID. | [optional] 

## Example

```python
from py_sp_api.generated.productPricingV0.models.http_response_headers import HttpResponseHeaders

# TODO update the JSON string below
json = "{}"
# create an instance of HttpResponseHeaders from a JSON string
http_response_headers_instance = HttpResponseHeaders.from_json(json)
# print the JSON string representation of the object
print(HttpResponseHeaders.to_json())

# convert the object into a dict
http_response_headers_dict = http_response_headers_instance.to_dict()
# create an instance of HttpResponseHeaders from a dict
http_response_headers_from_dict = HttpResponseHeaders.from_dict(http_response_headers_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


