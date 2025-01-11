# GetShippingLabelListResponse

The response schema for the getShippingLabels operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**ShippingLabelList**](ShippingLabelList.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShippingV1.models.get_shipping_label_list_response import GetShippingLabelListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetShippingLabelListResponse from a JSON string
get_shipping_label_list_response_instance = GetShippingLabelListResponse.from_json(json)
# print the JSON string representation of the object
print(GetShippingLabelListResponse.to_json())

# convert the object into a dict
get_shipping_label_list_response_dict = get_shipping_label_list_response_instance.to_dict()
# create an instance of GetShippingLabelListResponse from a dict
get_shipping_label_list_response_from_dict = GetShippingLabelListResponse.from_dict(get_shipping_label_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


