<template>
  <div class="login-container">
    <el-form ref="formRef" :model="form" class="login-form"  :rules="rules">
      <div class="title-container">
        <h3 class="title">用户登录</h3>
      </div>
      <el-form-item prop="username">
        <el-icon :size="20" class="svg-container">
          <User />
        </el-icon>
        <el-input v-model="form.username"></el-input>
      </el-form-item>
      <el-form-item prop="username">
        <el-icon :size="20" class="svg-container">
          <Lock />
        </el-icon>
        <el-input v-model="form.password" :type="passwordType"></el-input>
        <el-icon @click="changeType">
          <Hide v-if="passwordType === 'password'"/>
          <View v-else/>
        </el-icon>

      </el-form-item>
      <el-col :span="250" justify="center"
      align="middle">
      <el-button class="login-button" @click="handleLogin">登录</el-button>
    </el-col>

    </el-form>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import{ User,Lock,Hide,View } from '@element-plus/icons-vue'
import{ useStore }from 'vuex'
const store = useStore()
const form=ref({
  username:'ad',
  password:'111111'
})
const formRef=ref(null);

const handleLogin = () => {
  formRef.value.validate(async (valid) => {
          if (valid) {
            // const res = await login(form.value.username, form.value.password)
            // console.log(res)
            store.dispatch('app/login',form.value)
          } else {
            console.log('error submit!!');
            return false;
          }
        });
}
const rules=ref(
  {
    username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    //{ min: 3, max: 5, message: 'Length should be 3 to 5', trigger: 'blur' },
  ],
  password:({
    name: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    //{ min: 3, max: 10, message: 'Length should be 3 to 10', trigger: 'blur' },
  ]
  })
  }
)
const passwordType = ref('password')
const changeType = () => {
  if (passwordType.value === 'password') {
    passwordType.value = 'text'
  } else {
    passwordType.value = 'password'
  }
}
</script>
<style lang="scss" scoped>
$bg: #2d3a4b;
$dark_gray: #889aa4;
$light_gray: #eee;
$cursor: #fff;

.login-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;

  .login-form {
    position: relative;
    width: 500px;
    max-width: 100%;
    padding: 160px 35px 0;
    margin: 0 auto;
    overflow: hidden;

    :deep .el-form-item {
      border: 1px solid rgba(255, 255, 255, 0.1);
      background: rgba(0, 0, 0, 0.1);
      border-radius: 100px;
      color: #454545;
    }
    

    :deep .el-input {
      display: inline-block;
      height: 47px;
      width: 85%;

      .el-input__wrapper {
        box-shadow: 0 0 0 0px transparent;
        background-color: transparent;
      }
      input {
        text-align: left;
        background: transparent;
        border: 0px;
        -webkit-appearance: none;
        appearance: none;
        border-radius: 10px;
        padding: 12px 5px 12px 15px;
        color: #ffffff;
        height: 47px;
        caret-color: $cursor;
        box-shadow: 0 0 0 0px;
      }
    }
    .login-button {
      border-radius: 10px;
      border:0px#2d3a4b00;
      background-color: #4a74ff;
      position: relative;
      color: #ffffff;
      width: 20%;
      box-sizing: border-box;
      margin:0 auto;
      text-align:-webkit-center;
      border-radius: 10px;
    }
  }

  .tips {
    font-size: 16px;
    line-height: 28px;
    color: #fff;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      //color: $light_gray;
      color: #fff;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }

    ::v-deep .lang-select {
      position: absolute;
      top: 4px;
      right: 0;
      background-color: white;
      font-size: 22px;
      padding: 4px;
      border-radius: 4px;
      cursor: pointer;
    }
  }

  .show-pwd {
    // position: absolute;
    // right: 10px;
    // top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }
}
</style>

