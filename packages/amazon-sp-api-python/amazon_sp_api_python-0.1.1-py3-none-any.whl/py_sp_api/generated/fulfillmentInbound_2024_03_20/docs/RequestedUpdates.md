# RequestedUpdates

Objects that were included in the update request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**boxes** | [**List[BoxUpdateInput]**](BoxUpdateInput.md) | A list of boxes that will be present in the shipment after the update. | [optional] 
**items** | [**List[ItemInput]**](ItemInput.md) | A list of all items that will be present in the shipment after the update. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.requested_updates import RequestedUpdates

# TODO update the JSON string below
json = "{}"
# create an instance of RequestedUpdates from a JSON string
requested_updates_instance = RequestedUpdates.from_json(json)
# print the JSON string representation of the object
print(RequestedUpdates.to_json())

# convert the object into a dict
requested_updates_dict = requested_updates_instance.to_dict()
# create an instance of RequestedUpdates from a dict
requested_updates_from_dict = RequestedUpdates.from_dict(requested_updates_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


