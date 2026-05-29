<template>
  <scroll-view scroll-y class="item-content">
    <view class="section">
      <text class="section-title">基础装备</text>
      <view class="base-row">
        <view
          v-for="item in baseItems"
          :key="item.key"
          :class="['item-icon', item.bg]"
        >
          <text class="item-mark">{{ item.label }}</text>
        </view>
      </view>
    </view>

    <view class="section craft-section">
      <text class="section-title">装备合成</text>
      <view class="craft-board">
        <view class="corner-cell">
          <text class="axis-arrow">↘</text>
        </view>
        <view class="top-axis">
          <view
            v-for="item in baseItems"
            :key="`top-${item.key}`"
            :class="['axis-icon', item.bg]"
          >
            <text class="axis-mark">{{ item.label }}</text>
          </view>
        </view>

        <view class="left-axis">
          <view
            v-for="item in baseItems"
            :key="`left-${item.key}`"
            :class="['axis-icon', item.bg]"
          >
            <text class="axis-mark">{{ item.label }}</text>
          </view>
        </view>

        <view class="recipe-grid">
          <view
            v-for="recipe in recipes"
            :key="recipe.key"
            :class="['recipe-icon', recipe.bg]"
          >
            <text class="recipe-mark">{{ recipe.label }}</text>
          </view>
        </view>
      </view>
    </view>
  </scroll-view>
</template>

<script>
const baseItems = [
  { key: 'sword', label: '剑', bg: 'bg-sword' },
  { key: 'bow', label: '弓', bg: 'bg-bow' },
  { key: 'rod', label: '棒', bg: 'bg-rod' },
  { key: 'tear', label: '泪', bg: 'bg-tear' },
  { key: 'vest', label: '甲', bg: 'bg-vest' },
  { key: 'cloak', label: '斗', bg: 'bg-cloak' },
  { key: 'belt', label: '带', bg: 'bg-belt' },
  { key: 'glove', label: '套', bg: 'bg-glove' },
  { key: 'pan', label: '锅', bg: 'bg-pan' },
  { key: 'spatula', label: '铲', bg: 'bg-spatula' },
];

const recipePalette = [
  'recipe-flame',
  'recipe-tide',
  'recipe-venom',
  'recipe-storm',
  'recipe-void',
  'recipe-gold',
  'recipe-iron',
  'recipe-star',
  'recipe-sigil',
  'recipe-spirit',
];

export default {
  name: 'ItemDrawerContent',
  data() {
    return {
      baseItems,
    };
  },
  computed: {
    recipes() {
      const recipes = [];
      this.baseItems.forEach((rowItem, rowIndex) => {
        this.baseItems.forEach((colItem, colIndex) => {
          const paletteIndex = (rowIndex * 3 + colIndex * 5) % recipePalette.length;
          recipes.push({
            key: `${rowItem.key}-${colItem.key}`,
            label: `${rowItem.label}${colItem.label}`,
            bg: recipePalette[paletteIndex],
          });
        });
      });
      return recipes;
    },
  },
};
</script>

<style scoped>
.item-content {
  height: 100%;
  padding: 18rpx 20rpx 42rpx;
}

.section {
  padding: 20rpx 10rpx 0;
}

.craft-section {
  margin-top: 58rpx;
}

.section-title {
  display: block;
  color: #f2e2c9;
  font-size: 28rpx;
  font-weight: 900;
}

.base-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
  margin-top: 28rpx;
}

.item-icon,
.axis-icon,
.recipe-icon {
  position: relative;
  overflow: hidden;
  border: 2rpx solid rgba(231, 191, 132, 0.58);
  border-radius: 4rpx;
  box-shadow: inset 0 0 0 1rpx rgba(255, 255, 255, 0.12);
}

.item-icon {
  width: 58rpx;
  height: 58rpx;
}

.item-mark,
.axis-mark,
.recipe-mark {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 4rpx;
  color: #fff5de;
  font-weight: 900;
  text-align: center;
  text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.72);
}

.item-mark {
  font-size: 20rpx;
}

