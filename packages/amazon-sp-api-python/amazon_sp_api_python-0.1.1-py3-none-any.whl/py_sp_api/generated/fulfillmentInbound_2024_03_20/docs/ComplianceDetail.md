# ComplianceDetail

Contains item identifiers and related tax information.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asin** | **str** | The Amazon Standard Identification Number, which identifies the detail page identifier. | [optional] 
**fnsku** | **str** | The Fulfillment Network SKU, which identifies a real fulfillable item with catalog data and condition. | [optional] 
**msku** | **str** | The merchant SKU, a merchant-supplied identifier for a specific SKU. | [optional] 
**tax_details** | [**TaxDetails**](TaxDetails.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.compliance_detail import ComplianceDetail

# TODO update the JSON string below
json = "{}"
# create an instance of ComplianceDetail from a JSON string
compliance_detail_instance = ComplianceDetail.from_json(json)
# print the JSON string representation of the object
print(ComplianceDetail.to_json())

# convert the object into a dict
compliance_detail_dict = compliance_detail_instance.to_dict()
# create an instance of ComplianceDetail from a dict
compliance_detail_from_dict = ComplianceDetail.from_dict(compliance_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


