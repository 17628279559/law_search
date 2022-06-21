<script setup>
import { useStore } from 'vuex'
import Axios from 'axios'
import { computed, ref, onMounted, reactive } from 'vue'
import $ from 'jquery'
import { Timer } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import Waves from 'node-waves'
import dt from './dt.js'
import 'node-waves/dist/waves.min.css'

const search = ref(false)
const tableData = reactive({ 'data': [] })
const oldWords = ""
const words = reactive(["", "", "", "", "", "", "", "", ""])

const showUrl = [
  {
    url: 'https://cata.oss-cn-hongkong.aliyuncs.com/avatar/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E5%88%91%E6%B3%952020%E4%BF%AE%E6%AD%A3gP3fM8lF.pdf',
    name: "刑法",
    n: "xf"
  },
  {
    url: 'https://cata.oss-cn-hongkong.aliyuncs.com/avatar/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E5%AE%AA%E6%B3%952018%E5%B9%B43%E6%9C%8811%E6%97%A5%E4%BF%AE%E6%AD%A3cnNHWqfm.pdf',
    name: "宪法",
    n: "xianfa"
  },
  {
    url: 'https://cata.oss-cn-hongkong.aliyuncs.com/avatar/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E6%B0%91%E4%BA%8B%E8%AF%89%E8%AE%BC%E6%B3%958HAUumnB.pdf',
    name: "民事诉讼法",
    n: "msssf"
  },
  {
    url: 'https://cata.oss-cn-hongkong.aliyuncs.com/avatar/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E6%B0%91%E6%B3%95%E5%85%B8v7RAwgiQ.pdf',
    name: "民法典",
    n: "mfd"
  },
  {
    url: 'https://cata.oss-cn-hongkong.aliyuncs.com/avatar/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E8%A1%8C%E6%94%BF%E8%AE%B8%E5%8F%AF%E6%B3%957ubjPG0Q.pdf',
    name: "行政许可法",
    n: "xzxkf"
  }
]

const myDownload = url => {
  let link = document.createElement('a')
  link.setAttribute('target', '_blank')
  let name = url.slice(49)
  link.style.display = 'none'
  link.href = url
  link.setAttribute('download', name)
  document.body.appendChild(link)
  link.click()
}
const lawSearchApi = "/api/getlawdata"
const getLawCountApi = "/api/getlawcount"
const store = useStore()

const count = computed(() => store.state.count)

const change = data => store.commit('change', data)

const asyncChange = data => store.dispatch('asyncChange', data)

const nowId = ref('search_1')

const searchList = [
  { id: 'search_1', action: '', keyName: 'words', btype: 'button', shortName: '本站', method: '' },
  { id: 'search_2', action: 'https://www.baidu.com/s?wd=', keyName: 'wd', shortName: '百度', btype: 'submit', method: 'get' },
  { id: 'search_3', action: 'https://cn.bing.com/search?q=', keyName: 'q', shortName: 'Bing', btype: 'submit', method: 'get' },
  { id: 'search_4', action: 'https://www.so.com/s?q=', keyName: 'q', shortName: '360', btype: 'submit', method: 'get' },
  { id: 'search_5', action: 'https://www.sogou.com/web?query=', keyName: 'query', shortName: '搜狗', btype: 'submit', method: 'get' },
  { id: 'search_6', action: 'https://list.tmall.com/search_product.htm?q=', keyName: 'q', shortName: '天猫', btype: 'submit', method: 'get' },
  { id: 'search_7', action: 'https://s.taobao.com/search?q=', keyName: 'q', shortName: '淘宝', btype: 'submit', method: 'get' },
  { id: 'search_8', action: 'https://www.zhihu.com/search?q=', keyName: 'q', shortName: '知乎', btype: 'submit', method: 'get' },
  { id: 'search_9', action: 'https://www.google.com.hk/search?q=', keyName: 'q', shortName: '谷歌', btype: 'submit', method: 'get' }
]

const lawSearch = () => {
  if (words[0] === oldWords) {
    if (oldWords === "") {
      ElMessage({
        message: "请输入关键字",
        type: 'error',
      })
    }
  }
  else {
    let formData = new FormData();
    formData.append('words', words[0]);
    $('#loader').fadeIn(300)
    $('.mask').fadeIn(300)
    Axios.post(lawSearchApi, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    }).then((response) => {
      $("#loader").fadeOut(300);
      $(".mask").fadeOut(300)
      if (response.data.code === 200) {
        tableData.data = response.data.data
        search.value = true
        ElMessage({
          message: response.data.message,
          type: 'success',
        })
      }
      else if (response.data.code === 203) {
        tableData.data = []
        ElMessage({
          message: response.data.message,
          type: 'warning',
        })
      }
      else {
        search.value = false
        ElMessage({
          message: response.data.message,
          type: 'error',
        })
      }

    })
  }
}

