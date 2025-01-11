# PlacementOption

Contains information pertaining to the placement of the contents of an inbound plan and the related costs.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**discounts** | [**List[Incentive]**](Incentive.md) | Discount for the offered option. | 
**expiration** | **datetime** | The expiration date of the placement option. In [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) datetime format with pattern &#x60;yyyy-MM-ddTHH:mm:ss.sssZ&#x60;. | [optional] 
**fees** | [**List[Incentive]**](Incentive.md) | The fee for the offered option. | 
**placement_option_id** | **str** | The identifier of a placement option. A placement option represents the shipment splits and destinations of SKUs. | 
**shipment_ids** | **List[str]** | Shipment ids. | 
**status** | **str** | The status of a placement option. Possible values: &#x60;OFFERED&#x60;, &#x60;ACCEPTED&#x60;, &#x60;EXPIRED&#x60;. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.placement_option import PlacementOption

# TODO update the JSON string below
json = "{}"
# create an instance of PlacementOption from a JSON string
placement_option_instance = PlacementOption.from_json(json)
# print the JSON string representation of the object
print(PlacementOption.to_json())

# convert the object into a dict
placement_option_dict = placement_option_instance.to_dict()
# create an instance of PlacementOption from a dict
placement_option_from_dict = PlacementOption.from_dict(placement_option_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


