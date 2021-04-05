import request from '@/utils/request'

// 获取异常分析数据
export function getAnomalAnalysis() {
  return request({
    url: '/anomaly_analysis/getAnomalAnalysis/',
    method: 'get'
  })
}
// 获取异常分析页面今日统计数据
export function getAllCountDataOfTodayData() {
  return request({
    url: '/anomaly_analysis/getTodayData/',
    method: 'get'
  })
}

