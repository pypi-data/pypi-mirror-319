# PartyIdentification

Name, address and tax details of a party.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**party_id** | **str** | Assigned identification for the party. For example, warehouse code or vendor code. Please refer to specific party for more details. | 
**address** | [**Address**](Address.md) |  | [optional] 
**tax_info** | [**TaxRegistrationDetails**](TaxRegistrationDetails.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentOrders_2021_12_28.models.party_identification import PartyIdentification

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


