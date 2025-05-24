import sys
import os

output_dir = sys.argv[1] if len(sys.argv) > 1 else "generated_code/default"
project_root = os.getcwd()

tcl_lines = []
tcl_lines.append("open_project my_mlp_project")
tcl_lines.append("set_top mlp_inference\n")

static_files = [
    "dense.cpp", "gelu.cpp", "relu.cpp",
    "dense.h", "gelu.h", "relu.h", "top.h",
    "softmax.h", "softmax.cpp"
]
for f in static_files:
    tcl_lines.append(f'add_files "{f}"')

generated_files = ["top.cpp", "weights.h", "config.h", "common.h"]
for f in generated_files:
    tcl_lines.append(f'add_files "{f}"')
tcl_lines.append(f'add_files -tb "test.cpp"')

tcl_lines.append('open_solution "solution1"')
tcl_lines.append('set_part {xczu7ev-ffvc1156-2-e}')
tcl_lines.append('create_clock -period 10 -name default\n')
tcl_lines += [
    "csim_design",
    "csynth_design",
    "cosim_design",
    'export_design -format ip_catalog -output ./solution1/export',
    "exit"
]

with open(os.path.join(output_dir, "build_prj.tcl"), "w") as f:
    f.write("\n".join(tcl_lines))
