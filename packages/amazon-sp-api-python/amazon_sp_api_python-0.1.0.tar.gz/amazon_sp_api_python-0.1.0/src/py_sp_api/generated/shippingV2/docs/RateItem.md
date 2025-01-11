# RateItem

Rate Item for shipping (base cost, transaction fee, confirmation, insurance, etc.) Data source definition: 

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**rate_item_id** | [**RateItemID**](RateItemID.md) |  | [optional] 
**rate_item_type** | [**RateItemType**](RateItemType.md) |  | [optional] 
**rate_item_charge** | [**Currency**](Currency.md) |  | [optional] 
**rate_item_name_localization** | **str** | Used for the localization. | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.rate_item import RateItem

# TODO update the JSON string below
json = "{}"
# create an instance of RateItem from a JSON string
rate_item_instance = RateItem.from_json(json)
# print the JSON string representation of the object
print(RateItem.to_json())

# convert the object into a dict
rate_item_dict = rate_item_instance.to_dict()
# create an instance of RateItem from a dict
rate_item_from_dict = RateItem.from_dict(rate_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


