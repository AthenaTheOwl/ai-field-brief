# Prompt Matrix UI Spec

## Screens

### Matrix Runs
Shows each batch run, profile, lookback window, source count, lens count, cost, status, and failures.

### Matrix View
A table where:

- rows are source items
- columns are prompt lenses
- cells show answer preview, source chips, extraction mode, confidence, and faithfulness state

### Cell Detail
Shows:

- source item metadata
- lens prompt version
- cell output
- source refs
- faithfulness report
- patch history
- action candidates produced from the cell

### Prompt Lens Library
Reusable prompt cards tagged by category, source type, and profile.

### Synthesis View
Lets the editor build the weekly brief from verified cells and trace every claim back to cells.

## Cell badges

- `extractive`
- `interpretive`
- `synthetic`
- `critique`
- `faithfulness: passed / patch / failed`
- `confidence: high / medium / low`

## Batch actions

- Run selected lenses
- Rerun failed cells
- Verify cells
- Promote cell to action candidate
- Cluster rows into theme
- Export evidence bundle
