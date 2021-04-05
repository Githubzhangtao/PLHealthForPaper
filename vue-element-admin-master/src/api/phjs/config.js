import request from '@/utils/request'
// 获取静态数据，包括CPU、内存磁盘
export function initModuleData() {
  return request({
    url: '/config/initModuleData/',
    method: 'get'

  })
}
// 获取所有的modules
export function getAllModuleList() {
  return request({
    url: '/config/modules/getAllModuleList',
    method: 'get'
  })
}
// 添加modules到已有的module了中
export function addModules(realyAddModules) {
  return request({
    url: '/config/modules/putModules/',
    method: 'put',
    params: realyAddModules
  })
}
// 删除所选择的module
export function deleteModules(realyDeleteModules) {
  return request({
    url: '/config/modules/deleteModules/',
    method: 'delete',
    params: realyDeleteModules

  })
}
// 获取已经统计完成的的模块的列表
export function getDoneDefineModuleList() {
  return request({
    // url: '/vue-element-admin/routes',
    url: '/config/modules/getDoneDefineModuleList/',
    method: 'get'
  })
}
// 获取当前展示的模块的列表
export function getDefineModuleList() {
  return request({
    url: '/config/modules/getDefineModuleList/',
    method: 'get'

  })
}

// 获取是否统计数据完毕
export function getCountStatus() {
  return request({
    url: '/config/countStatus/',
    method: 'get'

  })
}

// 获取利用率范围配置数据
export function getUseRangeData(type) {
  return request({
    url: '/config/useRange/getUseRangeData',
    method: 'get',
    params: type
  })
}

// 保存编辑后的数据
export function saveUseRangeData(saveData) {
  return request({
    url: '/config/useRange/saveUseRangeData/',
    method: 'put',

    params: saveData
  })
}
