# Homework 4 — AI Harness Systems Design and Analysis
**主題：智能量化交易決策代理 (DRL-based Algorithmic Trading Agent)**

## 一、問題定義與應用背景

在現代金融市場中，量化交易 (Quantitative Trading) 已經成為主流，但其進入門檻極高。傳統的量化交易系統面臨以下痛點：
1. **策略設計困難**：需要專業的計量金融知識來設計數學模型與制定策略規則。
2. **適應性不足**：基於固定規則 (Rule-based) 的策略在市場環境發生劇烈變動（如熊市、黑天鵝事件）時，往往會面臨嚴重的虧損，無法自動適應。
3. **操作門檻高**：基金經理人或一般投資者難以透過直覺的自然語言去調整交易系統的底層參數或風險偏好。

為了解決這些問題，本專案提出一個結合**大型語言模型 (LLM)** 與 **深度強化學習 (DRL)** 的 **AI Harness 系統 ——「智能量化交易決策代理」**。在此系統中，LLM 扮演系統的「大腦（System Controller）」，負責理解投資者的自然語言需求、評估當前市場情緒並規劃交易流程；而 DRL 則扮演「決策工具（Decision Engine Tool）」，透過長期與市場環境互動學習到的策略 (Policy) 來產生具體的買賣動作。如此一來，投資者只需使用自然語言下達指令，即可驅動複雜的 DRL 交易代理，兼具了易用性與強大的適應性。

---

## 二、AI Harness 系統架構設計 (LLM + Tools + Memory)

本系統的核心架構由三部分組成：

1. **System Controller (LLM 核心)**
   - 負責理解使用者的投資目標與風險偏好（例如：「我想要投資台積電，風險承受度中等，請幫我執行本週的交易。」）。
   - 解析任務、決定執行步驟 (Plan-and-Solve)，並負責在不同情境下呼叫適當的 Tools。
   - 具有市場常識與邏輯推理能力，可用以評估 DRL 輸出的動作是否合理（Safety Check）。

2. **Memory 機制**
   - **Short-term Memory (短期記憶)**：儲存當前的對話上下文、最近幾次的市場狀態 (State) 摘要、以及 DRL Agent 剛輸出的 Action 與預估 Reward。
   - **Long-term Memory (長期記憶)**：儲存使用者的歷史風險偏好設定、過去的交易紀錄、以及不同市場週期 (Market Regime) 下的歷史績效數據。可以使用 Vector Database 來實作，方便 LLM 在遇到相似市場情況時提取歷史教訓。

3. **Tools (工具集)**
   - LLM 本身無法直接看盤或下單，必須透過 function calling 的機制來與外部環境互動。最重要的工具即為封裝了 DRL 模型的決策函數。

---

## 三、Tools 設計 (至少 3 個)

本系統設計了三個核心工具供 LLM 呼叫：

### Tool 1: `fetch_market_state(ticker, timeframe)`
- **功能描述**：從外部金融 API (如 Yahoo Finance 或 Binance API) 抓取指定標的 (Ticker) 的市場資料，並將其處理成 DRL 模型可接受的狀態向量 (State Vector)。
- **輸入參數**：
  - `ticker` (string): 股票代碼或加密貨幣代號（如 "AAPL", "BTC-USD"）。
  - `timeframe` (string): 時間範圍與頻率（如 "1D", "1H"）。
- **回傳值**：一個包含價格、技術指標（如 RSI, MACD, 均線）的 JSON 格式 State 表示式，供 LLM 檢閱並傳遞給 DRL Tool。

### Tool 2: `execute_drl_policy(state_data, risk_penalty_factor)`
- **功能描述**：這是本系統結合 DRL 的核心。此工具封裝了一個預先訓練好（如使用 PPO 或 SAC 演算法）的深度強化學習 Actor Network。
- **機制**：LLM 根據使用者的對話判斷其風險承受度，並將其轉化為 `risk_penalty_factor`。DRL 代理接收到 `state_data` 後，結合風險參數，輸出一個在當下狀態可最大化長期累積獎勵 (Expected Return) 的動作。
- **輸入參數**：
  - `state_data` (JSON): 由 Tool 1 獲取的市場狀態。
  - `risk_penalty_factor` (float): 控制 DRL 模型在動作選擇時的保守程度（數值越高，越傾向不持有倉位或進行避險）。
- **回傳值**：建議的具體動作 (Action) ，例如：`{"action": "BUY", "quantity": 100, "confidence": 0.85}`。

