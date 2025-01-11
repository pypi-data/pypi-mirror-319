# ContactDetails

The contact details

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**primary** | [**ContactDetailsPrimary**](ContactDetailsPrimary.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.supplySources_2020_07_01.models.contact_details import ContactDetails

# TODO update the JSON string below
json = "{}"
# create an instance of ContactDetails from a JSON string
contact_details_instance = ContactDetails.from_json(json)
# print the JSON string representation of the object
print(ContactDetails.to_json())

# convert the object into a dict
contact_details_dict = contact_details_instance.to_dict()
# create an instance of ContactDetails from a dict
contact_details_from_dict = ContactDetails.from_dict(contact_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


