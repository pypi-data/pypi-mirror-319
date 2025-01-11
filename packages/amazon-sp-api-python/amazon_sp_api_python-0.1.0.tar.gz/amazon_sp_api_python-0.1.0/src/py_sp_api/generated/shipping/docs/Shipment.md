# Shipment

The shipment related data.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipment_id** | **str** | The unique shipment identifier. | 
**client_reference_id** | **str** | Client reference id. | 
**ship_from** | [**Address**](Address.md) |  | 
**ship_to** | [**Address**](Address.md) |  | 
**accepted_rate** | [**AcceptedRate**](AcceptedRate.md) |  | [optional] 
**shipper** | [**Party**](Party.md) |  | [optional] 
**containers** | [**List[Container]**](Container.md) | A list of container. | 

## Example

```python
from py_sp_api.generated.shipping.models.shipment import Shipment

# TODO update the JSON string below
json = "{}"
# create an instance of Shipment from a JSON string
shipment_instance = Shipment.from_json(json)
# print the JSON string representation of the object
print(Shipment.to_json())

# convert the object into a dict
shipment_dict = shipment_instance.to_dict()
# create an instance of Shipment from a dict
shipment_from_dict = Shipment.from_dict(shipment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


