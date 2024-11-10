<template>
  <el-dialog
    :model-value="dialogVisible"
    :title="dialogTitle"
    width="40%"
    @close="handleClose"
  >
  <el-form ref="formRef" :model="form" label-width="100px" :rules="rules">

      <el-form-item label="楼宇地址" prop="build_address" >
        <el-select v-model="form.build_address" placeholder="请选择楼宇地址">
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
      <el-alert type="info" show-icon :closable="false">
        <p>宿舍编号格式以“楼宇编号-宿舍门牌号”为准。</p>
      </el-alert>
      <el-form-item label="宿舍编号" prop="room_number">
        <el-input v-model="form.room_number" />
      </el-form-item>
      <el-form-item label="可容纳人数" prop="capacity" >
        <el-select v-model="form.capacity" placeholder="请选择可容纳人数">
          <el-option
          v-for="item in numbers"
          :key="item.value"
          :label="item.label"
          :value="item.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="当前人数" prop="current_occupancy" >
        <el-select v-model="form.current_occupancy" placeholder="请选择当前人数">
          <el-option
          v-for="item in numbers"
          :key="item.value"
          :label="item.label"
          :value="item.value"
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
import { getBuilding } from '@/api/Building'
import { ElMessage } from 'element-plus'
import { addDormitory, editDormitory } from '@/api/Dormitory'
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
  build_address: '',
  room_number: '',
  capacity: '',
  current_occupancy: '',
})

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
const numbers = ref([
  {
    value: '1人',
    label: '1人',
  },
  {
    value: '2人',
    label: '2人',
  },{
    value: '3人',
    label: '3人',
  },
  {
    value: '4人',
    label: '4人',
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
      props.dialogTitle==='添加'? await addDormitory(form.value) : await editDormitory(form.value)
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
const rules = ref({
  number: [{ required: true, message: '请输入序号', trigger: 'blur' }],
  build_address: [
    { required: true, message: '请输入楼宇地址', trigger: 'blur' }
  ],room_number: [
    { required: true, message: '请输入宿舍编号', trigger: 'blur' },
    {
      validator(rule, value, callback) {
        // Check format
        const regex = /^\d+-\d+$/
        if (!regex.test(value)) {
          callback(new Error('宿舍编号格式不正确'))
          return
        }

        const roomBuildNumber = parseInt(value.split('-')[0])

        const buildNumbers = build.value.map(b => b.number)
        if (!buildNumbers.includes(roomBuildNumber)) {
          console.log(buildNumbers)
          console.log(roomBuildNumber)
          callback(new Error('楼宇不存在'))
        } else {
          
          console.log(roomBuildNumber)
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  capacity: [
    { required: true, message: '请输入可容纳人数', trigger: 'blur' }
  ],current_occupancy: [
    { required: true, message: '请输入当前人数', trigger: 'blur' },
    {
      validator(rule, value, callback) {
        if (parseInt(value) > parseInt(form.value.capacity)) {
          callback(new Error('当前人数已超过可容纳人数！'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
  
  
})

</script>

<style lang="scss" scoped>

:deep .el-date-editor {
  --el-date-editor-width: 352px;
}

</style>
