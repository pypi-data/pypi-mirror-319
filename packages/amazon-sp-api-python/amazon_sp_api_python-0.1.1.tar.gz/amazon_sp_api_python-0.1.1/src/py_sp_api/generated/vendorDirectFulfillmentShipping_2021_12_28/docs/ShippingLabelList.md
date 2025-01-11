# ShippingLabelList

Response payload with the list of shipping labels.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**Pagination**](Pagination.md) |  | [optional] 
**shipping_labels** | [**List[ShippingLabel]**](ShippingLabel.md) | An array containing the details of the generated shipping labels. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.models.shipping_label_list import ShippingLabelList

# TODO update the JSON string below
json = "{}"
# create an instance of ShippingLabelList from a JSON string
shipping_label_list_instance = ShippingLabelList.from_json(json)
# print the JSON string representation of the object
print(ShippingLabelList.to_json())

# convert the object into a dict
shipping_label_list_dict = shipping_label_list_instance.to_dict()
# create an instance of ShippingLabelList from a dict
shipping_label_list_from_dict = ShippingLabelList.from_dict(shipping_label_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


