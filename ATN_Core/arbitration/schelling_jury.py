import hashlib
import json
import random
from typing import Dict, List, Tuple
from enum import Enum

class VoteOption(Enum):
    """投票选项"""
    VALID = "valid"           # 交易有效
    INVALID = "invalid"       # 交易无效（欺诈）
    ABSTAIN = "abstain"       # 弃权

class JuryVote:
    """
    谢林点仲裁逻辑
    实现3个裁判Agent的多数派投票和少数派质押没收
    """
    
    # 质押要求
    JUROR_STAKE_REQUIRED = 0.1  # 每个裁判需要质押的SOL数量
    
    def __init__(self):
        self.jurors: Dict[str, dict] = {}  # juror_id -> juror_data
        self.disputes: Dict[str, dict] = {}  # dispute_id -> dispute_data
    
    def register_juror(self, juror_id: str, public_key: str, stake_amount: float) -> bool:
        """
        注册裁判Agent
        需要质押指定数量的SOL
        """
        if stake_amount < self.JUROR_STAKE_REQUIRED:
            print(f"[JuryVote] 错误: 质押金额不足，需要 {self.JUROR_STAKE_REQUIRED} SOL")
            return False
        
        self.jurors[juror_id] = {
            "juror_id": juror_id,
            "public_key": public_key,
            "stake_amount": stake_amount,
            "total_cases": 0,
            "correct_votes": 0,
            "slashed_amount": 0.0,
            "status": "active"
        }
        
        print(f"[JuryVote] 裁判 {juror_id} 已注册，质押: {stake_amount} SOL")
        return True
    
    def initiate_dispute(
        self,
        task_id: str,
        complainant_id: str,
        respondent_id: str,
        dispute_reason: str,
        evidence: dict
    ) -> str:
        """
        发起仲裁争议
        """
        dispute_id = f"DISPUTE_{task_id}"
        
        # 随机选择3个裁判
        available_jurors = list(self.jurors.keys())
        if len(available_jurors) < 3:
            raise ValueError("可用裁判数量不足，至少需要3个裁判")
        
        selected_jurors = random.sample(available_jurors, 3)
        
        dispute_data = {
            "dispute_id": dispute_id,
            "task_id": task_id,
            "complainant_id": complainant_id,  # 投诉方
            "respondent_id": respondent_id,    # 被投诉方
            "dispute_reason": dispute_reason,
            "evidence": evidence,
            "jurors": selected_jurors,
            "votes": {},  # juror_id -> vote
            "status": "voting",  # voting, resolved
            "result": None,
            "resolution_time": None
        }
        
        self.disputes[dispute_id] = dispute_data
        
        print(f"[JuryVote] 争议已发起: {dispute_id}")
        print(f"[JuryVote] 投诉方: {complainant_id}, 被投诉方: {respondent_id}")
        print(f"[JuryVote] 选定裁判: {selected_jurors}")
        
        return dispute_id
    
    def cast_vote(self, dispute_id: str, juror_id: str, vote: VoteOption) -> bool:
        """
        裁判投票
        """
        if dispute_id not in self.disputes:
            print(f"[JuryVote] 错误: 争议 {dispute_id} 不存在")
            return False
        
        dispute = self.disputes[dispute_id]
        
        if dispute["status"] != "voting":
            print(f"[JuryVote] 错误: 争议状态为 {dispute['status']}, 无法投票")
            return False
        
        if juror_id not in dispute["jurors"]:
            print(f"[JuryVote] 错误: {juror_id} 不是此争议的指定裁判")
            return False
        
        if juror_id in dispute["votes"]:
            print(f"[JuryVote] 错误: {juror_id} 已经投过票")
            return False
        
        dispute["votes"][juror_id] = vote
        print(f"[JuryVote] 裁判 {juror_id} 投票: {vote.value}")
        
        # 检查是否所有裁判都已投票
        if len(dispute["votes"]) == len(dispute["jurors"]):
            self._resolve_dispute(dispute_id)
        
        return True
    
    def _resolve_dispute(self, dispute_id: str):
        """
        解决争议
        实现多数派获胜、少数派没收质押的博弈算法
        """
        dispute = self.disputes[dispute_id]
        votes = dispute["votes"]
        
        # 统计投票
        vote_counts = {option: 0 for option in VoteOption}
        for vote in votes.values():
            vote_counts[vote] += 1
        
        # 确定多数派结果（排除弃权）
        valid_votes = {k: v for k, v in vote_counts.items() if k != VoteOption.ABSTAIN}
        
        if not valid_votes:
            print(f"[JuryVote] 错误: 没有有效投票")
            return
        
        majority_vote = max(valid_votes, key=valid_votes.get)
        majority_count = valid_votes[majority_vote]
        
        # 确定获胜方
        if majority_vote == VoteOption.VALID:
            # 交易有效，投诉方败诉
            winner = dispute["respondent_id"]
            loser = dispute["complainant_id"]
            result_description = "交易有效，投诉不成立"
        else:
            # 交易无效，投诉方胜诉
            winner = dispute["complainant_id"]
            loser = dispute["respondent_id"]
            result_description = "交易无效，投诉成立"
        
        # 更新争议状态
        dispute["status"] = "resolved"
        dispute["result"] = {
            "winner": winner,
            "loser": loser,
            "majority_vote": majority_vote.value,
            "vote_counts": {k.value: v for k, v in vote_counts.items()},
            "description": result_description
        }
        
        print(f"\n[JuryVote] 争议已解决: {dispute_id}")
        print(f"[JuryVote] 投票结果: {dict((k.value, v) for k, v in vote_counts.items())}")
        print(f"[JuryVote] 多数派决定: {majority_vote.value}")
        print(f"[JuryVote] 结果: {result_description}")
        
        # 处理质押奖励和惩罚
        self._distribute_stakes(dispute_id, majority_vote)
    
    def _distribute_stakes(self, dispute_id: str, majority_vote: VoteOption):
        """
        分配质押
        多数派获得奖励，少数派被没收质押
        """
        dispute = self.disputes[dispute_id]
        votes = dispute["votes"]
        
        majority_jurors = []
        minority_jurors = []
        
        for juror_id, vote in votes.items():
            if vote == majority_vote:
                majority_jurors.append(juror_id)
            elif vote != VoteOption.ABSTAIN:
                minority_jurors.append(juror_id)
            
            # 更新裁判统计数据
            self.jurors[juror_id]["total_cases"] += 1
            if vote == majority_vote:
                self.jurors[juror_id]["correct_votes"] += 1
        
        print(f"\n[JuryVote] 质押分配:")
        print(f"[JuryVote] 多数派裁判: {majority_jurors}")
        print(f"[JuryVote] 少数派裁判: {minority_jurors}")
        
        # 计算奖励
        if minority_jurors:
            total_slashed = len(minority_jurors) * self.JUROR_STAKE_REQUIRED
            reward_per_majority = total_slashed / len(majority_jurors) if majority_jurors else 0
            
            for juror_id in minority_jurors:
                self.jurors[juror_id]["slashed_amount"] += self.JUROR_STAKE_REQUIRED
                print(f"[JuryVote] 裁判 {juror_id} 被没收质押: {self.JUROR_STAKE_REQUIRED} SOL")
            
            for juror_id in majority_jurors:
                print(f"[JuryVote] 裁判 {juror_id} 获得奖励: {reward_per_majority:.4f} SOL")
        else:
            print(f"[JuryVote] 所有裁判意见一致，无质押没收")
    
    def get_dispute_result(self, dispute_id: str) -> dict:
        """获取争议结果"""
        return self.disputes.get(dispute_id)

if __name__ == "__main__":
    # 测试谢林点仲裁逻辑
    jury = JuryVote()
    
    # 注册3个裁判
    jury.register_juror("juror_001", "pk_001", 0.1)
    jury.register_juror("juror_002", "pk_002", 0.1)
    jury.register_juror("juror_003", "pk_003", 0.1)
    
    # 发起争议
    dispute_id = jury.initiate_dispute(
        task_id="task_001",
        complainant_id="buyer_001",
        respondent_id="seller_001",
        dispute_reason="提供的机票链接无效",
        evidence={"screenshot": "link_to_image", "timestamp": "2026-03-16T10:00:00Z"}
    )
    
    # 模拟投票
    # 场景1: 2票认为无效，1票认为有效（投诉成立）
    jury.cast_vote(dispute_id, "juror_001", VoteOption.INVALID)
    jury.cast_vote(dispute_id, "juror_002", VoteOption.INVALID)
    jury.cast_vote(dispute_id, "juror_003", VoteOption.VALID)
    
    print("\n最终争议结果:")
    print(json.dumps(jury.get_dispute_result(dispute_id), indent=2))
