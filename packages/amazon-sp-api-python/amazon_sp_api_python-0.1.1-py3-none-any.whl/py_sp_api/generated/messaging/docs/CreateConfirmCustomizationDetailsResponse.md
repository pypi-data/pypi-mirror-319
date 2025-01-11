# CreateConfirmCustomizationDetailsResponse

The response schema for the confirmCustomizationDetails operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.messaging.models.create_confirm_customization_details_response import CreateConfirmCustomizationDetailsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateConfirmCustomizationDetailsResponse from a JSON string
create_confirm_customization_details_response_instance = CreateConfirmCustomizationDetailsResponse.from_json(json)
# print the JSON string representation of the object
print(CreateConfirmCustomizationDetailsResponse.to_json())

# convert the object into a dict
create_confirm_customization_details_response_dict = create_confirm_customization_details_response_instance.to_dict()
# create an instance of CreateConfirmCustomizationDetailsResponse from a dict
create_confirm_customization_details_response_from_dict = CreateConfirmCustomizationDetailsResponse.from_dict(create_confirm_customization_details_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


