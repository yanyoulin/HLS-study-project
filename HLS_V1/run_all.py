import os
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = os.path.join("generated_code", timestamp)
os.makedirs(output_dir, exist_ok=True)

import shutil

STATIC_FILES = [
    "dense.cpp", "gelu.cpp", "relu.cpp",
    "dense.h", "gelu.h", "relu.h", "top.h", "test.cpp",
    "softmax.h", "softmax.cpp"
]

for f in STATIC_FILES:
    shutil.copy(f, os.path.join(output_dir, f))


print("Step 1: Train Keras model...")
os.system(f"python train_test.py {output_dir}")

print("Step 2: Extract weights and config from H5...")
os.system(f"python read_model.py {output_dir}")

print("Step 3: Generate top.cpp from config...")
os.system(f"python generate_top.py {output_dir}")

print("Step 4: Run Vitis HLS to synthesize...")
os.system(f"python generate_build_prj.py {output_dir}")
os.system(f'cd {output_dir} && vitis_hls -f build_prj.tcl')

print("All steps completed.")
