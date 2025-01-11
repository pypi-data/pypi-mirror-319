# BoxContentsFeeDetails

The manual processing fee per unit and total fee for a shipment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_units** | **int** | The item quantity. | [optional] 
**fee_per_unit** | [**Amount**](Amount.md) |  | [optional] 
**total_fee** | [**Amount**](Amount.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.box_contents_fee_details import BoxContentsFeeDetails

# TODO update the JSON string below
json = "{}"
# create an instance of BoxContentsFeeDetails from a JSON string
box_contents_fee_details_instance = BoxContentsFeeDetails.from_json(json)
# print the JSON string representation of the object
print(BoxContentsFeeDetails.to_json())

# convert the object into a dict
box_contents_fee_details_dict = box_contents_fee_details_instance.to_dict()
# create an instance of BoxContentsFeeDetails from a dict
box_contents_fee_details_from_dict = BoxContentsFeeDetails.from_dict(box_contents_fee_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


