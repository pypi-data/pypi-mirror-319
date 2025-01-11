# CreateShipmentResult

The payload schema for the createShipment operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipment_id** | **str** | The unique shipment identifier. | 
**eligible_rates** | [**List[Rate]**](Rate.md) | A list of all the available rates that can be used to send the shipment. | 

## Example

```python
from py_sp_api.generated.shipping.models.create_shipment_result import CreateShipmentResult

# TODO update the JSON string below
json = "{}"
# create an instance of CreateShipmentResult from a JSON string
create_shipment_result_instance = CreateShipmentResult.from_json(json)
# print the JSON string representation of the object
print(CreateShipmentResult.to_json())

# convert the object into a dict
create_shipment_result_dict = create_shipment_result_instance.to_dict()
# create an instance of CreateShipmentResult from a dict
create_shipment_result_from_dict = CreateShipmentResult.from_dict(create_shipment_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


