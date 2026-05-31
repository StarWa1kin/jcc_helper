<template>
  <view class="detail-page">
    <view v-if="loading" class="state-card">Loading hero data...</view>
    <view v-else-if="loadError" class="state-card error" @tap="loadHeroDetail">{{ loadError }}</view>

    <scroll-view v-else scroll-y class="page-scroll">
      <view class="hero-cover">
        <view
          :class="['cover-art', heroArt ? 'remote-image' : heroBg]"
          :style="heroArt ? { backgroundImage: `url(${heroArt})` } : {}"
        ></view>
        <view class="cover-mask"></view>
        <button class="back-btn" hover-class="button-hover" @tap="goBack">‹</button>
        <view class="cover-title">
          <view class="title-tags">
            <text class="cost-tag">{{ hero.cost }}费</text>
          </view>
          <text class="hero-name">{{ hero.name }}</text>
          <view class="chip-row">
            <text v-for="name in hero.traitNames" :key="`trait-${name}`" class="detail-chip trait">{{ name }}</text>
            <text v-for="name in hero.classNames" :key="`class-${name}`" class="detail-chip role">{{ name }}</text>
          </view>
        </view>
      </view>

      <view class="content-stack">
        <view class="detail-section skill-section">
          <view class="section-title-row">
            <image v-if="baseHero.raw.skillIcon" :src="baseHero.raw.skillIcon" mode="aspectFill" class="skill-icon"></image>
            <view v-else class="mini-mark">技</view>
            <view class="section-copy">
              <text class="section-title">英雄技能</text>
              <text class="section-sub">{{ baseHero.skillName || baseHero.raw.tftHeroId }}</text>
            </view>
          </view>
          <text class="desc-text">{{ baseHero.raw.skillDesc || '暂无技能描述' }}</text>
          <view v-if="skillValues.length" class="skill-value-list">
            <view v-for="value in skillValues" :key="value.label" class="skill-value-row">
              <text>{{ value.label }}</text>
              <text>{{ value.value }}</text>
            </view>
          </view>
        </view>

        <view class="detail-section">
          <view class="section-title-row">
            <view class="mini-mark">属</view>
            <view class="section-copy">
              <text class="section-title">属性</text>
              <text class="section-sub">1星 / 2星 / 3星 / 4星</text>
            </view>
          </view>
          <view class="stat-grid">
            <view v-for="stat in starStats" :key="stat.label" class="stat-cell">
              <text class="stat-label">{{ stat.label }}</text>
              <text class="stat-value">{{ stat.value }}</text>
            </view>
          </view>
        </view>

        <view class="detail-section">
          <view class="section-title-row">
            <view class="mini-mark">羁</view>
            <view class="section-copy">
              <text class="section-title">羁绊</text>
              <text class="section-sub">职业与特质效果</text>
            </view>
          </view>
          <view class="trait-list">
            <view v-for="trait in traitDetails" :key="trait.id" class="trait-card">
              <view class="trait-head">
                <image v-if="trait.picture" :src="trait.picture" mode="aspectFit" class="trait-icon"></image>
                <view v-else :class="['trait-icon', trait.tone]">{{ trait.icon }}</view>
                <view class="trait-copy">
                  <text class="trait-name">{{ trait.name }}</text>
                  <text class="trait-count">{{ trait.count }}</text>
                </view>
              </view>
              <text class="trait-desc">{{ trait.desc }}</text>
              <view class="trait-levels">
                <text v-for="level in trait.levels" :key="level">{{ level }}</text>
              </view>
            </view>
          </view>
        </view>

        <view v-if="allies.length" class="detail-section">
          <view class="section-title-row">
            <view class="mini-mark">协</view>
            <view class="section-copy">
              <text class="section-title">协同英雄</text>
              <text class="section-sub">共享职业或特质</text>
            </view>
          </view>
          <scroll-view scroll-x class="ally-scroll">
            <view class="ally-row">
              <view v-for="ally in allies" :key="ally.id" class="ally-card">
                <view
                  :class="['ally-avatar', ally.picture ? 'remote-image' : ally.bg]"
                  :style="ally.picture ? { backgroundImage: `url(${ally.picture})` } : {}"
                ></view>
                <text>{{ ally.name }}</text>
              </view>
            </view>
          </scroll-view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script>
