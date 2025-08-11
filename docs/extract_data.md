# Data
It is possible to look for the experimental data shipped with the `QSAR Toolbox`. To retrieve data, you need to provide `ChemId` and the end point position from the enpoints tree. The entire end points tree can be obtained by the method `get_endpoints_tree`. It returns a `list` of the available end points:

```python
endpoints_tree = qs.get_endpoints_tree()
```

The above command must produce the following list (perhaps with minor difference depending on your QSAR Toolbox installation):

<details>
<summary>Click to expand the endpoints tree list</summary>

```python
['Physical Chemical Properties',
 'Environmental Fate and Transport',
 'Ecotoxicological Information',
 'Intermediate effects - mechanistic information',
 'Observed metabolism',
 'Human Health Hazards',
 'Physical Chemical Properties#Autoflammability / Self-ignition temperature',
 'Physical Chemical Properties#Vapour pressure',
 'Physical Chemical Properties#Boiling point',
 'Physical Chemical Properties#Viscosity',
 'Physical Chemical Properties#Oxidation reduction potential',
 'Physical Chemical Properties#Self-reactive substances',
 'Physical Chemical Properties#Surface tension',
 'Physical Chemical Properties#Gases under pressure',
 'Physical Chemical Properties#pH',
 'Physical Chemical Properties#Particle size',
 'Physical Chemical Properties#Flash point',
 'Physical Chemical Properties#Density',
 'Physical Chemical Properties#Solubility in organic solvents / fat solubility',
 'Physical Chemical Properties#Water solubility',
 'Physical Chemical Properties#Oxidising properties',
 'Physical Chemical Properties#Explosive properties',
 'Physical Chemical Properties#Chemical reactivity',
 'Physical Chemical Properties#Stability in organic solvents and identity of relevant degradation products',
 'Physical Chemical Properties#Melting / freezing point',
 'Physical Chemical Properties#Dissociation Constant (pKa)',
 'Physical Chemical Properties#Corrosivity to metals',
 'Physical Chemical Properties#Flammability',
 'Physical Chemical Properties#Partition Coefficient:',
 'Physical Chemical Properties#Partition Coefficient:#Gas/Atmospheric particulates',
 'Physical Chemical Properties#Partition Coefficient:#N-Octanol/Air',
 'Physical Chemical Properties#Partition Coefficient:#N-Octanol/Water',
 'Environmental Fate and Transport#Stability',
 'Environmental Fate and Transport#Transport and Distribution',
 'Environmental Fate and Transport#Biodegradation',
 'Environmental Fate and Transport#Bioaccumulation',
 'Environmental Fate and Transport#Stability#Hydrolysis',
 'Environmental Fate and Transport#Stability#Photodegradation',
 'Environmental Fate and Transport#Stability#Photodegradation#in air',
 'Environmental Fate and Transport#Stability#Photodegradation#in soil',
 'Environmental Fate and Transport#Stability#Photodegradation#in water',
 'Environmental Fate and Transport#Transport and Distribution#Adsorption/desorption',
 'Environmental Fate and Transport#Transport and Distribution#Monitoring data',
 'Environmental Fate and Transport#Transport and Distribution#Distribution modelling',
 "Environmental Fate and Transport#Transport and Distribution#Henry's Law constant (H)",
 'Environmental Fate and Transport#Transport and Distribution#Water Volatilization Half-lives',
 'Environmental Fate and Transport#Biodegradation#in water and sediment: simulation tests',
 'Environmental Fate and Transport#Biodegradation#in Sewage Treatment Plant',
 'Environmental Fate and Transport#Biodegradation#in water: screening tests',
 'Environmental Fate and Transport#Biodegradation#in soil',
 'Environmental Fate and Transport#Bioaccumulation#aquatic / sediment',
 'Environmental Fate and Transport#Bioaccumulation#terrestrial',
 'Ecotoxicological Information#Sediment Toxicity',
 'Ecotoxicological Information#Aquatic Toxicity',
 'Ecotoxicological Information#Terrestrial Toxicity',
 'Human Health Hazards#Genetic Toxicity',
 'Human Health Hazards#Repeated Dose Toxicity',
 'Human Health Hazards#Toxicokinetics, Metabolism and Distribution',
 'Human Health Hazards#Developmental Toxicity / Teratogenicity',
 'Human Health Hazards#Toxicity to Reproduction',
 'Human Health Hazards#Neurotoxicity',
 'Human Health Hazards#Specific investigations',
 'Human Health Hazards#Sensitisation',
 'Human Health Hazards#Immunotoxicity',
 'Human Health Hazards#Irritation / Corrosion',
 'Human Health Hazards#Photoinduced toxicity',
 'Human Health Hazards#ToxCast',
 'Human Health Hazards#Carcinogenicity',
 'Human Health Hazards#Acute Toxicity',
 'Human Health Hazards#Toxicokinetics, Metabolism and Distribution#Dermal absorption',
 'Human Health Hazards#Toxicokinetics, Metabolism and Distribution#Basic toxicokinetics',
 'Human Health Hazards#Specific investigations#Endocrine disrupter',
 'Human Health Hazards#Specific investigations#other studies']
```
</details>

You then need to look for the desired end point in the tree using the right keyword. For instance, we look for "henry" to find the position of the Henry's law constant in the end points tree. We then need to call another function to find all the available end points for the obtained position:

```python
henry_position = [e for e in endpoints_tree if "henry" in e.lower()]
if len(henry_position) > 0:
    henry_position = henry_position[0]
print(f"Henry position: {henry_position}")
available_henry_endpoints = qs.get_endpoints_from_tree(henry_position)
if len(available_henry_endpoints) > 0:
    available_henry_endpoints = available_henry_endpoints[1]
print(f"Available endpoints: {available_henry_endpoints}")
```

It is now possible to look for this end point for a specific chemical ID. I repeat the procedure for CAS RN "50-00-0" (formaldehyde):

```python
casrn = "50-00-0"  # formaldehyde
res_chem_cas = qs.search_CAS(casrn)
HLC_value = qs.get_endpoint_data(
    chem_id=res_chem_cas[0]["ChemId"],
    position=henry_position,
    endpoint=available_henry_endpoints,
)
print(f"Henry's law constant experimental value is {(HLC_value[0]['Value'])} {(HLC_value[0]['Unit'])}")
```

There are other ways of looking at the endpoints tree. For instance, one useful way is to get all the endpoints for `Environmental Fate and Transport#Transport and Distribution`. This give all the endpoints available in the databases for the given category:

```python
all_endpoint_transport = qs.get_endpoints_from_tree(
    "Environmental Fate and Transport#Transport and Distribution"
)
print(f"Available endpoints: {all_endpoint_transport}")
```

And finally, the user can find from which database an end point is extracted. For example, for the Henry's law constant, we can find the name of the database by calling the following method:

```python
pKa_positions = [
    e for e in endpoints_tree if "pka" in e.lower() or "pka" in e.lower()
]
pKa_position = pKa_positions[0] 
available_pKa_endpoints = qs.get_endpoints_from_tree(pKa_position)
for endpoint in available_pKa_endpoints:
    pKa_database = qs.get_databases_for_endpoint(
        position=pKa_position, endpoint=endpoint
    )
    print(f"Available databases for {endpoint}: {pKa_database}")
```

## Next step
When there is no experimental data, you can [call a QSAR model](run_qsar.md) to estimate the desired parameter values.