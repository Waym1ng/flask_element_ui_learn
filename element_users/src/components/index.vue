<template>
  <div>
    <el-carousel indicator-position="outside">
      <el-carousel-item v-for="item in iamges" :key="item.index">
        <el-image
          style="width: 100%"
          :src="item.img"
          fit="fill"
        ></el-image>
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<script>
export default {
  name: "Index",
  data() {
    return {
      iamges: [
        { img: require("../assets/images/1.jpg") },
        { img: require("../assets/images/2.jpg") },
        { img: require("../assets/images/3.jpg") },
        { img: require("../assets/images/4.jpg") },
      ],
    };
  },
  methods: {},
};
</script>

<style scoped>
.el-carousel__item h3 {
  color: #475669;
  font-size: 18px;
  opacity: 0.75;
  line-height: 300px;
  margin: 0;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
</style>
