# CreateShipmentRequest

Request schema.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipment_request_details** | [**ShipmentRequestDetails**](ShipmentRequestDetails.md) |  | 
**shipping_service_id** | **str** | An Amazon-defined shipping service identifier. | 
**shipping_service_offer_id** | **str** | Identifies a shipping service order made by a carrier. | [optional] 
**hazmat_type** | [**HazmatType**](HazmatType.md) |  | [optional] 
**label_format_option** | [**LabelFormatOptionRequest**](LabelFormatOptionRequest.md) |  | [optional] 
**shipment_level_seller_inputs_list** | [**List[AdditionalSellerInputs]**](AdditionalSellerInputs.md) | A list of additional seller input pairs required to purchase shipping. | [optional] 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.create_shipment_request import CreateShipmentRequest

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


