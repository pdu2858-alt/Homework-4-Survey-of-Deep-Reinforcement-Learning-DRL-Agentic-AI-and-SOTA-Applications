# Homework 4 — AI 輔助設計與開發過程紀錄 (log.md)

本文件紀錄了在完成「Homework 4 — AI Harness Systems Design and Analysis」過程中的設計迭代、架構決策與互動過程。

## 1. 與 AI 的互動紀錄 (Chat History & Prompts)

- **使用者輸入 (Prompt 1)**: 提供 Homework 4 的完整 Syllabus，要求 AI 根據需求完成作業 4 的檔案，並放在 HW4 資料夾內。
- **AI 提案 (Iteration 1)**: AI 分析需求後，提出建立「企業智能資料分析代理 (Intelligent Business Data Analysis Agent)」的實作計畫，包含使用 SQL Query、資料視覺化等 Tools，並詢問使用者是否同意。
- **使用者回饋 (Prompt 2)**: 發現最初提案未涵蓋課程核心領域，要求：「主題請修改，主題必須要有深度強化學習的內容或範疇，因為這是一堂深度強化學習課程的作業。」
- **AI 調整與提案 (Iteration 2)**: AI 立即修正方向，提出兩種結合 DRL 與 AI Harness 的架構，讓 DRL 模型作為 Tool 被 LLM 呼叫：
  1. 自動化 DRL 實驗與調參助理 (Automated DRL Experiment Assistant)
  2. 智能量化交易決策代理 (DRL-based Algorithmic Trading Agent)
- **使用者決策 (Prompt 3)**: 選擇「提案二：智能量化交易決策代理」。
- **AI 執行**: AI 開始生成 `report.md`, `infographic.md` 與 `log.md` 三份文件。

## 2. 系統設計迭代過程

### Phase 1: 初步構思 (無 DRL 版本)
- **概念**：最初設計為純資料庫查詢與視覺化的 Agent。
- **缺點**：雖然符合 AI Harness (LLM + Tools) 的架構，但完全脫離了「深度強化學習」這門課程的核心目的。

### Phase 2: 結合 DRL 的架構設計 (最終版本)
- **概念轉變**：必須將 DRL 元素融入系統中。但由於作業要求「重點不在模型訓練，而在於 AI 系統如何透過 function calling 執行任務」，我們不能只做一個純 DRL 的 Trading Bot。
- **最終決策**：將 LLM 定位為「高階 System Controller」，將 DRL 定位為「底層 Tool (執行決策的神經網路)」。
  - LLM 負責：自然語言理解、風險參數萃取、呼叫市場資料 API (State)、呼叫 DRL (Policy)、結果解釋與安全性審查。
  - DRL 負責：接收 State 與 Penalty 參數，經過神經網路 (Actor Network) 計算出預期 Reward 最高的買賣動作。

## 3. 架構調整與設計決策理由

1. **選擇 ReAct (Reasoning and Acting) 流程**
   - **決策**：不採用單純的 Chain-of-Thought (CoT)，而是選擇 ReAct 模式。
   - **理由**：金融交易具有高風險，LLM 在決定呼叫 DRL 前需要先抓取資料 (Observation 1)，呼叫 DRL 取得 Action 後 (Observation 2)，也不能直接下單，必須再呼叫模擬環境 (Observation 3) 確認。ReAct 的 `Thought -> Action -> Observation` 循環能完美呈現這種嚴謹的多步驟檢查邏輯。

2. **記憶體 (Memory) 系統的切割**
   - **決策**：將記憶體劃分為 Short-term 與 Long-term。
   - **理由**：量化交易需要長期追蹤使用者的「風險偏好」(Long-term)，同時也需要記住「當前幾次對話的上下文」與「市場瞬間的波動狀態」(Short-term)。將其分開有助於 LLM 在呼叫 Tool 時傳遞更精確的 Context，避免 Token 超載。

## 4. 問題分析與修正過程

在設計 `execute_drl_policy` 這個 Tool 時，遇到了一個邏輯問題：
- **問題**：如果 DRL 模型是預先訓練好的，它怎麼能適應 LLM 臨時判斷出的「使用者低風險偏好」？
- **分析**：傳統 DRL 模型訓練完後，Reward Function 就固定了。如果 LLM 只是單純把 State 丟進去，DRL 依然會輸出同樣激進的 Action。
- **修正 (Reward Shaping via Parameter)**：為了讓 DRL Tool 能被 LLM 動態控制，我設計 Tool 的輸入參數必須包含 `risk_penalty_factor`。這意味著底層的 DRL 模型（例如 SAC）在訓練或推論時，其實是 Conditioned on 這個風險參數的（例如作為 State 的一部分，或是改變決策的閾值）。這樣 LLM 就能透過調整 `risk_penalty_factor` 參數，實質影響 DRL 代理的輸出行為，達成 System Controller 控制 Tool 的目的。這大大提升了設計的合理性與深度。
