# GetShippingLabelResponse

The response schema for the getShippingLabel operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**ShippingLabel**](ShippingLabel.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShippingV1.models.get_shipping_label_response import GetShippingLabelResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetShippingLabelResponse from a JSON string
get_shipping_label_response_instance = GetShippingLabelResponse.from_json(json)
# print the JSON string representation of the object
print(GetShippingLabelResponse.to_json())

# convert the object into a dict
get_shipping_label_response_dict = get_shipping_label_response_instance.to_dict()
# create an instance of GetShippingLabelResponse from a dict
get_shipping_label_response_from_dict = GetShippingLabelResponse.from_dict(get_shipping_label_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


