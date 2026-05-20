# Homework 4 — 資訊圖表 (Infographics)
**主題：智能量化交易決策代理 (DRL-based Algorithmic Trading Agent)**

以下圖表使用 Mermaid 語法繪製，展示了 AI Harness 系統架構與 Agent 的工作流程 (ReAct Workflow)。

## 1. System Architecture Diagram (AI 系統架構圖)

此架構圖展示了 LLM 如何作為核心控制器 (System Controller)，連接短期/長期記憶 (Memory)，並透過 Tool Chain 呼叫外部的 API 以及核心的 **DRL Policy Network**。

```mermaid
graph TD
    %% 定義節點樣式
    classDef llm fill:#f9f2f4,stroke:#d3a4b0,stroke-width:2px,color:#000
    classDef memory fill:#e8f4f8,stroke:#9bc4d6,stroke-width:2px,color:#000
    classDef tools fill:#f2f9e8,stroke:#b0d69b,stroke-width:2px,color:#000
    classDef user fill:#fff5e6,stroke:#ffd699,stroke-width:2px,color:#000
    classDef drl fill:#e6e6fa,stroke:#9370db,stroke-width:3px,color:#000,font-weight:bold

    User((使用者\nInvestor)):::user

    subgraph AI_Harness_System ["AI Harness System (Agent)"]
        LLM["Large Language Model\n(System Controller / ReAct)"]:::llm
        
        subgraph Memory_Module ["Memory"]
            STM["Short-term Memory\n(Context & Recent States)"]:::memory
            LTM["Long-term Memory\n(Risk Profile & History)"]:::memory
        end
        
        subgraph Tool_Chain ["Tools (Function Calling)"]
            Tool1["fetch_market_state()\n[Market Data API]"]:::tools
            Tool2["execute_drl_policy()\n[DRL Actor Network]"]:::drl
            Tool3["run_portfolio_simulation()\n[Backtest Engine]"]:::tools
        end
    end

    MarketData[("Market API\n(Yahoo/Binance)")]
    
    %% 連線關係
    User -- "Natural Language Request\n(e.g., 'Lower my risk')" --> LLM
    LLM -- "Read/Write" <--> STM
    LLM -- "Query/Retrieve" <--> LTM
    
    LLM -- "1. Plan & Call Tool" --> Tool1
    Tool1 -- "Fetch Data" --> MarketData
    MarketData -- "Return JSON State" --> Tool1
    Tool1 -- "Return State to LLM" --> LLM
    
    LLM -- "2. Parse State & Call Tool" --> Tool2
    Tool2 -- "Policy Forward Pass" --> Tool2
    Tool2 -- "Return Action (Buy/Sell)" --> LLM
    
    LLM -- "3. Verify Action" --> Tool3
    Tool3 -- "Return Simulation Metrics" --> LLM
    
    LLM -- "Final Answer / Explanation" --> User
```

---

## 2. Agent Workflow (Sequence Diagram - 時序圖)

此時序圖詳細呈現了使用者輸入指令後，系統內部的多步驟任務執行流程 (ReAct 模式)。特別著重於 LLM 如何與 DRL 模型互動。

```mermaid
sequenceDiagram
    autonumber
    actor User as Investor
    participant LLM as LLM Controller
    participant Mem as Memory
    participant T1 as Tool: fetch_market_state
    participant T2 as Tool: execute_drl_policy (DRL)
    participant T3 as Tool: run_portfolio_simulation

    User->>LLM: "幫我處理手上的 NVDA，現在市場波動大，我不想承擔太多風險。"
    
    Note over LLM: [Thought]<br/>使用者詢問 NVDA 且風險承受度低。<br/>需先獲取市場狀態，再調用 DRL 模型。
    
    LLM->>Mem: 獲取使用者過往投資偏好與近期上下文
    Mem-->>LLM: 回傳：偏好保守，持有 NVDA 100 股
    
    Note over LLM: [Action 1]<br/>Call fetch_market_state(ticker="NVDA", timeframe="1D")
    LLM->>T1: fetch_market_state("NVDA", "1D")
    T1-->>LLM: [Observation 1] 回傳 State (Price: 120, MACD: Bearish, VIX: High)
    
    Note over LLM: [Thought]<br/>市場波動確實高。我將 risk_penalty 設為 0.8 (保守)，<br/>傳給 DRL Policy Network 進行決策。
    
    Note over LLM: [Action 2]<br/>Call execute_drl_policy(state_data, risk_penalty=0.8)
    LLM->>T2: execute_drl_policy(state, 0.8)
    
    Note right of T2: DRL Agent 根據 State 與高風險懲罰，<br/>計算預期 Reward 並輸出 Action。
    T2-->>LLM: [Observation 2] 回傳 Action: {"action": "SELL", "proportion": "50%"}
    
    Note over LLM: [Thought]<br/>DRL 建議賣出 50%。<br/>在回覆前，我先執行沙盒回測確認績效。
    
    Note over LLM: [Action 3]<br/>Call run_portfolio_simulation(action, duration="7D")
    LLM->>T3: run_portfolio_simulation({"SELL": 50%}, "7D")
    T3-->>LLM: [Observation 3] 回傳 Metrics (MDD 降低 15%, Sharpe: 1.2)
    
    Note over LLM: [Final Answer]<br/>統整所有觀察結果，生成人類易讀的解釋。
    LLM->>User: "根據市場高波動狀態與您的保守偏好，DRL 決策模型建議您賣出 50% NVDA 持倉。模擬顯示此舉能有效降低 15% 的最大虧損風險。是否確認執行？"
```
