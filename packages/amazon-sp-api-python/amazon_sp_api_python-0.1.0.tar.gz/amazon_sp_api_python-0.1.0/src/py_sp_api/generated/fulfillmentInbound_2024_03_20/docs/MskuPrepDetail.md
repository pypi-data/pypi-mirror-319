# MskuPrepDetail

An MSKU and its related prep details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**all_owners_constraint** | [**AllOwnersConstraint**](AllOwnersConstraint.md) |  | [optional] 
**label_owner_constraint** | [**OwnerConstraint**](OwnerConstraint.md) |  | [optional] 
**msku** | **str** | The merchant SKU, a merchant-supplied identifier for a specific SKU. | 
**prep_category** | [**PrepCategory**](PrepCategory.md) |  | 
**prep_owner_constraint** | [**OwnerConstraint**](OwnerConstraint.md) |  | [optional] 
**prep_types** | [**List[PrepType]**](PrepType.md) | A list of preparation types associated with a preparation category. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.msku_prep_detail import MskuPrepDetail

# TODO update the JSON string below
json = "{}"
# create an instance of MskuPrepDetail from a JSON string
msku_prep_detail_instance = MskuPrepDetail.from_json(json)
# print the JSON string representation of the object
print(MskuPrepDetail.to_json())

# convert the object into a dict
msku_prep_detail_dict = msku_prep_detail_instance.to_dict()
# create an instance of MskuPrepDetail from a dict
msku_prep_detail_from_dict = MskuPrepDetail.from_dict(msku_prep_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


