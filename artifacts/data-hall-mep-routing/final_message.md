Implemented the deliverables:

- [solution.py](/app/files/dc_model__hall_seed000_d000__mep_routing/output/solution.py)  
  Self-contained IFC4 generator with:
  - 128 racks, six structural columns, four CRAHs, six PDUs, containment, access floor, and 63 sprinkler heads.
  - Connected tray, busway, and CHW networks with separate service tiers.
  - CHW perimeter branches to all CRAHs.
  - DCM property sets, service diagnostics, supports/hangers, and baked drawing-derived dimensions.

- [model.ifc](/app/files/dc_model__hall_seed000_d000__mep_routing/output/model.ifc)  
  Generated IFC4 model containing 8,189 entities:
  - 128 `IfcFurniture` racks
  - 28 `IfcPipeSegment` CHW elements
  - 44 `IfcCableCarrierSegment` tray/busway elements
  - 63 sprinkler heads
  - 6 columns, 4 CRAHs, 6 PDUs, and 33 supports

- [reconciliation.json](/app/files/dc_model__hall_seed000_d000__mep_routing/output/reconciliation.json)  
  Records the applied hall dimensions, equipment sizes, clearances, insulation, and route elevations.

Verification completed: the IFC reopens successfully and passes `ifcopenshell` validation with `express_rules=True` and zero reported errors.