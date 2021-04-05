<template>
  <div>
    <el-row :gutter="5">
      <el-col :span="8">
        <el-card class="box-card card-base-chart" style="height: 300px">
          <div slot="header" style="height: 5px">
            <span style="color:#00bfff">已选择的模块</span>
          </div>
          <div style="margin-left:20%">
            <div v-for="(item,index) in defineModules" :key="item">
              <span v-if="index <=9" style="color:#0000ff">{{ item }}</span>
            </div>
            <el-tooltip message="查看全部">
              <h2 v-if=" defineModules.length > 10" style="color:	#0040ff;" @click="showAllModulesModal=true">......</h2>
            </el-tooltip>

          </div>
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-card class="card-base-header">
          <div slot="header" style="height: 5px">
            <span style="color:#00bfff">今日统计{{ defineModules.length }}个模块的前日异常数据</span>
          </div>
          <div>
            <el-row :gutter="10">
              <el-col :span="4">
                <el-card class="card-small-header">
                  <div slot="header" style="height: 5px">
                    <span style="color: #0040ff">高负载</span>
                  </div>
                  <div>
                    <span>cpu高负载:<span style="color: red">{{ todayData.high_load.cpu }} </span> </span><br>
                    <span>内存高负载:<span style="color: red">{{ todayData.high_load.mem }} </span> </span><br>
                    <span>网卡入流量:<span style="color: red">{{ todayData.high_load.eth0_in }} </span> </span><br>
                    <span>网卡出流量:<span style="color: red">{{ todayData.high_load.eth0_out }} </span> </span>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="4">
                <el-card class="card-small-header">
                  <div slot="header" style="height: 5px">
                    <span style="color: #0040ff">低负载</span>
                  </div>
                  <div>
                    <span>cpu低负载:<span style="color: red">{{ todayData.low_load.cpu }} </span> </span><br>
                    <span>内存低负载:<span style="color: red">{{ todayData.low_load.mem }} </span> </span><br>
                    <span>网卡入流量:<span style="color: red">{{ todayData.low_load.eth0_in }} </span> </span><br>
                    <span>网卡出流量:<span style="color: red">{{ todayData.low_load.eth0_out }} </span> </span>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="4">
                <el-card class="card-small-header">
                  <div slot="header" style="height: 5px">
                    <span style="color: #0040ff">离线设备</span>
                  </div>
                  <div>
                    <span>离线设备:<span style="color: red">{{ todayData.offline_device }} </span> </span>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="4">
                <el-card class="card-small-header">
                  <div slot="header" style="height: 5px">
                    <span style="color: #0040ff">异常剔除数</span>
                  </div>
                  <div>
                    <span>异常剔除:<span style="color: red">{{ todayData.abnormal_removal + '次' }} </span> </span><br>
                    <span>异常反复剔除:<span style="color: red">{{ todayData.abnormal_removal_repeat +'次' }} </span> </span>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="8">
                <el-card class="card-small-header">
                  <div slot="header" style="height: 5px">
                    <span style="color: #0040ff">单机告警</span>
                  </div>
                  <div>
                    <el-row :gutter="5">
                      <el-col :span="12">
                        <span>Ping告警:<span style="color: red">{{ todayData.alarm_ping_res + '次' }} </span> </span><br>
                        <span>单机流量告警:<span style="color: red">{{ todayData.alarm_flow_res +'次' }} </span> </span><br>
                        <span>单机性能告警:<span style="color: red">{{ todayData.alarm_performance_res +'次' }} </span> </span><br>
                        <span>端口告警:<span style="color: red">{{ todayData.alarm_port_res +'次' }} </span> </span><br>
                        <!--                        <span>进程端口告警:<span style="color: red">{{ todayData.alarm_process_port_res +'次' }} </span> </span>-->
                      </el-col>
                      <el-col :span="12">
                        <span>进程告警:<span style="color: red">{{ todayData.alarm_process_res +'次' }} </span> </span><br>
                        <span>上报超时告警:<span style="color: red">{{ todayData.alarm_report_time_out_res +'次' }} </span> </span><br>
                        <span>硬盘告警:<span style="color: red">{{ todayData.alarm_disk_res +'次' }} </span> </span><br>
                        <span>硬盘只读告警:<span style="color: red">{{ todayData.alarm_disk_ro_res +'次' }} </span> </span><br>
                        <span>磁盘满告警:<span style="color: red">{{ todayData.alarm_disk_ro_full_res +'次' }} </span> </span>
                      </el-col>
                    </el-row>

                  </div>
                </el-card>
              </el-col>
            </el-row>

          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog
      title="详细信息"
      :visible.sync="showAllModulesModal"
      width="1000"
      style="height:1000px"
    >
      <div style="width:800px;">
        <li v-for="(item,index) in defineModules" :key="item" style="color:#0000ff">{{ '['+index+']:  '+item }}</li>
      </div>
    </el-dialog>
    <HighLoadComponent ref="highLoadC" />
    <LowLoadComponent ref="lowLoadC" />
    <OfflineDeviceComponent ref="offlineDeviceC" />
    <AbnormalRemovalComponent ref="abnormalRemovalC" />
    <AlarmComponent ref="alarmC" />

    <!--    <el-tabs v-model="tabSelect">-->
    <!--      <el-tabs-pane-->
    <!--        label="高负载"-->
    <!--        :value="1"-->
    <!--      >-->
    <!--        <HighLoadComponent ref="highLoadC" />-->
    <!--      </el-tabs-pane>-->
    <!--      <el-tabs-pane-->
    <!--        label="低负载"-->
    <!--        :value="2"-->
    <!--      >-->
    <!--        <LowLoadComponent ref="lowLoadC" />-->
    <!--      </el-tabs-pane>-->
    <!--      <el-tabs-pane-->
    <!--        label="离线设备"-->
    <!--        :value="3"-->
    <!--      >-->
    <!--        <OfflineDeviceComponent ref="offlineDeviceC" />-->
    <!--      </el-tabs-pane>-->
    <!--      <el-tabs-pane-->
    <!--        label="异常剔除"-->
    <!--        :value="4"-->
    <!--      >-->
    <!--        <AbnormalRemovalComponent ref="abnormalRemovalC" />-->

    <!--      </el-tabs-pane>-->
    <!--      <el-tabs-pane-->
    <!--        label="单机告警"-->
    <!--        :value="5"-->
    <!--      >-->
    <!--        <AlarmComponent ref="alarmC" />-->

    <!--      </el-tabs-pane>-->

    <!--    </el-tabs>-->

  </div>