const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');
const HERO_DETAIL_IMAGE_BASE = 'https://game.gtimg.cn/images/jk/jkimg/mode17s18/1624x750/';
const tonePalette = ['tone-gold', 'tone-blue', 'tone-violet', 'tone-rose'];
const heroPalette = ['hero-one', 'hero-two', 'hero-three', 'hero-four', 'hero-five', 'hero-six'];

function requestApi(path, params = {}) {
  return new Promise((resolve, reject) => {
    uni.request({
      url: `${API_BASE_URL}${path}`,
      method: 'GET',
      data: params,
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data || {});
          return;
        }
        reject(new Error(`HTTP ${res.statusCode}`));
      },
      fail: reject,
    });
  });
}

function compactText(value, fallback = '') {
  if (value === undefined || value === null) return fallback;
  return String(value).replace(/\s+/g, ' ').trim() || fallback;
}

function firstChar(value, fallback = '?') {
  return compactText(value, fallback).slice(0, 1) || fallback;
}

function splitIds(value) {
  return compactText(value)
    .split('|')
    .map((item) => compactText(item))
    .filter((item) => item && item !== '-1' && item !== '0');
}

function splitLevels(value) {
  return compactText(value)
    .split(/[|#]/)
    .map((item) => compactText(item))
    .filter(Boolean)
    .slice(0, 4);
}

function getHeroStar(hero) {
  const fromId = Number(compactText(hero.id).slice(0, 1));
  if (fromId >= 1 && fromId <= 4) return fromId;
  return Number(hero.star || hero.level || 1) || 1;
}

function buildHeroDetailImage(hero) {
  const heroPaint = compactText(hero?.heroPaint);
  return heroPaint ? `${HERO_DETAIL_IMAGE_BASE}${heroPaint}.jpg` : '';
}

export default {
  data() {
    return {
      heroId: '',
      loading: true,
      loadError: '',
      hero: {
        id: '',
        name: '',
        cost: '',
        traitIds: [],
        classIds: [],
        traitNames: [],
        classNames: [],
        variants: [],
        raw: {},
      },
      heroes: [],
      traits: [],
      traitNameMap: {},
      heroBg: 'hero-one',
    };
  },
  computed: {
    baseHero() {
      const variant = this.hero.variants[0] || { raw: this.hero.raw };
      const raw = variant.raw || {};
      return {
        ...this.hero,
        raw,
        skillName: compactText(raw.skillName, this.hero.skillName),
      };
    },
    heroArt() {
      return buildHeroDetailImage(this.baseHero.raw) || this.baseHero.raw.picture || this.hero.picture || '';
    },
    skillValues() {
      const text = compactText(this.baseHero.raw.skillValueDesc);
      if (!text) return [];
      return text
        .split('|')
        .map((part, index) => {
          const pieces = compactText(part).split(/[:：]/);
          if (pieces.length < 2) return { label: `数值 ${index + 1}`, value: compactText(part) };
          return { label: compactText(pieces.shift()), value: compactText(pieces.join('：')) };
        })
        .filter((item) => item.value)
        .slice(0, 4);
    },
    starStats() {
      const variants = this.hero.variants.length ? this.hero.variants : [{ raw: this.baseHero.raw }];
      const joinValues = (field, fallback = '-') => variants.map((variant) => compactText(variant.raw?.[field], fallback)).join('/');
      const joinMana = () => variants
        .map((variant) => {
          const raw = variant.raw || {};
          return `${compactText(raw.initMP, '0')}/${compactText(raw.maxMP, '0')}`;
        })
        .join('/');
      return [
        { label: '生命', value: joinValues('initHP') },
        { label: '暴击率', value: joinValues('criticalStrikeChance') },
        { label: '护甲', value: joinValues('armor') },
        { label: '攻击距离', value: joinValues('attackRange') },
        { label: '魔抗', value: joinValues('magicResist') },
        { label: '初始法力值', value: joinMana() },
        { label: '物攻', value: joinValues('initAttackDamage') },
        { label: '法力值', value: joinValues('maxMP') },
        { label: '攻速', value: joinValues('attackSpeed') },
      ];
    },
    traitDetails() {
      const ids = [...this.hero.traitIds, ...this.hero.classIds];
      return ids.map((id) => this.traits.find((trait) => trait.id === id)).filter(Boolean);
    },
    allies() {
      const ownIds = new Set([...this.hero.traitIds, ...this.hero.classIds]);
      return this.heroes
        .filter((hero) => hero.id !== this.hero.id)
        .map((hero) => {
          const shared = [...hero.traitIds, ...hero.classIds].filter((id) => ownIds.has(id));
          return { ...hero, sharedCount: shared.length };
        })
        .filter((hero) => hero.sharedCount > 0)
        .sort((a, b) => b.sharedCount - a.sharedCount || Number(a.cost || 0) - Number(b.cost || 0))
        .slice(0, 12);
    },
  },
  onLoad(query) {
    this.heroId = decodeURIComponent(query?.id || '');
    this.loadHeroDetail();
  },
  methods: {
    async loadHeroDetail() {
      this.loading = true;
      this.loadError = '';
      try {
        const [heroes, traits] = await Promise.all([
          requestApi('/api/heroes', { show_only: true }),
          requestApi('/api/traits'),
        ]);
        this.traits = this.mapTraits(traits.items || []);
        this.traitNameMap = this.traits.reduce((map, trait) => {
          map[trait.id] = trait.name;
          return map;
        }, {});
        this.heroes = this.mapHeroes(heroes.items || []);
        const selected = this.heroes.find((hero) => hero.variants.some((variant) => variant.key === this.heroId));
        if (!selected) throw new Error('Hero not found');
        this.hero = selected;
      } catch (error) {
        this.loadError = 'Hero detail request failed';
      } finally {
        this.loading = false;
      }
    },
    goBack() {
      uni.navigateBack();
    },
    mapHeroes(items) {
      const groups = new Map();
      items
        .filter((hero) => compactText(hero.name) && compactText(hero.showHeroTag, '1') === '1' && Number(hero.price || 0) > 0)
        .forEach((hero) => {
          const cost = compactText(hero.price, '0');
          const classIds = splitIds(hero.class);
          const traitIds = splitIds(hero.species);
          const key = [compactText(hero.name), cost, traitIds.join('|'), classIds.join('|')].join('__');
          if (!groups.has(key)) groups.set(key, { classIds, traitIds, variants: [] });
          const star = getHeroStar(hero);
          groups.get(key).variants.push({
            key: compactText(hero.id, `${key}-${star}`),
            label: `${star}星`,
            star,
            raw: hero,
          });
        });
      return Array.from(groups.values())
        .map((group) => {
          group.variants.sort((a, b) => a.star - b.star || Number(a.raw.id || 0) - Number(b.raw.id || 0));
          group.raw = group.variants[0].raw;
          return group;
        })
        .sort((a, b) => Number(a.raw.price || 0) - Number(b.raw.price || 0) || compactText(a.raw.name).localeCompare(compactText(b.raw.name)))
        .map(({ raw, classIds, traitIds, variants }, index) => ({
          id: [compactText(raw.name), compactText(raw.price), traitIds.join('|'), classIds.join('|')].join('__'),
          name: compactText(raw.name),
          cost: compactText(raw.price, '0'),
          skillName: compactText(raw.skillName),
          classIds,
          traitIds,
          classNames: classIds.map((id) => this.traitNameMap[id] || id),
          traitNames: traitIds.map((id) => this.traitNameMap[id] || id),
          variants,
          raw,
          picture: raw.picture,
          bg: heroPalette[index % heroPalette.length],
        }));
    },
    mapTraits(items) {
      const grouped = new Map();
      items.forEach((trait) => {
        const key = compactText(trait.checkId, compactText(trait.id));
        if (!key || grouped.has(key)) return;
        grouped.set(key, {
          id: key,
          name: compactText(trait.name),
          icon: firstChar(trait.name),
          count: compactText(trait.numList, compactText(trait.values)),
          desc: compactText(trait.prefix || trait.desc2 || trait.realDesc),
          levels: splitLevels(trait.desc2 || trait.numList || trait.values),
          picture: trait.picture,
          tone: tonePalette[grouped.size % tonePalette.length],
        });
      });
      return Array.from(grouped.values());
    },
  },
};
</script>

<style>
page {
  @apply [background:#12091d];
}

.detail-page {
  @apply [min-height:100vh];
  @apply [color:#fff2dc];
  background:
    linear-gradient(180deg, rgba(57, 36, 102, 0.78), rgba(23, 12, 36, 0.96) 38%, #12091d 100%),
    repeating-linear-gradient(0deg, rgba(255, 255, 255, 0.035) 0, rgba(255, 255, 255, 0.035) 1rpx, transparent 1rpx, transparent 6rpx);
}

.page-scroll {
  @apply [height:100vh];
}

.state-card {
  @apply [display:flex];
  @apply [align-items:center];
  @apply [justify-content:center];
  @apply [min-height:100vh];
  @apply [color:rgba(245,_230,_203,_0.76)];
  @apply [font-size:28rpx];
  @apply [font-weight:900];
}

.state-card.error {
  @apply [color:#ffd0bf];
}

.hero-cover {
  @apply [position:relative];
  @apply [height:560rpx];
  @apply [overflow:hidden];
}

.cover-art {
  @apply [position:absolute];
  @apply [inset:0];
  @apply [background-position:center_18%];
  @apply [background-repeat:no-repeat];
  @apply [background-size:cover];
  @apply [transform:scale(1.06)];
}

.cover-mask {
  @apply [position:absolute];
  @apply [inset:0];
  background:
    linear-gradient(90deg, rgba(14, 7, 24, 0.78) 0%, rgba(14, 7, 24, 0.2) 56%, rgba(14, 7, 24, 0.72) 100%),
    linear-gradient(180deg, rgba(14, 7, 24, 0.18) 0%, rgba(14, 7, 24, 0.18) 45%, #201037 100%);
}

.back-btn {
  @apply [position:absolute];
  @apply [left:24rpx];
  @apply [top:46rpx];
  @apply [display:flex];
  @apply [align-items:center];
  @apply [justify-content:center];
  @apply [width:70rpx];
  @apply [height:70rpx];
  @apply [padding:0];
  @apply [border:0];
  @apply [border-radius:50%];
  @apply [color:#fff2dc];
  @apply [font-size:58rpx];
  @apply [line-height:70rpx];
  @apply [background:rgba(16,_8,_28,_0.72)];
}

.back-btn::after {
  @apply [border:0];
}

.cover-title {
  @apply [position:absolute];
  @apply [left:28rpx];
  @apply [right:28rpx];
  @apply [bottom:32rpx];
}

.title-tags {
  @apply [display:flex];
  @apply [align-items:center];
}

.cost-tag {
  @apply [height:44rpx];
  @apply [padding:0_18rpx];
  @apply [border:1rpx_solid_rgba(232,_189,_130,_0.56)];
  @apply [border-radius:12rpx];
  @apply [color:#f6d49a];
  @apply [font-size:23rpx];
  @apply [font-weight:900];
  @apply [line-height:44rpx];
  @apply [background:rgba(22,_9,_28,_0.64)];
}

.hero-name {
  @apply [display:block];
  @apply [margin-top:16rpx];
  @apply [color:#fff4df];
  @apply [font-size:54rpx];
  @apply [font-weight:900];
}

.chip-row {
  @apply [display:flex];
  @apply [flex-wrap:wrap];
  @apply [gap:12rpx];
  @apply [margin-top:18rpx];
}

.detail-chip {
  @apply [height:44rpx];
  @apply [padding:0_16rpx];
  @apply [border-radius:12rpx];
  @apply [color:#241426];
  @apply [font-size:22rpx];
  @apply [font-weight:900];
  @apply [line-height:44rpx];
}

.detail-chip.trait,
.trait-levels text {
  @apply [background:linear-gradient(135deg,_#ffe0a3,_#c48b43)];
}

.detail-chip.role {
  @apply [background:linear-gradient(135deg,_#9ce6ff,_#4b9bd2)];
}

.content-stack {
  @apply [padding:22rpx_24rpx_52rpx];
}

.detail-section {
  @apply [margin-bottom:22rpx];
  @apply [padding:24rpx];
  @apply [overflow:hidden];
  @apply [border:1rpx_solid_rgba(221,_166,_100,_0.24)];
  @apply [border-radius:18rpx];
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.035)),
    rgba(19, 9, 31, 0.66);
}

.skill-section {
  @apply [border-color:rgba(245,_211,_122,_0.34)];
}

.section-title-row {
  @apply [display:flex];
  @apply [align-items:center];
  @apply [gap:16rpx];
}

.section-copy {
  @apply [min-width:0];
}

.section-title {
  @apply [display:block];
  @apply [color:#fff0d6];
  @apply [font-size:28rpx];
  @apply [font-weight:900];
}

.section-sub {
  @apply [display:block];
  @apply [margin-top:4rpx];
  @apply [overflow:hidden];
  @apply [color:rgba(239,_219,_188,_0.58)];
  @apply [font-size:21rpx];
  @apply [font-weight:800];
  @apply [text-overflow:ellipsis];
  @apply [white-space:nowrap];
}

.skill-icon,
.mini-mark {
  @apply [display:flex];
  @apply [align-items:center];
  @apply [justify-content:center];
  @apply [flex:0_0_auto];
  @apply [width:70rpx];
  @apply [height:70rpx];
  @apply [overflow:hidden];
  @apply [border:1rpx_solid_rgba(255,_224,_163,_0.5)];
  @apply [border-radius:14rpx];
  @apply [color:#ffe0a3];
  @apply [font-size:24rpx];
  @apply [font-weight:900];
  @apply [background:rgba(255,_224,_163,_0.12)];
}

.desc-text {
  @apply [display:block];
  @apply [margin-top:16rpx];
  @apply [color:rgba(245,_230,_203,_0.76)];
  @apply [font-size:24rpx];
  @apply [line-height:39rpx];
}

.skill-value-list {
  @apply [margin-top:18rpx];
  @apply [border-top:1rpx_solid_rgba(255,_224,_163,_0.16)];
}

.skill-value-row {
  @apply [display:grid];
  @apply [grid-template-columns:minmax(0,_0.9fr)_minmax(0,_1.4fr)];
  @apply [gap:16rpx];
  @apply [padding:14rpx_0];
  @apply [border-bottom:1rpx_solid_rgba(255,_224,_163,_0.12)];
  @apply [color:rgba(245,_230,_203,_0.74)];
  @apply [font-size:23rpx];
  @apply [font-weight:800];
  @apply [line-height:34rpx];
}

.skill-value-row text:last-child {
  @apply [color:#f6d49a];
}

.stat-grid {
  @apply [display:grid];
  @apply [grid-template-columns:repeat(2,_minmax(0,_1fr))];
  @apply [gap:12rpx];
  @apply [margin-top:20rpx];
}

.stat-cell {
  @apply [display:flex];
  @apply [align-items:flex-start];
  @apply [justify-content:space-between];
  @apply [gap:12rpx];
  @apply [min-height:82rpx];
  @apply [padding:14rpx_16rpx];
  @apply [border:1rpx_solid_rgba(255,_255,_255,_0.06)];
  @apply [border-radius:14rpx];
  @apply [background:rgba(18,_9,_27,_0.42)];
}

.stat-label,
.stat-value {
  @apply [display:block];
}

.stat-label {
  @apply [flex:0_0_auto];
  @apply [color:rgba(235,_214,_194,_0.54)];
  @apply [font-size:22rpx];
  @apply [font-weight:800];
}

.stat-value {
  @apply [min-width:0];
  @apply [color:#fff2dc];
  @apply [font-size:22rpx];
  @apply [font-weight:900];
  @apply [line-height:32rpx];
  @apply [text-align:right];
  @apply [word-break:break-all];
}

.trait-list {
  @apply [display:grid];
  @apply [gap:16rpx];
  @apply [margin-top:20rpx];
}

.trait-card {
  @apply [padding:18rpx];
  @apply [border:1rpx_solid_rgba(255,_255,_255,_0.07)];
  @apply [border-radius:16rpx];
  @apply [background:rgba(18,_9,_27,_0.42)];
}

.trait-head {
  @apply [display:flex];
  @apply [align-items:center];
  @apply [gap:14rpx];
}

.trait-icon {
  @apply [display:flex];
  @apply [align-items:center];
  @apply [justify-content:center];
  @apply [flex:0_0_auto];
  @apply [width:62rpx];
  @apply [height:62rpx];
  @apply [overflow:hidden];
  @apply [border-radius:50%];
  @apply [color:#fff2dc];
  @apply [font-size:22rpx];
  @apply [font-weight:900];
}

.trait-copy {
  @apply [min-width:0];
}

.trait-name {
  @apply [display:block];
  @apply [color:#fff0d6];
  @apply [font-size:25rpx];
  @apply [font-weight:900];
}

.trait-count {
  @apply [display:block];
  @apply [margin-top:4rpx];
  @apply [color:#e8c896];
  @apply [font-size:21rpx];
  @apply [font-weight:800];
}

.trait-desc {
  @apply [display:block];
  @apply [margin-top:14rpx];
  @apply [color:rgba(245,_230,_203,_0.7)];
  @apply [font-size:23rpx];
  @apply [line-height:36rpx];
}

.trait-levels {
  @apply [display:flex];
  @apply [flex-wrap:wrap];
  @apply [gap:10rpx];
  @apply [margin-top:14rpx];
}

.trait-levels text {
  @apply [max-width:100%];
  @apply [padding:8rpx_12rpx];
  @apply [border-radius:10rpx];
  @apply [color:#241426];
  @apply [font-size:20rpx];
  @apply [font-weight:900];
}

.ally-scroll {
  @apply [width:100%];
  @apply [margin-top:20rpx];
  @apply [white-space:nowrap];
}

.ally-row {
  @apply [display:flex];
  @apply [gap:16rpx];
}

.ally-card {
  @apply [flex:0_0_102rpx];
  @apply [width:102rpx];
}

.ally-avatar {
  @apply [width:96rpx];
  @apply [height:96rpx];
  @apply [overflow:hidden];
  @apply [border:2rpx_solid_rgba(255,_224,_163,_0.34)];
  @apply [border-radius:50%];
  @apply [background-position:center];
  @apply [background-repeat:no-repeat];
  @apply [background-size:cover];
}

.ally-card text {
  @apply [display:block];
  @apply [margin-top:10rpx];
  @apply [overflow:hidden];
  @apply [color:rgba(245,_230,_203,_0.76)];
  @apply [font-size:20rpx];
  @apply [font-weight:900];
  @apply [text-align:center];
  @apply [text-overflow:ellipsis];
  @apply [white-space:nowrap];
}

.hero-one { background: radial-gradient(circle at 66% 28%, #dcc067, transparent 20%), linear-gradient(135deg, #33205f, #7548ec 48%, #16091f); }
.hero-two { background: radial-gradient(circle at 70% 26%, #f0b16f, transparent 22%), linear-gradient(135deg, #122b55, #23a1e4 48%, #16091f); }
.hero-three { background: radial-gradient(circle at 25% 28%, #6dc7ff, transparent 24%), linear-gradient(135deg, #17235b, #435df0 52%, #16091f); }
.hero-four { background: radial-gradient(circle at 65% 42%, #78fff3, transparent 24%), linear-gradient(135deg, #3f2261, #31c4bc 48%, #16091f); }
.hero-five { background: radial-gradient(circle at 20% 26%, #f49133, transparent 23%), linear-gradient(135deg, #38162d, #a44d20 52%, #16091f); }
.hero-six { background: radial-gradient(circle at 60% 30%, #c66cff, transparent 24%), linear-gradient(135deg, #1b1d61, #7433cd 52%, #16091f); }
.tone-gold { background: linear-gradient(135deg, #fee7a0, #c39144); }
.tone-blue { background: linear-gradient(135deg, #92e9ff, #3d7ccf); }
.tone-violet { background: linear-gradient(135deg, #d7a4ff, #7f54e8); }
.tone-rose { background: linear-gradient(135deg, #ffb1b1, #d84e6a); }
.remote-image {
  @apply [background-position:center];
  @apply [background-repeat:no-repeat];
  @apply [background-size:cover];
}
</style>
