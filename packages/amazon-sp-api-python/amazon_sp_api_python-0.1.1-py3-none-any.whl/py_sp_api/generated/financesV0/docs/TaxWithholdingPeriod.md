# TaxWithholdingPeriod

Period which taxwithholding on seller's account is calculated.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 
**end_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.tax_withholding_period import TaxWithholdingPeriod

# TODO update the JSON string below
json = "{}"
# create an instance of TaxWithholdingPeriod from a JSON string
tax_withholding_period_instance = TaxWithholdingPeriod.from_json(json)
# print the JSON string representation of the object
print(TaxWithholdingPeriod.to_json())

# convert the object into a dict
tax_withholding_period_dict = tax_withholding_period_instance.to_dict()
# create an instance of TaxWithholdingPeriod from a dict
tax_withholding_period_from_dict = TaxWithholdingPeriod.from_dict(tax_withholding_period_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


