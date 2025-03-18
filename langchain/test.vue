<script setup>
import { ref, onMounted } from 'vue'

// 响应式数据
const count = ref(0)
const message = ref('Hello Vue 3!')

// 方法
const increment = () => {
  count.value++
}

// props 定义
const props = defineProps({
  title: {
    type: String,
    default: 'Default Title'
  },
  items: {
    type: Array,
    default: () => []
  }
})

// emit 事件
const emit = defineEmits(['update', 'delete'])

// 生命周期钩子
onMounted(() => {
  console.log('组件已挂载')
})

// 计算属性
const doubleCount = computed(() => count.value * 2)
</script>

<template>
  <div class="example-component">
    <h1>{{ props.title }}</h1>
    <p>{{ message }}</p>
    
    <div class="counter">
      <p>Count: {{ count }}</p>
      <p>Double Count: {{ doubleCount }}</p>
      <button @click="increment">增加</button>
    </div>
    
    <div class="list" v-if="props.items.length">
      <ul>
        <li v-for="(item, index) in props.items" 
            :key="index"
            @click="emit('update', item)">
          {{ item }}
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.example-component {
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;
}

.counter {
  margin: 20px 0;
  padding: 15px;
  border: 1px solid #eee;
  border-radius: 8px;
}

button {
  padding: 8px 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

.list {
  margin-top: 20px;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  padding: 10px;
  margin: 5px 0;
  background-color: #f5f5f5;
  border-radius: 4px;
  cursor: pointer;
}

li:hover {
  background-color: #e0e0e0;
}
</style>