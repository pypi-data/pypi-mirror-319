# SetPrepDetailsRequest

The `setPrepDetails` request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | The marketplace ID. For a list of possible values, refer to [Marketplace IDs](https://developer-docs.amazon.com/sp-api/docs/marketplace-ids). | 
**msku_prep_details** | [**List[MskuPrepDetailInput]**](MskuPrepDetailInput.md) | A list of MSKUs and related prep details. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.set_prep_details_request import SetPrepDetailsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SetPrepDetailsRequest from a JSON string
set_prep_details_request_instance = SetPrepDetailsRequest.from_json(json)
# print the JSON string representation of the object
print(SetPrepDetailsRequest.to_json())

# convert the object into a dict
set_prep_details_request_dict = set_prep_details_request_instance.to_dict()
# create an instance of SetPrepDetailsRequest from a dict
set_prep_details_request_from_dict = SetPrepDetailsRequest.from_dict(set_prep_details_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


