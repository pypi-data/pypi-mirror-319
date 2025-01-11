# RegulatedInformationField

A field collected from the regulatory form.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**field_id** | **str** | The unique identifier of the field. | 
**field_label** | **str** | The name of the field. | 
**field_type** | **str** | The type of field. | 
**field_value** | **str** | The content of the field as collected in regulatory form. Note that &#x60;FileAttachment&#x60; type fields contain a URL where you can download the attachment. | 

## Example

```python
from py_sp_api.generated.ordersV0.models.regulated_information_field import RegulatedInformationField

# TODO update the JSON string below
json = "{}"
# create an instance of RegulatedInformationField from a JSON string
regulated_information_field_instance = RegulatedInformationField.from_json(json)
# print the JSON string representation of the object
print(RegulatedInformationField.to_json())

# convert the object into a dict
regulated_information_field_dict = regulated_information_field_instance.to_dict()
# create an instance of RegulatedInformationField from a dict
regulated_information_field_from_dict = RegulatedInformationField.from_dict(regulated_information_field_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


