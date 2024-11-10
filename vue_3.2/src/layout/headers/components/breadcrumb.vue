<template>
    <el-breadcrumb separator="/">
        <el-breadcrumb-item 
        v-for="(item,index) in breadcrumb"
        :key ="index">
        {{ item.name }}
    </el-breadcrumb-item>
      </el-breadcrumb>
</template>

<script setup>
import { watch,ref } from 'vue';
import { useRoute } from 'vue-router';
const route =useRoute()
const breadcrumb=ref([])
const initBreadcrumb =()=>{
    breadcrumb.value=route.matched
}
watch(route,()=>{
    initBreadcrumb()
},{deep:true,immediate:true})
</script>

<style lang="scss" scoped>


</style>