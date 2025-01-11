# PurchaseShipmentRequest

The payload schema for the purchaseShipment operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**client_reference_id** | **str** | Client reference id. | 
**ship_to** | [**Address**](Address.md) |  | 
**ship_from** | [**Address**](Address.md) |  | 
**ship_date** | **datetime** | The start date and time. This defaults to the current date and time. | [optional] 
**service_type** | [**ServiceType**](ServiceType.md) |  | 
**containers** | [**List[Container]**](Container.md) | A list of container. | 
**label_specification** | [**LabelSpecification**](LabelSpecification.md) |  | 

## Example

```python
from py_sp_api.generated.shipping.models.purchase_shipment_request import PurchaseShipmentRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PurchaseShipmentRequest from a JSON string
purchase_shipment_request_instance = PurchaseShipmentRequest.from_json(json)
# print the JSON string representation of the object
print(PurchaseShipmentRequest.to_json())

# convert the object into a dict
purchase_shipment_request_dict = purchase_shipment_request_instance.to_dict()
# create an instance of PurchaseShipmentRequest from a dict
purchase_shipment_request_from_dict = PurchaseShipmentRequest.from_dict(purchase_shipment_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


