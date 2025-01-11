# CreateInboundPlanRequest

The `createInboundPlan` request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**destination_marketplaces** | **List[str]** | Marketplaces where the items need to be shipped to. Currently only one marketplace can be selected in this request. | 
**items** | [**List[ItemInput]**](ItemInput.md) | Items included in this plan. | 
**name** | **str** | Name for the Inbound Plan. If one isn&#39;t provided, a default name will be provided. | [optional] 
**source_address** | [**AddressInput**](AddressInput.md) |  | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.create_inbound_plan_request import CreateInboundPlanRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateInboundPlanRequest from a JSON string
create_inbound_plan_request_instance = CreateInboundPlanRequest.from_json(json)
# print the JSON string representation of the object
print(CreateInboundPlanRequest.to_json())

# convert the object into a dict
create_inbound_plan_request_dict = create_inbound_plan_request_instance.to_dict()
# create an instance of CreateInboundPlanRequest from a dict
create_inbound_plan_request_from_dict = CreateInboundPlanRequest.from_dict(create_inbound_plan_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


