# TaxClassification

The tax classification of the order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The type of tax. | [optional] 
**value** | **str** | The buyer&#39;s tax identifier. | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.tax_classification import TaxClassification

# TODO update the JSON string below
json = "{}"
# create an instance of TaxClassification from a JSON string
tax_classification_instance = TaxClassification.from_json(json)
# print the JSON string representation of the object
print(TaxClassification.to_json())

# convert the object into a dict
tax_classification_dict = tax_classification_instance.to_dict()
# create an instance of TaxClassification from a dict
tax_classification_from_dict = TaxClassification.from_dict(tax_classification_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


