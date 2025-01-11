# SubmitInventoryUpdateRequest

The request body for the submitInventoryUpdate operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**inventory** | [**InventoryUpdate**](InventoryUpdate.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentInventoryV1.models.submit_inventory_update_request import SubmitInventoryUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SubmitInventoryUpdateRequest from a JSON string
submit_inventory_update_request_instance = SubmitInventoryUpdateRequest.from_json(json)
# print the JSON string representation of the object
print(SubmitInventoryUpdateRequest.to_json())

# convert the object into a dict
submit_inventory_update_request_dict = submit_inventory_update_request_instance.to_dict()
# create an instance of SubmitInventoryUpdateRequest from a dict
submit_inventory_update_request_from_dict = SubmitInventoryUpdateRequest.from_dict(submit_inventory_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


