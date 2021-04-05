<template>
  <div>
    <el-card class="box-card card-base-chart">
      <div slot="header">
        <el-row :gutter="20">
          <el-col :span="12">
            低负载率
          </el-col>
          <el-col :span="12">
            <el-select
              v-model="lowLoadSelectItem"
              style="width:30%;"
              placeholder="请选择"
              @change="lowLoadChange()"
            >
              <el-option
                v-for="(item, index) in loadTypeList"
                :key="index"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-col>
        </el-row></div>
      <div id="lowLoadChart" class="formChart2" />
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
      lowLoad: {},
      allData: {},
      showIpDrawer: false,
      showIpList: [],
      defineModules: [],
      lowLoadChart: {},
      // 低负载展示选择
      lowLoadSelectItem: '1',
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
      // 初始化低负载chart
      this.lowLoadChart = this.$echarts.init(document.getElementById('lowLoadChart'))
      this.lowLoadChart.showLoading()
    },
    // 绘制低负载图
    drawLowLoadChart(allData, definedModules) {
      this.allData = allData
      const lowLoad = this.allData.low_load
      this.defineModules = definedModules
      this.lowLoadChart.clear()
      const option = this.getLoadChartOption(lowLoad, 'l')
      this.lowLoadChart.setOption(option)
      this.lowLoadChart.hideLoading()
      // 不清空事件会导致每次调用drawHighLoadChart都会添加相同的点击事件
      this.lowLoadChart.off('click')
      const that = this
      this.lowLoadChart.on('click', function(params) {
        let ips = lowLoad[params.seriesName].cpu.ips[params.dataIndex]
        if (that.lowLoadSelectItem === '1') {
          ips = lowLoad[params.seriesName].cpu.ips[params.dataIndex]
        } else if (that.lowLoadSelectItem === '2') {
          ips = lowLoad[params.seriesName].mem.ips[params.dataIndex]
        } else if (that.lowLoadSelectItem === '3') {
          ips = lowLoad[params.seriesName].eth0_in.ips[params.dataIndex]
        } else if (that.lowLoadSelectItem === '4') {
          ips = lowLoad[params.seriesName].eth0_out.ips[params.dataIndex]
        }
        that.showIpDrawer = true
        that.showIpList = ips

        // console.log(params.dataIndex) // 获取点击柱状图的第几个柱子 是从0开始的哦
      })
    },
    // 高负载与低负载将所有模块的平均数据放在一个linechart图中
    getLoadChartOption(loadData) {
      const selectItem = this.lowLoadSelectItem
      const moduleNames = JSON.parse(JSON.stringify(this.defineModules))
      // 存放缩减后的模块名称
      const series = []
      for (let i = 0; i < moduleNames.length; i++) {
        const moduleName = moduleNames[i]
        if (selectItem === '1') {
          series.push({ 'name': moduleName, 'type': 'line', 'data': loadData[moduleName].cpu })
        } else if (selectItem === '2') {
          series.push({ 'name': moduleName, 'type': 'line', 'data': loadData[moduleName].mem })
        } else if (selectItem === '3') {
          series.push({ 'name': moduleName, 'type': 'line', 'data': loadData[moduleName].eth0_in })
        } else if (selectItem === '4') {
          series.push({ 'name': moduleName, 'type': 'line', 'data': loadData[moduleName].eth0_out })
        }
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
        legend: { type: 'scroll',
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
    lowLoadChange() {
      this.drawLowLoadChart(this.allData, this.defineModules)
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
