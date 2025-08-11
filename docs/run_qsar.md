# QSAR models
We can call the available QSAR models for a chemical and an end point position selected from the end point tree. Here's how we can get a list of the available QSAR models for estimating the Henry's law constant, and then call the models for [a given chemID](search_chemicals.md):

```python
henry_qsar_models = qs.get_qsar_models(position=henry_position)
print(f"Available QSAR models: {henry_qsar_models}")

HLC_QSAR_list = []
for model in henry_qsar_models:
    HLC_QSAR = {}
    res = qs.apply_qsar_chemical(
        res_chem_cas[0]["ChemId"], qsar_model_guid=model["Guid"]
    )
    HLC_QSAR[model["Caption"]] = res["Value"]
    HLC_QSAR["Unit"] = res["Unit"]
    HLC_QSAR_list.append(HLC_QSAR)
print(HLC_QSAR_list)
```

The above values are estimated with the available QSAR methods for the Henry's law constant in the QSAR Toolbox. However, there is another way to do it, which is using `calculators`.  
   * __Note__: the OPERA interface takes longer to run (probably for converting SMILES to structure), between 2-5 minutes. Therefore, I suggest not running it from this interface and running it directly from `OPERA CLI`. We will release a Python package for doing it automatically.

```python
calculators_list = qs.get_available_calculators()
henry_calculators = []
henry_calculator_values = []
for c in calculators_list:
    if "henry" in c["Caption"].lower():
        h = {}
        h["Caption"] = c["Caption"]
        res = qs.run_calculator(
            calculation_guid=c["Guid"], chem_id=res_chem_cas[0]["ChemId"]
        )
        h["Value"] = res["Value"]
        h["Unit"] = res["Unit"]
        henry_calculator_values.append(h)
        henry_calculators.append(c)
print(henry_calculator_values)
```

Although not systematically tested, the `calculators` seem to run faster than models, and therefore can be recommended for longer list of chemicals.

## Next step
An [step by step guide](step_by_step.md) for obtaining experimental data and QSAR model results from QSAR Toolbox via Python.

