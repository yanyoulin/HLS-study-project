import h5py
import numpy as np
import os
import sys

output_dir = sys.argv[1] if len(sys.argv) > 1 else "generated_code/default_output"

weights_dict = {}
network_structure = []  # 這個新加，用來記錄每一層是什麼層 (Dense/Activation)
visited_layers = set()

def recursively_extract(name, obj):
    if isinstance(obj, h5py.Dataset):
        if 'kernel' in name or 'bias' in name:
            print(f"Found dataset: {name}, shape={obj.shape}")

            # 取出 layer 名稱
            parts = name.split('/')
            if len(parts) >= 4:
                layer_group = parts[3]  # 比如 'dense1', 'dense2'
                weight_name = parts[4]  # 'kernel' 或 'bias'

                key = f"{layer_group}_{weight_name}"
                weights_dict[key] = obj[()]
            else:
                print(f"Warning: Unrecognized structure at {name}")

    elif isinstance(obj, h5py.Group):
        layer_name = name.split('/')[-1]
        if layer_name not in visited_layers:
            visited_layers.add(layer_name)
            if layer_name.startswith('dense'):
                network_structure.append(('Dense', layer_name))
            elif 'activation' in layer_name or 'gelu' in layer_name or 'relu' in layer_name:
                network_structure.append(('Activation', layer_name))

# 開啟 h5 檔案
h5_path = os.path.join(output_dir, 'model.h5')

with h5py.File(h5_path, 'r') as f:
    f.visititems(recursively_extract)

# -------------------------------------------
# 印出確認
print("\nExtracted weights:")
for name, array in weights_dict.items():
    print(f"{name}: shape={array.shape}")

print("\nExtracted network structure:")
for idx, (layer_type, layer_name) in enumerate(network_structure):
    print(f"Layer {idx}: {layer_type} ({layer_name})")

# -------------------------------------------
# 寫出 weights.h
def array_to_c_array(name, arr):
    if arr.ndim == 2:
        out = f"const data_t {name}[{arr.shape[0]}][{arr.shape[1]}] = {{\n"
        for row in arr:
            row_str = ", ".join([f"data_t({x:.8f})" for x in row])
            out += "    {" + row_str + "},\n"
        out += "};\n\n"
    elif arr.ndim == 1:
        out = f"const data_t {name}[{arr.shape[0]}] = {{\n    "
        row_str = ", ".join([f"data_t({x:.8f})" for x in arr])
        out += row_str + "\n};\n\n"
    return out

# 儲存 weights.h
with open(os.path.join(output_dir, 'weights.h'), 'w') as f_out:
    f_out.write("#ifndef WEIGHTS_H\n")
    f_out.write("#define WEIGHTS_H\n\n")
    f_out.write('#include "common.h"\n\n')

    for key, array in weights_dict.items():
        f_out.write(array_to_c_array(key, array))

    f_out.write("#endif\n")

print("Saved weights.h")

# -------------------------------------------
# 寫出 config.h
with open(os.path.join(output_dir, 'config.h'), 'w') as f_out:
    f_out.write("#ifndef CONFIG_H\n")
    f_out.write("#define CONFIG_H\n\n")

    f_out.write(f"#define NUM_LAYERS {len(network_structure)}\n\n")

    for idx, (layer_type, layer_name) in enumerate(network_structure):
        if layer_type == 'Dense':
            f_out.write(f"#define LAYER{idx}_TYPE Dense\n")
            f_out.write(f"#define LAYER{idx}_NAME {layer_name}\n\n")
        elif layer_type == 'Activation':
            f_out.write(f"#define LAYER{idx}_TYPE Activation\n")
            f_out.write(f"#define LAYER{idx}_NAME {layer_name}\n\n")

    f_out.write("#endif\n")

print("Saved config.h")
