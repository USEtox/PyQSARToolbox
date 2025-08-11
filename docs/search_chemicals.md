# Search for chemicals

Search can be conducted by CAS, name, SMILES, or ChemID. The ChemID is a long string of the following format `323eca7f-fe36-6959-a6fd-1ae6839278b0`; therefore, it is highly unlikely that someone uses this function. Other identifiers, however, can be used as shown in the following examples.

## Search by name

The name can be specifed as a string and three options of "ExactMatch" (default), "StartWith", and "Contains" are available. It is possible to find multiple chemicals for a specified name; the results are returned as a `list` of `Dict`, with each item referring to a single chemical with a unique `ChemId`.

```python
chem_name = "caffeine"
options = ["ExactMatch", "StartWith", "Contains"]
for option in options:
    res_chem_name = qs.search_name(chem_name, options=option)
    print(f"Found {len(res_chem_name)} chemicals for {option} option")
res_chem_name = qs.search_name(chem_name, options="ExactMatch")
cas_number = [chem["Cas"] for chem in res_chem_name]
```

As you can see, the exact match for `caffeine` found fewer results, but more chemicals are found for compund names that starts with or contains the word caffeine.

## Search by CAS and SMILES

The cas number must be an integer without the customary dash, e.g. 50000 instead of "50-00-0" that is the CAS number of formaldehyde. The wrapper function, however, accepts both values.

```python
casrn = "50-00-0"  # formaldehyde
res_chem_cas = qs.search_CAS(casrn)
print(f"Found {len(res_chem_cas)} chemicals for CAS number {casrn}")
print(
    f"The chemical is called {res_chem_cas[0]['Names'][0]}, with SMILES {res_chem_cas[0]['Smiles']}, and ChemId {res_chem_cas[0]['ChemId']}"
)
```

We can also search for the same chemical using SMILES:

```python
smiles = "C=O"  # formaldehyde
res_chem_smiles = qs.search_smiles(smiles)
print(f"Found {len(res_chem_smiles)} chemicals for SMILES {smiles}")
```

Searching by the `CAS RN` gives a unique answer (note that a CAS RN refers to a unique chemical, but it does not mean that a chemical is identified by a single CASRN. Multiple CAS RN can refer to the same chemical). Searching by `SMILES` can find more than a single chemical, as you can see in the above call with `C=O` that is the `SMILES` string for formaldehyde.

## Next Step

How to [extract experimental data](extract_data.md) for a chemical.