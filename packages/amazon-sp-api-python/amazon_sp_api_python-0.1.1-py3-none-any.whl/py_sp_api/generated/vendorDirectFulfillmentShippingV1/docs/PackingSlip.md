# PackingSlip

Packing slip information.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**purchase_order_number** | **str** | Purchase order number of the shipment that corresponds to the packing slip. | 
**content** | **str** | A Base64encoded string of the packing slip PDF. | 
**content_type** | **str** | The format of the file such as PDF, JPEG etc. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShippingV1.models.packing_slip import PackingSlip

# TODO update the JSON string below
json = "{}"
# create an instance of PackingSlip from a JSON string
packing_slip_instance = PackingSlip.from_json(json)
# print the JSON string representation of the object
print(PackingSlip.to_json())

# convert the object into a dict
packing_slip_dict = packing_slip_instance.to_dict()
# create an instance of PackingSlip from a dict
packing_slip_from_dict = PackingSlip.from_dict(packing_slip_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


