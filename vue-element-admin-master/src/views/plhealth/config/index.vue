<template>
  <div>
    <ten-loading
      text="统计模块数据中..."
      :loading="loading"
    >
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card class="box-card card-base-chart">
            <div slot="header">
              <el-row :gutter="20">
                <el-col :span="12">
                  <h3>模块管理</h3>
                </el-col>
                <el-col :span="12">
                  <el-button
                    type="primary"
                    size="small"
                    icon="el-icon-plus"
                    :disabled="!count_over"
                    @click="showAddModal=true"
                  >
                    添加更多模块
                  </el-button>
                  <el-button
                    type="primary"
                    size="small"
                    icon="el-icon-minus"
                    :disabled="!count_over"
                    @click="showDeleteModal=true"
                  >
                    删除所选模块
                  </el-button>
                </el-col>
              </el-row>
            </div>
            <div>
              <el-table
                ref="multipleTable"
                :data="moduleTableData"
                tooltip-effect="dark"
                style="width: 100%"
                @selection-change="moduleOnSelectedChange"
              >
                <el-table-column
                  type="selection"
                />
                <el-table-column
                  label="ID"
                  prop="id"
                  width="140"
                />
                <el-table-column
                  label="模块名"
                  prop="module"
                  width="300"
                />
                <el-table-column
                  label="是否统计完成"
                  prop="is_done"
                  :formatter="formatIsDone"
                  width="140"
                />
              </el-table>
            </div>
          </el-card>
        </el-col>

        <el-col :span="12">
          <el-card class="box-card card-base-chart">
            <div slot="header">
              <el-row :gutter="20">
                <el-col :span="12">
                  <h3>利用率采集配置</h3>
                </el-col>
                <el-col :span="12">
                  <el-select
                    v-model="useRatioType"
                    style="width:50%;"
                    placeholder="请选择"
                    @change="useRatioTypeChange"
                  >
                    <el-option
                      v-for="(item, index) in useRatioTypeList"
                      :key="index"
                      :label="item.label"
                      :value="item.value"
                    />
                  </el-select>
                </el-col>
              </el-row>
            </div>
            <div>
              <el-table
                ref="multipleTable"
                :data="useRatioData"
                tooltip-effect="dark"
                style="width: 100%"
              >
                <el-table-column
                  :label="computeTitle('开始值')"
                  prop="start"
                  width="80"
                />
                <el-table-column
                  :label="computeTitle('结束值')"
                  width="80"
                  prop="stop"
                />
                <el-table-column
                  label="配置项"
                  prop="type"
                />
                <el-table-column
                  label="高负载"
                  prop="is_high_load"
                  :formatter="formatLoad"
                />
                <el-table-column
                  label="低负载"
                  prop="is_low_load"
                  :formatter="formatLoad"
                />
                <el-table-column
                  label="操作"
                  align="center"
                  width="300"
                >
                  <template slot-scope="scope">
                    <el-button type="text" style="width:70px" icon="edit" size="small" @click="editPre(scope.row)">编辑</el-button>
                    <el-button type="text" style="width:70px" icon="add" size="small" @click.native.prevent="addPre(scope.$index)">添加</el-button>
                    <el-button type="text" style="width:70px" icon="delete" size="small" @click.native.prevent="deletePre(scope.$index, useRatioData)">删除</el-button>
                    <!-- <ten-button type="text" icon="delete" size="small" @click="deletePre(scope.row)">删除</ten-button> -->

                  </template>
                </el-table-column>
              </el-table>

            </div>
            <div class="div-right">
              <el-button
                type="danger"
                icon="el-icon-close"
                @click="clearUseRangeData"
              >
                不保存
              </el-button>
              <el-button
                type="success"
                icon="el-icon-check"
                :disabled="!count_over"
                @click="saveUseRangeData"
              >
                保存
              </el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </ten-loading>

    <el-dialog
      title="选择要添加的模块"
      :visible.sync="showAddModal"
      :width="800"
      style="height:1000px"
    >
      <div style="width:600px;height:200px">
        <el-select
          v-model="addModules"
          multiple
          collapse-tags
          style="width: 600px"
          size="medium"
          placeholder="请选择"
        >
          <el-option
            v-for="item in allModules"
            :key="item"
            :label="item"
            :value="item"
          />
        </el-select>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showAddModal = false">取 消</el-button>
        <el-button type="primary" @click="showConfirmModal=true">确 定</el-button>
      </span>
    </el-dialog>

    <el-dialog
      title="确认添加这些模块吗？"
      :visible.sync="showConfirmModal"
      :width="400"
    >
      <div>
        <p>将会在后台执行数据统计，这段时间内不能再修改或删除模块！</p>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showConfirmModal = false">取 消</el-button>
        <el-button type="primary" @click="confirmAddModules">确 定</el-button>
      </span>
    </el-dialog>

    <el-dialog
      title="确认删除所选的模块吗？"
      :visible.sync="showDeleteModal"
      :width="400"
    >
      <div>
        <p>将会在后台执行数据统计，这段时间内不能再修改或删除模块！</p>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showDeleteModal = false">取 消</el-button>
        <el-button type="primary" @click="confirmDeleteModules">确 定</el-button>
      </span>
    </el-dialog>

    <el-dialog
      title="确认添加保存配置信息吗？"
      :visible.sync="showConfirmUseRangeModal"
      :width="400"
    >
      <div>
        <p>将会执行一段时间去统计数据！</p>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showConfirmUseRangeModal = false">取 消</el-button>
        <el-button type="primary" @click="confirmSaveUseRange">确 定</el-button>
      </span>
    </el-dialog>

    <UseRangeForm ref="useRangeForm" @addUseRange="addUseRangeData" @updateUseRangeTable="getUseRangeData" />

  </div>
