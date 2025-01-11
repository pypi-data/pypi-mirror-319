# OfferIdentifier

Identifies an offer from a particular seller for a specified ASIN.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | A marketplace identifier. Specifies the marketplace for which data is returned. | 
**seller_id** | **str** | The seller identifier for the offer. | [optional] 
**sku** | **str** | The seller SKU of the item. This will only be present for the target offer, which belongs to the requesting seller. | [optional] 
**asin** | **str** | The ASIN of the item. | 
**fulfillment_type** | [**FulfillmentType**](FulfillmentType.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.offer_identifier import OfferIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of OfferIdentifier from a JSON string
offer_identifier_instance = OfferIdentifier.from_json(json)
# print the JSON string representation of the object
print(OfferIdentifier.to_json())

# convert the object into a dict
offer_identifier_dict = offer_identifier_instance.to_dict()
# create an instance of OfferIdentifier from a dict
offer_identifier_from_dict = OfferIdentifier.from_dict(offer_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


