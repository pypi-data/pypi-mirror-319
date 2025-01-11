# RelationshipType

Specific variations of the item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**identifiers** | [**IdentifierType**](IdentifierType.md) |  | [optional] 
**color** | **str** | The color variation of the item. | [optional] 
**edition** | **str** | The edition variation of the item. | [optional] 
**flavor** | **str** | The flavor variation of the item. | [optional] 
**gem_type** | **List[str]** | The gem type variations of the item. | [optional] 
**golf_club_flex** | **str** | The golf club flex variation of an item. | [optional] 
**hand_orientation** | **str** | The hand orientation variation of an item. | [optional] 
**hardware_platform** | **str** | The hardware platform variation of an item. | [optional] 
**material_type** | **List[str]** | The material type variations of an item. | [optional] 
**metal_type** | **str** | The metal type variation of an item. | [optional] 
**model** | **str** | The model variation of an item. | [optional] 
**operating_system** | **List[str]** | The operating system variations of an item. | [optional] 
**product_type_subcategory** | **str** | The product type subcategory variation of an item. | [optional] 
**ring_size** | **str** | The ring size variation of an item. | [optional] 
**shaft_material** | **str** | The shaft material variation of an item. | [optional] 
**scent** | **str** | The scent variation of an item. | [optional] 
**size** | **str** | The size variation of an item. | [optional] 
**size_per_pearl** | **str** | The size per pearl variation of an item. | [optional] 
**golf_club_loft** | [**DecimalWithUnits**](DecimalWithUnits.md) |  | [optional] 
**total_diamond_weight** | [**DecimalWithUnits**](DecimalWithUnits.md) |  | [optional] 
**total_gem_weight** | [**DecimalWithUnits**](DecimalWithUnits.md) |  | [optional] 
**package_quantity** | **int** | The package quantity variation of an item. | [optional] 
**item_dimensions** | [**DimensionType**](DimensionType.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.catalogItemsV0.models.relationship_type import RelationshipType

# TODO update the JSON string below
json = "{}"
# create an instance of RelationshipType from a JSON string
relationship_type_instance = RelationshipType.from_json(json)
# print the JSON string representation of the object
print(RelationshipType.to_json())

# convert the object into a dict
relationship_type_dict = relationship_type_instance.to_dict()
# create an instance of RelationshipType from a dict
relationship_type_from_dict = RelationshipType.from_dict(relationship_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


