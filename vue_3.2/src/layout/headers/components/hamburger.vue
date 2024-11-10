<template>
    <div class='hamburger-container'>
        <el-icon  @click="toggleClick">
          <Fold v-if="store.getters.siderType === true"/>
          <Expand v-else/>
        </el-icon>
    </div>
</template>

<script setup>
import { Fold,Expand }  from '@element-plus/icons-vue'
import { useStore } from 'vuex'
const store = useStore()
const toggleClick  =() =>{
    store.commit('app/changeSiderType')
}
</script>

<style lang="scss" scoped>

.hamburger-container{
    margin-right: 16px;
    box-sizing: border-box;
    cursor: pointer;
}

</style>