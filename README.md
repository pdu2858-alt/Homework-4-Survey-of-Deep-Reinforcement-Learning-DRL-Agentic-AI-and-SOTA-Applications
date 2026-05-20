# Homework 4 — AI Harness Systems Design and Analysis
**主題：智能量化交易決策代理 (DRL-based Algorithmic Trading Agent)**

本專案為「深度強化學習」課程作業四的成果，展示如何設計並實作一個結合 **大型語言模型 (LLM)** 與 **深度強化學習 (DRL)** 的 AI Harness 系統。系統中，LLM 作為高階系統控制器 (System Controller)，透過 ReAct (Reasoning and Acting) 流程解析使用者需求，並呼叫封裝了 DRL 模型的工具 (Tool) 來進行交易決策。

## 📁 專案目錄與檔案說明

本專案包含作業要求的書面設計文件，以及具體將設計轉化為 Python 的模擬執行程式碼。

### 1. 作業繳交文件 (Deliverables)
*   **`report.md`**: 系統設計書面報告。包含問題定義、AI 系統架構、核心 Tools 設計、Agent Workflow 以及系統評估方法。
*   **`infographic.md`**: 資訊圖表。使用 Mermaid 語法繪製的系統架構圖 (Architecture Diagram) 與時序圖 (Sequence Diagram)。
*   **`log.md`**: 系統設計迭代與 AI 輔助開發的過程紀錄。

### 2. 程式碼實作 (Python Simulation)
*   **`agent.py`**: 核心系統控制器。實作 `TradingAgent` 類別，展示 LLM 如何透過 ReAct 流程進行思考並呼叫工具。
*   **`tools.py`**: 工具集。實作供 LLM 呼叫的三個核心工具，包含市場資料抓取、沙盒回測，以及呼叫 DRL 策略網路。
*   **`drl_model.py`**: 深度強化學習模型模擬器。實作 `DummyDRLPolicy`，展示 DRL 如何根據外部傳入的狀態 (State) 與風險懲罰係數 (Risk Penalty) 輸出動作 (Action)。
*   **`main.py`**: 系統執行入口。

## 🚀 如何執行程式碼

本程式碼旨在展示 AI Harness 系統的「工作流編排 (Orchestration)」與「工具呼叫 (Function Calling)」，因此採用原生 Python 撰寫模擬流程，**無須** 安裝龐大的第三方套件或設定 API Key 即可執行。

請在終端機中執行以下指令：

```bash
python main.py
```

執行後，您將在終端機中看見完整的 ReAct 執行日誌，包含：
1. `[LLM Thought]`: LLM 如何解析使用者的風險承受度。
2. `[Action]`: 呼叫對應的 Tool。
3. `[Observation]`: Tool 執行結果回傳（如 DRL 模型的輸出）。
4. `[Final Answer To User]`: 最終生成給使用者的建議。

## ⚙️ 系統架構亮點
*   **動態控制 DRL 模型**: 傳統 DRL 訓練完成後行為固定。本系統創新地在 Tool 中設計了 `risk_penalty_factor` 參數，讓 LLM 能將自然語言中解析出的風險承受度轉化為數值，動態改變 DRL 輸出的保守/激進程度。
*   **多步驟安全性驗證**: 在 DRL 輸出決策後，系統不會直接下單，而是強制呼叫 `run_portfolio_simulation` 進行沙盒回測，確認夏普值 (Sharpe Ratio) 合格後才回覆使用者，確保金融交易的安全性。