</template>
<script>
import * as PHConfig from '@/api/phjs/config.js'
import UseRangeForm from './useRangeForm'
export default {
  name: 'Psstaticdata',
  components: {
    UseRangeForm
  },
  data() {
    return {
      count_over: true,
      moduleTableData: [
        {
          'id': 1,
          'module': '模块1',
          'is_done': 1
        }
      ],
      defineModules: [],
      personList: [],
      moduleSelectedRowKeys: [],
      current: 1,
      showAddModal: false,
      showDeleteModal: false,
      showConfirmModal: false,
      showConfirmUseRangeModal: false,
      addModules: [],
      allModules: [
        '模块1',
        '模块2',
        '模块3',
        '模块4',
        '模块5',
        '模块6',
        '模块7',
        '模块8'
      ],
      loading: false,
      // 利用率配置
      useRatioData: [
        {
          'start': 0,
          'stop': 20,
          'type': 'cpu',
          'is_high_load': 0,
          'is_low_load': 1
        }
      ],
      useRatioType: 'cpu',
      useRatioTypeList: [
        {
          value: 'cpu',
          label: 'CPU利用率范围配置'
        },
        {
          value: 'mem',
          label: '内存利用率范围配置'
        },
        {
          value: 'eth0_in',
          label: 'eth0入流量范围配置'
        },
        {
          value: 'eth0_out',
          label: 'eth0出流量范围配置'
        }
      ],
      titlePrompt: ['百分比', 'M']

    }
  },
  computed: {
    computeTitle() {
      return function(pre) {
        if (this.useRatioType === 'cpu' || this.useRatioType === 'mem') {
          return pre + '(百分比)'
        } else {
          return pre + '(M)'
        }
      }
    }
  },
  mounted() {
    this.isCountOver()
  },
  methods: {
    // 格式化输出
    formatIsDone(row, column) {
      // console.log(row.is_done)
      if (row.is_done === 0) return '否'
      else return '是'
    },
    // 添加一行的数据
    addUseRangeData(index, newRowData) {
      this.useRatioData.splice(index, 0, newRowData)
    },
    // 点击不保存，清空编辑的数据
    clearUseRangeData() {
      this.getUseRangeData()
    },
    confirmSaveUseRange() {
      const res = this.validUseRange()
      if (res.flag) {
        const saveData = {
          type: this.useRatioType,
          data: this.useRatioData
        }
        this.loading = true
        PHConfig.saveUseRangeData({ saveData }).then(res => {
          if (res.code === 20000) {
            this.getUseRangeData()
            this.loading = false
          } else {
            this.$message({
              type: 'warning',
              message: res.msg
            })
          }
        }).catch(e => {
          console.log(e)
        })
      } else {
        this.$message({
          type: 'error',
          message: res.info
        })
        this.getUseRangeData()
      }
    },
    // 确认保存事件、保存编辑后的数据
    saveUseRangeData() {
      this.showConfirmUseRangeModal = true
    },
    // 校验利用率数据是否合理
    validUseRange(callback) {
      let flag = true
      let info = '格式正确！'
      const data = this.useRatioData
      if (this.useRatioType === 'cpu' || this.useRatioType === 'mem') {
        if (data[0].start !== 0 || data[data.length - 1].stop !== 100) {
          flag = false
          info = '必须以0开始且以100结束！'
        }
        for (let i = 1; i < data.length; i++) {
          if (data[i - 1].stop !== (data[i].start)) {
            flag = false
            info = '请输入连续的数字！'
          }
        }
      } else if (this.useRatioType === 'eth0_in' || this.useRatioType === 'eth0_out') {
        console.log(1)
      }
      if (data[0].is_high_load === 1 || data[data.length - 1].is_low_load === 1) {
        flag = false
        info = '高负载或低负载配置错误！'
      }
      return { flag, info }
      // callback({ flag, info })
    },

    // 格式化输出，0表示否，1表示是
    formatLoad(row, column) {
      if (column.label === '高负载') {
        if (row.is_high_load === 0) return '否'
        else return '是'
      } else {
        if (row.is_low_load === 0) return '否'
        else return '是'
      }
    },
    // 获取利用率范围数据
    getUseRangeData() {
      PHConfig.getUseRangeData({ type: this.useRatioType }).then(res => {
        if (res.code === 20000) {
          this.useRatioData = res.data
        } else {
          this.$message({
            type: 'warning',
            message: '查询失败！'
          })
        }
      }).catch(e => {
        console.log(e)
      })
    },
    addPre(index) {
      this.$refs['useRangeForm'].addPre(index, this.useRatioType)
    },
    editPre(row) {
      this.$refs['useRangeForm'].editPre(row, this.useRatioType)
    },
    deletePre(index, rows) {
      rows.splice(index, 1)
    },
    useRatioTypeChange() {
      this.getUseRangeData()
    },
    // 判断是否统计完成,统计完成再去查询数据
    isCountOver() {
      PHConfig.getCountStatus().then(res => {
        if (res.code === 20000) {
          if (res.data === 1) {
            this.count_over = true
          } else {
            this.count_over = false
          }
          this.getModuleList()
          this.getAllModules()
          this.getUseRangeData()
        }
      }).catch(e => {
        console.log(e)
      })
    },
    // 获取当前展示的模块的列表
    getModuleList() {
      PHConfig.getDefineModuleList().then(res => {
        if (res.code === 20000) {
          if (res.data !== null) {
            this.moduleTableData = res.data
            // this.defineModules = res.data
            for (let i = 0; i < res.data.length; i++) {
              this.defineModules.push(res.data[i].module)
            }
          } else {
            this.defineModules = []
            this.addModules = []
            this.moduleTableData = []
          }
        }
      }).catch(e => {
        // if (this.defineModules.length === 0) {
        //   this.$message.warning({
        //     message: '尚未定义模块'
        //   })
        // } else {
        //   this.$message.error({
        //     message: '查询失败'
        //   })
        // }
        //
        // console.log(e)
        // this.chartHideLoad()
      })
    },
    getAllModules() {
      PHConfig.getAllModuleList().then(res => {
        if (res.code === 20000) {
          this.allModules = res.data
        }
      }).catch(e => {
        this.$message.error({
          message: '查询失败'
        })
        console.log(e)
        this.chartHideLoad()
      })
    },
    moduleOnSelectedChange(keys, selections) {
      this.moduleSelectedRowKeys = keys
    },
    // 确认删除模块
    confirmDeleteModules() {
      if (this.moduleSelectedRowKeys.length === 0) {
        this.$message({
          type: 'warning',
          message: '请先选择要删除的模块！'
        })
      } else {
        this.loading = true
        PHConfig.deleteModules(this.moduleSelectedRowKeys).then(res => {
          if (res.code === 20000) {
            // console.log('ok')
            this.$message({
              type: 'success',
              message: '删除成功！'
            })
            this.showDeleteModal = false
            this.isCountOver()
            this.loading = false
          }
        }).catch(e => {
          this.$message.error({ message: '查询失败' })
        })
      }
    },
    // 确认添加模块
    confirmAddModules() {
      // debugger
      const realyAddModules = []
      for (let i = 0; i < this.addModules.length; i++) {
        if (this.defineModules.length === 0 || this.defineModules.indexOf(this.addModules[i]) < 0) {
          realyAddModules.push(this.addModules[i])
        }
      }
      if (realyAddModules.length === 0) {
        this.$message.warning({
          message: '选择模块已存在或未选择任何模块！'
        })
      } else {
        this.loading = true
        PHConfig.addModules(realyAddModules).then(res => {
          if (res.code === 20000) {
            this.$message({
              type: 'success',
              message: '添加成功！'
            })
            this.isCountOver()
            this.loading = false
          }
        }).catch(e => {
          this.$message.error({ message: '查询失败' })
        })
      }
    }
  }
}
</script>

<style scoped>
  .card-base-header{
    /* height:1800px; */
    margin:15px;
    width:100%;
    height:1000px;
  }
  .div-right{
    float: right;
    margin-top:20px;
    margin-right:20px;
  }
</style>
<style>
  .ten-main{
    overflow: hidden !important;
  }
</style>
