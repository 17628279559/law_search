import { createStore } from 'vuex'

const store = createStore({
  state: {
    count: 0
  },
  getters: {
    //计算属性
    sqrtCount(state) {
      return Math.sqrt(state.count)
    }
  },
  mutations: {
    //修改属性
    change(state, data) {
      state.count += data
    }
  },
  actions: {
    asyncChange({ commit }, data) {
      setTimeout(() => {
        commit('change', data)
      }, 1000)
    }
  } //异步函数
})

export default store
