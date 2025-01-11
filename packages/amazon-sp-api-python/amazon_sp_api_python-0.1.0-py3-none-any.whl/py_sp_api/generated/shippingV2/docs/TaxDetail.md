# TaxDetail

Indicates the tax specifications associated with the shipment for customs compliance purposes in certain regions.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tax_type** | [**TaxType**](TaxType.md) |  | 
**tax_registration_number** | **str** | The shipper&#39;s tax registration number associated with the shipment for customs compliance purposes in certain regions. | 

## Example

```python
from py_sp_api.generated.shippingV2.models.tax_detail import TaxDetail

# TODO update the JSON string below
json = "{}"
# create an instance of TaxDetail from a JSON string
tax_detail_instance = TaxDetail.from_json(json)
# print the JSON string representation of the object
print(TaxDetail.to_json())

# convert the object into a dict
tax_detail_dict = tax_detail_instance.to_dict()
# create an instance of TaxDetail from a dict
tax_detail_from_dict = TaxDetail.from_dict(tax_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


