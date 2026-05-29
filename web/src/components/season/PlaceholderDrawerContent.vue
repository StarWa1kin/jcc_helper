<template>
  <scroll-view scroll-y class="placeholder-scroll">
    <view class="placeholder-panel">
      <view :class="['placeholder-bg', type]"></view>
      <text class="placeholder-title">{{ title }}</text>
      <text class="placeholder-desc">{{ desc }}</text>
      <view class="placeholder-list">
        <view v-for="item in examples" :key="item" class="placeholder-item">
          <text>{{ item }}</text>
          <text class="arrow">›</text>
        </view>
      </view>
    </view>
  </scroll-view>
</template>

<script>
export default {
  name: 'PlaceholderDrawerContent',
  props: {
    title: {
      type: String,
      default: '',
    },
    desc: {
      type: String,
      default: '',
    },
    type: {
      type: String,
      default: 'traits',
    },
  },
  computed: {
    examples() {
      const map = {
        traits: ['羁绊等级效果', '适配英雄', '推荐阵容'],
        items: ['装备合成路径', '适合英雄', '优先级说明'],
        runes: ['推荐场景', '强度评级', '适配阵容'],
        gods: ['神明机制', '选择建议', '阵容适配'],
      };
      return map[this.type] || ['资料详情', '推荐搭配', '版本说明'];
    },
  },
};
</script>

<style scoped>
.placeholder-scroll {
  height: 100%;
  padding: 20rpx;
}

.placeholder-panel {
  min-height: 620rpx;
  padding: 28rpx;
  border: 1rpx solid rgba(216, 163, 101, 0.42);
  border-radius: 22rpx;
  background: rgba(255, 255, 255, 0.06);
}

.placeholder-bg {
  height: 260rpx;
  border-radius: 18rpx;
  background:
    radial-gradient(circle at 70% 30%, rgba(255, 220, 148, 0.7), transparent 18%),
    linear-gradient(135deg, #362058, #7447c7 48%, #1b0b23);
}

.placeholder-bg.items {
  background:
    radial-gradient(circle at 68% 28%, rgba(120, 222, 255, 0.72), transparent 20%),
    linear-gradient(135deg, #122948, #2068b8 48%, #160b20);
}

.placeholder-bg.runes {
  background:
    radial-gradient(circle at 65% 34%, rgba(172, 255, 206, 0.72), transparent 20%),
    linear-gradient(135deg, #17382d, #3f9f66 48%, #140d1f);
}

.placeholder-bg.gods {
  background:
    radial-gradient(circle at 68% 30%, rgba(255, 172, 194, 0.78), transparent 20%),
    linear-gradient(135deg, #492036, #a13a58 48%, #170b20);
}

.placeholder-title {
  display: block;
  margin-top: 30rpx;
  color: #fff4df;
  font-size: 36rpx;
  font-weight: 900;
}

.placeholder-desc {
  display: block;
  margin-top: 12rpx;
  color: rgba(247, 236, 218, 0.62);
  font-size: 25rpx;
  line-height: 36rpx;
}

.placeholder-list {
  margin-top: 28rpx;
}

.placeholder-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 78rpx;
  margin-top: 14rpx;
  padding: 0 24rpx;
  border-radius: 16rpx;
  color: #efd8b0;
  font-size: 26rpx;
  font-weight: 800;
  background: rgba(255, 255, 255, 0.07);
}

.arrow {
  color: #b99569;
  font-size: 42rpx;
}
</style>
