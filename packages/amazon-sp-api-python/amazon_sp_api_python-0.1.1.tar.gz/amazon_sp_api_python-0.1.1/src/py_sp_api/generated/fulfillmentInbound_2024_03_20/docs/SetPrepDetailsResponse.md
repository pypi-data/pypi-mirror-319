# SetPrepDetailsResponse

The `setPrepDetails` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**operation_id** | **str** | UUID for the given operation. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.set_prep_details_response import SetPrepDetailsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SetPrepDetailsResponse from a JSON string
set_prep_details_response_instance = SetPrepDetailsResponse.from_json(json)
# print the JSON string representation of the object
print(SetPrepDetailsResponse.to_json())

# convert the object into a dict
set_prep_details_response_dict = set_prep_details_response_instance.to_dict()
# create an instance of SetPrepDetailsResponse from a dict
set_prep_details_response_from_dict = SetPrepDetailsResponse.from_dict(set_prep_details_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


