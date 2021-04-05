import request from '@/utils/request'

export function testGet() {
  return request({
    url: '/test/getUser/',
    method: 'get'
  })
}

export function getDynamicData() {
  return request({
    url: '/dynamic/getDynamicData/',
    method: 'get'
  })
}
