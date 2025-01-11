# TaxWithholdingEvent

A TaxWithholding event on seller's account.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**posted_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 
**base_amount** | [**Currency**](Currency.md) |  | [optional] 
**withheld_amount** | [**Currency**](Currency.md) |  | [optional] 
**tax_withholding_period** | [**TaxWithholdingPeriod**](TaxWithholdingPeriod.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.tax_withholding_event import TaxWithholdingEvent

# TODO update the JSON string below
json = "{}"
# create an instance of TaxWithholdingEvent from a JSON string
tax_withholding_event_instance = TaxWithholdingEvent.from_json(json)
# print the JSON string representation of the object
print(TaxWithholdingEvent.to_json())

# convert the object into a dict
tax_withholding_event_dict = tax_withholding_event_instance.to_dict()
# create an instance of TaxWithholdingEvent from a dict
tax_withholding_event_from_dict = TaxWithholdingEvent.from_dict(tax_withholding_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


