# HLS-study-project
```
Vitis HLS 2024.2
part=xcku035-fbva676-2-e
```
## 什麼是HLS
將高階語言的演算法轉換為RTL代碼，進一步用於FPGA的硬體實現

## HLS pragma
pragma是用來向Vitis HLS提供指令的關鍵字，幫助優化硬體設計並控制生成的RTL代碼的行為。這些指令可以用來進行性能調整、資源分配以及設計流程的優化。<br>
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
![image](https://github.com/yanyoulin/HLS-study-project/blob/main/pics/%E8%9E%A2%E5%B9%95%E6%93%B7%E5%8F%96%E7%95%AB%E9%9D%A2%202025-04-14%20020312.png)
pipeline讓多個操作分工並行執行，將一段運算「拆解成多個階段」，讓每個clock cycle都能輸入新的資料、產出新的結果<br>
可以自行設定Initiation Interval(II):啟動新一次迭代所需的clock cycle，若II=1則效率最高<br>


