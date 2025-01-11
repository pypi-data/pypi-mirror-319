# PackingSlipList

A list of packing slips.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**Pagination**](Pagination.md) |  | [optional] 
**packing_slips** | [**List[PackingSlip]**](PackingSlip.md) | An array of packing slip objects. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShippingV1.models.packing_slip_list import PackingSlipList

# TODO update the JSON string below
json = "{}"
# create an instance of PackingSlipList from a JSON string
packing_slip_list_instance = PackingSlipList.from_json(json)
# print the JSON string representation of the object
print(PackingSlipList.to_json())

# convert the object into a dict
packing_slip_list_dict = packing_slip_list_instance.to_dict()
# create an instance of PackingSlipList from a dict
packing_slip_list_from_dict = PackingSlipList.from_dict(packing_slip_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


