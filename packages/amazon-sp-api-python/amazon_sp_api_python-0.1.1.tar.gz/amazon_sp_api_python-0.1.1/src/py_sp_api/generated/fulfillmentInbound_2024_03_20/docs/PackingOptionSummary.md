# PackingOptionSummary

Summary information about a packing option.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**packing_option_id** | **str** | Identifier of a packing option. | 
**status** | **str** | The status of a packing option. Possible values: &#39;OFFERED&#39;, &#39;ACCEPTED&#39;, &#39;EXPIRED&#39;. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.packing_option_summary import PackingOptionSummary

# TODO update the JSON string below
json = "{}"
# create an instance of PackingOptionSummary from a JSON string
packing_option_summary_instance = PackingOptionSummary.from_json(json)
# print the JSON string representation of the object
print(PackingOptionSummary.to_json())

# convert the object into a dict
packing_option_summary_dict = packing_option_summary_instance.to_dict()
# create an instance of PackingOptionSummary from a dict
packing_option_summary_from_dict = PackingOptionSummary.from_dict(packing_option_summary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


