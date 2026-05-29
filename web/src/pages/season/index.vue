<template>
  <view class="season-page">
    <view class="top-visual">
      <view class="title-bar">
        <text class="title-deco">◇</text>
        <text class="page-title">赛季资料</text>
        <text class="title-deco">◇</text>
      </view>
      <view class="window-actions">
        <text>•••</text>
        <text class="divider"></text>
        <text>−</text>
        <text class="circle"></text>
      </view>
    </view>

    <view class="tab-shell">
      <view
        v-for="tab in tabs"
        :key="tab.key"
        :class="['tab-item', activeTab === tab.key ? 'active' : '']"
        @tap="activeTab = tab.key"
      >
        <text class="tab-icon">{{ tab.icon }}</text>
        <text class="tab-label">{{ tab.label }}</text>
      </view>
    </view>

    <scroll-view scroll-y class="content-scroll">
      <view v-if="activeTab === 'heroes'" class="tab-panel hero-panel">
        <view class="search-box">
          <text class="search-icon">⌕</text>
          <input
            v-model="heroKeyword"
            class="search-input"
            confirm-type="search"
            placeholder="搜索英雄"
            placeholder-class="placeholder"
          />
        </view>

        <view class="filter-row">
          <view v-for="filter in heroFilters" :key="filter.label" class="filter-pill">
            <text class="filter-icon">{{ filter.icon }}</text>
            <text>{{ filter.label }}</text>
            <text class="chevron">⌄</text>
          </view>
        </view>

        <view class="guide-card">
          <view class="guide-bg">
            <text class="guide-badge">推荐攻略</text>
            <view class="mini-items">
              <view v-for="index in 8" :key="index" :class="['mini-item', `mini-${index}`]"></view>
            </view>
          </view>
          <view class="guide-copy">
            <text class="guide-title">跟着弈老师打宝不迷路，传奇小怪狂掉神装攻略</text>
            <text class="guide-desc">新版打宝思路详解，阵容搭配与装备优先级全解析。</text>
            <view class="review-row">
              <view class="avatar"></view>
              <text>玩心手游测评</text>
              <text class="review-arrow">›</text>
            </view>
          </view>
        </view>

        <view class="hero-grid">
          <view v-for="hero in visibleHeroes" :key="hero.name" class="hero-card">
            <view :class="['hero-bg', hero.bg]"></view>
            <view class="hero-shade"></view>
            <view class="cost-badge">{{ hero.cost }}</view>
            <view class="hero-meta">
              <text class="hero-name">{{ hero.name }}</text>
              <view class="views">
                <text>◉</text>
                <text>{{ hero.views }}</text>
              </view>
            </view>
          </view>
        </view>
      </view>

      <view v-else-if="activeTab === 'traits'" class="tab-panel trait-panel">
        <view class="section-head">
          <text class="section-title">羁绊效果</text>
          <text class="section-sub">按职业与特质快速查看等级收益</text>
        </view>
        <view class="trait-list">
          <view v-for="trait in traits" :key="trait.name" class="trait-card">
            <view :class="['trait-emblem', trait.tone]">{{ trait.icon }}</view>
            <view class="trait-main">
              <view class="trait-top">
                <text class="trait-name">{{ trait.name }}</text>
                <text class="trait-count">{{ trait.count }}</text>
              </view>
              <text class="trait-desc">{{ trait.desc }}</text>
              <view class="trait-levels">
                <text v-for="level in trait.levels" :key="level">{{ level }}</text>
              </view>
            </view>
          </view>
        </view>
      </view>

      <view v-else-if="activeTab === 'items'" class="tab-panel item-panel">
        <view class="section-head">
          <text class="section-title">基础装备</text>
        </view>
        <view class="base-items">
          <view v-for="item in baseItems" :key="item.key" :class="['equip-icon', item.bg]">
            <text>{{ item.label }}</text>
          </view>
        </view>

        <view class="section-head craft-title">
          <text class="section-title">装备合成</text>
        </view>
        <view class="craft-board">
          <view class="corner">↘</view>
          <view class="top-axis">
            <view v-for="item in baseItems" :key="`top-${item.key}`" :class="['axis-icon', item.bg]">
              <text>{{ item.label }}</text>
            </view>
          </view>
          <view class="left-axis">
            <view v-for="item in baseItems" :key="`left-${item.key}`" :class="['axis-icon', item.bg]">
              <text>{{ item.label }}</text>
            </view>
          </view>
          <view class="recipe-grid">
            <view v-for="recipe in recipes" :key="recipe.key" :class="['recipe-icon', recipe.bg]">
              <text>{{ recipe.label }}</text>
            </view>
          </view>
        </view>
      </view>

      <view v-else-if="activeTab === 'runes'" class="tab-panel rune-panel">
        <view class="section-head">
          <text class="section-title">强化符文</text>
          <text class="section-sub">按经济、战力、转职和专属分类</text>
        </view>
        <view class="rune-grid">
          <view v-for="rune in runes" :key="rune.name" class="rune-card">
            <view :class="['rune-mark', rune.tone]">{{ rune.icon }}</view>
            <text class="rune-name">{{ rune.name }}</text>
            <text class="rune-desc">{{ rune.desc }}</text>
            <view class="rune-tags">
              <text v-for="tag in rune.tags" :key="tag">{{ tag }}</text>
            </view>
          </view>
        </view>
      </view>

      <view v-else class="tab-panel god-panel">
        <view class="god-hero">
          <view class="god-bg"></view>
          <text class="god-title">神明资料</text>
          <text class="god-desc">查看神明机制、选择建议和阵容适配关系。</text>
        </view>
        <view class="god-list">
          <view v-for="god in gods" :key="god.name" class="god-card">
            <view :class="['god-icon', god.tone]">{{ god.icon }}</view>
            <view>
              <text class="god-name">{{ god.name }}</text>
              <text class="god-tip">{{ god.tip }}</text>
            </view>
            <text class="god-arrow">›</text>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
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
  data() {
    return {
      activeTab: 'heroes',
      heroKeyword: '',
      tabs: [
        { key: 'heroes', label: '英雄', icon: '♜' },
        { key: 'traits', label: '羁绊', icon: '❖' },
        { key: 'items', label: '装备', icon: '♛' },
        { key: 'runes', label: '强化符文', icon: '✧' },
        { key: 'gods', label: '神明', icon: '✬' },
      ],
      heroFilters: [
        { icon: '◉', label: '全部费用' },
        { icon: '⬟', label: '全部职业' },
        { icon: '⬡', label: '全部特质' },
      ],
      heroes: [
        { name: '崔斯特', views: '12.3万', cost: '1', bg: 'hero-one' },
        { name: '伊泽瑞尔', views: '8.7万', cost: '1', bg: 'hero-two' },
        { name: '泰隆', views: '10.6万', cost: '1', bg: 'hero-three' },
        { name: '内瑟斯', views: '9.1万', cost: '1', bg: 'hero-four' },
        { name: '暮光吸', views: '7.6万', cost: '2', bg: 'hero-five' },
        { name: '吉克蓝', views: '6.2万', cost: '2', bg: 'hero-six' },
      ],
      traits: [
        { name: '星神', icon: '星', count: '2/4/6', desc: '友军造成伤害时获得治疗，后期容错更高。', levels: ['2: 12%', '4: 25%', '6: 45%'], tone: 'tone-gold' },
        { name: '圣盾使', icon: '盾', count: '2/4/6', desc: '释放技能后获得护盾，适合前排持续作战。', levels: ['2: 20%', '4: 35%', '6: 50%'], tone: 'tone-blue' },
        { name: '狙神', icon: '狙', count: '2/4', desc: '距离越远伤害越高，适合后排主 C。', levels: ['2: +8%', '4: +18%'], tone: 'tone-violet' },
      ],
      baseItems,
      runes: [
        { name: '经济扩张', icon: '金', desc: '更快成型，适合连胜或高费运营。', tags: ['经济', '运营'], tone: 'tone-gold' },
        { name: '前排壁垒', icon: '盾', desc: '补足坦度，提升阵容启动时间。', tags: ['防御', '前排'], tone: 'tone-blue' },
        { name: '火力倾泻', icon: '攻', desc: '提升主 C 输出峰值，适合爆发阵容。', tags: ['输出', '主C'], tone: 'tone-rose' },
        { name: '职业之心', icon: '转', desc: '提前开启关键羁绊节点。', tags: ['转职', '羁绊'], tone: 'tone-violet' },
      ],
      gods: [
        { name: '裁决之神', icon: '裁', tip: '适合斩杀与爆发阵容', tone: 'tone-gold' },
        { name: '守护之神', icon: '守', tip: '适合前排厚度不足时选择', tone: 'tone-blue' },
        { name: '秘术之神', icon: '秘', tip: '适合法系和控制链阵容', tone: 'tone-violet' },
      ],
    };
  },
  computed: {
    visibleHeroes() {
      const keyword = this.heroKeyword.trim();
      if (!keyword) return this.heroes;
      return this.heroes.filter((hero) => hero.name.includes(keyword));
    },
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
.season-page {
  min-height: 100vh;
  overflow: hidden;
  color: #f5e6cb;
  background: #21102a;
}

.top-visual {
  position: relative;
  height: 158rpx;
  padding-top: calc(var(--status-bar-height) + 38rpx);
  overflow: hidden;
  border-bottom: 1rpx solid rgba(226, 176, 108, 0.45);
  border-radius: 0 0 34rpx 34rpx;
  background:
    radial-gradient(circle at 46% 0%, rgba(211, 136, 71, 0.18), transparent 18%),
    radial-gradient(circle at 20% 0%, rgba(95, 48, 171, 0.62), transparent 46%),
    linear-gradient(135deg, #16091f 0%, #351a49 52%, #12091b 100%);
}

.title-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 14rpx;
}

.page-title {
  color: #fff1d5;
  font-size: 38rpx;
  font-weight: 900;
}

.title-deco {
  color: #ba8350;
  font-size: 24rpx;
}

.window-actions {
  position: absolute;
  right: 18rpx;
  top: calc(var(--status-bar-height) + 22rpx);
  display: flex;
  align-items: center;
  gap: 20rpx;
  height: 58rpx;
  padding: 0 18rpx;
  border: 1rpx solid rgba(233, 198, 148, 0.42);
  border-radius: 30rpx;
  color: #f1dcc0;
  font-size: 27rpx;
  font-weight: 900;
  background: rgba(37, 17, 49, 0.74);
}

.divider {
  width: 1rpx;
  height: 34rpx;
  background: rgba(233, 198, 148, 0.35);
}

.circle {
  width: 22rpx;
  height: 22rpx;
  border: 6rpx solid #f0dcc1;
  border-radius: 50%;
}

.tab-shell {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  height: 102rpx;
  border-bottom: 1rpx solid rgba(182, 132, 84, 0.32);
  background: linear-gradient(180deg, #24152f, #1c1027);
}

.tab-item {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: rgba(223, 202, 176, 0.62);
}

.tab-item.active {
  color: #ffe3a5;
  background: linear-gradient(180deg, rgba(216, 149, 72, 0.18), rgba(216, 149, 72, 0.02));
}

.tab-item.active::after {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 4rpx;
  background: linear-gradient(90deg, transparent, #e6ad58, transparent);
  content: '';
}

.tab-icon {
  font-size: 36rpx;
  line-height: 38rpx;
}

.tab-label {
  margin-top: 6rpx;
  font-size: 23rpx;
  font-weight: 900;
}

.content-scroll {
  height: calc(100vh - 260rpx - var(--status-bar-height));
  background:
    radial-gradient(circle at 100% 4%, rgba(111, 65, 138, 0.24), transparent 30%),
    linear-gradient(180deg, #21102a 0%, #35173a 100%);
}

.tab-panel {
  padding: 22rpx 18rpx 34rpx;
}

.search-box {
  display: flex;
  align-items: center;
  height: 76rpx;
  padding: 0 26rpx;
  border: 1rpx solid rgba(219, 173, 116, 0.2);
  border-radius: 38rpx;
  background: rgba(255, 255, 255, 0.06);
}

.search-icon {
  margin-right: 18rpx;
  color: #bd9d82;
  font-size: 38rpx;
}

.search-input {
  flex: 1;
  height: 76rpx;
  color: #fff2d8;
  font-size: 27rpx;
  font-weight: 800;
}

.placeholder {
  color: rgba(231, 206, 181, 0.48);
}

.filter-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18rpx;
  margin-top: 22rpx;
}

.filter-pill {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 0;
  height: 62rpx;
  border-radius: 12rpx;
  color: #e7d4b8;
  font-size: 23rpx;
  font-weight: 900;
  background: rgba(255, 255, 255, 0.06);
}

.filter-icon {
  margin-right: 8rpx;
  color: #c49b72;
}

.chevron {
  margin-left: 8rpx;
  color: #b28a67;
}

.guide-card {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24rpx;
  min-height: 280rpx;
  margin-top: 28rpx;
  padding: 18rpx;
  border: 1rpx solid rgba(221, 166, 100, 0.54);
  border-radius: 16rpx;
  background: rgba(255, 255, 255, 0.05);
}

.guide-bg {
  position: relative;
  min-height: 244rpx;
  overflow: hidden;
  border-radius: 14rpx;
  background:
    radial-gradient(circle at 62% 25%, #f0d77b, transparent 15%),
    radial-gradient(circle at 50% 43%, #7a3aff, transparent 36%),
    linear-gradient(135deg, #2d1537, #5c38a8 52%, #16091f);
}

.guide-badge {
  position: absolute;
  left: 0;
  top: 0;
  padding: 10rpx 18rpx;
  border-radius: 0 0 16rpx 0;
  color: #fff3dc;
  font-size: 22rpx;
  font-weight: 900;
  background: rgba(167, 102, 48, 0.82);
}

.mini-items {
  position: absolute;
  left: 90rpx;
  bottom: 26rpx;
  display: grid;
  grid-template-columns: repeat(4, 34rpx);
  gap: 8rpx;
}

.mini-item {
  width: 34rpx;
  height: 34rpx;
  border: 1rpx solid rgba(237, 197, 136, 0.68);
  border-radius: 4rpx;
}

.mini-1,.mini-5 { background: #c99b39; }
.mini-2,.mini-6 { background: #286bd8; }
.mini-3,.mini-7 { background: #7932b8; }
.mini-4,.mini-8 { background: #1b994f; }

.guide-copy {
  padding: 12rpx 0;
}

.guide-title {
  display: block;
  color: #fff2dc;
  font-size: 30rpx;
  font-weight: 900;
  line-height: 42rpx;
}

.guide-desc {
  display: block;
  margin-top: 18rpx;
  color: rgba(235, 214, 194, 0.58);
  font-size: 24rpx;
  line-height: 34rpx;
}

.review-row,
.hero-meta,
.views,
.trait-card,
.trait-top,
.god-card {
  display: flex;
  align-items: center;
}

.review-row {
  gap: 14rpx;
  margin-top: 24rpx;
  color: #e7d0ad;
  font-size: 23rpx;
  font-weight: 800;
}

.avatar {
  width: 44rpx;
  height: 44rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, #ffe3a3, #895421 52%, #2b1631);
}

.review-arrow {
  margin-left: auto;
  color: #b99569;
  font-size: 42rpx;
}

.hero-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18rpx;
  margin-top: 28rpx;
}

.hero-card {
  position: relative;
  height: 220rpx;
  overflow: hidden;
  border: 1rpx solid rgba(221, 166, 100, 0.62);
  border-radius: 14rpx;
  background: #25122e;
}

.hero-bg,
.hero-shade {
  position: absolute;
  inset: 0;
}

.hero-shade {
  background: linear-gradient(180deg, transparent 35%, rgba(17, 7, 23, 0.86) 100%);
}

.hero-one { background: radial-gradient(circle at 66% 28%, #dcc067, transparent 20%), linear-gradient(135deg, #33205f, #7548ec 48%, #16091f); }
.hero-two { background: radial-gradient(circle at 70% 26%, #f0b16f, transparent 22%), linear-gradient(135deg, #122b55, #23a1e4 48%, #16091f); }
.hero-three { background: radial-gradient(circle at 25% 28%, #6dc7ff, transparent 24%), linear-gradient(135deg, #17235b, #435df0 52%, #16091f); }
.hero-four { background: radial-gradient(circle at 65% 42%, #78fff3, transparent 24%), linear-gradient(135deg, #3f2261, #31c4bc 48%, #16091f); }
.hero-five { background: radial-gradient(circle at 20% 26%, #f49133, transparent 23%), linear-gradient(135deg, #38162d, #a44d20 52%, #16091f); }
.hero-six { background: radial-gradient(circle at 60% 30%, #c66cff, transparent 24%), linear-gradient(135deg, #1b1d61, #7433cd 52%, #16091f); }

.cost-badge {
  position: absolute;
  left: 14rpx;
  top: 14rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40rpx;
  height: 40rpx;
  border: 1rpx solid rgba(232, 189, 130, 0.72);
  border-radius: 10rpx;
  color: #f2cf97;
  font-size: 20rpx;
  font-weight: 900;
  background: rgba(22, 9, 28, 0.72);
}

.hero-meta {
  position: absolute;
  left: 16rpx;
  right: 16rpx;
  bottom: 16rpx;
  justify-content: space-between;
}

.hero-name {
  color: #fff2dc;
  font-size: 30rpx;
  font-weight: 900;
}

.views {
  gap: 6rpx;
  color: rgba(239, 219, 188, 0.72);
  font-size: 22rpx;
  font-weight: 800;
}

.section-head {
  padding: 8rpx 0 20rpx;
}

.section-title {
  display: block;
  color: #fff0d6;
  font-size: 31rpx;
  font-weight: 900;
}

.section-sub {
  display: block;
  margin-top: 8rpx;
  color: rgba(235, 214, 194, 0.56);
  font-size: 24rpx;
}

.trait-list {
  display: grid;
  gap: 18rpx;
}

.trait-card {
  gap: 20rpx;
  padding: 22rpx;
  border: 1rpx solid rgba(221, 166, 100, 0.32);
  border-radius: 18rpx;
  background: rgba(255, 255, 255, 0.055);
}

.trait-emblem,
.rune-mark,
.god-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: #1c1027;
  font-weight: 900;
}

.trait-emblem {
  width: 76rpx;
  height: 76rpx;
  border-radius: 22rpx;
  font-size: 30rpx;
}

.trait-main {
  flex: 1;
}

.trait-top {
  justify-content: space-between;
}

.trait-name {
  color: #fff1d5;
  font-size: 30rpx;
  font-weight: 900;
}

.trait-count {
  color: #d5aa72;
  font-size: 23rpx;
  font-weight: 900;
}

.trait-desc {
  display: block;
  margin-top: 10rpx;
  color: rgba(235, 214, 194, 0.62);
  font-size: 24rpx;
  line-height: 34rpx;
}

.trait-levels,
.rune-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10rpx;
  margin-top: 16rpx;
}

.trait-levels text,
.rune-tags text {
  padding: 7rpx 12rpx;
  border-radius: 999rpx;
  color: #e8c896;
  font-size: 20rpx;
  font-weight: 900;
  background: rgba(226, 174, 105, 0.12);
}

.base-items {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.equip-icon,
.axis-icon,
.recipe-icon {
  position: relative;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  overflow: hidden;
  border: 2rpx solid rgba(231, 191, 132, 0.58);
  border-radius: 4rpx;
  color: #fff5de;
  font-weight: 900;
  text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.72);
}

.equip-icon {
  width: 58rpx;
  height: 58rpx;
  font-size: 19rpx;
}

.craft-title {
  margin-top: 54rpx;
}

.craft-board {
  display: grid;
  grid-template-columns: 48rpx 1fr;
  grid-template-rows: 48rpx auto;
  gap: 6rpx;
}

.corner {
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(217, 180, 128, 0.55);
  font-size: 36rpx;
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
  font-size: 14rpx;
}

.rune-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18rpx;
}

.rune-card {
  min-height: 246rpx;
  padding: 22rpx;
  border: 1rpx solid rgba(221, 166, 100, 0.32);
  border-radius: 18rpx;
  background: rgba(255, 255, 255, 0.055);
}

.rune-mark {
  width: 62rpx;
  height: 62rpx;
  border-radius: 18rpx;
  font-size: 25rpx;
}

.rune-name {
  display: block;
  margin-top: 22rpx;
  color: #fff1d5;
  font-size: 29rpx;
  font-weight: 900;
}

.rune-desc {
  display: block;
  margin-top: 10rpx;
  color: rgba(235, 214, 194, 0.62);
  font-size: 23rpx;
  line-height: 33rpx;
}

.god-hero {
  position: relative;
  min-height: 330rpx;
  overflow: hidden;
  padding: 34rpx;
  border: 1rpx solid rgba(221, 166, 100, 0.44);
  border-radius: 22rpx;
  background: rgba(255, 255, 255, 0.055);
}

.god-bg {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 72% 38%, rgba(255, 205, 130, 0.68), transparent 18%),
    radial-gradient(circle at 42% 55%, rgba(112, 61, 176, 0.7), transparent 34%),
    linear-gradient(135deg, #241137, #5a2b76 52%, #16091f);
}

.god-title,
.god-desc {
  position: relative;
  display: block;
}

.god-title {
  color: #fff1d5;
  font-size: 42rpx;
  font-weight: 900;
}

.god-desc {
  width: 420rpx;
  margin-top: 16rpx;
  color: rgba(247, 229, 203, 0.72);
  font-size: 26rpx;
  line-height: 38rpx;
}

.god-list {
  display: grid;
  gap: 16rpx;
  margin-top: 22rpx;
}

.god-card {
  gap: 18rpx;
  min-height: 96rpx;
  padding: 18rpx 22rpx;
  border: 1rpx solid rgba(221, 166, 100, 0.3);
  border-radius: 18rpx;
  background: rgba(255, 255, 255, 0.055);
}

.god-icon {
  width: 62rpx;
  height: 62rpx;
  border-radius: 18rpx;
}

.god-name,
.god-tip {
  display: block;
}

.god-name {
  color: #fff1d5;
  font-size: 28rpx;
  font-weight: 900;
}

.god-tip {
  margin-top: 6rpx;
  color: rgba(235, 214, 194, 0.58);
  font-size: 22rpx;
}

.god-arrow {
  margin-left: auto;
  color: #b99569;
  font-size: 42rpx;
}

.tone-gold { background: linear-gradient(135deg, #ffe0a3, #a97334); }
.tone-blue { background: linear-gradient(135deg, #7fd7ff, #1b5fb9); }
.tone-violet { background: linear-gradient(135deg, #be8bff, #5631b3); }
.tone-rose { background: linear-gradient(135deg, #ff91ad, #9b2948); }

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
