# Party

The account related with the shipment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**account_id** | **str** | This is the Amazon Shipping account id generated during the Amazon Shipping onboarding process. | [optional] 

## Example

```python
from py_sp_api.generated.shipping.models.party import Party

# TODO update the JSON string below
json = "{}"
# create an instance of Party from a JSON string
party_instance = Party.from_json(json)
# print the JSON string representation of the object
print(Party.to_json())

# convert the object into a dict
party_dict = party_instance.to_dict()
# create an instance of Party from a dict
party_from_dict = Party.from_dict(party_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


