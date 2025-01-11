# ListPrepDetailsResponse

The response to the `listPrepDetails` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**msku_prep_details** | [**List[MskuPrepDetail]**](MskuPrepDetail.md) | A list of MSKUs and related prep details. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.list_prep_details_response import ListPrepDetailsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListPrepDetailsResponse from a JSON string
list_prep_details_response_instance = ListPrepDetailsResponse.from_json(json)
# print the JSON string representation of the object
print(ListPrepDetailsResponse.to_json())

# convert the object into a dict
list_prep_details_response_dict = list_prep_details_response_instance.to_dict()
# create an instance of ListPrepDetailsResponse from a dict
list_prep_details_response_from_dict = ListPrepDetailsResponse.from_dict(list_prep_details_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


