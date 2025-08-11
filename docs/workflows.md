# Workflows

There is another option in the QSAR Toolbox called `workflows`. Here's how we can get a list of the available ones:

```python
workflows = qs.get_workflows()
print(workflows)
```

The following workflows are available for my QSAR Toolbox (v 4.8) installation:

```
[{'Caption': 'Skin sensitisation from GPMT assay',
  'Guid': '36d8cd9a-bf22-4d8f-8690-468affb13a39',
  'Endpoint': 'S M W N <OR> Skin sensitisation',
  'RigidPath': 'Human Health Hazards#Sensitisation'},
 {'Caption': 'Fish, LC50(EC50) at 96h for Pimephales promelas (mortality)',
  'Guid': 'ba31e827-bf06-4a27-81ae-56aaa763ce36',
  'Endpoint': 'EC50 <OR> LC50',
  'RigidPath': 'Ecotoxicological Information#Aquatic Toxicity'},
 {'Caption': 'Demo workflow',
  'Guid': '33b163fd-7e42-47f8-b52c-59d911785aa8',
  'Endpoint': None,
  'RigidPath': None},
 {'Caption': 'tb_sys_default_functions',
  'Guid': '8225142f-5c56-4fd5-918e-70a181f0dffb',
  'Endpoint': None,
  'RigidPath': None},
 {'Caption': 'EC3 from LLNA or Skin sensitisation from GPMT assays',
  'Guid': '2a26b617-d8e8-4a32-9dd6-06e983ae44be',
  'Endpoint': 'EC3 <OR> S M W N <OR> Skin sensitisation',
  'RigidPath': 'Human Health Hazards#Sensitisation'},
 {'Caption': 'EC3 from LLNA assay',
  'Guid': '14fe5e12-fec8-4ac1-ba53-1dd9874fe031',
  'Endpoint': 'EC3',
  'RigidPath': 'Human Health Hazards#Sensitisation'},
 {'Caption': 'EC3 from LLNA or Skin sensitization from GPMT assays for defined approaches (SS AW for DASS)',
  'Guid': '0c5bc24e-da70-46d5-9165-adbe21dc5935',
  'Endpoint': 'EC3 <OR> S M W N <OR> Skin sensitisation',
  'RigidPath': 'Human Health Hazards#Sensitisation'}]
```

It is possible to call the above workflows on a chemical using the method `workflow_on_chemical`. For instance, the following code runs workflow for Skin sensitisation from GPMT assay for chemical formaldehyde.

```python
chem = qs.search_CAS("50-00-0")
chem_id = chem[0]["ChemId"]
print(f"Running workflow {workflows[0]['Caption']} for chemical {chem[0]["Names"][0]}")
res = qs.workflow_on_chemical(workflow_guid=workflows[0]["Guid"], chem_id=chem_id)
print(res)
```

{'Result': 'Positive from " Subcategorized: Protein binding alerts for skin sensitization by OASIS " for C=O',
 'Prediction': {'DomainResult': None,
  'DomainExplain': None,
  'DataType': 'Read-across prediction.',
  'RigidPath': 'Human Health Hazards#Sensitisation',
  'Endpoint': 'S M W N <OR> Skin sensitisation',
  'MetaData': None,
  'Value': 'Positive',
  'Qualifier': None,
  'MinValue': None,
  'MinQualifier': None,
  'MaxValue': None,
  'MaxQualifier': None,
  'Unit': None,
  'Family': None}}

  ## Next step
  Have a look at [the API](api.md) and give it a shot!