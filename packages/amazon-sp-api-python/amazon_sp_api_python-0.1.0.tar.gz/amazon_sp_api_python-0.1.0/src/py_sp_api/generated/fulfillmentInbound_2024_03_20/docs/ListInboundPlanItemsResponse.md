# ListInboundPlanItemsResponse

The `listInboundPlanItems` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**items** | [**List[Item]**](Item.md) | The items in an inbound plan. | 
**pagination** | [**Pagination**](Pagination.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.list_inbound_plan_items_response import ListInboundPlanItemsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListInboundPlanItemsResponse from a JSON string
list_inbound_plan_items_response_instance = ListInboundPlanItemsResponse.from_json(json)
# print the JSON string representation of the object
print(ListInboundPlanItemsResponse.to_json())

# convert the object into a dict
list_inbound_plan_items_response_dict = list_inbound_plan_items_response_instance.to_dict()
# create an instance of ListInboundPlanItemsResponse from a dict
list_inbound_plan_items_response_from_dict = ListInboundPlanItemsResponse.from_dict(list_inbound_plan_items_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


