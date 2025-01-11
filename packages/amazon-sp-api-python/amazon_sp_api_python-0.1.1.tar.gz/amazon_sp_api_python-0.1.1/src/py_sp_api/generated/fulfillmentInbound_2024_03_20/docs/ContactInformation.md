# ContactInformation

The seller's contact information.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**email** | **str** | The email address. | [optional] 
**name** | **str** | The contact&#39;s name. | 
**phone_number** | **str** | The phone number. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.contact_information import ContactInformation

# TODO update the JSON string below
json = "{}"
# create an instance of ContactInformation from a JSON string
contact_information_instance = ContactInformation.from_json(json)
# print the JSON string representation of the object
print(ContactInformation.to_json())

# convert the object into a dict
contact_information_dict = contact_information_instance.to_dict()
# create an instance of ContactInformation from a dict
contact_information_from_dict = ContactInformation.from_dict(contact_information_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


