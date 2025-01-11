# PackingOption

A packing option contains a set of pack groups plus additional information about the packing option, such as any discounts or fees if it's selected.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**discounts** | [**List[Incentive]**](Incentive.md) | Discount for the offered option. | 
**expiration** | **datetime** | The time at which this packing option is no longer valid. In [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) datetime format with pattern &#x60;yyyy-MM-ddTHH:mm:ss.sssZ&#x60;. | [optional] 
**fees** | [**List[Incentive]**](Incentive.md) | Fee for the offered option. | 
**packing_groups** | **List[str]** | Packing group IDs. | 
**packing_option_id** | **str** | Identifier of a packing option. | 
**status** | **str** | The status of the packing option. Possible values: &#x60;OFFERED&#x60;, &#x60;ACCEPTED&#x60;, &#x60;EXPIRED&#x60;. | 
**supported_shipping_configurations** | [**List[ShippingConfiguration]**](ShippingConfiguration.md) | List of supported shipping modes. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.packing_option import PackingOption

# TODO update the JSON string below
json = "{}"
# create an instance of PackingOption from a JSON string
packing_option_instance = PackingOption.from_json(json)
# print the JSON string representation of the object
print(PackingOption.to_json())

# convert the object into a dict
packing_option_dict = packing_option_instance.to_dict()
# create an instance of PackingOption from a dict
packing_option_from_dict = PackingOption.from_dict(packing_option_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


