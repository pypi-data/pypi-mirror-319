# RejectionReason

The reason for rejecting the order's regulated information. This is only present if the order is rejected.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**rejection_reason_id** | **str** | The unique identifier for the rejection reason. | 
**rejection_reason_description** | **str** | The description of this rejection reason. | 

## Example

```python
from py_sp_api.generated.ordersV0.models.rejection_reason import RejectionReason

# TODO update the JSON string below
json = "{}"
# create an instance of RejectionReason from a JSON string
rejection_reason_instance = RejectionReason.from_json(json)
# print the JSON string representation of the object
print(RejectionReason.to_json())

# convert the object into a dict
rejection_reason_dict = rejection_reason_instance.to_dict()
# create an instance of RejectionReason from a dict
rejection_reason_from_dict = RejectionReason.from_dict(rejection_reason_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


