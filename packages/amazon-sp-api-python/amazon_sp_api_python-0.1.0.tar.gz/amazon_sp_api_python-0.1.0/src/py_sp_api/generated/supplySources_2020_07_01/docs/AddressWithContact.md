# AddressWithContact

The address and contact details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**contact_details** | [**ContactDetails**](ContactDetails.md) |  | [optional] 
**address** | [**Address**](Address.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.supplySources_2020_07_01.models.address_with_contact import AddressWithContact

# TODO update the JSON string below
json = "{}"
# create an instance of AddressWithContact from a JSON string
address_with_contact_instance = AddressWithContact.from_json(json)
# print the JSON string representation of the object
print(AddressWithContact.to_json())

# convert the object into a dict
address_with_contact_dict = address_with_contact_instance.to_dict()
# create an instance of AddressWithContact from a dict
address_with_contact_from_dict = AddressWithContact.from_dict(address_with_contact_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


