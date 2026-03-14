# Group 16 - Milestone 1 Progress Report

**Course:** EE 4310 - Power Systems Analysis  
**Milestone:** M1 (Parser + Y-bus + Small-System Validation)  
**Group:** 16

## 1. Objective

Milestone 1 required:
1. A working parser
2. Correct Y-bus construction
3. Validation using a small test system

## 2. What We Implemented

### 2.1 Working Parser

We implemented a MATPOWER-style plain-text parser that reads:
- `mpc.bus`
- `mpc.gen`
- `mpc.branch`

The parser converts these sections into typed internal models and performs structural checks (missing sections, malformed numeric rows, insufficient row columns).

### 2.2 Correct Y-bus Construction

We implemented Y-bus stamping with:
- branch series admittance (`1 / (r + jx)`)
- line charging susceptance (`b/2` at each end)
- off-nominal transformer tap ratio and angle handling
- bus shunt contribution (`Gs + jBs`, normalized by base MVA)

### 2.3 Validation Cases

We added:
- a 3-bus hand-checkable reference case
- a 2-bus case with both tap ratio and line charging
- an IEEE-14 sample input based on team data for parser/Y-bus scaling checks

## 3. How We Implemented It

We followed a simple modular flow:
1. Define data schemas (`src/models/`)
2. Parse input into typed objects (`src/parser/`)
3. Build Y-bus from parsed network model (`src/ybus/`)
4. Validate with scripted checks (`src/validation/`)
5. Add automated tests for both happy-path and failure-path behavior (`tests/`)

This kept logic clear, reduced duplication, and made each module easy to test.

## 4. Verification Results

- Automated test suite: **11 passed**
- Small-case validation script: **pass**
- Parser correctly reads IEEE-14 sample dimensions:
  - 14 buses
  - 5 generators
  - 20 branches

## 5. Key Deliverables Produced

- Parser module and tests
- Y-bus module and tests
- Validation script and report artifacts
- Sample datasets for IEEE-14 and small validation cases
- M1 checklist updated with evidence links

## 6. Outcome

Group 16 now has a functioning and validated M1 foundation that is ready for M2 (Gauss-Seidel implementation) with low rework risk.