</template>
<script>
import * as PHConfig from '@/api/phjs/config.js'
import * as PHAnomalyAnalysis from '@/api/phjs/anomaly-analysis.js'
import HighLoadComponent from './highLoadComponent'
import LowLoadComponent from './lowLoadComponent'
import OfflineDeviceComponent from './offlineDeviceComponent'
import AbnormalRemovalComponent from './abnormalRemovalComponent'
import AlarmComponent from './standAloneAlarmComponent'

export default {
  name: 'PHAnomalyAnalysis',
  components: {
    HighLoadComponent,
    LowLoadComponent,
    OfflineDeviceComponent,
    AbnormalRemovalComponent,
    AlarmComponent

  },
  data() {
    return {
      tabSelect: 1,
      queryAllData: {},
      defineModules: [],
      showAllModulesModal: false,
      loading: false,
      todayData: {
        high_load: {
          'cpu': 0,
          'mem': 0,
          'eth0_in': 0,
          'eth0_out': 0
        },
        low_load: {
          'cpu': 0,
          'mem': 0,
          'eth0_in': 0,
          'eth0_out': 0
        },
        offline_device: 0,
        abnormal_removal: 0,
        abnormal_removal_repeat: 0,
        alarm_ping_res: 0,
        alarm_flow_res: 0,
        alarm_performance_res: 0,
        alarm_port_res: 0,
        alarm_process_port_res: 0,
        alarm_process_res: 0,
        alarm_report_time_out_res: 0,
        alarm_disk_res: 0,
        alarm_disk_ro_res: 0,
        alarm_disk_ro_full_res: 0
      }
    }
  },
  mounted() {
    this.initQuery()
  },
  methods: {
    // 页面创建时初始化查询
    initQuery() {
      this.getModuleList()
      this.getAllCountData()
      const that = this
      setTimeout(function() {
        that.initChart()
        that.queryData()
      }, 200)
    },
    // 初始化chart
    initChart() {
      this.$refs['highLoadC'].initChart()
      this.$refs['lowLoadC'].initChart()
      this.$refs['offlineDeviceC'].initChart()
      this.$refs['abnormalRemovalC'].initChart()
      this.$refs['alarmC'].initChart()
    },
    // 查询数据绘制图形
    queryData() {
      PHAnomalyAnalysis.getAnomalAnalysis().then(res => {
        if (res.code === 20000) {
          this.queryAllData = res.data
          this.drawChart()
        }
      }).catch(e => {
        // this.$message.error({
        //   conelt: '查询失败！'
        // })
        console.log(e)
      })
    },
    getAllCountData() {
      PHAnomalyAnalysis.getAllCountDataOfTodayData().then(res => {
        if (res.code === 20000) {
          this.todayData = res.data
        } else if (res.code === 1) {
          // this.$message.warning({
          //   conelt: '请先添加要展示的模块!'
          // })
        }
      }).catch(e => {
        this.$message.error({
          conelt: '查询失败'
        })
        console.log(e)
      })
    },
    // 获取模块列表
    getModuleList() {
      PHConfig.getDoneDefineModuleList().then(res => {
        if (res.code === 20000) {
          for (let i = 0; i < res.data.length; i++) {
            this.defineModules.push(res.data[i].module)
          }
        } else if (res.code === 1) {
          this.$message.warning({
            conelt: '请先添加要展示的模块!'
          })
        }
      }).catch(e => {
        this.$message.error({
          conelt: '查询失败'
        })
        console.log(e)
      })
    },

    // 根据查询的数据创建图表
    drawChart() {
      // this.drawHighLoadChart()
      this.$refs['highLoadC'].drawHighLoadChart(this.queryAllData, this.defineModules)
      this.$refs['lowLoadC'].drawLowLoadChart(this.queryAllData, this.defineModules)
      this.$refs['offlineDeviceC'].drawOfflineDeviceChart(this.queryAllData, this.defineModules)
      this.$refs['abnormalRemovalC'].drawAbnormalRemovalChart(this.queryAllData)
      this.$refs['alarmC'].drawAlarmChart(this.queryAllData, this.defineModules)
    }
  }
}
</script>
<style scoped>
  .formDiv {
    margin-left: 50px;
    margin-top: 30px;
  }

  .formChart1 {
    width: 70%;
    height: 600px;
  }

  .formChart2 {
    width: 80%;
    height: 500px;
  }

  .card-base-chart {
    height: 600px;
    margin: 15px;
  }

  .card-base-header {
    height: 300px;
    margin: 15px;
    /* width:50% */
  }

  .card-small-header {
    height: 200px;
    width: 100%;
    margin: 15px;
  }

  .h5-class {
    color: #0040ff;
  }

  .card-base-chart {
    height: 600px;
    margin: 15px;

  }

</style>
