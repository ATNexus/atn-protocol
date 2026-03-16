import unittest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

# 从ATN_Protocol导入
from ATN_Protocol.financial_adapter.financial_envelope import FinancialEnvelope

# 从ATN_Core导入
from ATN_Core.arbitration.schelling_jury import JuryVote, VoteOption
from ATN_Core.escrow.atomic_escrow import AtomicEscrow
from ATN_Core.reputation.agent_identity import AgentIdentity

class TestFinancialEnvelope(unittest.TestCase):
    """金融信封测试"""
    
    def setUp(self):
        self.envelope = FinancialEnvelope()
    
    def test_create_envelope(self):
        """测试创建信封"""
        result = self.envelope.wrap_request({
            "source": "Claude",
            "task": "flight_search"
        }, {
            "escrow_amount_sol": 0.1,
            "slashing_penalty_sol": 0.02
        })
        
        self.assertIn("atn_task_id", result)
        self.assertIn("solana_escrow_details", result)
        self.assertEqual(result["solana_escrow_details"]["escrow_amount_sol"], 0.1)

class TestAtomicEscrow(unittest.TestCase):
    """原子托管测试"""
    
    def setUp(self):
        self.escrow = AtomicEscrow()
    
    def test_create_escrow(self):
        """测试创建托管"""
        self.escrow.deposit("buyer_001", 1.0)
        task_id = self.escrow.create_escrow(
            buyer_id="buyer_001",
            seller_id="seller_001",
            amount=0.05,
            task_description={"type": "flight_search"},
            timeout_minutes=15
        )
        self.assertIsNotNone(task_id)
        
        status = self.escrow.get_escrow_status(task_id)
        self.assertEqual(status["status"], "locked")

class TestAgentIdentity(unittest.TestCase):
    """Agent身份测试"""
    
    def setUp(self):
        self.identity = AgentIdentity()
    
    def test_register_agent(self):
        """测试注册Agent"""
        result = self.identity.handshake(
            public_key="test_pubkey",
            agent_type="flight_search"
        )
        self.assertIn("agent_id", result)
        self.assertIn("sbt_profile", result)
        self.assertEqual(result["sbt_profile"]["credit_score"], 100)

if __name__ == '__main__':
    unittest.main(verbosity=2)
