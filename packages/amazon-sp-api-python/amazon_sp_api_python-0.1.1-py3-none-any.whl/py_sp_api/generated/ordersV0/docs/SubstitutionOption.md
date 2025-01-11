# SubstitutionOption

Substitution options for an order item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asin** | **str** | The item&#39;s Amazon Standard Identification Number (ASIN). | [optional] 
**quantity_ordered** | **int** | The number of items to be picked for this substitution option.  | [optional] 
**seller_sku** | **str** | The item&#39;s seller stock keeping unit (SKU). | [optional] 
**title** | **str** | The item&#39;s title. | [optional] 
**measurement** | [**Measurement**](Measurement.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.substitution_option import SubstitutionOption

# TODO update the JSON string below
json = "{}"
# create an instance of SubstitutionOption from a JSON string
substitution_option_instance = SubstitutionOption.from_json(json)
# print the JSON string representation of the object
print(SubstitutionOption.to_json())

# convert the object into a dict
substitution_option_dict = substitution_option_instance.to_dict()
# create an instance of SubstitutionOption from a dict
substitution_option_from_dict = SubstitutionOption.from_dict(substitution_option_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


