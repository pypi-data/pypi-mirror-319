# ImportDetails

Import details for an import order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**method_of_payment** | **str** | If the recipient requests, contains the shipment method of payment. This is for import PO&#39;s only. | [optional] 
**international_commercial_terms** | **str** | Incoterms (International Commercial Terms) are used to divide transaction costs and responsibilities between buyer and seller and reflect state-of-the-art transportation practices. This is for import purchase orders only.  | [optional] 
**port_of_delivery** | **str** | The port where goods on an import purchase order must be delivered by the vendor. This should only be specified when the internationalCommercialTerms is FOB. | [optional] 
**import_containers** | **str** | Types and numbers of container(s) for import purchase orders. Can be a comma-separated list if the shipment has multiple containers. HC signifies a high-capacity container. Free-text field, limited to 64 characters. The format will be a comma-delimited list containing values of the type: $NUMBER_OF_CONTAINERS_OF_THIS_TYPE-$CONTAINER_TYPE. The list of values for the container type is: 40&#39;(40-foot container), 40&#39;HC (40-foot high-capacity container), 45&#39;, 45&#39;HC, 30&#39;, 30&#39;HC, 20&#39;, 20&#39;HC. | [optional] 
**shipping_instructions** | **str** | Special instructions regarding the shipment. This field is for import purchase orders. | [optional] 

## Example

```python
from py_sp_api.generated.vendorOrders.models.import_details import ImportDetails

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


