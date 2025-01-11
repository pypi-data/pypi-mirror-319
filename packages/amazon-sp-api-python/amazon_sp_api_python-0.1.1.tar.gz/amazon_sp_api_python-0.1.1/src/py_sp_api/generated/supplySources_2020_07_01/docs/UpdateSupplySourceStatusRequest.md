# UpdateSupplySourceStatusRequest

A request to update the status of a supply source.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | [**SupplySourceStatus**](SupplySourceStatus.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.supplySources_2020_07_01.models.update_supply_source_status_request import UpdateSupplySourceStatusRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateSupplySourceStatusRequest from a JSON string
update_supply_source_status_request_instance = UpdateSupplySourceStatusRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateSupplySourceStatusRequest.to_json())

# convert the object into a dict
update_supply_source_status_request_dict = update_supply_source_status_request_instance.to_dict()
# create an instance of UpdateSupplySourceStatusRequest from a dict
update_supply_source_status_request_from_dict = UpdateSupplySourceStatusRequest.from_dict(update_supply_source_status_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


