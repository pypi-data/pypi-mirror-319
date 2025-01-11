# ActiveAccount

Active Account Details

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**account_id** | **str** | Account Id associated with this account. | [optional] 
**carrier_id** | **str** | The carrier identifier for the offering, provided by the carrier. | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.active_account import ActiveAccount

# TODO update the JSON string below
json = "{}"
# create an instance of ActiveAccount from a JSON string
active_account_instance = ActiveAccount.from_json(json)
# print the JSON string representation of the object
print(ActiveAccount.to_json())

# convert the object into a dict
active_account_dict = active_account_instance.to_dict()
# create an instance of ActiveAccount from a dict
active_account_from_dict = ActiveAccount.from_dict(active_account_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


