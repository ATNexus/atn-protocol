use anchor_lang::prelude::*;
use anchor_spl::token::{TokenAccount};
use solana_program::hash::hash;

/// Proof Validator - 交付证明验证器 (Rust实现)
/// 对应Python: ATN_Core/validation/proof_validator_v2.py

#[derive(AnchorSerialize, AnchorDeserialize, Clone)]
pub struct FlightProof {
    pub task_id: String,
    pub price: u64,              // 以美分存储，避免浮点
    pub airline: String,
    pub flight_number: String,
    pub booking_url: String,
    pub departure_time: i64,
    pub arrival_time: i64,
    pub evidence_hash: [u8; 32],
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone)]
pub struct MarketDataPoint {
    pub route: String,
    pub avg_price: u64,          // 美分
    pub min_price: u64,
    pub max_price: u64,
    pub timestamp: i64,
    pub source: String,          // amadeus, skyscanner, expedia
}

pub struct MarketOracle;

impl MarketOracle {
    /// 5% 偏差容忍度 (以基点表示: 500 = 5%)
    pub const TOLERANCE_BPS: u64 = 500;
    
    /// 验证价格是否在合理范围内
    pub fn validate_price(
        submitted_price: u64,
        route: &str,
        market_data: &[MarketDataPoint]
    ) -> Result<PriceValidationResult> {
        // 筛选对应航线的市场数据
        let route_data: Vec<&MarketDataPoint> = market_data
            .iter()
            .filter(|d| d.route == route)
            .collect();
        
        if route_data.is_empty() {
            return Err(ATNError::NoMarketData.into());
        }
        
        // 计算市场共识价格
        let consensus_avg = route_data.iter().map(|d| d.avg_price).sum::<u64>() 
            / route_data.len() as u64;
        let consensus_min = route_data.iter().map(|d| d.min_price).min().unwrap();
        let consensus_max = route_data.iter().map(|d| d.max_price).max().unwrap();
        
        // 计算偏差 (基点)
        let deviation = if submitted_price > consensus_avg {
            ((submitted_price - consensus_avg) * 10000) / consensus_avg
        } else {
            ((consensus_avg - submitted_price) * 10000) / consensus_avg
        };
        
        let within_tolerance = deviation <= Self::TOLERANCE_BPS;
        let within_range = submitted_price >= consensus_min 
            && submitted_price <= consensus_max;
        
        // 计算置信度 (0-10000)
        let confidence = if within_tolerance && within_range {
            // 偏差越小，置信度越高
            10000 - (deviation * 2)
        } else if within_range {
            5000 - deviation
        } else {
            0
        };
        
        Ok(PriceValidationResult {
            valid: within_tolerance && within_range,
            submitted_price,
            consensus_avg,
            consensus_min,
            consensus_max,
            deviation_bps: deviation,
            tolerance_bps: Self::TOLERANCE_BPS,
            within_tolerance,
            within_market_range: within_range,
            confidence: confidence.max(0).min(10000),
            data_sources: route_data.len() as u8,
        })
    }
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone)]
pub struct PriceValidationResult {
    pub valid: bool,
    pub submitted_price: u64,
    pub consensus_avg: u64,
    pub consensus_min: u64,
    pub consensus_max: u64,
    pub deviation_bps: u64,      // 基点 (100 = 1%)
    pub tolerance_bps: u64,
    pub within_tolerance: bool,
    pub within_market_range: bool,
    pub confidence: u64,         // 0-10000
    pub data_sources: u8,
}

pub struct ProofValidator;

impl ProofValidator {
    pub const REQUIRED_FIELDS: [&'static str; 7] = [
        "task_id", "price", "airline", 
        "flight_number", "booking_url", "evidence_hash"
    ];
    
    /// 验证机票证明
    pub fn validate_flight_proof(
        proof: &FlightProof,
        market_data: &[MarketDataPoint]
    ) -> Result<ValidationResult> {
        let mut checks = ValidationChecks::default();
        let mut errors: Vec<String> = vec![];
        
        // 1. 验证必需字段
        checks.has_task_id = !proof.task_id.is_empty();
        checks.has_price = proof.price > 0;
        checks.has_airline = !proof.airline.is_empty();
        checks.has_flight_number = !proof.flight_number.is_empty();
        checks.has_booking_url = Self::validate_url(&proof.booking_url);
        checks.has_evidence_hash = proof.evidence_hash != [0u8; 32];
        
        if !checks.has_task_id { errors.push("Missing task_id".to_string()); }
        if !checks.has_price { errors.push("Invalid price".to_string()); }
        if !checks.has_airline { errors.push("Missing airline".to_string()); }
        if !checks.has_flight_number { errors.push("Missing flight_number".to_string()); }
        if !checks.has_booking_url { errors.push("Invalid booking_url".to_string()); }
        if !checks.has_evidence_hash { errors.push("Invalid evidence_hash".to_string()); }
        
        // 2. 验证evidence_hash格式 (必须是32字节)
        checks.valid_evidence_hash = proof.evidence_hash.len() == 32;
        
        // 3. 验证价格合理性
        let route = Self::extract_route(&proof.airline, &proof.flight_number);
        let market_validation = MarketOracle::validate_price(
            proof.price,
            &route,
            market_data
        )?;
        
        checks.price_within_tolerance = market_validation.within_tolerance;
        checks.price_within_range = market_validation.within_market_range;
        
        // 4. 计算总体置信度
        let passed_checks = [
            checks.has_task_id,
            checks.has_price,
            checks.has_airline,
            checks.has_flight_number,
            checks.has_booking_url,
            checks.has_evidence_hash,
            checks.valid_evidence_hash,
            checks.price_within_tolerance,
            checks.price_within_range,
        ].iter().filter(|&&x| x).count();
        
        let total_checks = 9u64;
        let base_confidence = (passed_checks as u64 * 10000) / total_checks;
        
        // 综合市场验证置信度
        let final_confidence = (base_confidence + market_validation.confidence) / 2;
        
        // 5. 最终判定 (置信度 >= 80% 且通过所有关键检查)
        let valid = final_confidence >= 8000 
            && checks.price_within_tolerance 
            && checks.price_within_range
            && errors.is_empty();
        
        Ok(ValidationResult {
            valid,
            confidence: final_confidence,
            checks,
            market_validation,
            errors,
        })
    }
    
