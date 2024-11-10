<template>
  <el-dialog
    :model-value="dialogVisible"
    :title="dialogTitle"
    width="40%"
    @close="handleClose"
  >
  <el-form ref="formRef" :model="form" label-width="100px" :rules="rules">

      <el-form-item label="学号" prop="id">
        <el-input v-model="form.id" />
      </el-form-item>
      <el-form-item label="姓名"  prop="student_name">
        <el-input v-model="form.student_name" />
      </el-form-item>
      <el-form-item label="迁出时间" prop="move_out_time" >
        <el-date-picker
        v-model="form.move_out_time"
        type="date"
        placeholder="请选择一个日期"
        value-format="YYYY-MM-DD"
        :size="large"
      />
      </el-form-item>
      <el-form-item label="迁出原因" prop="reason" >
        <el-select v-model="form.reason" placeholder="请选择迁出原因">
          <el-option
          v-for="item in reasons"
          :key="item.value"
          :label="item.label"
          :value="item.value"
          />
          <template #footer>
            <el-button v-if="!isAdding" text bg size="small" @click="onAddOption">
              Add an option
            </el-button>
            <template v-else>
              <el-input
                v-model="optionName"
                class="option-input"
                placeholder="input option name"
                size="small"
              />
              <el-button type="primary" size="small" @click="onConfirm">
                confirm
              </el-button>
              <el-button size="small" @click="clear">cancel</el-button>
            </template>
          </template>
        </el-select>
      </el-form-item>
      
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleConfirm"> 确认 </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { defineEmits, ref, defineProps, watch } from 'vue'
import { options } from '../options'
import { ElMessage } from 'element-plus'
import { editMoveoutstudents,addMoveoutstudents } from '@/api/move_out_records'

const emits = defineEmits(['update:modelValue', 'initList'])
const isAdding = ref(false)
const optionName = ref('')
const onAddOption = () => {
  isAdding.value = true
}
const onConfirm = () => {
  if (optionName.value) {
    reasons.value.push({
      label: optionName.value,
      value: optionName.value,
    })
    clear()
  }
}
const clear = () => {
  optionName.value = ''
  isAdding.value = false
}

const formRef = ref(null)
const form = ref({
  id: '',
  student_name: '',
  move_out_time: '',
  reason: '',
})
const reasons = ref([
  {
    value: '病假',
    label: '病假',
  },
  {
    value: '毕业',
    label: '毕业',
  },
])


const props = defineProps({
  dialogTitle: {
    type: String,
    default: '',
    required: true
  },
  dialogTableValue: {
    type: Object,
    default: () => {}
  }
})


watch(
  () => props.dialogTableValue,
  () => {
    form.value=props.dialogTableValue
  },
  { deep: true, immediate: true }
)

const handleClose = () => {
  emits('update:modelValue', false)
}
const handleConfirm = () => {
  formRef.value.validate(async (valid) => {
    if (valid) {
      console.log(form.value)
      props.dialogTitle==='添加'? await addMoveoutstudents(form.value) : await editMoveoutstudents(form.value)
      ElMessage({
        showClose: true,
        message: props.dialogTitle==='添加'?'添加成功！' : '编辑成功',
        type: 'success'
      })
      emits('initList')
      handleClose()
    } else {
      console.log('error submit!')
    }
  })
}

const rules = ref({
  id: [{ required: true, message: '请输入学号', trigger: 'blur' }],
  student_name: [
    { required: true, message: '请输入学生姓名', trigger: 'blur' }
  ],
  move_out_time: [
    { required: true, message: '请输入迁出时间', trigger: 'blur' }
  ],
  reason: [
    { required: true, message: '请输入迁出原因', trigger: 'blur' }
  ],
})

</script>

<style lang="scss" scoped>

:deep .el-date-editor {
  --el-date-editor-width: 352px;
}

</style>
