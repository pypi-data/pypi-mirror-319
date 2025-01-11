# BuyerTaxInfo

Tax information about the buyer.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**company_legal_name** | **str** | The legal name of the company. | [optional] 
**taxing_region** | **str** | The country or region imposing the tax. | [optional] 
**tax_classifications** | [**List[TaxClassification]**](TaxClassification.md) | The list of tax classifications. | [optional] 

## Example

```python
from py_sp_api.generated.shipmentInvoicingV0.models.buyer_tax_info import BuyerTaxInfo

# TODO update the JSON string below
json = "{}"
# create an instance of BuyerTaxInfo from a JSON string
buyer_tax_info_instance = BuyerTaxInfo.from_json(json)
# print the JSON string representation of the object
print(BuyerTaxInfo.to_json())

# convert the object into a dict
buyer_tax_info_dict = buyer_tax_info_instance.to_dict()
# create an instance of BuyerTaxInfo from a dict
buyer_tax_info_from_dict = BuyerTaxInfo.from_dict(buyer_tax_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


