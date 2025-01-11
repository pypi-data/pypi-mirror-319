# PrimaryContact

Information about the seller's primary contact.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The full name of the seller&#39;s primary contact. | 
**address** | [**Address**](Address.md) |  | 
**non_latin_name** | **str** | The non-Latin script version of the primary contact&#39;s name, if applicable. | [optional] 

## Example

```python
from py_sp_api.generated.sellers.models.primary_contact import PrimaryContact

# TODO update the JSON string below
json = "{}"
# create an instance of PrimaryContact from a JSON string
primary_contact_instance = PrimaryContact.from_json(json)
# print the JSON string representation of the object
print(PrimaryContact.to_json())

# convert the object into a dict
primary_contact_dict = primary_contact_instance.to_dict()
# create an instance of PrimaryContact from a dict
primary_contact_from_dict = PrimaryContact.from_dict(primary_contact_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


