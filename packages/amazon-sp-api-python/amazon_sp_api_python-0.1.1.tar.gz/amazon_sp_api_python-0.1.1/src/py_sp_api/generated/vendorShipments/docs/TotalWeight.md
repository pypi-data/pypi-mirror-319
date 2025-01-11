# TotalWeight

The total weight of units that are sold by weight in a shipment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**unit_of_measure** | **str** | The unit of measure for the weight of items that are ordered by cases and support pricing by weight. | 
**amount** | **str** | A decimal number with no loss of precision. Useful when precision loss is unacceptable, as with currencies. Follows RFC7159 for number representation. &lt;br&gt;**Pattern** : &#x60;^-?(0|([1-9]\\d*))(\\.\\d+)?([eE][+-]?\\d+)?$&#x60;. | 

## Example

```python
from py_sp_api.generated.vendorShipments.models.total_weight import TotalWeight

# TODO update the JSON string below
json = "{}"
# create an instance of TotalWeight from a JSON string
total_weight_instance = TotalWeight.from_json(json)
# print the JSON string representation of the object
print(TotalWeight.to_json())

# convert the object into a dict
total_weight_dict = total_weight_instance.to_dict()
# create an instance of TotalWeight from a dict
total_weight_from_dict = TotalWeight.from_dict(total_weight_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


