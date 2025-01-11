# PurchaseShipmentRequest

The request schema for the purchaseShipment operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**request_token** | **str** | A unique token generated to identify a getRates operation. | 
**rate_id** | **str** | An identifier for the rate (shipment offering) provided by a shipping service provider. | 
**requested_document_specification** | [**RequestedDocumentSpecification**](RequestedDocumentSpecification.md) |  | 
**requested_value_added_services** | [**List[RequestedValueAddedService]**](RequestedValueAddedService.md) | The value-added services to be added to a shipping service purchase. | [optional] 
**additional_inputs** | **Dict[str, object]** | The additional inputs required to purchase a shipping offering, in JSON format. The JSON provided here must adhere to the JSON schema that is returned in the response to the getAdditionalInputs operation.  Additional inputs are only required when indicated by the requiresAdditionalInputs property in the response to the getRates operation. | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.purchase_shipment_request import PurchaseShipmentRequest

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


