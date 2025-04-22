# 以Vitis HLS實作Transformer Encoder Block之組成

---

### 一、作業目的

目的為了實作Transformer Encoder Block，包括 Multi-Head Attention, Feed-Forward Network, GELU, LayerNorm 和 Residual等基礎操作，並通過Vitis HLS轉成RTL以便後續應用於FPGA或AI加速器上。

---

### 二、實作過程

#### 步驟 1: 基礎類別寫成

1. **dense.h / dense.cpp**
   - 實作一個簡易的dense layer，可用於FFN或attention
   
2. **gelu.h / gelu.cpp**
   - 使用簡易方法描述模擬 GELU：
     \[ \text{GELU}(x) \approx x \cdot 0.5 \cdot (1 + \tanh(\sqrt{2/\pi}(x + 0.044715 x^3))) \]

3. **layernorm.h / layernorm.cpp**
   - 實作Layer Normalization的簡化版，按平均數與方差做標準化，尚未加入scale/shift

4. **residual_norm.h / residual_norm.cpp**
   - 將input + residual之後做一次 LayerNorm，是Transformer Block中重要步驟

#### 步驟 2: 實作 Multi-Head Attention

- 含有一顆head的attention_score + softmax + 機組添加
- 並行使用幾顆heads進行projection，最後接着用W_O轉換output

#### 步驟 3: 將前述各部分組合成 Transformer Encoder Block

- Input: Q, K, V
- Multi-Head Attention 轉換 Q, K, V 後計算 attention 輸出
- Residual + LayerNorm
- FFN (Dense1 + GELU + Dense2)
- Residual + LayerNorm 再一次

---

### 三、素質組件瞭解與行為

| 組件 | 功能 |
|--------|--------|
| `dense.cpp` | matrix-vector multiplication + bias |
| `gelu.cpp` | non-linear activation |
| `layernorm.cpp` | 標準化輸入 |
| `multi_head_attention.cpp` | 將多機組的 attention 封裝 |
| `residual_norm.cpp` | 封裝 skip connection + LayerNorm |

---

### 四、補充

- **Transformer Encoder Block 結構**
  - Attention(Q, K, V) + Residual + Norm
  - FFN(Dense1 + GELU + Dense2) + Residual + Norm

- **Attention 計算步驟**：
  - Q 和 K 做 dot product
  - softmax(score)
  - weighted sum(V)

---

### 五、實作成果

- 我們成功將 Transformer Encoder Block 以 HLS 轉成 RTL
- 通過 Vitis HLS 執行 csim, csyn, cosim全準
- 各個單元 (dense, gelu, attention, norm) 均有獨立 testbench 驗證

---

### 六、結論

我們將 Transformer Encoder Block 作為根基組件作為前篇，爲下一步 Stable Diffusion / LLM 的系統安裝做好基礎。

意義在於實際執行 Transformer 分段功能以轉成硬體 IP，並簡化了後續大型 AI 機組作業的展開。

