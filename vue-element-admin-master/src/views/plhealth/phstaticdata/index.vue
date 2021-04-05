<template>
  <div>
    <el-row :gutter="10">
      <el-col :span="12">
        <el-card class="box-card card-base-chart" style="height: 300px">
          <div slot="header" style="height: 5px">
            <span style="color:#00bfff">已选择的模块</span>
          </div>
          <div style="margin-left:20%">
            <div v-for="(item,index) in defineModules" :key="item">
              <span v-if="index <=9" style="color:#0000ff">{{ item }}</span>
            </div>
            <el-tooltip class="item" effect="dark" message="查看全部" placement="top-start">
              <h2 v-if=" defineModules.length > 10" style="color:	#0040ff;" @click="showAllModulesModal=true">......</h2>
            </el-tooltip>

          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="box-card card-base-chart" style="height: 300px">
          <div slot="header" class="clearfix" style="height: 5px;">
            <span>查询选项</span>
          </div>
          <div style="margin-left:50px">
            <el-select
              v-model="selectItem"
              style="width:30%;"
              placeholder="请选择"
            >
              <el-option
                v-for="(item, index) in selectList"
                :key="index"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
            <el-select
              v-model="selectChartType"
              style="width:30%;"
              placeholder="请选择"
            >
              <el-option
                v-for="(item, index) in chartTypeList"
                :key="index"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
            <el-button
              type="primary"
              size="default"
              style="margin-top:20px;margin-left:30px"
              icon="el-icon-search"
              @click="queryData()"
            >
              查询
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <div v-for="(item,index) in showModuleNames" :key="item">
      <el-row v-if="index%2 == 0" :gutter="20">
        <el-col :span="12">
          <el-card class="box-card card-base-chart">
            <div slot="header" class="clearfix">
              {{ showModuleNames[index] }}
            </div>
            <div :id="showModuleNames[index]" class="formChart2" />
          </el-card>
        </el-col>
        <el-col :span="12">
          <!-- <ten-card v-if="defineModules.length % 2 ==1 && (index !== defineModules.length - 1)" class="card-base-chart"> -->
          <el-card v-if="index !== NaN" class="card-base-chart">
            <div slot="header" class="clearfix">
              {{ showModuleNames[index+1] }}
            </div>
            <div :id="showModuleNames[index+1]" class="formChart2" />
          </el-card>
        </el-col>

      </el-row>
    </div>
    <el-dialog title="详细信息" :visible.sync="showAllModulesModal">
      <div style="width:800px;">
        <li v-for="(item,index) in defineModules" :key="item" style="color:#0000ff">{{ '['+index+']:  '+item }}</li>
      </div>
    </el-dialog>

  </div>
