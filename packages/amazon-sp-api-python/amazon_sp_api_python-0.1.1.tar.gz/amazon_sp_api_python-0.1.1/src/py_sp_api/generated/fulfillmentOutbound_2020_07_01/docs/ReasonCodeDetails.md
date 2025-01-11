# ReasonCodeDetails

A return reason code, a description, and an optional description translation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**return_reason_code** | **str** | A code that indicates a valid return reason. | 
**description** | **str** | A human readable description of the return reason code. | 
**translated_description** | **str** | A translation of the description. The translation is in the language specified in the Language request parameter. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.reason_code_details import ReasonCodeDetails

# TODO update the JSON string below
json = "{}"
# create an instance of ReasonCodeDetails from a JSON string
reason_code_details_instance = ReasonCodeDetails.from_json(json)
# print the JSON string representation of the object
print(ReasonCodeDetails.to_json())

# convert the object into a dict
reason_code_details_dict = reason_code_details_instance.to_dict()
# create an instance of ReasonCodeDetails from a dict
reason_code_details_from_dict = ReasonCodeDetails.from_dict(reason_code_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


