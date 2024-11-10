<template>
    <div>
        <el-dropdown>
            <span class="el-dropdown-link">
                <el-icon size="25px"><User /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="logout">退出系统</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
    </div>
</template>

<script setup>
//import store from '@/store';
import { User } from '@element-plus/icons-vue'

import { useStore } from 'vuex'
const store=useStore()
const logout=()=>{
   store.dispatch('app/logout')
}
</script>

<style lang="scss" scoped>

</style>