# TaxItemDetails

Total tax details for the line item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tax_line_item** | [**List[TaxDetails]**](TaxDetails.md) | A list of tax line items. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentOrders_2021_12_28.models.tax_item_details import TaxItemDetails

# TODO update the JSON string below
json = "{}"
# create an instance of TaxItemDetails from a JSON string
tax_item_details_instance = TaxItemDetails.from_json(json)
# print the JSON string representation of the object
print(TaxItemDetails.to_json())

# convert the object into a dict
tax_item_details_dict = tax_item_details_instance.to_dict()
# create an instance of TaxItemDetails from a dict
tax_item_details_from_dict = TaxItemDetails.from_dict(tax_item_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


