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
      <el-form-item label="入住时间" prop="move_in_time" >
        <el-date-picker
        v-model="form.move_in_time"
        type="date"
        placeholder="请选择一个日期"
        value-format="YYYY-MM-DD"
        :size="large"
      />
      </el-form-item>
      <el-form-item label="楼宇编号" prop="build_number" ref="buildFormItem">
        <el-select v-model="form.build_number" placeholder="请选择楼宇编号">
          <el-option
            v-for="item in build"
            :key="item.id"
            :label="item.number"
            :value="item.number"
          />
        </el-select>
      </el-form-item>
      <el-alert type="info" show-icon :closable="false">
        <p>宿舍编号格式以“楼宇编号-宿舍门牌号”为准。</p>
      </el-alert>
      <el-form-item label="宿舍编号" prop="room_number">
        <el-select v-model="form.room_number" placeholder="请选择宿舍编号">
          <el-option
            v-for="item in dormitory"
            :key="item.room_number"
            :label="item.room_number"
            :value="item.room_number"
          />
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
import { addMoveinstudents, editMoveinstudents } from '@/api/moveinstudents'
import { getBuilding } from '@/api/Building'
import { getDormitory } from '@/api/Dormitory'
const emits = defineEmits(['update:modelValue', 'initList'])

const formRef = ref(null)
const form = ref({
  id: '',
  student_name: '',
  move_in_time: '',
  build_number: '',
  room_number: ''
})
const dormitory = ref([])
const build = ref([])
const fetchBuildingData = async () => {
  try {
    const res = await getBuilding('')
    build.value = res.result
  } catch (error) {
    ElMessage.error('获取楼宇数据失败')
  }
}
fetchBuildingData()
const buildFormItem = ref(null)


//const change_build_number = ref('')
// 监视 form.build_number 的变化
const fetchDormitory= async () => {  
    try {
      const res = await getDormitory()
      console.log(res)
      dormitory.value = res.result
    } catch (error) {
      ElMessage.error('获取宿舍数据失败')
    }
}
fetchDormitory()
watch(
  () => form.build_number,
  () => {
    change_build_number=form.build_number
  },
  { deep: true, immediate: false }
)


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
      props.dialogTitle==='添加'? await addMoveinstudents(form.value) : await editMoveinstudents(form.value)
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
  move_in_time: [
    { required: true, message: '请输入入住时间', trigger: 'blur' }
  ],
  build_number: [
    { required: true, message: '请输入楼宇编号', trigger: 'blur' }
  ],
  room_number: [{ required: true, message: '请输入宿舍编号', trigger: 'blur' },
    {
      validator(rule, value, callback) {
        const buildNumber = form.value.build_number
        const regex = new RegExp(`^${buildNumber}-.+`)
        if (regex.test(value)) {
          callback()
        } else {
          callback(new Error('宿舍编号格式不正确'))
        }
      },
      trigger: 'blur'
    }]
})

</script>

<style lang="scss" scoped>

:deep .el-date-editor {
  --el-date-editor-width: 352px;
}

</style>
