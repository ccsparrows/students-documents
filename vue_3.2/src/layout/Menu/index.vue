<template>
  <el-menu
    background-color="$menuBg"
    class="el-menu-vertical-demo"
    text-color="#fff"
    :default-active="defaultActive"
    router
    :collapse = "!$store.getters.siderType"
  >
    <el-sub-menu>
      <template #title>
        <el-icon><UserFilled /></el-icon>
        <span>学生管理</span>
      </template>
      <el-menu-item-group>
        <el-menu-item index="/MoveInRecord" @click="savePath(MoveInRecord)">入住记录</el-menu-item>
        <el-menu-item index="/MoveOutRecord" @click="savePath(MoveOutRecord)">迁出记录</el-menu-item>
        <el-menu-item index="/AbsenceRecord" @click="savePath(AbsenceRecord)">缺寝记录</el-menu-item>
      </el-menu-item-group>
    </el-sub-menu>
    <el-menu-item index="/Building" @click="savePath(Building)">
      <el-icon><School /></el-icon>
      <span>楼宇管理</span>
    </el-menu-item>
    <el-menu-item index="/Dormitory" @click="savePath(Dormitory)">
      <el-icon><HomeFilled /></el-icon>
      <span>宿舍管理</span>
    </el-menu-item>
  </el-menu>
</template>

<script setup>
import { School, HomeFilled, UserFilled } from '@element-plus/icons-vue'
import { StudentsList } from '@/api/menu'
import { ref } from 'vue'
import variables from '@/styles/variables.scss'
const menuList = ref([])

const defaultActive =ref(sessionStorage.getItem('path')||'/MoveInRecord')

const savePath=(path)=>{
  sessionStorage.setItem('path',`/${path}`)
}


</script>

<style scoped>
span {
  color: #ffe59d;
  font-size: 15px;
  font-weight: bold;
}
:deep.el-icon {
  color:#ffe59d;
}
:deep.el-menu-item.is-active {
  color: #ffd04b;
}
</style>
