<template>

  <div class="demo-form-box">
    <el-dialog
      :title="titleList[useRatioType]"
      :visible.sync="showFormModal"
      :width="500"
      style="height:1000px"
    >

      <!--    <ten-modal-->
      <!--      v-model="showFormModal"-->
      <!--      :title="titleList[useRatioType]"-->
      <!--      :width="500"-->
      <!--      :close-after-action="false"-->
      <!--      @cancel="cancelEdit"-->
      <!--      @confirm="confirmEdit"-->
      <!--    >-->
      <div>
        <el-form ref="form" :model="formData" :rules="rules" label-width="80px">
          <el-form-item
            label="开始值"
            prop="start"
          >
            <el-input v-model.number="formData.start" />
          </el-form-item>
          <el-form-item
            label="结束值"
            prop="stop"
          >
            <el-input v-model.number="formData.stop" />
          </el-form-item>
          <el-form-item
            label="高负载"
            prop="is_high_load"
          >

            <el-radio-group
              v-model.number="formData.is_high_load"
              :disabled="formData.is_low_load === 1"
              @change="onChange"
            >
              <el-radio :label="0">
                否
              </el-radio>
              <el-radio :label="1">
                是
              </el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item
            label="低负载"
            prop="is_low_load"
          >
            <el-radio-group
              v-model.number="formData.is_low_load"
              :disabled="formData.is_high_load === 1"
              @change="onChange"
            >
              <el-radio :label="0">
                否
              </el-radio>
              <el-radio :label="1">
                是
              </el-radio>
            </el-radio-group>
          </el-form-item>

        </el-form>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="cancelEdit">取 消</el-button>
        <el-button type="primary" @click="confirmEdit">确 定</el-button>
      </span>
    </el-dialog>

  </div>
</template>
<script>
export default {
  name: 'UseRangeForm',
  data() {
    return {
      insertIndex: 0,
      modalType: 'add',
      showFormModal: false,
      useRatioType: '',
      titleList: { 'cpu': 'cpu利用率范围配置', 'mem': '内存利用率范围配置', 'eth0_in': 'eth0入流量范围配置', 'eth0_out': 'eth0出流量范围配置' },
      formData: {},
      rules: {
        start: [
          { required: true, message: '不能输入空值' }
        ],
        stop: [
          { required: true, message: '不能输入空值' }
        ]
      }
    }
  },
  computed: {
    // disableMin: function() {
    //   if (this.useRatioType === 'cpu' || this.useRatioType === 'mem') {
    //     if (this.formData.start === 0) {
    //       return true
    //     } else {
    //       return false
    //     }
    //   } else {
    //     if (this.formData.start === 0) {
    //       return true
    //     } else {
    //       return false
    //     }
    //   }
    // },
    // disableMax: function() {
    //   if (this.useRatioType === 'cpu' || this.useRatioType === 'mem') {
    //     if (this.formData.stop === 100) {
    //       return true
    //     } else {
    //       return false
    //     }
    //   } else {
    //     if (this.formData.stop === 9999) {
    //       return true
    //     } else {
    //       return false
    //     }
    //   }
    // }
  },
  methods: {
    disableMaxMin(val) {
      console.log(val)
      return true
    },
    cancelEdit() {
      this.$emit('updateUseRangeTable')
      this.showFormModal = false
    },
    onChange(row) {
      // console.log(row)
    },
    addPre(index, useRatioType) {
      this.insertIndex = index
      this.modalType = 'add'
      this.showFormModal = true
      this.formData = {
        is_high_load: 0,
        is_low_load: 0,
        type: useRatioType
      }
      this.useRatioType = useRatioType
    },

    // 编辑前数据回显
    editPre(row, useRatioType) {
      this.modalType = 'edit'
      this.showFormModal = true
      this.formData = row
      this.useRatioType = useRatioType
    },
    // 编辑确认，验证数据并保存
    confirmEdit() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          if (this.formData.start >= this.formData.stop) {
            this.$message({
              type: 'warning',
              content: '开始值不能大于结束值!'
            })
          } else {
            if (this.modalType === 'add') {
              this.$emit('addUseRange', this.insertIndex + 1, this.formData)
            }
            this.showFormModal = false
          }
        } else {
          console.log('校验失败')
        }
      })
    },
    onSubmitClick() {
      this.$refs.form.validate((valid, errors) => {
        if (valid) {
          console.log('校验通过')
          this.$message.success('校验通过')
        } else {
          console.log('校验失败', errors)
        }
      })
    }
  }
}
</script>

<style scoped>

</style>
