<template>
  <div class="shadow-container" style="text-align: left;">
    <a :href="card.cover_href" target="_blank">
      <img class="cover" :src="card.cover_url">
    </a>
    <div class="linear"></div>
    <div class="show">
      <a :href="card.face_href" target="_blank" style="--size: 60px; margin: 12px;">
        <div class="pendant" :url="card.pendant != ''" :style="`background-image: url(${card.pendant})`">
          <img :src="card.face_url" :style="`outline-color: ${card.pendant_color}`">
        </div>
      </a>
      <strong>  
        <p class="title" :style="`color: ${card.title_color};`">{{ card.title }}</p>
        <span class="subtitle">{{ card.subtitle }}</span>
      </strong>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, Ref } from 'vue'
import axios from 'axios'

export interface userInfo {
    face_href: string
    face_url: string
    pendant: string
    pendant_color: string
    cover_href: string
    cover_url: string
    title: string
    title_color: string
    subtitle: string
}

const card = ref()

axios.get(`https://aliyun.nana7mi.link/live.LiveRoom(21452505).get_room_info()`).then(res => {
  let data = res.data.data
  let info: userInfo = {
    cover_href: `https://live.bilibili.com/${data.room_info.room_id}`,
    cover_url: data.room_info.cover,
    face_href: `https://space.bilibili.com/${data.room_info.uid}`,
    face_url: data.anchor_info.base_info.face,
    pendant: "",
    pendant_color: "rgb(251, 114, 153)",
    title: data.anchor_info.base_info.uname,
    title_color: "rgb(251, 114, 153)",
    subtitle: `粉丝 ${data.anchor_info.relation_info.attention} - 舰长 ${data.guard_info.count}`
  }
  card.value = info
})
</script>

<style scoped>
.shadow-container {
  width: 300px;
  padding: 0;
  position: relative;
  z-index: 1;
  margin: 8px auto;
  border-radius: 5px;
  transition: all 0.2s;
  background-color: rgba(255,255,255,0.75);
  box-shadow: 0 3px 1px -2px rgb(0 0 0 / 12%),
              0 2px 2px 0 rgb(0 0 0 / 14%),
              0 1px 5px 0 rgb(0 0 0 / 20%);
}
.pendant {
  width: var(--size);
  height: var(--size);
  position: relative;
  background-size: contain;
}

.pendant img {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: -1;
  border-radius: 50%;
  height: var(--size);
  outline-style: solid;
  outline-width: 0.0428 * var(--size);
  outline-color: rgb(0, 161, 214);
}

.cover {
  width: 100%;
  border-radius: 5px 5px 0 0;
  display: block;
}

.linear {
  position: relative;
  height: 20px;
  z-index: 2;
  margin-top: -20px;
  background-image: linear-gradient(rgba(255, 255, 255, 0), rgba(255, 255, 255, 1));
}

.show {
  display: flex;
  align-items: center;
  z-index: 2;
  position: relative;
}

.title {
  font-size: 1.5em;
  margin: 0;
}

.subtitle {
  color: grey;
  font-size: 8px;
}
</style>