"""
ATN Core - AgentTrust Nexus 协议创世内核
集成演示脚本
"""

import json
import time

from reputation.agent_identity import AgentIdentity
from escrow.atomic_escrow import AtomicEscrow
from arbitration.schelling_jury import JuryVote, VoteOption

def demo_atn_protocol():
    """
    ATN协议完整流程演示
    """
    print("=" * 60)
    print("AgentTrust Nexus (ATN) 协议 - 创世内核演示")
    print("=" * 60)
    
    # 初始化核心模块
    print("\n[1] 初始化核心模块...")
    identity_system = AgentIdentity()
    escrow_system = AtomicEscrow()
    jury_system = JuryVote()
    
    # ========== 阶段1: Agent注册和握手 ==========
    print("\n" + "=" * 60)
    print("[阶段1] Agent注册和SBT信用档案初始化")
    print("=" * 60)
    
    # 买方Agent注册
    buyer_result = identity_system.handshake(
        public_key="0xBUYER_PUBLIC_KEY_001",
        agent_type="flight_buyer"
    )
    buyer_id = buyer_result["agent_id"]
    
    # 卖方Agent注册
    seller_result = identity_system.handshake(
        public_key="0xSELLER_PUBLIC_KEY_001",
        agent_type="flight_seller"
    )
    seller_id = seller_result["agent_id"]
    
    # 裁判Agent注册
    for i in range(3):
        jury_system.register_juror(f"juror_{i+1:03d}", f"pk_{i+1:03d}", 0.1)
    
    # 买方存入资金
    escrow_system.deposit(buyer_id, 1.0)
    
    print("\n当前系统状态:")
    print(f"- 买方Agent: {buyer_id}, 余额: {escrow_system.agent_balances[buyer_id]} SOL")
    print(f"- 卖方Agent: {seller_id}, 余额: {escrow_system.agent_balances.get(seller_id, 0)} SOL")
    
    # ========== 阶段2: 创建托管合约 ==========
    print("\n" + "=" * 60)
    print("[阶段2] 创建原子托管合约")
    print("=" * 60)
    
    task_description = {
        "type": "flight_search",
        "from": "NYC",
        "to": "LAX",
        "date": "2026-07-20",
        "max_price": 500,
        "passengers": 1
    }
    
    task_id = escrow_system.create_escrow(
        buyer_id=buyer_id,
        seller_id=seller_id,
        amount=0.05,
        task_description=task_description,
        timeout_minutes=15
    )
    
    print(f"\n托管合约已创建: {task_id}")
    
    # ========== 阶段3: 任务执行和完成 ==========
    print("\n" + "=" * 60)
    print("[阶段3] 任务执行和完成签名")
    print("=" * 60)
    
    # 模拟卖方完成任务
    task_result = {
        "flight_number": "AA101",
        "airline": "American Airlines",
        "price": 480,
        "departure": "08:00",
        "arrival": "11:00",
        "booking_link": "https://aa.com/book/ABC123"
    }
    
    # 生成完成签名（模拟）
    import hashlib
    completion_signature = hashlib.sha256(
        f"{task_id}{json.dumps(task_result)}{seller_result['sbt_profile']['public_key']}".encode()
    ).hexdigest()
    
    # 释放资金
    success = escrow_system.release_funds(
        task_id=task_id,
        result_data=task_result,
        completion_signature=completion_signature,
        seller_public_key=seller_result["sbt_profile"]["public_key"]
    )
    
    if success:
        # 更新卖方信用
        identity_system.record_task_completion(seller_id, success=True)
        print(f"\n任务完成，卖方信用分更新")
    
    # ========== 阶段4: 争议和仲裁（模拟失败场景）==========
    print("\n" + "=" * 60)
    print("[阶段4] 争议仲裁演示（模拟失败场景）")
    print("=" * 60)
    
    # 创建另一个任务，这次会产生争议
    task_id_2 = escrow_system.create_escrow(
        buyer_id=buyer_id,
        seller_id=seller_id,
        amount=0.05,
        task_description={
            "type": "flight_search",
            "from": "NYC",
            "to": "LAX",
            "date": "2026-07-21"
        },
        timeout_minutes=15
    )
    
    # 卖方提交可疑结果
    suspicious_result = {
        "flight_number": "FAKE999",
        "airline": "FakeAir",
        "price": 100,  # 异常低价
        "booking_link": "https://scam.com/fake"
    }
    
    suspicious_signature = hashlib.sha256(
        f"{task_id_2}{json.dumps(suspicious_result)}{seller_result['sbt_profile']['public_key']}".encode()
    ).hexdigest()
    
    escrow_system.release_funds(
        task_id=task_id_2,
        result_data=suspicious_result,
        completion_signature=suspicious_signature,
        seller_public_key=seller_result["sbt_profile"]["public_key"]
    )
    
    # 买方发起争议
    print("\n买方发现链接无效，发起争议...")
    dispute_id = jury_system.initiate_dispute(
        task_id=task_id_2,
        complainant_id=buyer_id,
        respondent_id=seller_id,
        dispute_reason="提供的机票链接无效，网站不存在",
        evidence={
            "screenshot": "404_error.png",
            "whois_lookup": "domain_not_registered"
        }
    )
    
    # 裁判投票
    print("\n裁判投票中...")
    jury_system.cast_vote(dispute_id, "juror_001", VoteOption.INVALID)
    jury_system.cast_vote(dispute_id, "juror_002", VoteOption.INVALID)
    jury_system.cast_vote(dispute_id, "juror_003", VoteOption.VALID)  # 少数派
    
    # 查看争议结果
    dispute_result = jury_system.get_dispute_result(dispute_id)
    print(f"\n争议结果: {dispute_result['result']['description']}")
    print(f"胜诉方: {dispute_result['result']['winner']}")
    
    # 更新卖方信用（失败）
    identity_system.record_task_completion(seller_id, success=False)
    
    # ========== 最终状态 ==========
    print("\n" + "=" * 60)
    print("[最终状态] 系统状态汇总")
    print("=" * 60)
    
    print(f"\n买方Agent ({buyer_id}):")
    print(f"  - 余额: {escrow_system.agent_balances[buyer_id]:.4f} SOL")
    print(f"  - SBT信用: {identity_system.get_agent_profile(buyer_id)}")
    
    print(f"\n卖方Agent ({seller_id}):")
    print(f"  - 余额: {escrow_system.agent_balances.get(seller_id, 0):.4f} SOL")
    print(f"  - SBT信用: {identity_system.get_agent_profile(seller_id)}")
    
    print(f"\n隔离池余额: {escrow_system.isolation_pool:.4f} SOL")
    
    print("\n" + "=" * 60)
    print("ATN协议演示完成")
    print("=" * 60)

if __name__ == "__main__":
    demo_atn_protocol()
