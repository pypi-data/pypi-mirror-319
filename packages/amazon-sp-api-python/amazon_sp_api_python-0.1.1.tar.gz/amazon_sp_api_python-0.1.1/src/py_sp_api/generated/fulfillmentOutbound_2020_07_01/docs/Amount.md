# Amount

A quantity based on unit of measure.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**unit_of_measure** | **str** | The unit of measure for the amount. | 
**value** | **str** | A decimal number with no loss of precision. Useful when precision loss is unacceptable, as with currencies. Follows RFC7159 for number representation. | 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.amount import Amount

# TODO update the JSON string below
json = "{}"
# create an instance of Amount from a JSON string
amount_instance = Amount.from_json(json)
# print the JSON string representation of the object
print(Amount.to_json())

# convert the object into a dict
amount_dict = amount_instance.to_dict()
# create an instance of Amount from a dict
amount_from_dict = Amount.from_dict(amount_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


