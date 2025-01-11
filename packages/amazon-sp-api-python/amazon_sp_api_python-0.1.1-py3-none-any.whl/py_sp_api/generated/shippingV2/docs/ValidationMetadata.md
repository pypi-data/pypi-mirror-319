# ValidationMetadata

ValidationMetadata Details

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error_message** | **str** | errorMessage for the error. | [optional] 
**validation_strategy** | **str** | validationStrategy for the error. | [optional] 
**value** | **str** | Value. | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.validation_metadata import ValidationMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of ValidationMetadata from a JSON string
validation_metadata_instance = ValidationMetadata.from_json(json)
# print the JSON string representation of the object
print(ValidationMetadata.to_json())

# convert the object into a dict
validation_metadata_dict = validation_metadata_instance.to_dict()
# create an instance of ValidationMetadata from a dict
validation_metadata_from_dict = ValidationMetadata.from_dict(validation_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


