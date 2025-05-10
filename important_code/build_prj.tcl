# 建立工程
open_project my_mlp_project
set_top mlp_inference

# 加入原始碼與標頭檔
add_files top.cpp
add_files dense.cpp
add_files gelu.cpp
add_files relu.cpp

add_files weights.h
add_files config.h
add_files common.h
add_files dense.h
add_files gelu.h
add_files relu.h
add_files top.h

add_files -tb test.cpp

# 設定 solution 與裝置（可根據 FPGA 修改）
open_solution "solution1"
set_part {xczu7ev-ffvc1156-2-e} ;# ← 這是 ZCU102 可用裝置，依需要修改
create_clock -period 10 -name default ;# 200MHz 時脈

# 執行流程
csim_design
csynth_design
cosim_design

export_design -format ip_catalog -output ./solution1/export

exit
