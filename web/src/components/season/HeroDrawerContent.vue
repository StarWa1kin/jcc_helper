<template>
  <view class="hero-content">
    <view class="content-safe">
      <view class="drawer-search">
        <text class="drawer-search-icon">⌕</text>
        <input
          v-model="keyword"
          class="drawer-input"
          confirm-type="search"
          placeholder="搜索英雄"
          placeholder-class="drawer-input-placeholder"
        />
      </view>

      <view class="filter-row">
        <view v-for="filter in filters" :key="filter.label" class="filter-pill">
          <text class="filter-icon">{{ filter.icon }}</text>
          <text>{{ filter.label }}</text>
          <text class="chevron">⌄</text>
        </view>
      </view>
    </view>

    <scroll-view scroll-y class="content-scroll">
      <view class="feature-panel">
        <view class="feature-bg main-bg"></view>
        <view class="feature-copy">
          <text class="feature-title">跟着弈老师打宝不迷路，传奇小怪狂掉神装攻略</text>
          <text class="feature-desc">新版打宝思路详解，阵容搭配与装备优先级全解析。</text>
          <view class="review-row">
            <view class="avatar-bg"></view>
            <text>玩心手游测评</text>
            <text class="review-arrow">›</text>
          </view>
        </view>
      </view>

      <view class="hero-grid">
        <view v-for="hero in visibleHeroes" :key="hero.name" class="hero-card">
          <view :class="['hero-bg', hero.bg]"></view>
          <view class="hero-overlay"></view>
          <view class="hero-badge">{{ hero.cost }}</view>
          <view class="hero-info">
            <text class="hero-name">{{ hero.name }}</text>
            <view class="views">
              <text class="eye">◉</text>
              <text>{{ hero.views }}</text>
            </view>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script>
export default {
  name: 'HeroDrawerContent',
  data() {
    return {
      keyword: '',
      filters: [
        { icon: '◉', label: '全部费用' },
        { icon: '⬟', label: '全部职业' },
        { icon: '⬡', label: '全部特质' },
      ],
      heroes: [
        { name: '崔斯特', views: '12.3万', cost: '1', bg: 'bg-one' },
        { name: '伊泽瑞尔', views: '8.7万', cost: '1', bg: 'bg-two' },
        { name: '泰隆', views: '10.6万', cost: '1', bg: 'bg-three' },
        { name: '内瑟斯', views: '9.1万', cost: '1', bg: 'bg-four' },
        { name: '暮光吸', views: '7.6万', cost: '2', bg: 'bg-five' },
        { name: '吉克蓝', views: '6.2万', cost: '2', bg: 'bg-six' },
      ],
    };
  },
  computed: {
    visibleHeroes() {
      const keyword = this.keyword.trim();
      if (!keyword) return this.heroes;
      return this.heroes.filter((hero) => hero.name.includes(keyword));
    },
  },
};
</script>

<style scoped>
.hero-content {
  height: 100%;
}

.content-safe {
  padding: 18rpx 20rpx 0;
}

.drawer-search {
  display: flex;
  align-items: center;
  height: 86rpx;
  padding: 0 28rpx;
  border: 1rpx solid rgba(224, 175, 116, 0.2);
  border-radius: 43rpx;
  background: rgba(255, 255, 255, 0.07);
}

.drawer-search-icon {
  margin-right: 18rpx;
  font-size: 42rpx;
  color: #c7a985;
}

.drawer-input {
  flex: 1;
  height: 86rpx;
  color: #fff4df;
  font-size: 28rpx;
  font-weight: 700;
}

.drawer-input-placeholder {
  color: rgba(247, 236, 218, 0.48);
}

.filter-row {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18rpx;
  margin-top: 20rpx;
}

.filter-pill {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 0;
  height: 64rpx;
  border-radius: 14rpx;
  color: #ead9bd;
  font-size: 23rpx;
  font-weight: 900;
  background: rgba(255, 255, 255, 0.07);
}

.filter-icon {
  margin-right: 8rpx;
  color: #d5a66c;
  font-size: 24rpx;
}

.chevron {
  margin-left: 8rpx;
  color: #b99366;
}

.content-scroll {
  height: calc(100% - 188rpx);
  margin-top: 18rpx;
  padding-bottom: 32rpx;
}