.craft-board {
  display: grid;
  grid-template-columns: 48rpx 1fr;
  grid-template-rows: 48rpx auto;
  gap: 6rpx;
  margin-top: 26rpx;
}

.corner-cell {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48rpx;
  height: 48rpx;
}

.axis-arrow {
  color: rgba(217, 180, 128, 0.55);
  font-size: 40rpx;
  font-weight: 900;
}

.top-axis,
.recipe-grid {
  display: grid;
  grid-template-columns: repeat(10, 1fr);
  gap: 6rpx;
}

.left-axis {
  display: grid;
  grid-template-rows: repeat(10, 1fr);
  gap: 6rpx;
}

.axis-icon,
.recipe-icon {
  width: 48rpx;
  height: 48rpx;
}

.axis-mark {
  font-size: 16rpx;
}

.recipe-mark {
  font-size: 15rpx;
}

.bg-sword { background: linear-gradient(135deg, #1b2a66, #e1c86e 52%, #402616); }
.bg-bow { background: linear-gradient(135deg, #283b1c, #c7d092 50%, #3a2614); }
.bg-rod { background: radial-gradient(circle at 62% 32%, #ff9de6, transparent 24%), linear-gradient(135deg, #36104e, #b932a0 55%, #1b0c27); }
.bg-tear { background: radial-gradient(circle at 55% 36%, #55d7ff, transparent 28%), linear-gradient(135deg, #10225a, #164fde 58%, #070d2c); }
.bg-vest { background: linear-gradient(135deg, #153b49, #5fc3bf 48%, #1b2229); }
.bg-cloak { background: linear-gradient(135deg, #fff0a8, #a67836 46%, #463322); }
.bg-belt { background: linear-gradient(135deg, #372313, #a36f43 45%, #e6c29a); }
.bg-glove { background: linear-gradient(135deg, #f1e06c, #b59c1e 48%, #2a240d); }
.bg-pan { background: linear-gradient(135deg, #3a3a3a, #a8a29a 48%, #171717); }
.bg-spatula { background: radial-gradient(circle at 46% 44%, #fff07a, transparent 24%), linear-gradient(135deg, #563c16, #d6a328 58%, #3b2608); }

.recipe-flame { background: radial-gradient(circle at 58% 36%, #ffcf72, transparent 24%), linear-gradient(135deg, #4b1111, #f36b20 55%, #220807); }
.recipe-tide { background: radial-gradient(circle at 56% 34%, #a5f8ff, transparent 25%), linear-gradient(135deg, #0d3954, #218dd9 56%, #091626); }
.recipe-venom { background: radial-gradient(circle at 58% 36%, #bbff90, transparent 24%), linear-gradient(135deg, #123a22, #22a35a 55%, #08180f); }
.recipe-storm { background: radial-gradient(circle at 58% 36%, #e2f0ff, transparent 22%), linear-gradient(135deg, #271f5c, #5f7cff 55%, #100a24); }
.recipe-void { background: radial-gradient(circle at 58% 36%, #d897ff, transparent 24%), linear-gradient(135deg, #35184e, #8c35b3 55%, #16091f); }
.recipe-gold { background: radial-gradient(circle at 58% 36%, #fff2a7, transparent 24%), linear-gradient(135deg, #5a3714, #d9962b 55%, #1d1207); }
.recipe-iron { background: radial-gradient(circle at 58% 36%, #d3dde6, transparent 22%), linear-gradient(135deg, #242d36, #738391 55%, #0e1115); }
.recipe-star { background: radial-gradient(circle at 58% 36%, #ffffff, transparent 20%), linear-gradient(135deg, #363e8a, #9aa7ff 55%, #151833); }
.recipe-sigil { background: radial-gradient(circle at 58% 36%, #ffafda, transparent 23%), linear-gradient(135deg, #4a1738, #d35a94 55%, #1d0a18); }
.recipe-spirit { background: radial-gradient(circle at 58% 36%, #f7fff1, transparent 22%), linear-gradient(135deg, #2b4e3b, #9dcc8a 55%, #111c13); }
</style>
