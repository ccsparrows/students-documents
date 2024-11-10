<template>
  <el-dialog
    :model-value="dialogVisible"
    :title="dialogTitle"
    width="40%"
    @close="handleClose"
  >
  <el-form ref="formRef" :model="form" label-width="100px" :rules="rules">
      
      <el-form-item label="楼宇编号" prop="number" >
        <el-select v-model="form.number" placeholder="请选择楼宇编号">
          <el-option
          v-for="item in numbers"
          :key="item.value"
          :label="item.label"
          :value="item.value"
          />
          <template #footer>
            <el-button v-if="!isAdding" text bg size="small" @click="onAddOption">
              自定义编号
            </el-button>
            <template v-else>
              <el-input
                v-model="optionName"
                class="option-input"
                placeholder="输入自定义编号"
                size="small"
              />
              <el-button type="primary" size="small" @click="onConfirmbuildings">
                确认
              </el-button>
              <el-button size="small" @click="clear">取消</el-button>
            </template>
          </template>
        </el-select>
      </el-form-item>

      <el-form-item label="楼宇地址" prop="address" >
        <el-select v-model="form.address" placeholder="请选择楼宇地址">
          <el-option
          v-for="item in addresses"
          :key="item.value"
          :label="item.label"
          :value="item.value"
          />
          <template #footer>
            <el-button v-if="!isAdding" text bg size="small" @click="onAddOption">
              新增地址
            </el-button>
            <template v-else>
              <el-input
                v-model="optionName"
                class="option-input"
                placeholder="输入新增地址"
                size="small"
              />
              <el-button type="primary" size="small" @click="onConfirmaddresses">
                确认
              </el-button>
              <el-button size="small" @click="clear">取消</el-button>
            </template>
          </template>
        </el-select>
      </el-form-item>
      <el-form-item label="宿管编号" prop="dorm_manager_id">
        <el-input v-model="form.dorm_manager_id" />
      </el-form-item>
      <el-form-item label="宿管姓名" prop="dorm_manager">
        <el-input v-model="form.dorm_manager" />
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
import { addBuilding, editBuilding } from '@/api/Building'
const emits = defineEmits(['update:modelValue', 'initList'])
const isAdding = ref(false)
const optionName = ref('')
const onAddOption = () => {
  isAdding.value = true
}
const onConfirmbuildings = () => {
  if (optionName.value) {
    numbers.value.push({
      label: optionName.value,
      value: optionName.value,
    })
    clear()
  }
}
const onConfirmaddresses = () => {
  if (optionName.value) {
    addresses.value.push({
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
  number: '',
  address: '',
  dorm_manager_id: '',
  dorm_manager: '',
})
const numbers = ref([
  {
    value: '1',
    label: '1',
  },
  {
    value: '2',
    label: '2',
  },{
    value: '3',
    label: '3',
  },{
    value: '4',
    label: '4',
  },{
    value: '5',
    label: '5',
  },{
    value: '6',
    label: '6',
  },
])
const addresses = ref([
  {
    value: '北区',
    label: '北区',
  },
  {
    value: '南区',
    label: '南区',
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
      props.dialogTitle==='添加'? await addBuilding(form.value) : await editBuilding(form.value)
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
  number: [{ required: true, message: '请输入序号', trigger: 'blur' }],
  address: [
    { required: true, message: '请输入楼宇地址', trigger: 'blur' }
  ],
  dorm_manager_id: [
    { required: true, message: '请输入宿管编号', trigger: 'blur' }
  ],dorm_manager: [
    { required: true, message: '请输入宿管姓名', trigger: 'blur' }
  ],
  
  
})

</script>

<style lang="scss" scoped>

:deep .el-date-editor {
  --el-date-editor-width: 352px;
}

</style>
