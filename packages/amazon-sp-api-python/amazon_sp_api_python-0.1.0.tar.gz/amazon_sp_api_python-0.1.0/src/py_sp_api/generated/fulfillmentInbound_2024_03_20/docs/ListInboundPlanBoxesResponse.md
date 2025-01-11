# ListInboundPlanBoxesResponse

The `listInboundPlanBoxes` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**boxes** | [**List[Box]**](Box.md) | A list of boxes in an inbound plan. | 
**pagination** | [**Pagination**](Pagination.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.list_inbound_plan_boxes_response import ListInboundPlanBoxesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListInboundPlanBoxesResponse from a JSON string
list_inbound_plan_boxes_response_instance = ListInboundPlanBoxesResponse.from_json(json)
# print the JSON string representation of the object
print(ListInboundPlanBoxesResponse.to_json())

# convert the object into a dict
list_inbound_plan_boxes_response_dict = list_inbound_plan_boxes_response_instance.to_dict()
# create an instance of ListInboundPlanBoxesResponse from a dict
list_inbound_plan_boxes_response_from_dict = ListInboundPlanBoxesResponse.from_dict(list_inbound_plan_boxes_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