</template>
<script>
import * as PHStatic from '@/api/phjs/phstatic'
import * as PHConfig from '@/api/phjs/config.js'
export default {
  name: 'Psstaticdata',
  data() {
    return {
      chartList: [],
      selectChartType: '2',
      chartTypeList: [
        {
          value: '1',
          label: '线形图'
        }, {
          value: '2',
          label: '饼图'
        }
      ],
      selectItem: '1',

      selectList: [
        {
          value: '1',
          label: 'CPU核数分布图'
        },
        {
          value: '2',
          label: '内存大小分布图'
        },
        {
          value: '3',
          label: '磁盘大小分布图'
        }
      ],
      defineModules: [
      ],
      showModuleNames: [],
      showAllModulesModal: false,
      loading: false
    }
  },
  computed: {
  },
  created() {
  },
  mounted() {
    this.initQuery()
  },
  methods: {
    // 页面创建时初始化查询
    initQuery() {
      this.getModuleList()
      const that = this
      setTimeout(function() {
        that.initChart()
        that.queryData()
      }, 500)
    },
    // 获取当前展示的模块的列表
    getModuleList() {
      PHConfig.getDoneDefineModuleList().then(res => {
        if (res.code === 20000) {
          console.log(res.data)
          for (let i = 0; i < res.data.length; i++) {
            this.defineModules.push(res.data[i].module)
          }
          this.showModuleNames.push('汇总数据')
          for (let i = 0; i < res.data.length; i++) {
            this.showModuleNames.push(res.data[i].module)
          }
        } else if (res.code === 1) {
          this.$message.warning({
            message: '请先添加要展示的模块!'
          })
        }
      }).catch(e => {
        this.$message.error({
          message: '查询失败'
        })
        console.log(e)
        this.chartHideLoad()
      })
    },
    // 初始化echart
    initChart() {
      let i = 0
      for (; i < this.showModuleNames.length; i++) {
        const name = this.showModuleNames[i]
        const chartTemp = this.$echarts.init(document.getElementById(name))
        this.chartList.push(chartTemp)
        chartTemp.showLoading()
      }
    },
    chartShowLoad() {
      for (let i = 0; i < 10; i++) {
        this.chartList[i].showLoading()
      }
    },
    chartHideLoad() {
      for (let i = 0; i < this.showModuleNames.length; i++) {
        this.chartList[i].hideLoading()
      }
    },
    // 查询数据绘制图形
    queryData() {
      if (this.selectItem) {
        // this.chartShowLoad()
        PHStatic.getStaticData().then(res => {
          if (res.code === 20000) {
            this.drawChart(res.data)
          } else if (res.code === 1) {
            this.chartHideLoad()
          }
        }).catch(e => {
          // this.$message.error({
          //   message: '查询失败！'
          // })
          console.log(e)
          this.chartHideLoad()
        })
      } else {
        this.$message.error({
          message: '请先选择查询类型！'
        })
      }
    },
    // 根据查询的数据创建图表
    drawChart(data) {
      let i = 0
      for (; i < this.showModuleNames.length; i++) {
        // debugger
        const chartTemp = this.chartList[i]
        chartTemp.clear()
        const name = this.showModuleNames[i]
        let option = this.getLineChartOption(i, data[name])
        if (this.selectChartType === '2') {
          option = this.getPieChartOption(i, data[name])
        }

        chartTemp.setOption(option)
        chartTemp.hideLoading()
      }
    },
    // 依据每一个平台的data绘制chart,柱状图和线形图
    getLineChartOption(i, data) {
      let avg = 0
      let showItems = data.cpu
      if (this.selectItem === '1') {
        showItems = data.cpu
        avg = data.cpu.avg
      } else if (this.selectItem === '2') {
        showItems = data.mem
        avg = data.mem.avg
      } else if (this.selectItem === '3') {
        showItems = data.disk
        avg = data.disk.avg
      }
      // console.log(avg)
      const option = {
        title: {
          // text: '平均值: '
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: [this.selectList[this.selectItem - 1].label + '  平均值:  ' + avg],
          left: 'center'
          // textStyle: {
          //   color: 'lime'
          // }
        },
        toolbox: {
          show: true,
          feature: {
            dataView: { show: true, readOnly: false },
            magicType: { show: true, type: ['line', 'bar'] },
            restore: { show: true },
            saveAsImage: { show: true }
          }
        },
        calculable: true,
        xAxis: [
          {
            type: 'category',
            data: showItems.x
          }
        ],
        yAxis: [
          {
            type: 'value'
          }
        ],
        series: [
          {
            name: this.selectList[this.selectItem - 1].label + '  平均值:  ' + avg,
            type: 'line',
            data: showItems.y,
            barWidth: 50,
            // itemStyle: {
            //   color: 'rgba(0,0,0,0.05)'
            // },
            barGap: '-100%',
            barCategoryGap: '40%',
            markPoint: {
              data: [
                { type: 'max', name: '最大值' },
                { type: 'min', name: '最小值' }
              ]
            },
            markLine: {
              data: [
                { type: 'average', name: '平均值' }
              ]
            }
          }

        ],
        color: ['#4d004c', '#336600', '#ffd966', '#ffff00', '#0040ff', '#ff0080']

      }
      return option
    },
    // 依据每一个平台的data绘制chart,饼图（pie）
    getPieChartOption(i, data) {
      let avg = 0
      const pieData = []
      let showItems = data.cpu
      if (this.selectItem === '1') {
        showItems = data.cpu
        avg = data.cpu.avg
      } else if (this.selectItem === '2') {
        showItems = data.mem
        avg = data.mem.avg
      } else if (this.selectItem === '3') {
        showItems = data.disk
        avg = data.disk.avg
      }

      for (let i = 0; i < showItems.x.length; i++) {
        pieData.push({
          name: showItems.x[i],
          value: showItems.y[i]
        })
      }
      const option = {
        title: {
          text: '平均值: ' + avg,
          // left: 'center',
          // top: 'center'
          right: 30,
          top: 50
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        // legend: {
        //   left: 'center',
        //   top: 'bottom',
        //   data: data.x
        // },
        legend: {
          orient: 'vertical',
          left: 10,
          data: data.x
        },
        toolbox: {
          show: true,
          feature: {
            mark: { show: true },
            dataView: { show: true, readOnly: false },
            magicType: {
              show: true,
              type: ['pie', 'funnel'],
              top: 'center'
            },
            restore: { show: true },
            saveAsImage: { show: true }
          }
        },
        series: [
          {
            name: this.selectList[this.selectItem - 1].label,
            type: 'pie',
            radius: '60%',
            center: ['60%', '50%'],
            // roseType: 'area',
            data: pieData,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ],
        color: ['#6666ff', '#0040ff', '#4d004c', '#336600', '#ffd966', '#b266ff']

      }
      return option
    }

  }
}
</script>
<style scoped>

  .formDiv {
    margin-left: 50px;
    margin-top: 30px;
  }

  .formChart1{
    width: 70%;
    height: 600px;
  }
  .formChart2 {
    width: 70%;
    height: 500px;
  }
  .card-base-chart{
    height:600px;
    margin:15px;
  }
  .card-base-header{
    height:300px;
    margin:15px;
    /* width:50% */
  }
  .card-base-chart{
    height:600px;
    margin:15px;

  }

</style>
