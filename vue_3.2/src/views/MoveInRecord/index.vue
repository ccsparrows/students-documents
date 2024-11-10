<template>
  <el-card style="height: 570px; position: relative;">
    <el-row :gutter="20">
      <el-col :span="7">
        <el-input placeholder="请输入学生姓名或学号" clearable v-model="queryForm.query">
        </el-input>
      </el-col>
      <el-button type="primary" :icon="Search" @click="initGetMist">搜索</el-button>
      <el-button type="primary" @click="handleDialogValue()">添加</el-button>
    </el-row>

    <el-table :data="tableData" style="width: 100%">
      <el-table-column
      :width="item.width"
      :label="item.label"
        :prop="item.prop"
        v-for="(item, index) in options"
        :key="index">

        <template #default="{row}" v-if="item.prop==='action'">
          <el-button type="primary" round size="small" :icon="Edit" @click="handleDialogValue(row)"></el-button>
          <el-button type="danger" round size="small" :icon="Delete"
          @click="del(row)"></el-button>
        </template>

      </el-table-column>
    </el-table>
    
    <el-pagination
      v-model:current-page="queryForm.pagenum"
      v-model:page-size="queryForm.pagesize"
      :page-sizes="[1,5, 10, 15]"
      :small="small"
      :disabled="disabled"
      :background="background"
      layout="total, sizes, prev, pager, next, jumper"
      :total="total"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      class="pagination"
    />
  </el-card>
  <Diolog v-model="dialogVisible" 
  :dialogTitle="dialogTitle" 
  v-if="dialogVisible"
  @initList="initGetMist"
  :dialogTableValue="dialogTableValue"
   />
</template>

<script setup>
import { ref } from 'vue'
import { options } from './options'
import { getMoveinstudents, delMoveinstudents, editMoveinstudents } from '@/api/moveinstudents'
import { Search, Edit, Delete } from '@element-plus/icons-vue'
import { placeholderSign } from 'element-plus/es/components/table-v2/src/private'
import { isNull } from '@/utils/filters'
import { ElMessage, ElMessageBox } from 'element-plus'
import Diolog from './components/dialog.vue'

const queryForm = ref({
  query: '',
  pagenum: 1,
  pagesize: 5
})
const dialogTitle = ref('')
const tableData = ref([])
const total = ref(0)
const dialogTableValue = ref({})
const dialogVisible = ref(false)

const del = (row) => {
  ElMessageBox.confirm(
    '信息将被永久删除，是否继续？',
    '警告',
    {
      confirmButtonText: '是',
      cancelButtonText: '否',
      type: 'warning',
    }
  )
    .then(async () => {
      const res = await delMoveinstudents(row.id)
      ElMessage({
        type: 'success',
        message: '删除成功',
      })
      initGetMist()
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: '删除已取消',
      })
    })
}

const handleDialogValue = (row) => {
  if (isNull(row)) {
    dialogTitle.value = '添加'
    dialogTableValue.value = {}
  } else {
    dialogTitle.value = '编辑'
    dialogTableValue.value = JSON.parse(JSON.stringify(row))
  }
  dialogVisible.value = true
}

const initGetMist = async () => {
  const res = await getMoveinstudents(queryForm.value)
  console.log(res)
  total.value = res.total
  tableData.value = res.result
}
initGetMist()

const handleSizeChange = (pageSize) => {
  queryForm.value.pagenum = 1
  queryForm.value.pagesize = pageSize
  initGetMist()
}

const handleCurrentChange = (pageNum) => {
  queryForm.value.pagesize = pageNum
  initGetMist()
}
</script>

<style scoped>
.pagination {
  position: absolute;
  bottom: 16px; /* 调整这个值来确定分页组件离卡片底部的距离 */
  left: 50%;
  transform: translateX(-50%);
}
</style>
