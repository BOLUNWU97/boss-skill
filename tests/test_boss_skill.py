#!/usr/bin/env python3
"""
Boss Skill Test Suite
Comprehensive tests for all components
"""

import pytest
import json
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.evolution_logger import EvolutionLogger
from tools.pattern_detector import PatternDetector
from tools.rl_feedback import RLFeedbackTracker
from tools.multi_boss_battle import MultiBossBattle
from tools.leaderboard import NightmareLeaderboard


class TestEvolutionLogger:
    """Test evolution logger functionality"""
    
    def setup_method(self):
        """Setup test environment"""
        self.test_dir = Path("/tmp/boss_test")
        self.test_dir.mkdir(exist_ok=True)
        self.logger = EvolutionLogger("test_boss", str(self.test_dir))
    
    def test_log_correction(self):
        """Test logging a correction"""
        event_id = self.logger.log_correction(
            user_correction="他不说好的",
            context="方案评审",
            before="说好的",
            after="说不够好"
        )
        assert event_id is not None
        assert "correction" in event_id
    
    def test_get_corrections(self):
        """Test retrieving corrections"""
        self.logger.log_correction("test", "context", "before", "after")
        corrections = self.logger.get_corrections()
        assert len(corrections) >= 1
    
    def test_create_version(self):
        """Test creating a version snapshot"""
        # Create test files
        boss_dir = self.test_dir / "test_boss"
        boss_dir.mkdir(parents=True, exist_ok=True)
        (boss_dir / "SKILL.md").write_text("# Test")
        
        event_id = self.logger.create_version("v1.0", "test version")
        assert event_id is not None


class TestPatternDetector:
    """Test pattern detector functionality"""
    
    def setup_method(self):
        """Setup test environment"""
        self.detector = PatternDetector("test")
    
    def test_analyze_conversation(self):
        """Test conversation analysis"""
        conversation = [
            {"role": "boss", "content": "这个方案 impact 是什么？数据呢？"},
            {"role": "boss", "content": "不够好。重写。"},
            {"role": "user", "content": "好的老板。"},
        ]
        
        result = self.detector.analyze_conversation(conversation)
        
        assert result["total_boss_messages"] == 2
        assert result["pressure_index"] >= 0
        assert "质疑追问" in result["detected_patterns"]
        assert "直接否定" in result["detected_patterns"]
    
    def test_pressure_index_calculation(self):
        """Test pressure index calculation"""
        conversation = [
            {"role": "boss", "content": "impact 是什么？数据呢？为什么？"},
            {"role": "boss", "content": "不够好！不行！重做！"},
        ] * 5
        
        result = self.detector.analyze_conversation(conversation)
        
        assert result["pressure_index"] >= 5.0  # Should be high pressure
    
    def test_new_pattern_detection(self):
        """Test detecting new patterns"""
        conversation = [
            {"role": "boss", "content": "impact 是什么？这是第N次问你了。"},
            {"role": "boss", "content": "impact 是什么？同样的问题。"},
            {"role": "boss", "content": "impact 是什么？又说一遍。"},
        ]
        
        result = self.detector.analyze_conversation(conversation)
        assert len(result["new_patterns"]) >= 0


class TestRLFeedbackTracker:
    """Test RL feedback tracker"""
    
    def setup_method(self):
        """Setup test environment"""
        self.test_dir = Path("/tmp/boss_test")
        self.test_dir.mkdir(exist_ok=True)
        self.tracker = RLFeedbackTracker("test_boss", str(self.test_dir))
    
    def test_record_action(self):
        """Test recording an action with reward"""
        entry = self.tracker.record_action(
            action_type="追问",
            context="方案被质疑",
            user_reaction="对抗",
            reward=0.8
        )
        
        assert entry["reward"] == 0.8
        assert entry["cumulative_score"] == 0.8
    
    def test_behavior_grade(self):
        """Test getting behavior grade"""
        self.tracker.record_action("追问", "c", "r", 0.9)
        self.tracker.record_action("追问", "c", "r", 0.7)
        
        grade = self.tracker.get_behavior_grade("追问")
        
        assert grade["count"] == 2
        assert grade["score"] >= 0.7
    
    def test_suggest_actions(self):
        """Test getting action suggestions"""
        # Record multiple actions
        for _ in range(5):
            self.tracker.record_action("追问", "c", "r", 0.8)
        
        suggestions = self.tracker.suggest_actions()
        assert len(suggestions) >= 1


class TestMultiBossBattle:
    """Test multi-boss battle system"""
    
    def setup_method(self):
        """Setup test environment"""
        self.test_dir = Path("/tmp/boss_test/bosses")
        self.test_dir.mkdir(parents=True, exist_ok=True)
        
        # Create test boss
        boss_dir = self.test_dir / "test_wang"
        boss_dir.mkdir(parents=True, exist_ok=True)
        meta = {
            "name": "测试老板",
            "slug": "test_wang",
            "tags": {
                "nightmare_level": "4.5/5",
                "management_style": ["高控型"]
            }
        }
        (boss_dir / "meta.json").write_text(json.dumps(meta))
        
        self.battle = MultiBossBattle(str(self.test_dir.parent))
    
    def test_list_bosses(self):
        """Test listing available bosses"""
        bosses = self.battle.list_bosses()
        assert len(bosses) >= 1
    
    def test_create_battle(self):
        """Test creating a battle"""
        battle = self.battle.create_battle(
            user_profile="小王",
            boss_slugs=["test_wang"],
            goal="争取晋升",
            tension_level="high"
        )
        
        assert "battle_id" in battle
        assert battle["goal"] == "争取晋升"
    
    def test_simulate_round(self):
        """Test simulating a battle round"""
        battle = self.battle.create_battle(
            "小王", ["test_wang"], "争取晋升"
        )
        
        result = self.battle.simulate_round(battle, "老板我想晋升")
        
        assert result["round"] == 1
        assert len(result["boss_responses"]) >= 1


class TestLeaderboard:
    """Test nightmare leaderboard"""
    
    def setup_method(self):
        """Setup test environment"""
        self.test_dir = Path("/tmp/boss_test")
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.lb = NightmareLeaderboard(str(self.test_dir))
    
    def test_submit_boss(self):
        """Test submitting a boss"""
        entry = self.lb.submit_boss(
            name="测试老板",
            company="测试公司",
            nightmare_level=4.5,
            description="测试描述"
        )
        
        assert entry["nightmare_level"] == 4.5
        assert entry["votes"] == 0
    
    def test_vote_boss(self):
        """Test voting for a boss"""
        entry = self.lb.submit_boss("老板", "公司", 4.0)
        boss_id = entry["id"]
        
        success = self.lb.vote_boss(boss_id, "user1")
        assert success == True
        
        # Second vote should fail
        success = self.lb.vote_boss(boss_id, "user1")
        assert success == False
    
    def test_statistics(self):
        """Test getting statistics"""
        self.lb.submit_boss("老板1", "公司1", 3.5)
        self.lb.submit_boss("老板2", "公司2", 4.5)
        
        stats = self.lb.get_statistics()
        
        assert stats["total_bosses"] == 2
        assert stats["avg_nightmare"] >= 3.5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
