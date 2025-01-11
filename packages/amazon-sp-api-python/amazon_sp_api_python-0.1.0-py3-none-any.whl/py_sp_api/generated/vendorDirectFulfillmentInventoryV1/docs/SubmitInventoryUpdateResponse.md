# SubmitInventoryUpdateResponse

The response schema for the submitInventoryUpdate operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**TransactionReference**](TransactionReference.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentInventoryV1.models.submit_inventory_update_response import SubmitInventoryUpdateResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SubmitInventoryUpdateResponse from a JSON string
submit_inventory_update_response_instance = SubmitInventoryUpdateResponse.from_json(json)
# print the JSON string representation of the object
print(SubmitInventoryUpdateResponse.to_json())

# convert the object into a dict
submit_inventory_update_response_dict = submit_inventory_update_response_instance.to_dict()
# create an instance of SubmitInventoryUpdateResponse from a dict
submit_inventory_update_response_from_dict = SubmitInventoryUpdateResponse.from_dict(submit_inventory_update_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


