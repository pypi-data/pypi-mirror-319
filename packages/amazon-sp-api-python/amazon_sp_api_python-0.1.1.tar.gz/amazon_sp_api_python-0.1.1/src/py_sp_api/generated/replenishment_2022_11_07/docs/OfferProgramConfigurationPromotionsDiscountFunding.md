# OfferProgramConfigurationPromotionsDiscountFunding

A promotional percentage discount applied to the offer.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**percentage** | **float** | The percentage discount on the offer. | [optional] 

## Example

```python
from py_sp_api.generated.replenishment_2022_11_07.models.offer_program_configuration_promotions_discount_funding import OfferProgramConfigurationPromotionsDiscountFunding

# TODO update the JSON string below
json = "{}"
# create an instance of OfferProgramConfigurationPromotionsDiscountFunding from a JSON string
offer_program_configuration_promotions_discount_funding_instance = OfferProgramConfigurationPromotionsDiscountFunding.from_json(json)
# print the JSON string representation of the object
print(OfferProgramConfigurationPromotionsDiscountFunding.to_json())

# convert the object into a dict
offer_program_configuration_promotions_discount_funding_dict = offer_program_configuration_promotions_discount_funding_instance.to_dict()
# create an instance of OfferProgramConfigurationPromotionsDiscountFunding from a dict
offer_program_configuration_promotions_discount_funding_from_dict = OfferProgramConfigurationPromotionsDiscountFunding.from_dict(offer_program_configuration_promotions_discount_funding_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


