# SellingPartnerMetadata

Metadata that describes the seller.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selling_partner_id** | **str** | A unique seller identifier. | [optional] 
**account_type** | **str** | The type of account in the transaction. | [optional] 
**marketplace_id** | **str** | The identifier of the marketplace where the transaction occurred. | [optional] 

## Example

```python
from py_sp_api.generated.finances_2024_06_19.models.selling_partner_metadata import SellingPartnerMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of SellingPartnerMetadata from a JSON string
selling_partner_metadata_instance = SellingPartnerMetadata.from_json(json)
# print the JSON string representation of the object
print(SellingPartnerMetadata.to_json())

# convert the object into a dict
selling_partner_metadata_dict = selling_partner_metadata_instance.to_dict()
# create an instance of SellingPartnerMetadata from a dict
selling_partner_metadata_from_dict = SellingPartnerMetadata.from_dict(selling_partner_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


