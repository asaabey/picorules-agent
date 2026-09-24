# Picorules Projections Infographic Brief

## Working title
**From Raw EADV Data to Reusable Clinical Projections**

## Core message
When a Picorules rule runs, it does not just return a single answer.

It transforms raw **EADV** clinical data into a new structured **object** that can be reused across multiple downstream use cases.

At TKC, these reusable outputs are referred to as **projections**.

## One-sentence version
**Picorules turns raw EADV data into reusable clinical projections.**

## Suggested infographic narrative

### 1. Input layer
**Raw EADV data**

- `eid` - patient identifier
- `att` - clinical attribute
- `dt` - date
- `val` - value

This data is highly flexible, but not yet shaped for a specific product or workflow outcome.

### 2. Transformation layer
**Picorules execution**

Picorules applies deterministic clinical logic to the raw EADV stream and produces a structured output object.

This object is:

- clinically meaningful
- deterministic
- testable
- reusable

### 3. Output layer
**Projection object**

The output can be thought of as a projection of the raw data into a form that is useful for a particular clinical or technical purpose.

Examples of projections include:

- a **phenotype object**
- a **recommendation object**
- a **risk object**
- a **disease-state summary**

### 4. Downstream use cases
The same projection can then be used in different ways:

- render a phenotype or summary as an **HTML object** for UI display
- convert the projection into **FHIR**
- map it into another **medical modeling language construct**
- feed other downstream applications, reporting pipelines, or decision-support services

## Slide copy option

### Header
**Picorules creates reusable clinical objects**

### Body
Raw EADV data is not usually in the right shape for direct product use.

Picorules transforms that raw data into structured projection objects that represent clinically meaningful states, phenotypes, risks, or recommendations.

Those projections can then be rendered in HTML, converted to FHIR, or mapped into other clinical interoperability models.

### Footer / takeaway
**One deterministic rules layer, many downstream representations.**

## Simple visual layout

Use a 4-step horizontal flow:

**Raw EADV data -> Picorules logic -> Projection object -> Multiple outputs**

Suggested labels under each step:

1. **Raw EADV data**
   clinical facts in `eid / att / dt / val`

2. **Picorules logic**
   deterministic transformation

3. **Projection object**
   phenotype / risk / recommendation / summary

4. **Outputs**
   HTML, FHIR, other medical models

## Comparison line
Instead of binding each use case directly to raw data, Picorules creates an intermediate clinical object that can be reused across many representations.

## Keywords
Picorules, projections, phenotype, EADV, FHIR, interoperability, deterministic clinical logic, structured clinical object
