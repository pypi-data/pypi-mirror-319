# InvalidItemReason

The reason that the item is invalid for return.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**invalid_item_reason_code** | [**InvalidItemReasonCode**](InvalidItemReasonCode.md) |  | 
**description** | **str** | A human readable description of the invalid item reason code. | 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.invalid_item_reason import InvalidItemReason

# TODO update the JSON string below
json = "{}"
# create an instance of InvalidItemReason from a JSON string
invalid_item_reason_instance = InvalidItemReason.from_json(json)
# print the JSON string representation of the object
print(InvalidItemReason.to_json())

# convert the object into a dict
invalid_item_reason_dict = invalid_item_reason_instance.to_dict()
# create an instance of InvalidItemReason from a dict
invalid_item_reason_from_dict = InvalidItemReason.from_dict(invalid_item_reason_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


