# GetPreorderInfoResult

Result for the get preorder info operation

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipment_contains_preorderable_items** | **bool** | Indicates whether the shipment contains items that have been enabled for pre-order. For more information about enabling items for pre-order, see the Seller Central Help. | [optional] 
**shipment_confirmed_for_preorder** | **bool** | Indicates whether this shipment has been confirmed for pre-order. | [optional] 
**need_by_date** | **date** | Type containing date in string format | [optional] 
**confirmed_fulfillable_date** | **date** | Type containing date in string format | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.get_preorder_info_result import GetPreorderInfoResult

# TODO update the JSON string below
json = "{}"
# create an instance of GetPreorderInfoResult from a JSON string
get_preorder_info_result_instance = GetPreorderInfoResult.from_json(json)
# print the JSON string representation of the object
print(GetPreorderInfoResult.to_json())

# convert the object into a dict
get_preorder_info_result_dict = get_preorder_info_result_instance.to_dict()
# create an instance of GetPreorderInfoResult from a dict
get_preorder_info_result_from_dict = GetPreorderInfoResult.from_dict(get_preorder_info_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


