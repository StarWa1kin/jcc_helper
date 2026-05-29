<template>
  <uni-drawer
    ref="drawer"
    mode="right"
    :width="drawerWidth"
    :mask-click="true"
    @change="handleChange"
  >
    <view class="drawer-shell">
      <view class="drawer-safe">
        <view class="drawer-header">
          <button class="icon-button" hover-class="button-hover" @tap="close">‹</button>
          <view class="title-block">
            <text class="drawer-kicker">赛季资料</text>
            <text class="drawer-title">{{ title }}</text>
          </view>
          <button class="icon-button" hover-class="button-hover">⋯</button>
        </view>
      </view>

      <view class="drawer-body">
        <slot />
      </view>
    </view>
  </uni-drawer>
</template>

<script>
export default {
  name: 'SeasonDrawer',
  props: {
    title: {
      type: String,
      default: '英雄资料',
    },
    type: {
      type: String,
      default: 'heroes',
    },
  },
  emits: ['opened', 'closed'],
  data() {
    return {
      drawerWidth: 375,
    };
  },
  mounted() {
    const systemInfo = uni.getSystemInfoSync();
    this.drawerWidth = systemInfo.windowWidth;
  },
  methods: {
    open() {
      this.$refs.drawer.open();
    },
    close() {
      this.$refs.drawer.close();
    },
    handleChange(opened) {
      this.$emit(opened ? 'opened' : 'closed');
    },
  },
};
</script>

<style scoped>
.drawer-shell {
  width: 100%;
  height: 100vh;
  overflow: hidden;
  background:
    radial-gradient(circle at 20% 0%, rgba(117, 77, 154, 0.28), transparent 28%),
    linear-gradient(180deg, #1b1028 0%, #2a1434 55%, #210c26 100%);
}

.drawer-safe {
  padding: calc(var(--status-bar-height) + 18rpx) 20rpx 0;
}

.drawer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 74rpx;
}

.title-block {
  text-align: center;
}

.drawer-kicker {
  display: block;
  font-size: 22rpx;
  font-weight: 700;
  color: #c39b70;
  letter-spacing: 0;
}

.drawer-title {
  display: block;
  margin-top: 2rpx;
  font-size: 34rpx;
  font-weight: 900;
  color: #fff3dd;
}

.icon-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60rpx;
  height: 60rpx;
  padding: 0;
  border: 0;
  border-radius: 50%;
  color: #f6e6c8;
  font-size: 44rpx;
  line-height: 60rpx;
  background: rgba(255, 255, 255, 0.08);
}

.icon-button::after {
  border: 0;
}

.button-hover {
  opacity: 0.82;
}

.drawer-body {
  height: calc(100vh - 92rpx - var(--status-bar-height));
}
</style>
