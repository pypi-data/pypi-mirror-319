# ImportDetails

Provide these fields only if this shipment is a direct import.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**method_of_payment** | **str** | This is used for import purchase orders only. If the recipient requests, this field will contain the shipment method of payment. | [optional] 
**seal_number** | **str** | The container&#39;s seal number. | [optional] 
**route** | [**Route**](Route.md) |  | [optional] 
**import_containers** | **str** | Types and numbers of container(s) for import purchase orders. Can be a comma-separated list if shipment has multiple containers. | [optional] 
**billable_weight** | [**Weight**](Weight.md) |  | [optional] 
**estimated_ship_by_date** | **datetime** | Date on which the shipment is expected to be shipped. This value should not be in the past and not more than 60 days out in the future. | [optional] 
**handling_instructions** | **str** | Identification of the instructions on how specified item/carton/pallet should be handled. | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.import_details import ImportDetails

# TODO update the JSON string below
json = "{}"
# create an instance of ImportDetails from a JSON string
import_details_instance = ImportDetails.from_json(json)
# print the JSON string representation of the object
print(ImportDetails.to_json())

# convert the object into a dict
import_details_dict = import_details_instance.to_dict()
# create an instance of ImportDetails from a dict
import_details_from_dict = ImportDetails.from_dict(import_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