.feature-panel {
  position: relative;
  min-height: 292rpx;
  margin: 0 20rpx 26rpx;
  overflow: hidden;
  border: 1rpx solid rgba(216, 163, 101, 0.52);
  border-radius: 18rpx;
  background: rgba(255, 255, 255, 0.06);
}

.feature-bg {
  position: absolute;
  left: 18rpx;
  top: 18rpx;
  width: 344rpx;
  height: 246rpx;
  border-radius: 14rpx;
}

.main-bg {
  background:
    radial-gradient(circle at 54% 28%, #f7df93 0 5%, transparent 18%),
    radial-gradient(circle at 60% 45%, #6428f7 0 18%, transparent 40%),
    linear-gradient(135deg, #2b1137, #6845bd 42%, #1b0b23);
}

.feature-copy {
  position: relative;
  margin-left: 386rpx;
  padding: 36rpx 22rpx 26rpx 0;
}

.feature-title {
  display: block;
  color: #fff7e7;
  font-size: 30rpx;
  font-weight: 900;
  line-height: 42rpx;
}

.feature-desc {
  display: block;
  margin-top: 18rpx;
  color: rgba(238, 218, 191, 0.58);
  font-size: 23rpx;
  line-height: 34rpx;
}

.review-row,
.hero-info,
.views {
  display: flex;
  align-items: center;
}

.review-row {
  margin-top: 26rpx;
  gap: 14rpx;
  color: #efdcbf;
  font-size: 24rpx;
  font-weight: 800;
}

.avatar-bg {
  width: 46rpx;
  height: 46rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, #ffe0a5, #8f572d 52%, #36182a);
}

.review-arrow {
  margin-left: auto;
  color: #b99569;
  font-size: 44rpx;
}

.hero-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 20rpx;
  padding: 0 20rpx 36rpx;
}

.hero-card {
  position: relative;
  height: 220rpx;
  overflow: hidden;
  border: 1rpx solid rgba(221, 167, 99, 0.66);
  border-radius: 16rpx;
  background: #28132c;
}

.hero-bg,
.hero-overlay {
  position: absolute;
  inset: 0;
}

.hero-overlay {
  background: linear-gradient(180deg, transparent 36%, rgba(15, 5, 22, 0.84) 100%);
}

.bg-one { background: radial-gradient(circle at 72% 22%, #f7da83, transparent 22%), linear-gradient(135deg, #34205c, #7c4ffc 46%, #1a0c22); }
.bg-two { background: radial-gradient(circle at 73% 24%, #f6c074, transparent 22%), linear-gradient(135deg, #102f55, #2aa9ff 42%, #1a0c22); }
.bg-three { background: radial-gradient(circle at 22% 30%, #5db9ff, transparent 24%), linear-gradient(135deg, #18245a, #4867ff 45%, #120917); }
.bg-four { background: radial-gradient(circle at 64% 42%, #74f7f2, transparent 26%), linear-gradient(135deg, #33226a, #2ec9ca 44%, #190d21); }
.bg-five { background: radial-gradient(circle at 20% 24%, #f08d35, transparent 24%), linear-gradient(135deg, #35162d, #a34a20 45%, #1b0c22); }
.bg-six { background: radial-gradient(circle at 58% 30%, #ca75ff, transparent 28%), linear-gradient(135deg, #1d1d61, #7b35d6 44%, #170b20); }

.hero-badge {
  position: absolute;
  left: 16rpx;
  top: 16rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 42rpx;
  height: 42rpx;
  border: 1rpx solid rgba(232, 189, 130, 0.72);
  border-radius: 12rpx;
  color: #f1d09a;
  font-size: 22rpx;
  font-weight: 900;
  background: rgba(22, 9, 28, 0.72);
}

.hero-info {
  position: absolute;
  left: 16rpx;
  right: 16rpx;
  bottom: 16rpx;
  justify-content: space-between;
}

.hero-name {
  color: #fff4df;
  font-size: 30rpx;
  font-weight: 900;
}

.views {
  gap: 6rpx;
  color: rgba(239, 219, 188, 0.72);
  font-size: 22rpx;
  font-weight: 800;
}

.eye {
  font-size: 20rpx;
}
</style>