    /// 验证URL格式
    fn validate_url(url: &str) -> bool {
        (url.starts_with("http://") || url.starts_with("https://"))
            && url.contains('.')
            && url.len() > 10
    }
    
    /// 从航班信息提取航线 (简化版)
    fn extract_route(airline: &str, flight_number: &str) -> String {
        // 实际实现需要更复杂的逻辑
        // 这里返回模拟航线
        if flight_number.starts_with("AA") {
            "NYC-LAX".to_string()
        } else if flight_number.starts_with("BA") {
            "LON-PAR".to_string()
        } else {
            "HKG-TYO".to_string()
        }
    }
    
    /// 生成预期的evidence_hash
    pub fn generate_expected_hash(proof: &FlightProof) -> [u8; 32] {
        let data = format!(
            "{}:{}:{}:{}:{}:{}",
            proof.task_id,
            proof.price,
            proof.airline,
            proof.flight_number,
            proof.booking_url,
            proof.departure_time
        );
        hash(data.as_bytes()).to_bytes()
    }
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone, Default)]
pub struct ValidationChecks {
    pub has_task_id: bool,
    pub has_price: bool,
    pub has_airline: bool,
    pub has_flight_number: bool,
    pub has_booking_url: bool,
    pub has_evidence_hash: bool,
    pub valid_evidence_hash: bool,
    pub price_within_tolerance: bool,
    pub price_within_range: bool,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone)]
pub struct ValidationResult {
    pub valid: bool,
    pub confidence: u64,           // 0-10000
    pub checks: ValidationChecks,
    pub market_validation: PriceValidationResult,
    pub errors: Vec<String>,
}

#[error_code]
pub enum ATNError {
    #[msg("No market data available for route")]
    NoMarketData,
    #[msg("Invalid proof format")]
    InvalidProofFormat,
    #[msg("Price deviation exceeds tolerance")]
    PriceDeviationTooHigh,
}

// =============================================================================
// 测试模块
// =============================================================================

#[cfg(test)]
mod tests {
    use super::*;
    
    fn create_test_market_data() -> Vec<MarketDataPoint> {
        vec![
            MarketDataPoint {
                route: "NYC-LAX".to_string(),
                avg_price: 45000,      // $450.00
                min_price: 38000,
                max_price: 62000,
                timestamp: 1699900000,
                source: "amadeus".to_string(),
            },
            MarketDataPoint {
                route: "NYC-LAX".to_string(),
                avg_price: 46500,
                min_price: 39000,
                max_price: 64000,
                timestamp: 1699900000,
                source: "skyscanner".to_string(),
            },
        ]
    }
    
    #[test]
    fn test_valid_proof() {
        let market_data = create_test_market_data();
        
        let proof = FlightProof {
            task_id: "TASK_001".to_string(),
            price: 46500,            // $465.00, 在5%容忍度内
            airline: "American Airlines".to_string(),
            flight_number: "AA101".to_string(),
            booking_url: "https://aa.com/book/ABC123".to_string(),
            departure_time: 1699900000,
            arrival_time: 1699903600,
            evidence_hash: [1u8; 32],
        };
        
        let result = ProofValidator::validate_flight_proof(&proof, &market_data).unwrap();
        
        assert!(result.valid);
        assert!(result.confidence >= 8000);
        assert!(result.checks.price_within_tolerance);
    }
    
    #[test]
    fn test_invalid_price() {
        let market_data = create_test_market_data();
        
        let proof = FlightProof {
            task_id: "TASK_002".to_string(),
            price: 10000,            // $100.00, 远低于市场价
            airline: "American Airlines".to_string(),
            flight_number: "AA102".to_string(),
            booking_url: "https://fake.com".to_string(),
            departure_time: 1699900000,
            arrival_time: 1699903600,
            evidence_hash: [2u8; 32],
        };
        
        let result = ProofValidator::validate_flight_proof(&proof, &market_data).unwrap();
        
        assert!(!result.valid);
        assert!(!result.checks.price_within_range);
    }
}
