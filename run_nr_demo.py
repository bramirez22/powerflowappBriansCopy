from src.parser.matpower_parser import parse_matpower_case
from src.powerflow.nr.newton_raphson import solve_newton_raphson
import numpy as np

case = parse_matpower_case(r"data\raw\ieee14\case14_sample.m")

result = solve_newton_raphson(case, tolerance=1e-6, max_iterations=20)

print("Converged:", result.converged)
print("Iterations:", result.iterations)
print("\nBus Voltages:\n")

for i, v in enumerate(result.voltages, start=1):
    print(
        f"Bus {i}: |V|={abs(v):.6f}, angle={np.degrees(np.angle(v)):.6f} deg"
    )