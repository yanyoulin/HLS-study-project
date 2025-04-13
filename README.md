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






