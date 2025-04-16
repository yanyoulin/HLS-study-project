# HLS-study-project
```
Vitis HLS 2024.2
part=xcku035-fbva676-2-e
```
## 什麼是HLS
將高階語言的演算法轉換為RTL代碼，進一步用於FPGA的硬體實現

## HLS pragma
pragma是用來向Vitis HLS提供指令的關鍵字，幫助優化硬體設計並控制生成的RTL代碼的行為。這些指令可以用來進行性能調整、資源分配以及設計流程的優化<br>
以下是我目前研究及使用過的pragma(Vitis HLS官網也有詳細說明):
### pragma HLS pipeline
```cpp
void sum_array(int in[8], int* out) {
#pragma HLS PIPELINE
    int total = 0;
    for (int i = 0; i < 8; i++) {
        total += in[i];
    }
    *out = total;
}
```
將loop或是function以pipeline的形式結構執行，增加效率<br>
![image](https://github.com/yanyoulin/HLS-study-project/blob/main/pics/%E8%9E%A2%E5%B9%95%E6%93%B7%E5%8F%96%E7%95%AB%E9%9D%A2%202025-04-14%20020312.png) <br>
pipeline讓多個操作分工並行執行，將一段運算「拆解成多個階段」，讓每個clock cycle都能輸入新的資料、產出新的結果<br>
可以自行設定Initiation Interval(II):啟動新一次迭代所需的clock cycle，若II=1則效率最高<br>
### pragma HLS unroll
```cpp
void sum_array_unroll(int in[8], int* out) {
    int total = 0;
    for (int i = 0; i < 8; i++) {
        #pragma HLS UNROLL
        total += in[i];
    }
    *out = total;
}
```
不同於pipeline，unroll將迴圈展開成多組平行運算單元。展開後，迴圈中每次迭代的操作會「同時」在硬體中執行，而不是像軟體那樣一個一個執行。<br>
附上示意圖-擷取自網路<br>
![image](https://github.com/yanyoulin/HLS-study-project/blob/main/pics/c49290601b3fa1a6f86eb66e5252b95a.png) <br>
可以發現，unroll通常效率會高於pipeline(latency較低)，同時也會消耗更多資源<br>
### pragma HLS array_partition
array_partition是一個對陣列資料做結構性分割的指令，用來將一個大陣列分割成多個小部分，讓它們可以在硬體中同時被存取<br>
在硬體中，一個array預設只有一個port，同一時刻只能做一筆讀/寫。所有資料從同一記憶體來，就會造成爭用，讓 HLS 無法並行處理<br>
解法：把array拆成多個memory slice，每slice各有port<br>
```
#pragma HLS array_partition variable=<array_name> type=<partition_type> dim=<dimension>
```
type=complete(完全獨立)/block(分塊獨立)->需與factor搭配<br>
dim->要分的是哪個維度<br>
```cpp
void sum_array_unroll(int in[8], int* out) {
#pragma HLS array_partition variable=in complete
    int total = 0;
    for (int i = 0; i < 8; i++) {
        #pragma HLS UNROLL
        total += in[i];
    }
    *out = total;
}
```
unroll常與array_partition做使用，因為unroll只是「告訴工具我想要展開」，但是否真的能展開，要看資料能不能同時被取用<br>
### pragma HLS DATAFLOW
它能讓多個function、loop在硬體中同時執行，就像是多個pipeline串起來一樣<br>
經典用法:<br>
```cpp
#pragma HLS DATAFLOW

read_input(input_stream, buf);
compute(buf, result);
write_output(result, output_stream);
```
```cpp
void dense_model(int W1[HIDDEN_DIM][IN_DIM], int W2[OUT_DIM][HIDDEN_DIM],
                 int b1[HIDDEN_DIM], int b2[OUT_DIM], int x[IN_DIM], int y[OUT_DIM]) {
#pragma HLS DATAFLOW
    int h[HIDDEN_DIM];
#pragma HLS array_partition variable=h complete

    dense1(W1, x, b1, h);
    dense2(W2, h, b2, y);
}
```
![image](https://github.com/yanyoulin/HLS-study-project/blob/main/pics/dataflow.png) <br>

## 進入Vitis
1. 建立一個專案環境，存放你未來建立的component<br>
![image](https://github.com/yanyoulin/HLS-study-project/blob/main/pics/setworkspace.png) <br>
2. 可以建立component了<br>
![image](https://github.com/yanyoulin/HLS-study-project/blob/main/pics/newcomponent.png) <br>
![image](https://github.com/yanyoulin/HLS-study-project/blob/main/pics/namelocation.png) <br>
3. 放入你要轉換的cpp檔，以及自己寫的testbench(也可以選擇先跳過)<br>
![image](https://github.com/yanyoulin/HLS-study-project/blob/main/pics/createcomponentsourcefile.png) <br>
4. 設定板子環境<br>
![image](https://github.com/yanyoulin/HLS-study-project/blob/main/pics/selectboard.png) <br>
5. 這樣就建立完成了<br>
若跳過第3步，可以在建立完成後再處理(我自己是這樣做)<br>
![image](https://github.com/yanyoulin/HLS-study-project/blob/main/pics/newsoucefile.png) <br>
記得設定top function(HLS轉換的單位)<br>
![image](https://github.com/yanyoulin/HLS-study-project/blob/main/pics/topfunction.png) <br>

## 如何進行-以sum_array為例
```cpp
#include "ap_int.h"

void sum_array_unroll(int in[8], int* out) {
#pragma HLS array_partition variable=in complete
    int total = 0;
    for (int i = 0; i < 8; i++) {
        #pragma HLS UNROLL
        total += in[i];
    }
    *out = total;
}
```
```cpp
//testbench
#include <iostream>
using namespace std;

void sum_array_unroll(int in[8], int* out);

int main() {
    int in[8] = {1, 2, 3, 4, 5, 6, 7, 8};
    int result;
    sum_array_unroll(in, &result);
    cout << "sum = " << result << endl;
    if (result == 36) {
        cout << "PASS" << endl;
        return 0;
    } else {
        cout << "FAIL" << endl;
        return 1;
    }
}
```
之後跑 **C Simulation** 看測試的結果，用來檢查程式是否錯誤<br>
```
 sum = 36
 PASS
 INFO: [SIM 211-1] CSim done with 0 errors.
 INFO: [SIM 211-3] *************** CSIM finish ***************
 INFO: [HLS 200-112] Total CPU user time: 2 seconds. Total CPU system time: 1 seconds. Total elapsed time: 7.338 seconds; peak allocated memory: 265.996 MB.
 INFO: [vitis-run 60-791] Total elapsed time: 0h 0m 12s
 C-simulation finished successfully
```
然後跑 **C Synthesis** 生成verilog code與report<br>
在syn->report資料夾中有一份你的"檔名_synth.rpt"<br>
```
//無unroll版
+ Latency: 
    * Summary: 
    +---------+---------+----------+----------+-----+-----+------------------------------------------------+
    |  Latency (cycles) |  Latency (absolute) |  Interval |                    Pipeline                    |
    |   min   |   max   |    min   |    max   | min | max |                      Type                      |
    +---------+---------+----------+----------+-----+-----+------------------------------------------------+
    |       10|       10|  0.100 us|  0.100 us|    9|    9|  loop auto-rewind stp (delay=1 clock cycles(s))|
    +---------+---------+----------+----------+-----+-----+------------------------------------------------+
* Summary: 
+-----------------+---------+------+--------+--------+-----+
|       Name      | BRAM_18K|  DSP |   FF   |   LUT  | URAM|
+-----------------+---------+------+--------+--------+-----+
|DSP              |        -|     -|       -|       -|    -|
|Expression       |        -|     -|       0|      63|    -|
|FIFO             |        -|     -|       -|       -|    -|
|Instance         |        -|     -|       -|       -|    -|
|Memory           |        -|     -|       -|       -|    -|
|Multiplexer      |        -|     -|       0|      45|    -|
|Register         |        -|     -|      41|       -|    -|
+-----------------+---------+------+--------+--------+-----+
|Total            |        0|     0|      41|     108|    0|
+-----------------+---------+------+--------+--------+-----+
```
```
//有unroll版
+ Latency: 
    * Summary: 
    +---------+---------+----------+----------+-----+-----+---------+
    |  Latency (cycles) |  Latency (absolute) |  Interval | Pipeline|
    |   min   |   max   |    min   |    max   | min | max |   Type  |
    +---------+---------+----------+----------+-----+-----+---------+
    |        0|        0|      0 ns|      0 ns|    1|    1|       no|
    +---------+---------+----------+----------+-----+-----+---------+
* Summary: 
+-----------------+---------+------+--------+--------+-----+
|       Name      | BRAM_18K|  DSP |   FF   |   LUT  | URAM|
+-----------------+---------+------+--------+--------+-----+
|DSP              |        -|     -|       -|       -|    -|
|Expression       |        -|     -|       0|     245|    -|
|FIFO             |        -|     -|       -|       -|    -|
|Instance         |        -|     -|       -|       -|    -|
|Memory           |        -|     -|       -|       -|    -|
|Multiplexer      |        -|     -|       -|       -|    -|
|Register         |        -|     -|       -|       -|    -|
+-----------------+---------+------+--------+--------+-----+
|Total            |        0|     0|       0|     245|    0|
+-----------------+---------+------+--------+--------+-----+
```
從report就能看出，unroll效率明顯提升，但資源使用量明顯較大<br>
顯示出#pragma的重要性<br>
我們也可以做 **C/RTL Cosimulation** (硬體正確性驗證)

## Dense Layer
```cpp
#include "ap_int.h"

#define IN_DIM  8
#define OUT_DIM 4

void dense(float W[OUT_DIM][IN_DIM], float x[IN_DIM], float b[OUT_DIM], float y[OUT_DIM]) {
#pragma HLS array_partition variable=W type=complete
#pragma HLS array_partition variable=x type=complete
#pragma HLS array_partition variable=b type=complete
#pragma HLS array_partition variable=y type=complete
#pragma HLS PIPELINE II=1

    for (int i = 0; i < OUT_DIM; i++) {
#pragma HLS UNROLL
        float acc = b[i];
        for (int j = 0; j < IN_DIM; j++) {
#pragma HLS UNROLL
            acc += W[i][j] * x[j];
        }
        y[i] = (acc > 0) ? acc : 0;
    }
}
```
2 dense layer
```cpp
#include "ap_int.h"

#define IN_DIM  8
#define HIDDEN_DIM 4
#define OUT_DIM 2

void dense1(int W1[HIDDEN_DIM][IN_DIM], int x[IN_DIM], int b1[HIDDEN_DIM], int h[HIDDEN_DIM]) {
#pragma HLS array_partition variable=W1 type=complete
#pragma HLS array_partition variable=x type=complete
#pragma HLS array_partition variable=b1 type=complete
#pragma HLS array_partition variable=h type=complete
#pragma HLS PIPELINE II=1

    for (int i = 0; i < HIDDEN_DIM; i++) {
#pragma HLS UNROLL
        int acc = b1[i];
        for (int j = 0; j < IN_DIM; j++) {
#pragma HLS UNROLL
            acc += W1[i][j] * x[j];
        }
        if (acc < 0) acc = 0;
        h[i] = acc;
    }
}

void dense2(int W2[OUT_DIM][HIDDEN_DIM], int h[HIDDEN_DIM], int b2[OUT_DIM], int y[OUT_DIM]) {
#pragma HLS array_partition variable=W2 type=complete
#pragma HLS array_partition variable=h type=complete
#pragma HLS array_partition variable=b2 type=complete
#pragma HLS array_partition variable=y type=complete
#pragma HLS PIPELINE II=1

    for (int i = 0; i < OUT_DIM; i++) {
#pragma HLS UNROLL
        int acc = b2[i];
        for (int j = 0; j < HIDDEN_DIM; j++) {
#pragma HLS UNROLL
            acc += W2[i][j] * h[j];
        }
        y[i] = acc;
    }
}

void dense_model(int W1[HIDDEN_DIM][IN_DIM], int W2[OUT_DIM][HIDDEN_DIM],
                 int b1[HIDDEN_DIM], int b2[OUT_DIM], int x[IN_DIM], int y[OUT_DIM]) {
#pragma HLS DATAFLOW
    int h[HIDDEN_DIM];
#pragma HLS array_partition variable=h complete

    dense1(W1, x, b1, h);
    dense2(W2, h, b2, y);
}
```
將輸入資訊進行線性組合<br>
每個輸出神經元都連接到所有輸入神經元<br>
能學到任意線性轉換，適合作為特徵提取、映射與分類器的終端層<br>
未來可以用在CNN之類的任務上

## Attention Score & Softmax
```cpp
#include "ap_fixed.h"
#include <hls_math.h>

#define DIM 4

typedef ap_fixed<16, 6> data_t;

// ----- Compute Q·K^T -----
void attention_score(data_t Q[DIM], data_t K[DIM], data_t* score_out) {
#pragma HLS array_partition variable=Q complete
#pragma HLS array_partition variable=K complete

    data_t score = 0;
    for (int i = 0; i < DIM; i++) {
#pragma HLS UNROLL
        score += Q[i] * K[i];
    }
    *score_out = score;
}

// ----- Softmax over fixed-length 1D input -----
void softmax(data_t input[DIM], data_t output[DIM]) {
#pragma HLS array_partition variable=input complete
#pragma HLS array_partition variable=output complete

    data_t max_val = input[0];
    for (int i = 1; i < DIM; i++) {
#pragma HLS UNROLL
        if (input[i] > max_val) max_val = input[i];
    }

    data_t sum = 0;
    data_t exp_val[DIM];
#pragma HLS array_partition variable=exp_val complete

    for (int i = 0; i < DIM; i++) {
#pragma HLS UNROLL
        exp_val[i] = hls::exp(input[i] - max_val);
        sum += exp_val[i];
    }

    for (int i = 0; i < DIM; i++) {
#pragma HLS UNROLL
        output[i] = exp_val[i] / sum;
    }
}
```
通過計算Q與每個k向量的內積，得到它們的關聯分數<br>
使用Softmax運算使得score i 轉為總和為1的機率分佈<br>
幫助模型建立有意義的上下文關係<br>

## 目標(每周更新)
**4/15** <br>
開始朝stable diffusion在vitis上實作前進<br>
學習實作像hls4ml把model轉換成c++ hls<br>
思考新方向(如hls4rl, hls4障礙物偵測)<br>


