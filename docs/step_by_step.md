# Step by step guide

This page shows an example of the usage of `PyQSARToolbox` based on one of the author's projects.

## Problem statement

We have a list of compounds identified by their `CAS RN` and `SMILES`. We want to call all the available QSAR models for vapor pressure and also extract the available experimental data. 

### Step 1: extract `ChemId`

First, we look for the `ChemId` for all the compounds, first by searching with `CAS RN`, followed by `SMILES` and potentially `names`.

```python
# water solubility of 50-03-3
chem_by_cas = qs.search_CAS("50-03-3")
chem_id = chem_by_cas[0]["ChemId"]
```

### Step 2: find the location of endpoint

We get the `endpoint tree` and look for the desired endpoint in it. The goal is to extract the positions in the tree that seem to be relevant to our desired endpoint properties.
  > WARNING: you can find irrelevant values too, depending on the keywords used to search for the endpoints.

```python
endpoints_tree = qs.get_endpoints_tree()
water_solubility_position = [
    e for e in endpoints_tree if "water solubility" in e.lower()
][0]
```

### Step 3: extracting data

After finding the position of the desired endpoint in the tree, we use it to find the available data and models for it. First, we have to get the available endpoint for the selected position in the endpoints tree by calling the method `get_endpoints_from_tree`:

```python
available_water_solubility_endpoints = qs.get_endpoints_from_tree(
    water_solubility_position
)
print("Available endpoints:")
for endpoint in available_water_solubility_endpoints:
    print("  - " + endpoint)
```

As you can see, the first entry does not match what we are looking for (which is the solubility of organic compounds). Therefore, we will only use the last two elements (note the small and capital `W` in water. It becomes important because each one refers to a different dataset!) Here's how we can search for data using the method `get_endpoint_data`:

```python
water_solubility_values = [
    qs.get_endpoint_data(
        chem_id=chem_id,
        position=water_solubility_position,
        endpoint=available_water_solubility_endpoints[i],
    )
    for i in [1, 2]
]
# print each end point dict in the list
for i in range(len(water_solubility_values)):
    print(json.dumps(water_solubility_values[i], indent=2))
```

### Step 4: running QSAR models

The above results are identical for both `water solubility` entries with small and capital `W`. Now, we can find the `QSAR` models for the same endpoints. It is done by calling the method `get_qsar_models`:

```python
# run QSAR model for water solubility
ws_qsar_models = qs.get_qsar_models(position=water_solubility_position)
print(f"Available QSAR models:")
for model in ws_qsar_models:
    print(json.dumps(model, indent=2))
```

We can see that four models are available for predicting water solubility: two models from EPI Suite, and one model each for VEGA and OPERA. We can run the models now:

```python
# run the models and time each one
import time

results = []
ws_QSAR_list = []
for model in ws_qsar_models:
    start = time.time()
    res = qs.apply_qsar_chemical(chem_id, qsar_model_guid=model["Guid"])
    results.append(res)
    end = time.time()
    ws_QSAR = {}
    res = qs.apply_qsar_chemical(chem_id, qsar_model_guid=model["Guid"])
    ws_QSAR[model["Caption"]] = res["Value"]
    ws_QSAR["Unit"] = res["Unit"]
    ws_QSAR_list.append(ws_QSAR)
    print(f"Time elapsed for {model['Caption']}: {end-start:.2f} seconds")
```

On my system, I obtained the following run times (note the longer runtime of OPERA):  

```
Time elapsed for Water Solubility (EPISUITE): 0.06 seconds
Time elapsed for VEGA - Water solubility model (IRFMN): 7.29 seconds
Time elapsed for Water Solubility (fragments) (EPISUITE): 0.03 seconds
Time elapsed for OPERA WS: 28.05 seconds
```

You can also dump the results as `JSON` for a higher readability:

```python
# print the results
for r in results:
    print(json.dumps(r, indent=2))
```

### Step 4 (alternative): using calculators

Another way of calling `QSAR` model in QSAR Toolbox is using `calculators`. First, we need to get the list of the available calculators:

```python
calculators_list = qs.get_available_calculators()
calculators_list
```

There are too many of these calculators. We can look for the right one by looking into the 'Caption' or 'Description' of each element. For instance, we can look for 'water solubility':

```python
WS_calculators = []
for c in calculators_list:
    if "water solubility" in c["Caption"].lower():
        WS_calculators.append(c)
print(WS_calculators)
```

Note that these calculators are only available for the "native" QSAR Toolbox methods and data. The addons (e.g. VEGA and OPERA) are either not part of the calculators or possibly I could not find them. Now, we can call the calculators using the method `run_calculator` for a specified chemical.

```python
WS_values = []
for c in WS_calculators:
    res = qs.run_calculator(calculation_guid=c["Guid"], chem_id=chem_id)
    WS_values.append(res)
print(WS_values)
```

The advantage of using `calculators` over the alternative methods is that it is simpler to set up and also faster computationally (based on my limited tests).

## Next step
Have a look at the [QSAR Toolbox `workflows`](workflows.md).