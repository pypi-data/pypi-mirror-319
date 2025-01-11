# ContactDetailsPrimary


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**email** | **str** | The email address to which email messages are delivered. | [optional] 
**phone** | **str** | The phone number of the person, business or institution. | [optional] 

## Example

```python
from py_sp_api.generated.supplySources_2020_07_01.models.contact_details_primary import ContactDetailsPrimary

# TODO update the JSON string below
json = "{}"
# create an instance of ContactDetailsPrimary from a JSON string
contact_details_primary_instance = ContactDetailsPrimary.from_json(json)
# print the JSON string representation of the object
print(ContactDetailsPrimary.to_json())

# convert the object into a dict
contact_details_primary_dict = contact_details_primary_instance.to_dict()
# create an instance of ContactDetailsPrimary from a dict
contact_details_primary_from_dict = ContactDetailsPrimary.from_dict(contact_details_primary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


