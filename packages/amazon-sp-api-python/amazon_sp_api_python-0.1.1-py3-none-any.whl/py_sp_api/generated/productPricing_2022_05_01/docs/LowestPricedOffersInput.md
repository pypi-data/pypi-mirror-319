# LowestPricedOffersInput

The input required for building `LowestPricedOffers` data in the response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**item_condition** | [**Condition**](Condition.md) |  | 
**offer_type** | **str** | The input parameter specifies the type of offers requested for &#x60;LowestPricedOffers&#x60;. This applies to &#x60;Consumer&#x60; and &#x60;Business&#x60; offers. &#x60;Consumer&#x60; is the default &#x60;offerType&#x60;. | 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.lowest_priced_offers_input import LowestPricedOffersInput

# TODO update the JSON string below
json = "{}"
# create an instance of LowestPricedOffersInput from a JSON string
lowest_priced_offers_input_instance = LowestPricedOffersInput.from_json(json)
# print the JSON string representation of the object
print(LowestPricedOffersInput.to_json())

# convert the object into a dict
lowest_priced_offers_input_dict = lowest_priced_offers_input_instance.to_dict()
# create an instance of LowestPricedOffersInput from a dict
lowest_priced_offers_input_from_dict = LowestPricedOffersInput.from_dict(lowest_priced_offers_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


