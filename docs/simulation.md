# Simulation (Isaac Sim)

## Notes
Isaac Sim usually ships with its own Python environment and packages.
Because of that, this repo **does not** attempt to `pip install isaacsim`.

## How to run
1. Open Isaac Sim.
2. Ensure your robot USD is available on disk.
3. Update the USD path in the script or set an environment variable (recommended).

### Recommended approach: environment variable
Set `SPIDER_USD_PATH` to your USD file and let the script read it.

Example (Windows PowerShell):
```powershell
$env:SPIDER_USD_PATH = "C:\path\to\robot.usd"
```

Then run the script in Isaac Sim's Python environment.

## Common issues
- Joint names do not match: update the mapping dictionary in the script
- Robot collapses: increase joint stiffness/damping (PD gains) or fix mass/inertia
- Motion too fast: increase interpolation steps or frame duration
