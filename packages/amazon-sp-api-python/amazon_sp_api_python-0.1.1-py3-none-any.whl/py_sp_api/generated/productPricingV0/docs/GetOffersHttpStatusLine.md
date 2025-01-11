# GetOffersHttpStatusLine

The HTTP status line associated with the response.  For more information, consult [RFC 2616](https://www.w3.org/Protocols/rfc2616/rfc2616-sec6.html).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status_code** | **int** | The HTTP response Status Code. | [optional] 
**reason_phrase** | **str** | The HTTP response Reason-Phase. | [optional] 

## Example

```python
from py_sp_api.generated.productPricingV0.models.get_offers_http_status_line import GetOffersHttpStatusLine

# TODO update the JSON string below
json = "{}"
# create an instance of GetOffersHttpStatusLine from a JSON string
get_offers_http_status_line_instance = GetOffersHttpStatusLine.from_json(json)
# print the JSON string representation of the object
print(GetOffersHttpStatusLine.to_json())

# convert the object into a dict
get_offers_http_status_line_dict = get_offers_http_status_line_instance.to_dict()
# create an instance of GetOffersHttpStatusLine from a dict
get_offers_http_status_line_from_dict = GetOffersHttpStatusLine.from_dict(get_offers_http_status_line_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


