import random
import hashlib
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class VoteOption(Enum):
    FRAUD = "fraud"
    HONEST = "honest"
    ABSTAIN = "abstain"

class DisputeStatus(Enum):
    PENDING = "pending"
    VOTING = "voting"
    RESOLVED = "resolved"
    APPEALED = "appealed"

@dataclass
class Juror:
    id: str
    public_key: str
    reputation: float
    staked_amount: float
    vote: Optional[VoteOption] = None
    vote_hash: str = ""
    has_revealed: bool = False

@dataclass
class Dispute:
    id: str
    task_id: str
    complainant_id: str
    respondent_id: str
    reason: str
    escrow_amount: float
    jurors: List[Juror]
    status: DisputeStatus
    created_at: float
    resolved_at: Optional[float] = None
    verdict: Optional[str] = None
    majority_vote: Optional[VoteOption] = None

class ArbitrationEngine:
    """
    完整的仲裁引擎
    实现谢林点博弈机制
    """
    
    # 经济参数
    JURY_SIZE = 3
    JUROR_STAKE_REQUIRED = 10.0  # ATN
    MAJORITY_REWARD_RATE = 0.70   # 70%
    TREASURY_RATE = 0.20          # 20%
    INSURANCE_RATE = 0.10         # 10%
    SLASH_PERCENTAGE = 1.0        # 100%
    
    def __init__(self):
        self.disputes: Dict[str, Dispute] = {}
        self.juror_pool: List[Juror] = []
        self._initialize_juror_pool()
    
    def _initialize_juror_pool(self):
        """初始化陪审员池"""
        for i in range(100):
            self.juror_pool.append(Juror(
                id=f"juror_{i:03d}",
                public_key=f"pk_{i:03d}",
                reputation=random.uniform(100, 2000),
                staked_amount=random.uniform(10, 500)
            ))
    
    def create_dispute(
        self,
        task_id: str,
        complainant_id: str,
        respondent_id: str,
        reason: str,
        escrow_amount: float,
        evidence: Dict
    ) -> Dispute:
        """创建争议"""
        dispute_id = f"DISPUTE_{task_id}_{int(time.time())}"
        
        # 随机选择陪审员
        selected_jurors = self._select_jurors()
        
        dispute = Dispute(
            id=dispute_id,
            task_id=task_id,
            complainant_id=complainant_id,
            respondent_id=respondent_id,
            reason=reason,
            escrow_amount=escrow_amount,
            jurors=selected_jurors,
            status=DisputeStatus.VOTING,
            created_at=time.time()
        )
        
        self.disputes[dispute_id] = dispute
        
        print(f"\n[Arbitration] 争议创建: {dispute_id}")
        print(f"  投诉方: {complainant_id}")
        print(f"  被诉方: {respondent_id}")
        print(f"  原因: {reason}")
        print(f"  陪审团: {[j.id for j in selected_jurors]}")
        
        return dispute
    
    def _select_jurors(self) -> List[Juror]:
        """选择陪审员 (基于声誉加权)"""
        # 按声誉排序，高声誉者有更高概率被选中
        weights = [j.reputation for j in self.juror_pool]
        total_weight = sum(weights)
        
        selected = []
        available = self.juror_pool.copy()
        
        for _ in range(self.JURY_SIZE):
            if not available:
                break
            
            # 加权随机选择
            r = random.uniform(0, sum(j.reputation for j in available))
            cumulative = 0
            for juror in available:
                cumulative += juror.reputation
                if r <= cumulative:
                    selected.append(juror)
                    available.remove(juror)
                    break
        
        return selected
    
    def commit_vote(self, dispute_id: str, juror_id: str, vote_hash: str) -> bool:
        """提交投票承诺 (盲审)"""
        if dispute_id not in self.disputes:
            return False
        
        dispute = self.disputes[dispute_id]
        
        # 找到陪审员
        juror = next((j for j in dispute.jurors if j.id == juror_id), None)
        if not juror:
            return False
        
        if juror.vote_hash:
            return False  # 已投票
        
        juror.vote_hash = vote_hash
        print(f"[Arbitration] {juror_id} 已提交投票承诺")
        
        # 检查是否所有陪审员都已承诺
        if all(j.vote_hash for j in dispute.jurors):
            print("[Arbitration] 所有陪审员已承诺，进入揭示阶段")
        
        return True
    
    def reveal_vote(
        self,
        dispute_id: str,
        juror_id: str,
        vote: VoteOption,
        secret: str
    ) -> bool:
        """揭示投票"""
        if dispute_id not in self.disputes:
            return False
        
        dispute = self.disputes[dispute_id]
        juror = next((j for j in dispute.jurors if j.id == juror_id), None)
        
        if not juror or not juror.vote_hash:
            return False
        
        # 验证承诺
        expected_hash = hashlib.sha256(
            f"{juror_id}{vote.value}{secret}".encode()
        ).hexdigest()[:16]
        
        # 简化验证
        juror.vote = vote
        juror.has_revealed = True
        
        print(f"[Arbitration] {juror_id} 揭示投票: {vote.value}")
        
        # 检查是否所有陪审员都已揭示
        if all(j.has_revealed for j in dispute.jurors):
            self._resolve_dispute(dispute_id)
        
        return True
    
    def _resolve_dispute(self, dispute_id: str):
        """解决争议"""
        dispute = self.disputes[dispute_id]
        
        # 统计投票
        votes = {VoteOption.FRAUD: 0, VoteOption.HONEST: 0, VoteOption.ABSTAIN: 0}
        for juror in dispute.jurors:
            if juror.vote:
                votes[juror.vote] += 1
        
        # 确定多数派
        if votes[VoteOption.FRAUD] > votes[VoteOption.HONEST]:
            majority_vote = VoteOption.FRAUD
            verdict = "fraud_confirmed"
            winner = dispute.complainant_id
            loser = dispute.respondent_id
        elif votes[VoteOption.HONEST] > votes[VoteOption.FRAUD]:
            majority_vote = VoteOption.HONEST
            verdict = "honest_confirmed"
            winner = dispute.respondent_id
            loser = dispute.complainant_id
        else:
            majority_vote = VoteOption.ABSTAIN
            verdict = "tie"
            winner = None
            loser = None
        
        dispute.verdict = verdict
        dispute.majority_vote = majority_vote
        dispute.status = DisputeStatus.RESOLVED
        dispute.resolved_at = time.time()
        
        print(f"\n[Arbitration] 争议解决: {dispute_id}")
        print(f"  投票统计: FRAUD={votes[VoteOption.FRAUD]}, HONEST={votes[VoteOption.HONEST]}")
        print(f"  判决: {verdict}")
        print(f"  胜诉方: {winner}")
        
        # 分配奖励和惩罚
        self._distribute_rewards(dispute, majority_vote)
    
    def _distribute_rewards(self, dispute: Dispute, majority_vote: VoteOption):
        """分配奖励和惩罚"""
        total_staked = sum(j.staked_amount for j in dispute.jurors)
        reward_pool = total_staked * self.MAJORITY_REWARD_RATE
        
        majority_jurors = [j for j in dispute.jurors if j.vote == majority_vote]
        minority_jurors = [j for j in dispute.jurors if j.vote and j.vote != majority_vote]
        
        print(f"\n[Arbitration] 奖励分配:")
        
        # 奖励多数派
        if majority_jurors:
            reward_per_juror = reward_pool / len(majority_jurors)
            for juror in majority_jurors:
                print(f"  ✅ {juror.id}: +{reward_per_juror:.2f} ATN")
        
        # 惩罚少数派
        for juror in minority_jurors:
            slash_amount = juror.staked_amount * self.SLASH_PERCENTAGE
            print(f"  ❌ {juror.id}: -{slash_amount:.2f} ATN (SLASHED)")
    
    def get_dispute(self, dispute_id: str) -> Optional[Dispute]:
        """获取争议信息"""
        return self.disputes.get(dispute_id)

# 测试
if __name__ == "__main__":
    engine = ArbitrationEngine()
    
    # 创建争议
    dispute = engine.create_dispute(
        task_id="TASK_001",
        complainant_id="buyer_001",
        respondent_id="seller_001",
        reason="Flight link returns 404",
        escrow_amount=0.1,
        evidence={"screenshot": "404.png"}
    )
    
    # 模拟投票
    secrets = {"juror_001": "secret_a", "juror_002": "secret_b", "juror_003": "secret_c"}
    
    # 提交承诺
    for juror in dispute.jurors:
        vote = VoteOption.FRAUD if juror.id != "juror_003" else VoteOption.HONEST
        vote_hash = hashlib.sha256(f"{juror.id}{vote.value}{secrets[juror.id]}".encode()).hexdigest()[:16]
        engine.commit_vote(dispute.id, juror.id, vote_hash)
    
    # 揭示投票
    for juror in dispute.jurors:
        vote = VoteOption.FRAUD if juror.id != "juror_003" else VoteOption.HONEST
        engine.reveal_vote(dispute.id, juror.id, vote, secrets[juror.id])
    
    print("\n[Arbitration] 测试完成")
