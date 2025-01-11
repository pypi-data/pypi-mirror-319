# ItemOffersRequestParams


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | A marketplace identifier. Specifies the marketplace for which prices are returned. | 
**item_condition** | [**ItemCondition**](ItemCondition.md) |  | 
**customer_type** | [**CustomerType**](CustomerType.md) |  | [optional] 
**asin** | **str** | The Amazon Standard Identification Number (ASIN) of the item. This is the same Asin passed as a request parameter. | [optional] 

## Example

```python
from py_sp_api.generated.productPricingV0.models.item_offers_request_params import ItemOffersRequestParams

# TODO update the JSON string below
json = "{}"
# create an instance of ItemOffersRequestParams from a JSON string
item_offers_request_params_instance = ItemOffersRequestParams.from_json(json)
# print the JSON string representation of the object
print(ItemOffersRequestParams.to_json())

# convert the object into a dict
item_offers_request_params_dict = item_offers_request_params_instance.to_dict()
# create an instance of ItemOffersRequestParams from a dict
item_offers_request_params_from_dict = ItemOffersRequestParams.from_dict(item_offers_request_params_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


