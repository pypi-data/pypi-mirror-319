# ListHandoverSlotsResponse

The response schema for the `listHandoverSlots` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amazon_order_id** | **str** | An Amazon-defined order identifier. Identifies the order that the seller wants to deliver using Amazon Easy Ship. | 
**time_slots** | [**List[TimeSlot]**](TimeSlot.md) | A list of time slots. | 

## Example

```python
from py_sp_api.generated.easyShip_2022_03_23.models.list_handover_slots_response import ListHandoverSlotsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListHandoverSlotsResponse from a JSON string
list_handover_slots_response_instance = ListHandoverSlotsResponse.from_json(json)
# print the JSON string representation of the object
print(ListHandoverSlotsResponse.to_json())

# convert the object into a dict
list_handover_slots_response_dict = list_handover_slots_response_instance.to_dict()
# create an instance of ListHandoverSlotsResponse from a dict
list_handover_slots_response_from_dict = ListHandoverSlotsResponse.from_dict(list_handover_slots_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


