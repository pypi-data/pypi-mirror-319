# ListPackingGroupBoxesResponse

The `listPackingGroupBoxes` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**boxes** | [**List[Box]**](Box.md) | Provides the information about the list of boxes in the packing group. | 
**pagination** | [**Pagination**](Pagination.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.list_packing_group_boxes_response import ListPackingGroupBoxesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListPackingGroupBoxesResponse from a JSON string
list_packing_group_boxes_response_instance = ListPackingGroupBoxesResponse.from_json(json)
# print the JSON string representation of the object
print(ListPackingGroupBoxesResponse.to_json())

# convert the object into a dict
list_packing_group_boxes_response_dict = list_packing_group_boxes_response_instance.to_dict()
# create an instance of ListPackingGroupBoxesResponse from a dict
list_packing_group_boxes_response_from_dict = ListPackingGroupBoxesResponse.from_dict(list_packing_group_boxes_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


