# ListInboundPlanPalletsResponse

The `listInboundPlanPallets` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**Pagination**](Pagination.md) |  | [optional] 
**pallets** | [**List[Pallet]**](Pallet.md) | The pallets in an inbound plan. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.list_inbound_plan_pallets_response import ListInboundPlanPalletsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListInboundPlanPalletsResponse from a JSON string
list_inbound_plan_pallets_response_instance = ListInboundPlanPalletsResponse.from_json(json)
# print the JSON string representation of the object
print(ListInboundPlanPalletsResponse.to_json())

# convert the object into a dict
list_inbound_plan_pallets_response_dict = list_inbound_plan_pallets_response_instance.to_dict()
# create an instance of ListInboundPlanPalletsResponse from a dict
list_inbound_plan_pallets_response_from_dict = ListInboundPlanPalletsResponse.from_dict(list_inbound_plan_pallets_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


