<template>
  <div>
    <el-card class="box-card card-base-chart">
      <div slot="header">
        <el-row :gutter="20">
          <el-col :span="12">
            离线设备数
          </el-col>
          <el-col :span="12" />
        </el-row></div>
      <div id="offlineDeviceChart" class="formChart2" />
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
  name: 'HighLoadComponent',
  data() {
    return {
      allData: {},
      showIpDrawer: false,
      showIpList: [],
      defineModules: [],
      offlineDeviceChart: {},
      highLoadSelectItem: '1',
      loadTypeList: [
        {
          value: '1',
          label: 'CPU利用率'
        },
        {
          value: '2',
          label: '内存利用率'
        },
        {
          value: '3',
          label: '网卡入流量'
        },
        {
          value: '4',
          label: '网卡出流量'
        }
      ]
    }
  },
  created() {
  },
  methods: {
    initChart() {
      // 初始化离线设备chart
      this.offlineDeviceChart = this.$echarts.init(document.getElementById('offlineDeviceChart'))
      this.offlineDeviceChart.showLoading()
    },

    // 绘制离线设备图
    drawOfflineDeviceChart(allData, definedModules) {
      this.allData = allData
      this.defineModules = definedModules
      const offlineDevice = this.allData.offline_device
      this.offlineDeviceChart.clear()
      const option = this.getOfflineDeviceChartOption(offlineDevice)
      this.offlineDeviceChart.setOption(option)
      this.offlineDeviceChart.hideLoading()
      const that = this
      this.offlineDeviceChart.on('click', function(params) {
        const ips = offlineDevice[params.seriesName].ips[params.dataIndex]
        that.showIpDrawer = true
        that.showIpList = ips
      })
    },
    getOfflineDeviceChartOption(data) {
      const moduleNames = JSON.parse(JSON.stringify(this.defineModules))
      // 存放缩减后的模块名称
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
          data: moduleNames
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
    }, // 处理高负载展示下拉框选择事件
    highLoadChange() {
      this.drawHighLoadChart(this.allData, this.defineModules)
    }

  }
}

</script>

<style>
  .card-base-chart{
    height:600px;
    margin:15px;

  }
  .formChart2 {
    width: 80%;
    height: 500px;
  }
</style>