onMounted(() => {
  Waves.init()
  Waves.attach('.btn')
  Axios.get(getLawCountApi).then((response) => {
    let data = response.data
    dt(data, {
      id: '#lawMap',
      mapSize: 480,
      width: 550,
      height: 480,
      frontText: "共收录",
      endText: "份法律法规文件",
      ylable: "全国各地法律法规发布情况",
    })
  })
})
</script>

<template>
  <div>
    <div class="mask">
      <div id="loader"></div>
    </div>
    <div style="position:absolute;width:100%;z-index: 20;">
      <ul class="flex flex-justify-end">
        <li>
          <a href="https://zwt666.top/" target="_blank"><i class="fa fa-user" style="color:white;font-size: 30px;margin:15px 15px 0px 10px;"></i></a>
        </li>
        <li>
          <a href="https://github.com/17628279559" target="_blank"><i class="fa fa-github" style="color:white;font-size: 30px;margin:15px 30px 0px 10px;"></i></a>
        </li>
      </ul>
    </div>
    <div class="flex column" style="height:100vh">
      <div id="banner-bear" class="preserve3d csstransforms3d">

        <p class="typing">全国各省份法规政策检索</p>
        <div class="primary-menus">
          <ul>
            <li v-for="(item, index) in searchList" :key="index" :class="[item.id === nowId? 'current':'']" @click="nowId = item.id"><span>{{item.shortName}}</span></li>
          </ul>
          <div class="cont">
            <div class="left-cont">
              <form v-for="(item, index) in searchList" :key="index" :class="[item.id === nowId? 'search':'search hidden']" :id="item.id" :action="item.action" :method="item.method" :target="[item.id === 'search_1'? '':'_blank']">
                <input type="text" v-model="words[index]" :name="item.keyName" class="s" placeholder="请输入法律关键词">
                <button :type="item.btype" name="" class="btn" @click="[item.id === 'search_1'? lawSearch():null]">{{item.shortName + "搜索"}}</button>
              </form>
            </div>
          </div>
        </div>
        <div class="banner-wrap scenes-ready">
          <div id="stage">
            <div class="space"></div>
            <div class="mountains">
              <div class="mountain mountain-1"></div>
              <div class="mountain mountain-2"></div>
              <div class="mountain mountain-3"></div>
            </div>
            <div class="bear"></div>
          </div>
        </div>
      </div>
      <div class="flex1" style="background:url(/src/assets/images/bg.png) no-repeat 0px 0px;background-size: cover;">
        <div class="flex1 flex flex-justify-center" v-show="!search">
          <div id="lawMap"></div>
          <div class="flex column">
            <div class="flex flex-justify-center">
              <div class="text">热门法律浏览</div>
            </div>
            <div class="flex">
              <div v-for="(item,index) in showUrl" :key="index" class="law-item transition flex flex-justify-center flex-wrap" style="width:150px;height:240px;margin: 10px;z-index: 99;" @click="myDownload(item.url)">
                <img class="lawImg" :src="`/src/assets/images/${item.n}.png`" alt="" width="150" height="220">
                <p>{{item.name}}</p>
              </div>
            </div>
          </div>
        </div>
        <div class="flex1 flex flex-justify-center" v-show="search">

          <div id="shuju" style="width: 80%">
            <el-table :data="tableData.data" style="width: 100%" :stripe="true" height="500" :highlight-current-row="true" :default-sort="{ prop: 'legalPublishedTime', order: 'descending' }">
              <el-table-column label="Id" class="id" type="index" width="60">
              </el-table-column>
              <el-table-column label="法规名称">
                <template #default="scope">
                  <el-link :href="scope.row.legalUrl" target="_blank">{{scope.row.legalPolicyName}}</el-link>
                </template>
              </el-table-column>
              <el-table-column label="法规来源" width="200">
                <template #default="scope">
                  <el-tag>{{ scope.row.legalProvince }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="法规文号">
                <template #default="scope">
                  <el-tag>{{ scope.row.legalDocumentNumber }}</el-tag>
                </template>
              </el-table-column>

              <el-table-column label="发布时间" width="130" prop="legalPublishedTime" sortable>
                <template #default="scope">
                  <div style="display: flex; align-items: center">
                    <el-icon>
                      <timer />
                    </el-icon>
                    <span style="margin-left: 10px">{{ scope.row.legalPublishedTime }}</span>
                  </div>
                </template>
              </el-table-column>
              <el-table-column label="下载pdf" width="130">
                <template #default="scope">
                  <el-button type="primary" plain @click="myDownload(scope.row.legalPolicyText)">点击下载</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>
        <div class="rect1">
          <img alt="" src="../../assets/images/shape-1.png">
        </div>
        <div class="rect2">
          <img alt="" src="../../assets/images/shape-2.png">
        </div>
        <div class="rect3">
          <img alt="" src="../../assets/images/shape-3.png">
        </div>
        <div class="rect4">
          <img alt="" src="../../assets/images/shape-4.png">
        </div>
        <div class="rect5">
          <img alt="" src="../../assets/images/shape-3.png">
        </div>
      </div>

    </div>

  </div>

</template>

<style scoped>
</style>
