# ListHandoverSlotsRequest

The request schema for the `listHandoverSlots` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | A string of up to 255 characters. | 
**amazon_order_id** | **str** | An Amazon-defined order identifier. Identifies the order that the seller wants to deliver using Amazon Easy Ship. | 
**package_dimensions** | [**Dimensions**](Dimensions.md) |  | 
**package_weight** | [**Weight**](Weight.md) |  | 

## Example

```python
from py_sp_api.generated.easyShip_2022_03_23.models.list_handover_slots_request import ListHandoverSlotsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ListHandoverSlotsRequest from a JSON string
list_handover_slots_request_instance = ListHandoverSlotsRequest.from_json(json)
# print the JSON string representation of the object
print(ListHandoverSlotsRequest.to_json())

# convert the object into a dict
list_handover_slots_request_dict = list_handover_slots_request_instance.to_dict()
# create an instance of ListHandoverSlotsRequest from a dict
list_handover_slots_request_from_dict = ListHandoverSlotsRequest.from_dict(list_handover_slots_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


