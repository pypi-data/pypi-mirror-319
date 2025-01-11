# ShipperInstruction

The shipper instruction.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**delivery_notes** | **str** | The delivery notes for the shipment | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.shipper_instruction import ShipperInstruction

# TODO update the JSON string below
json = "{}"
# create an instance of ShipperInstruction from a JSON string
shipper_instruction_instance = ShipperInstruction.from_json(json)
# print the JSON string representation of the object
print(ShipperInstruction.to_json())

# convert the object into a dict
shipper_instruction_dict = shipper_instruction_instance.to_dict()
# create an instance of ShipperInstruction from a dict
shipper_instruction_from_dict = ShipperInstruction.from_dict(shipper_instruction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


