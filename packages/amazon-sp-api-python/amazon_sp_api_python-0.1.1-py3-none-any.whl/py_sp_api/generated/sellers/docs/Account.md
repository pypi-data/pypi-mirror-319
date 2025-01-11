# Account

The response schema for the `getAccount` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_participation_list** | [**List[MarketplaceParticipation]**](MarketplaceParticipation.md) | List of marketplace participations. | 
**business_type** | **str** | The type of business registered for the seller account. | 
**selling_plan** | **str** | The selling plan details. | 
**business** | [**Business**](Business.md) |  | [optional] 
**primary_contact** | [**PrimaryContact**](PrimaryContact.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.sellers.models.account import Account

# TODO update the JSON string below
json = "{}"
# create an instance of Account from a JSON string
account_instance = Account.from_json(json)
# print the JSON string representation of the object
print(Account.to_json())

# convert the object into a dict
account_dict = account_instance.to_dict()
# create an instance of Account from a dict
account_from_dict = Account.from_dict(account_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