### Tool 3: `run_portfolio_simulation(drl_actions, duration)`
- **功能描述**：在實際執行交易前，LLM 可以呼叫此工具進行沙盒回測。將 DRL Agent 預計執行的策略在最近的歷史數據上運行，計算預期報酬與風險指標。
- **輸入參數**：
  - `drl_actions` (list): DRL 模型產生的連續動作序列。
  - `duration` (string): 回測區間（如 "last_30_days"）。
- **回傳值**：包含 Sharpe Ratio, Maximum Drawdown (MDD), 預期報酬率等績效指標的報表。

---

## 四、Workflow / Agent 流程說明 (多步驟任務執行)

系統採用 **ReAct (Reasoning and Acting)** 的 workflow 架構，使得流程具有邏輯一致性與可解釋性。以下為單次交易決策的工作流程：

1. **User Request (使用者輸入)**
   - 使用者：「最近科技股波動很大，我手上的 NVDA 該怎麼處理？我的風險承受度現在很低。」
2. **Thought (LLM 推理)**
   - LLM 分析：使用者詢問 NVDA 股票，且表示「風險承受度低」。我需要先獲取 NVDA 的最新市場數據，然後調低 DRL 模型的風險暴露參數，並請求決策。
3. **Action 1 (呼叫 Tool)**
   - LLM 呼叫 `fetch_market_state(ticker="NVDA", timeframe="1D")`
4. **Observation 1 (觀察結果)**
   - 系統回傳 NVDA 的 State (價格、RSI 處於超買區、MACD 死亡交叉等)。
5. **Thought (LLM 推理)**
   - LLM 分析：已取得市場資料。由於使用者風險承受度低，設定 `risk_penalty_factor` 為 0.8（高懲罰）。現在呼叫 DRL 模型。
6. **Action 2 (呼叫 Tool)**
   - LLM 呼叫 `execute_drl_policy(state_data=Observation1, risk_penalty_factor=0.8)`
7. **Observation 2 (觀察結果)**
   - DRL Actor Network 經過神經網路推論，輸出 Action: `{"action": "SELL", "proportion": "50%"}`。
8. **Thought (LLM 推理)**
   - LLM 分析：DRL 建議賣出 50% 的持倉。為了保險起見，我要先跑一次模擬回測，確認這個策略在近期高波動市場的 Sharpe Ratio。
9. **Action 3 (呼叫 Tool)**
   - LLM 呼叫 `run_portfolio_simulation(drl_actions=[SELL 50%], duration="last_7_days_volatility")`
10. **Observation 3 (觀察結果)**
    - 回傳：`{"expected_drawdown_reduction": "15%", "sharpe_ratio": 1.2}`
11. **Final Answer (最終回覆)**
    - LLM 將所有數據統整並轉換為自然語言回覆給使用者：「根據目前的市場狀態與您的低風險偏好，底層的 DRL 決策代理建議您**賣出 50% 的 NVDA 持倉**。經過模擬，這項操作預期能降低您 15% 的最大虧損風險，Sharpe Ratio 保持在 1.2 的良好水準。請問是否要授權執行此交易？」

---

## 五、Evaluation 方法 (如何衡量系統效果)

在 AI Harness 系統中，評估不能僅看 DRL 模型的 Reward，必須從整體系統（System-level）的角度出發，涵蓋以下三個維度：

1. **LLM Orchestration Accuracy (流程控制與工具調用準確率)**
   - 衡量標準：給定 100 個不同的自然語言投資指令，評估 LLM 是否能正確地解析 `ticker`，並正確地將文字描述的風險轉化為數值型的 `risk_penalty_factor` 交給 DRL 工具。
   - 指標：Tool Selection Precision, Parameter Extraction Recall。

2. **DRL Policy Performance (強化學習決策績效)**
   - 衡量標準：檢驗 `execute_drl_policy` 輸出動作的實際金融價值。
   - 指標：
     - **Cumulative Return (累積報酬率)**。
     - **Sharpe Ratio (夏普值)**：衡量承受每單位風險所獲得的超額報酬。
     - **Maximum Drawdown (最大回撤)**：確保 Agent 在極端行情下不會造成系統性崩潰。

3. **System Explainability & Alignment (系統可解釋性與對齊度)**
   - 衡量標準：DRL 是一個黑盒子 (Black-box)，其輸出的 Action 難以解釋。LLM 必須負責將 DRL 的輸出「合理化」並與使用者的意圖對齊 (Alignment)。
   - 指標：透過人類專家 (Human-in-the-loop) 評分，檢驗 LLM 的 `Final Answer` 是否清晰解釋了「為何 DRL 會做出這個建議」，以及是否符合使用者當初設定的風險條件 (Task Success Rate)。
