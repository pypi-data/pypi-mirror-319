# DangerousGoodsDetails

Details related to any dangerous goods/items that are being shipped.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**united_nations_regulatory_id** | **str** | The specific UNID of the item being shipped. | [optional] 
**transportation_regulatory_class** | **str** | The specific regulatory class  of the item being shipped. | [optional] 
**packing_group** | **str** | The specific packaging group of the item being shipped. | [optional] 
**packing_instruction** | **str** | The specific packing instruction of the item being shipped. | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.dangerous_goods_details import DangerousGoodsDetails

# TODO update the JSON string below
json = "{}"
# create an instance of DangerousGoodsDetails from a JSON string
dangerous_goods_details_instance = DangerousGoodsDetails.from_json(json)
# print the JSON string representation of the object
print(DangerousGoodsDetails.to_json())

# convert the object into a dict
dangerous_goods_details_dict = dangerous_goods_details_instance.to_dict()
# create an instance of DangerousGoodsDetails from a dict
dangerous_goods_details_from_dict = DangerousGoodsDetails.from_dict(dangerous_goods_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


