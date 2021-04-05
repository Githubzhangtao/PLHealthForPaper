<template lang="html">
  <div>
    <el-card class="box-card card-base-chart">
      <div slot="header">
        <el-row :gutter="20" :span="12">
          <el-col>
            异常剔除
          </el-col>
          <el-col :span="12" />
        </el-row></div>
      <div id="abnormalRemovalChart" class="formChart2" />
    </el-card>
    <el-card class="box-card card-base-chart">
      <div slot="header">
        <el-row :gutter="20">
          <el-col :span="12">
            异常反复剔除
          </el-col>
          <el-col :span="12" />
        </el-row></div>
      <div id="abnormalRemovalRepeatChart" class="formChart2" />
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
        </el-row>
      </div>
    </el-drawer>
  </div>
</template>

<script>
import clip from '@/utils/clipboard'

export default {
  name: 'AbnormalRemovalComponent',
  data() {
    return {
      allData: {},
      abnormalRemovalChart: {},
      abnormalRemovalRepeatChart: {},
      zhiBoModules: [],
      showIpList: [],
      showIpDrawer: false

    }
  },
  methods: {
    initChart() {
      // 异常剔除
      this.abnormalRemovalChart = this.$echarts.init(document.getElementById('abnormalRemovalChart'))
      this.abnormalRemovalChart.showLoading()
      // 异常反复剔除
      this.abnormalRemovalRepeatChart = this.$echarts.init(document.getElementById('abnormalRemovalRepeatChart'))
      this.abnormalRemovalRepeatChart.showLoading()
    },
    drawAbnormalRemovalChart(allData) {
      this.allData = allData
      const abnormalRemoval = this.allData.abnormal_removal
      const abnormalRemovalRepeat = this.allData.abnormal_repeat_removal
      this.zhiBoModules = Object.keys(abnormalRemoval)
      this.abnormalRemovalChart.clear()
      this.abnormalRemovalRepeatChart.clear()

      const abnormalRemovalOption = this.getAbnormalRemovalChartOption(abnormalRemoval)
      const abnormalRemovalRepeatOption = this.getAbnormalRemovalRepeatChartOption(abnormalRemovalRepeat)
      this.abnormalRemovalChart.setOption(abnormalRemovalOption)
      this.abnormalRemovalRepeatChart.setOption(abnormalRemovalRepeatOption)
      this.abnormalRemovalChart.hideLoading()
      this.abnormalRemovalRepeatChart.hideLoading()
      const that = this
      this.abnormalRemovalRepeatChart.on('click', function(params) {
        const ips = abnormalRemovalRepeat[params.seriesName].ips[params.dataIndex]
        that.showIpList = ips
        that.showIpDrawer = true
      })
    },
    // 反复剔除异常chart Option
    getAbnormalRemovalRepeatChartOption(data) {
      const moduleNames = JSON.parse(JSON.stringify(this.zhiBoModules))
      const series = []
      for (let i = 0; i < moduleNames.length; i++) {
        const moduleName = moduleNames[i]
        series.push({ 'name': moduleName, 'type': 'line', 'data': data[moduleName] })
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
    // 剔除异常chart Option
    getAbnormalRemovalChartOption(data) {
      const moduleNames = JSON.parse(JSON.stringify(this.zhiBoModules))
      const series = []
      for (let i = 0; i < moduleNames.length; i++) {
        const moduleName = moduleNames[i]
        series.push({ 'name': moduleName, 'type': 'line', 'data': data[moduleName] })
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
        content: '复制成功！共' + this.showIpList.length + '条数据！',
        type: 'success',
        duration: 1500
      })
    }
  }
}

</script>

<style>
</style>
