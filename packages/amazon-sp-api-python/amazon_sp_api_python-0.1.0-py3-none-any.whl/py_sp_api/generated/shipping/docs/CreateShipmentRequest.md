# CreateShipmentRequest

The request schema for the createShipment operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**client_reference_id** | **str** | Client reference id. | 
**ship_to** | [**Address**](Address.md) |  | 
**ship_from** | [**Address**](Address.md) |  | 
**containers** | [**List[Container]**](Container.md) | A list of container. | 

## Example

```python
from py_sp_api.generated.shipping.models.create_shipment_request import CreateShipmentRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateShipmentRequest from a JSON string
create_shipment_request_instance = CreateShipmentRequest.from_json(json)
# print the JSON string representation of the object
print(CreateShipmentRequest.to_json())

# convert the object into a dict
create_shipment_request_dict = create_shipment_request_instance.to_dict()
# create an instance of CreateShipmentRequest from a dict
create_shipment_request_from_dict = CreateShipmentRequest.from_dict(create_shipment_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


