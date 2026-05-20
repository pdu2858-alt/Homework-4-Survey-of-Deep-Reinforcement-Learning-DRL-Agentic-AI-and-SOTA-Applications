from agent import TradingAgent

def main():
    print("====================================================")
    print("      DRL-based Algorithmic Trading Agent (HW4)     ")
    print("====================================================")
    
    # 建立系統控制器 (Agent)
    agent = TradingAgent()
    
    # 模擬使用者輸入
    # 情境：使用者詢問 NVDA，且當前市場狀況為 VIX=High, MACD=Bearish (預設的 mock 狀態)
    # 使用者希望降低風險，這會觸發高 risk_penalty_factor，進而影響 DRL 的輸出
    user_prompt = "最近科技股波動很大，我手上的 NVDA 該怎麼處理？我的風險承受度現在很低。"
    
    try:
        # 開始執行多步驟 ReAct 工作流
        agent.process_request(user_prompt)
    except KeyboardInterrupt:
        print("\n\n[系統提示] 使用者中斷執行。")
    except Exception as e:
        print(f"\n\n[系統錯誤] 發生未預期的錯誤: {e}")

if __name__ == "__main__":
    main()
