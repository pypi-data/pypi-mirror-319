# SetPackingInformationResponse

The `setPackingInformation` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**operation_id** | **str** | UUID for the given operation. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.set_packing_information_response import SetPackingInformationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SetPackingInformationResponse from a JSON string
set_packing_information_response_instance = SetPackingInformationResponse.from_json(json)
# print the JSON string representation of the object
print(SetPackingInformationResponse.to_json())

# convert the object into a dict
set_packing_information_response_dict = set_packing_information_response_instance.to_dict()
# create an instance of SetPackingInformationResponse from a dict
set_packing_information_response_from_dict = SetPackingInformationResponse.from_dict(set_packing_information_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


