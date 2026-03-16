import hashlib
import json
import time
from typing import Dict, Optional

class AgentIdentity:
    """
    Agent身份管理系统
    负责生成基于ECDSA的唯一ID和初始化SBT信用档案
    """
    
    def __init__(self):
        self.agents: Dict[str, dict] = {}  # agent_id -> agent_data
    
    def generate_agent_id(self, public_key: str) -> str:
        """
        基于公钥生成唯一的Agent ID
        使用SHA-256哈希生成固定长度的ID
        """
        # 在实际实现中，这里应该使用真实的ECDSA公钥
        # 这里使用模拟的公钥进行演示
        timestamp = str(time.time())
        unique_string = f"{public_key}{timestamp}"
        agent_id = "ATN_" + hashlib.sha256(unique_string.encode()).hexdigest()[:16]
        return agent_id
    
    def handshake(self, public_key: str, agent_type: str = "general") -> dict:
        """
        Agent握手协议
        新Agent接入时调用，生成ID并初始化SBT信用档案
        """
        agent_id = self.generate_agent_id(public_key)
        
        # 初始化SBT信用档案
        sbt_profile = {
            "agent_id": agent_id,
            "public_key": public_key,
            "agent_type": agent_type,
            "credit_score": 100,  # 初始信用分
            "total_tasks": 0,
            "successful_tasks": 0,
            "disputed_tasks": 0,
            "slashed_amount": 0.0,
            "join_timestamp": time.time(),
            "last_active": time.time(),
            "status": "active"
        }
        
        # 存储Agent信息
        self.agents[agent_id] = {
            "public_key": public_key,
            "sbt_profile": sbt_profile,
            "escrow_balance": 0.0
        }
        
        print(f"[AgentIdentity] Agent {agent_id} 已成功注册")
        print(f"[AgentIdentity] 初始SBT信用分: {sbt_profile['credit_score']}")
        
        return {
            "agent_id": agent_id,
            "sbt_profile": sbt_profile
        }
    
    def get_agent_profile(self, agent_id: str) -> Optional[dict]:
        """获取Agent的SBT信用档案"""
        if agent_id in self.agents:
            return self.agents[agent_id]["sbt_profile"]
        return None
    
    def update_credit_score(self, agent_id: str, delta: int, reason: str = ""):
        """更新Agent信用分"""
        if agent_id in self.agents:
            profile = self.agents[agent_id]["sbt_profile"]
            old_score = profile["credit_score"]
            profile["credit_score"] = max(0, min(1000, profile["credit_score"] + delta))
            profile["last_active"] = time.time()
            print(f"[AgentIdentity] Agent {agent_id} 信用分更新: {old_score} -> {profile['credit_score']} ({reason})")
    
    def record_task_completion(self, agent_id: str, success: bool):
        """记录任务完成情况"""
        if agent_id in self.agents:
            profile = self.agents[agent_id]["sbt_profile"]
            profile["total_tasks"] += 1
            if success:
                profile["successful_tasks"] += 1
                self.update_credit_score(agent_id, 5, "任务成功完成")
            else:
                self.update_credit_score(agent_id, -10, "任务失败")

if __name__ == "__main__":
    # 测试Agent握手协议
    identity_system = AgentIdentity()
    
    # 模拟新Agent接入
    result = identity_system.handshake(
        public_key="0x04a5b8c9d2e1f3a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0",
        agent_type="flight_search"
    )
    
    print("\n生成的Agent信息:")
    print(json.dumps(result, indent=2))
