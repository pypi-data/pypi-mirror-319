# BuyerTaxInformation

Contains the business invoice tax information. Available only in the TR marketplace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**buyer_legal_company_name** | **str** | Business buyer&#39;s company legal name. | [optional] 
**buyer_business_address** | **str** | Business buyer&#39;s address. | [optional] 
**buyer_tax_registration_id** | **str** | Business buyer&#39;s tax registration ID. | [optional] 
**buyer_tax_office** | **str** | Business buyer&#39;s tax office. | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.buyer_tax_information import BuyerTaxInformation

# TODO update the JSON string below
json = "{}"
# create an instance of BuyerTaxInformation from a JSON string
buyer_tax_information_instance = BuyerTaxInformation.from_json(json)
# print the JSON string representation of the object
print(BuyerTaxInformation.to_json())

# convert the object into a dict
buyer_tax_information_dict = buyer_tax_information_instance.to_dict()
# create an instance of BuyerTaxInformation from a dict
buyer_tax_information_from_dict = BuyerTaxInformation.from_dict(buyer_tax_information_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


