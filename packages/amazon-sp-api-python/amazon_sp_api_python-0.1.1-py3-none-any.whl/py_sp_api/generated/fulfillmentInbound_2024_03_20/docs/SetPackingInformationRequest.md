# SetPackingInformationRequest

The `setPackingInformation` request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**package_groupings** | [**List[PackageGroupingInput]**](PackageGroupingInput.md) | List of packing information for the inbound plan. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.set_packing_information_request import SetPackingInformationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SetPackingInformationRequest from a JSON string
set_packing_information_request_instance = SetPackingInformationRequest.from_json(json)
# print the JSON string representation of the object
print(SetPackingInformationRequest.to_json())

# convert the object into a dict
set_packing_information_request_dict = set_packing_information_request_instance.to_dict()
# create an instance of SetPackingInformationRequest from a dict
set_packing_information_request_from_dict = SetPackingInformationRequest.from_dict(set_packing_information_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


