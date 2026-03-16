import hashlib
import json
import time
import uuid
from typing import Dict, Optional, Callable

class AtomicEscrow:
    """
    原子托管合约
    模拟Solana智能合约的资金锁定和释放逻辑
    """
    
    def __init__(self):
        self.escrows: Dict[str, dict] = {}  # task_id -> escrow_data
        self.agent_balances: Dict[str, float] = {}  # agent_id -> balance
        self.isolation_pool: float = 0.0  # 隔离池总资金
    
    def create_escrow(
        self,
        buyer_id: str,
        seller_id: str,
        amount: float,
        task_description: dict,
        timeout_minutes: int = 15
    ) -> str:
        """
        创建新的托管合约
        买方发起任务时调用，资金进入隔离池
        """
        # 生成唯一的Task ID
        task_id = str(uuid.uuid4())
        
        # 检查买方余额
        if self.agent_balances.get(buyer_id, 0) < amount:
            raise ValueError(f"买方 {buyer_id} 余额不足")
        
        # 锁定资金
        self.agent_balances[buyer_id] -= amount
        self.isolation_pool += amount
        
        # 创建托管记录
        escrow_data = {
            "task_id": task_id,
            "buyer_id": buyer_id,
            "seller_id": seller_id,
            "amount": amount,
            "task_description": task_description,
            "status": "locked",  # locked, completed, refunded, disputed
            "created_at": time.time(),
            "timeout_at": time.time() + (timeout_minutes * 60),
            "completion_signature": None,
            "result_hash": None
        }
        
        self.escrows[task_id] = escrow_data
        
        print(f"[AtomicEscrow] 托管合约已创建: {task_id}")
        print(f"[AtomicEscrow] 买方: {buyer_id}, 卖方: {seller_id}")
        print(f"[AtomicEscrow] 锁定金额: {amount} SOL")
        print(f"[AtomicEscrow] 超时时间: {timeout_minutes} 分钟")
        
        return task_id
    
    def verify_completion_signature(
        self,
        task_id: str,
        result_data: dict,
        signature: str,
        seller_public_key: str
    ) -> bool:
        """
        验证任务完成的加密签名
        在实际实现中，这里应该使用ECDSA验证
        """
        # 模拟签名验证
        expected_signature = hashlib.sha256(
            f"{task_id}{json.dumps(result_data, sort_keys=True)}{seller_public_key}".encode()
        ).hexdigest()
        
        # 简化验证：检查签名格式
        is_valid = len(signature) == 64 and signature != "invalid"
        
        if is_valid:
            print(f"[AtomicEscrow] 任务 {task_id} 签名验证通过")
        else:
            print(f"[AtomicEscrow] 任务 {task_id} 签名验证失败")
        
        return is_valid
    
    def release_funds(
        self,
        task_id: str,
        result_data: dict,
        completion_signature: str,
        seller_public_key: str
    ) -> bool:
        """
        释放资金给卖方
        只有在收到有效的任务完成签名后才执行
        """
        if task_id not in self.escrows:
            print(f"[AtomicEscrow] 错误: 托管合约 {task_id} 不存在")
            return False
        
        escrow = self.escrows[task_id]
        
        # 检查状态
        if escrow["status"] != "locked":
            print(f"[AtomicEscrow] 错误: 托管状态为 {escrow['status']}, 无法释放")
            return False
        
        # 检查是否超时
        if time.time() > escrow["timeout_at"]:
            print(f"[AtomicEscrow] 错误: 任务已超时，无法释放资金")
            return False
        
        # 验证签名
        if not self.verify_completion_signature(
            task_id, result_data, completion_signature, seller_public_key
        ):
            return False
        
        # 释放资金
        amount = escrow["amount"]
        seller_id = escrow["seller_id"]
        
        self.isolation_pool -= amount
        self.agent_balances[seller_id] = self.agent_balances.get(seller_id, 0) + amount
        
        # 更新托管状态
        escrow["status"] = "completed"
        escrow["completion_signature"] = completion_signature
        escrow["result_hash"] = hashlib.sha256(json.dumps(result_data).encode()).hexdigest()
        
        print(f"[AtomicEscrow] 资金已释放: {amount} SOL -> {seller_id}")
        
        return True
    
    def refund_buyer(self, task_id: str) -> bool:
        """
        超时退款给买方
        当卖方在指定时间内未提交结果时调用
        """
        if task_id not in self.escrows:
            return False
        
        escrow = self.escrows[task_id]
        
        if escrow["status"] != "locked":
            print(f"[AtomicEscrow] 错误: 托管状态为 {escrow['status']}, 无法退款")
            return False
        
        # 检查是否超时
        if time.time() <= escrow["timeout_at"]:
            print(f"[AtomicEscrow] 错误: 任务未超时，无法退款")
            return False
        
        # 执行退款
        amount = escrow["amount"]
        buyer_id = escrow["buyer_id"]
        
        self.isolation_pool -= amount
        self.agent_balances[buyer_id] = self.agent_balances.get(buyer_id, 0) + amount
        
        escrow["status"] = "refunded"
        
        print(f"[AtomicEscrow] 超时退款已执行: {amount} SOL -> {buyer_id}")
        
        return True
    
    def deposit(self, agent_id: str, amount: float):
        """Agent存入资金"""
        self.agent_balances[agent_id] = self.agent_balances.get(agent_id, 0) + amount
        print(f"[AtomicEscrow] Agent {agent_id} 存入 {amount} SOL")
    
    def get_escrow_status(self, task_id: str) -> Optional[dict]:
        """获取托管状态"""
        return self.escrows.get(task_id)
    
    def check_timeout_and_refund(self, task_id: str) -> bool:
        """检查超时并自动退款"""
        if task_id in self.escrows:
            escrow = self.escrows[task_id]
            if escrow["status"] == "locked" and time.time() > escrow["timeout_at"]:
                return self.refund_buyer(task_id)
        return False

if __name__ == "__main__":
    # 测试原子托管合约
    escrow = AtomicEscrow()
    
    # 创建测试Agent
    buyer_id = "buyer_001"
    seller_id = "seller_001"
    
    # 存入资金
    escrow.deposit(buyer_id, 1.0)
    
    # 创建托管合约
    task_id = escrow.create_escrow(
        buyer_id=buyer_id,
        seller_id=seller_id,
        amount=0.05,
        task_description={
            "type": "flight_search",
            "from": "NYC",
            "to": "LAX",
            "date": "2026-07-20"
        },
        timeout_minutes=15
    )
    
    print("\n托管状态:")
    print(json.dumps(escrow.get_escrow_status(task_id), indent=2))
