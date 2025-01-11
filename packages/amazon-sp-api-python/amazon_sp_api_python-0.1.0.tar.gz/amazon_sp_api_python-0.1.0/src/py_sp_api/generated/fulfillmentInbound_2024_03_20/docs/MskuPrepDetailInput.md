# MskuPrepDetailInput

An MSKU and its related prep details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**msku** | **str** | The merchant SKU, a merchant-supplied identifier for a specific SKU. | 
**prep_category** | [**PrepCategory**](PrepCategory.md) |  | 
**prep_types** | [**List[PrepType]**](PrepType.md) | A list of preparation types associated with a preparation category. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.msku_prep_detail_input import MskuPrepDetailInput

# TODO update the JSON string below
json = "{}"
# create an instance of MskuPrepDetailInput from a JSON string
msku_prep_detail_input_instance = MskuPrepDetailInput.from_json(json)
# print the JSON string representation of the object
print(MskuPrepDetailInput.to_json())

# convert the object into a dict
msku_prep_detail_input_dict = msku_prep_detail_input_instance.to_dict()
# create an instance of MskuPrepDetailInput from a dict
msku_prep_detail_input_from_dict = MskuPrepDetailInput.from_dict(msku_prep_detail_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


