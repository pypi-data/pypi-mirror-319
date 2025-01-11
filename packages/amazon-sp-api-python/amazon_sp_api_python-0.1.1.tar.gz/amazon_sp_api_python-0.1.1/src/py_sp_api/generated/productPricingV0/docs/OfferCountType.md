# OfferCountType

The total number of offers for the specified condition and fulfillment channel.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**condition** | **str** | Indicates the condition of the item. For example: New, Used, Collectible, Refurbished, or Club. | [optional] 
**fulfillment_channel** | [**FulfillmentChannelType**](FulfillmentChannelType.md) |  | [optional] 
**offer_count** | **int** | The number of offers in a fulfillment channel that meet a specific condition. | [optional] 

## Example

```python
from py_sp_api.generated.productPricingV0.models.offer_count_type import OfferCountType

# TODO update the JSON string below
json = "{}"
# create an instance of OfferCountType from a JSON string
offer_count_type_instance = OfferCountType.from_json(json)
# print the JSON string representation of the object
print(OfferCountType.to_json())

# convert the object into a dict
offer_count_type_dict = offer_count_type_instance.to_dict()
# create an instance of OfferCountType from a dict
offer_count_type_from_dict = OfferCountType.from_dict(offer_count_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


