# PlacementOptionSummary

Summary information about a placement option.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**placement_option_id** | **str** | The identifier of a placement option. A placement option represents the shipment splits and destinations of SKUs. | 
**status** | **str** | The status of a placement option. Possible values: &#x60;OFFERED&#x60;, &#x60;ACCEPTED&#x60;. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.placement_option_summary import PlacementOptionSummary

# TODO update the JSON string below
json = "{}"
# create an instance of PlacementOptionSummary from a JSON string
placement_option_summary_instance = PlacementOptionSummary.from_json(json)
# print the JSON string representation of the object
print(PlacementOptionSummary.to_json())

# convert the object into a dict
placement_option_summary_dict = placement_option_summary_instance.to_dict()
# create an instance of PlacementOptionSummary from a dict
placement_option_summary_from_dict = PlacementOptionSummary.from_dict(placement_option_summary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


