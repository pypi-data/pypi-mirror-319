# GetOffersResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | A marketplace identifier. | 
**asin** | **str** | The Amazon Standard Identification Number (ASIN) of the item. | [optional] 
**sku** | **str** | The stock keeping unit (SKU) of the item. | [optional] 
**item_condition** | [**ConditionType**](ConditionType.md) |  | 
**status** | **str** | The status of the operation. | 
**identifier** | [**ItemIdentifier**](ItemIdentifier.md) |  | 
**summary** | [**Summary**](Summary.md) |  | 
**offers** | [**List[OfferDetail]**](OfferDetail.md) |  | 

## Example

```python
from py_sp_api.generated.productPricingV0.models.get_offers_result import GetOffersResult

# TODO update the JSON string below
json = "{}"
# create an instance of GetOffersResult from a JSON string
get_offers_result_instance = GetOffersResult.from_json(json)
# print the JSON string representation of the object
print(GetOffersResult.to_json())

# convert the object into a dict
get_offers_result_dict = get_offers_result_instance.to_dict()
# create an instance of GetOffersResult from a dict
get_offers_result_from_dict = GetOffersResult.from_dict(get_offers_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


