<template>
  <div>

    <el-card class="box-card card-base-chart">
      <div slot="header">
        <el-row :gutter="20">
          <el-col :span="12">
            单机告警
          </el-col>
          <el-col :span="12">
            <el-select
              v-model="alarmTypeSelectItem"
              style="width:30%;"
              placeholder="请选择"
              @change="alarmTypeChange()"
            >
              <el-option
                v-for="(item, index) in alarmType"
                :key="index"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-col>
        </el-row></div>
      <div id="alarmChart" class="formChart2" />
    </el-card>

    <el-drawer
      title="IP列表"
      :visible.sync="showIpDrawer"
      direction="ltr"
      size="300"
    >
      <div style="padding: 20px; line-height: 30px;">

        <el-row :gutter="20">
          <el-col :span="12">
            <li v-for="item in showIpList" :key="item">{{ item }}</li>
          </el-col>
          <el-col :span="12">
            <el-button type="primary" size="small" icon="el-icon-document" @click="handleCopy($event)">
              复制
            </el-button>
          </el-col>
        </el-row></div>
    </el-drawer>

  </div>
</template>

<script>
import clip from '@/utils/clipboard'

export default {
  name: 'AlarmComponent',
  data() {
    return {
      alarmChart: {},
      allData: {},
      alarmTypeSelectItem: 'alarm_ping',
      alarmType: [
        {
          value: 'alarm_ping',
          label: 'Ping告警'
        },
        {
          value: 'alarm_flow',
          label: '单机流量告警'
        },
        {
          value: 'alarm_performance',
          label: '单机性能告警'
        },
        {
          value: 'alarm_port',
          label: '端口告警'
        },
        {
          value: 'alarm_process_port',
          label: '进程端口配置告警'
        },
        {
          value: 'alarm_process',
          label: '进程告警'
        },
        {
          value: 'alarm_report_time_out',
          label: '上报超时告警'
        },
        {
          value: 'alarm_disk',
          label: '硬盘告警'
        },
        {
          value: 'alarm_disk_ro',
          label: '硬盘只读告警'
        },
        {
          value: 'alarm_disk_ro_full',
          label: '硬盘只读告警[磁盘满]'
        }
      ],
      showIpList: [],
      definedModules: [],
      showIpDrawer: false

    }
  },
  methods: {
    initChart() {
      // 初始化离线设备chart
      this.alarmChart = this.$echarts.init(document.getElementById('alarmChart'))
      this.alarmChart.showLoading()
    },
    drawAlarmChart(allData, definedModules) {
      this.allData = allData
      this.definedModules = definedModules
      let alarm = {}
      alarm = this.allData.alarm
      this.alarmChart.clear()
      const alarmChartOption = this.getAlarmChartOption(alarm)
      this.alarmChart.setOption(alarmChartOption)
      this.alarmChart.hideLoading()
      const that = this
      this.alarmChart.on('click', function(params) {
        const ips = alarm[params.seriesName][that.alarmTypeSelectItem].ips[params.dataIndex]
        console.log(ips)
        that.showIpDrawer = true
        that.showIpList = ips
      })
    },
    alarmTypeChange() {
      this.drawAlarmChart(this.allData, this.definedModules)
    },
    // 反复剔除异常chart Option
    getAlarmChartOption(data) {
      const moduleNames = JSON.parse(JSON.stringify(this.definedModules))
      const series = []
      for (let i = 0; i < moduleNames.length; i++) {
        const moduleName = moduleNames[i]
        series.push({ 'name': moduleName, 'type': 'line', 'data': data[moduleName][this.alarmTypeSelectItem] })
      }
      const todayDate = new Date()
      let dateData = []
      for (let i = 1; i <= 30; i++) {
        todayDate.setDate(todayDate.getDate() - 1)
        dateData.push(todayDate.getMonth() + 1 + '-' + todayDate.getDate())
      }
      dateData = dateData.reverse()
      return this.getOption(dateData, series)
    },
    getOption(dateData, series) {
      const option = {
        title: {
          // text: '折线图'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          type: 'scroll',
          // orient: 'vertical',
          top: 5,
          width: '90%',
          data: this.zhiBoModules
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        toolbox: {
          itemSize: 15,
          orient: 'vertical',
          feature: {
            dataView: { show: true, readOnly: false },
            magicType: { show: true, type: ['line', 'bar'] },
            restore: { show: true },
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: dateData
        },
        yAxis: {
          type: 'value'
        },
        series: series
      }
      return option
    },
    // 处理复制按钮时，将展示的ip时复制到粘贴板中
    handleCopy(event) {
      clip(this.showIpList, event)
      this.$message({
        message: '复制成功！共' + this.showIpList.length + '条数据！',
        type: 'success',
        duration: 1500
      })
    }

  }
}

</script>

<style>
  .formChart2 {
    width: 80%;
    height: 500px;
  }
</style>
