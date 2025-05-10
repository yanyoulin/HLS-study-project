import os

print("Step 1: Train Keras model...")
os.system("python train_test.py")

print("Step 2: Extract weights and config from H5...")
os.system("python read_model.py")

print("Step 3: Generate top.cpp from config...")
os.system("python generate_top.py")

print("Step 4: Run Vitis HLS to synthesize...")
os.system("vitis_hls -f build_prj.tcl")

# print("Step 5: Vivado implementation...")
# os.system("vivado -mode batch -source vivado_synth.tcl")

print("All steps completed.")
