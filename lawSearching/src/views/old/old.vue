<script setup>
import { useStore } from 'vuex'
import { computed, ref } from 'vue'
const store = useStore()


const count = computed(() => store.state.count)
const change = data => store.commit("change", data)
const asyncChange = data => store.dispatch("asyncChange", data)
const nowId = ref('search_1')
const inputTxt = ref(null)
const lawSearch = () => {

}

const searchList = [
  { id: 'search_2', action: "https://www.baidu.com/s?wd=", name: "百度搜索", shortName: "百度", method: "get" },
  { id: 'search_3', action: "https://cn.bing.com/search?q=", name: "Bing搜索", shortName: "Bing", method: "get" },
  { id: 'search_4', action: "https://www.so.com/s?q=", name: "360搜索", shortName: "360", method: "get" },
  { id: 'search_5', action: "https://www.sogou.com/web?query=", name: "搜狗搜索", shortName: "搜狗", method: "get" },
  { id: 'search_6', action: "https://list.tmall.com/search_product.htm?q=", name: "天猫搜索", shortName: "天猫", method: "get" },
  { id: 'search_7', action: "https://s.taobao.com/search?q=", name: "淘宝搜索", shortName: "淘宝", method: "get" },
  { id: 'search_8', action: "https://www.zhihu.com/search?q=", name: "知乎搜索", method: "get" }
]



</script>

<template>
  <div id="banner-bear" class="preserve3d csstransforms3d">
    <p class="typing web-font transition">全国各省份法律检索</p>
    <div class="primary-menus">
      <ul class="selects">
        <li :class="[nowId === 'search_1' ? 'current' :'']" @click="nowId = 'search_1'"><span>本站</span></li>
        <li v-for="(item, index) in searchList" :key="index" :class="[item.id === nowId? 'current':'']" @click="nowId = item.id"><span>{{item.shortName}}</span></li>
      </ul>
      <div class="cont">
        <div class="left-cont">
          <form :class="[nowId === 'search_1' ? 'search':'search hidden']" id="search_1">
            <input ref="inputTxt" type="text" name="wd" class="s" placeholder="请输入法律关键词">
            <button type="submit" name="" class="btn" @click="lawSearch()">站内搜索</button>
          </form>
          <form v-for="(item, index) in searchList" :key="index" :class="[item.id === nowId? 'search':'search hidden']" :id="item.id" :action="item.action" :method="item.method" :target="_blank">
            <input type="text" name="wd" class="s" placeholder="请输入法律关键词">
            <button type="submit" name="" class="btn">{{item.name}}</button>
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
</template>

<style scoped>
</style>
