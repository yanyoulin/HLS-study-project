import re

# 讀取 config.h
config_path = 'config.h'
output_path = 'top.cpp'

layer_list = []

with open(config_path, 'r') as f:
    lines = f.readlines()
    num_layers = 0
    for line in lines:
        if '#define NUM_LAYERS' in line:
            num_layers = int(line.strip().split()[-1])
        elif '#define LAYER' in line and '_TYPE' in line:
            parts = line.strip().split()
            layer_type = parts[-1]
            layer_list.append({'type': layer_type})
        elif '#define LAYER' in line and '_NAME' in line:
            parts = line.strip().split()
            layer_name = parts[-1]
            idx = int(re.search(r'LAYER(\d+)_NAME', line).group(1))
            layer_list[idx]['name'] = layer_name

# 確認解析出來的結構
print(f"Parsed network ({num_layers} layers):")
for idx, layer in enumerate(layer_list):
    print(f"  Layer {idx}: {layer['type']} ({layer['name']})")

# --------------------------
# 生成 top.cpp 內容
with open(output_path, 'w') as f_out:
    f_out.write('#include "top.h"\n')
    f_out.write('#include "dense.h"\n')
    f_out.write('#include "gelu.h"\n')
    f_out.write('#include "relu.h"\n')
    f_out.write('#include "weights.h"\n\n')

    f_out.write('void mlp_inference(data_t input[DIM], data_t output[DIM]) {\n')
    f_out.write('#pragma HLS array_partition variable=input complete\n')
    f_out.write('#pragma HLS array_partition variable=output complete\n\n')

    f_out.write('    data_t buffer0[DIM];\n')
    f_out.write('    data_t buffer1[DIM];\n')
    f_out.write('    data_t *cur = input;\n')
    f_out.write('    data_t *tmp = nullptr;\n')
    f_out.write('    data_t *next = buffer0;\n\n')

    for idx, layer in enumerate(layer_list):
        if layer['type'] == 'Dense':
            f_out.write(f'    dense(cur, {layer["name"]}_kernel, {layer["name"]}_bias, next);\n')
        elif layer['type'] == 'Activation':
            activation_name = layer['name'].lower()
            if 'relu' in activation_name:
                f_out.write(f'    relu(cur, next);\n')
            elif 'gelu' in activation_name:
                f_out.write('    for (int i = 0; i < DIM; i++) {\n')
                f_out.write('#pragma HLS UNROLL\n')
                f_out.write('        next[i] = gelu(cur[i]);\n')
                f_out.write('    }\n')
            else:
                raise ValueError(f"Unknown activation: {activation_name}")
        else:
            raise ValueError(f"Unknown layer type: {layer['type']}")

        # swap buffer
        f_out.write('    tmp = cur;\n')
        f_out.write('    cur = next;\n')
        f_out.write('    next = tmp;\n\n')

    # 最後輸出
    f_out.write('    for (int i = 0; i < DIM; i++) {\n')
    f_out.write('#pragma HLS UNROLL\n')
    f_out.write('        output[i] = cur[i];\n')
    f_out.write('    }\n')

    f_out.write('}\n')

print(f"Successfully generated {output_path}")
