# ATN Protocol 性能监控工具

import time
import json
from typing import Dict, List
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class PerformanceMetrics:
    """性能指标"""
    operation: str
    start_time: float
    end_time: float
    success: bool
    metadata: Dict
    
    @property
    def duration_ms(self) -> float:
        return (self.end_time - self.start_time) * 1000

class ATNPerformanceMonitor:
    """ATN协议性能监控器"""
    
    def __init__(self):
        self.metrics: List[PerformanceMetrics] = []
        self.operation_counts = defaultdict(int)
        self.operation_times = defaultdict(list)
    
    def record_operation(self, operation: str, success: bool, metadata: Dict = None):
        """记录操作性能"""
        self.operation_counts[operation] += 1
        if metadata and 'duration_ms' in metadata:
            self.operation_times[operation].append(metadata['duration_ms'])
    
    def get_stats(self) -> Dict:
        """获取性能统计"""
        stats = {}
        for op, times in self.operation_times.items():
            if times:
                stats[op] = {
                    'count': len(times),
                    'avg_ms': sum(times) / len(times),
                    'min_ms': min(times),
                    'max_ms': max(times),
                    'total_ms': sum(times)
                }
        return stats
    
    def print_report(self):
        """打印性能报告"""
        print("\n" + "="*60)
        print("ATN Protocol 性能报告")
        print("="*60)
        
        stats = self.get_stats()
        for op, data in stats.items():
            print(f"\n{op}:")
            print(f"  调用次数: {data['count']}")
            print(f"  平均耗时: {data['avg_ms']:.2f} ms")
            print(f"  最小耗时: {data['min_ms']:.2f} ms")
            print(f"  最大耗时: {data['max_ms']:.2f} ms")
            print(f"  总耗时: {data['total_ms']:.2f} ms")
        
        print("\n" + "="*60)

class ATNCache:
    """简单缓存系统"""
    
    def __init__(self, ttl_seconds: int = 300):
        self.cache = {}
        self.ttl = ttl_seconds
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str) -> any:
        """获取缓存"""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                self.hits += 1
                return value
            else:
                del self.cache[key]
        self.misses += 1
        return None
    
    def set(self, key: str, value: any):
        """设置缓存"""
        self.cache[key] = (value, time.time())
    
    def get_stats(self) -> Dict:
        """获取缓存统计"""
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        return {
            'size': len(self.cache),
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': f"{hit_rate*100:.1f}%"
        }

# 使用示例
if __name__ == "__main__":
    monitor = ATNPerformanceMonitor()
    cache = ATNCache(ttl_seconds=60)
    
    # 模拟操作
    for i in range(100):
        start = time.time()
        # 模拟缓存查询
        result = cache.get(f"key_{i % 10}")
        if not result:
            cache.set(f"key_{i % 10}", f"value_{i}")
        end = time.time()
        
        monitor.record_operation(
            "cache_lookup",
            True,
            {'duration_ms': (end - start) * 1000}
        )
    
    monitor.print_report()
    print("\n缓存统计:", cache.get_stats())
