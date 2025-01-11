# PartyIdentification

Name, address and tax details of a party.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**party_id** | **str** | Assigned identification for the party. | 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentInventoryV1.models.party_identification import PartyIdentification

# TODO update the JSON string below
json = "{}"
# create an instance of PartyIdentification from a JSON string
party_identification_instance = PartyIdentification.from_json(json)
# print the JSON string representation of the object
print(PartyIdentification.to_json())

# convert the object into a dict
party_identification_dict = party_identification_instance.to_dict()
# create an instance of PartyIdentification from a dict
party_identification_from_dict = PartyIdentification.from_dict(party_identification_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


