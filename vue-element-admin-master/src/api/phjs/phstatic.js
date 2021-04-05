import request from '@/utils/request'
// 获取静态数据，包括CPU、内存磁盘
export function getStaticData() {
  return request({
    url: '/static/getStaticData/',
    method: 'get'
  })
}
