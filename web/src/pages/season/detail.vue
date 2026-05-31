<template>
  <view class="detail-page min-h-screen text-[#fff2dc] bg-[#12091d]">
    <view v-if="loading" class="state-card flex items-center justify-center min-h-screen text-[28rpx] font-black text-[rgba(245,230,203,0.76)]">Loading hero data...</view>
    <view v-else-if="loadError" class="state-card error flex items-center justify-center min-h-screen text-[28rpx] font-black text-[#ffd0bf]" @tap="loadHeroDetail">{{ loadError }}</view>

    <scroll-view v-else scroll-y class="page-scroll h-screen">
      <view class="hero-cover relative h-[560rpx] overflow-hidden">
        <view
          :class="['cover-art', heroArt ? 'remote-image' : heroBg]"
          :style="heroArt ? { backgroundImage: `url(${heroArt})` } : {}"
        ></view>
        <view class="cover-mask"></view>
        <button class="back-btn absolute left-[24rpx] top-[46rpx] flex items-center justify-center w-[70rpx] h-[70rpx] p-0 border-0 rounded-full text-[#fff2dc] text-[58rpx] leading-[70rpx] bg-[rgba(16,8,28,0.72)]" hover-class="button-hover" @tap="goBack">‹</button>
        <view class="cover-title absolute left-[28rpx] right-[28rpx] bottom-[32rpx]">
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

      <view class="content-stack px-[24rpx] pt-[22rpx] pb-[52rpx]">
        <view class="detail-section skill-section mb-[22rpx] p-[24rpx] overflow-hidden border border-[rgba(245,211,122,0.34)] rounded-[18rpx] bg-[rgba(19,9,31,0.66)]">
          <view class="section-title-row flex items-center gap-[16rpx]">
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

        <view class="detail-section mb-[22rpx] p-[24rpx] overflow-hidden border border-[rgba(221,166,100,0.24)] rounded-[18rpx] bg-[rgba(19,9,31,0.66)]">
          <view class="section-title-row flex items-center gap-[16rpx]">
            <view class="mini-mark">属</view>
            <view class="section-copy">
              <text class="section-title">属性</text>
              <text class="section-sub">1星 / 2星 / 3星 / 4星</text>
            </view>
          </view>
          <view class="stat-grid grid grid-cols-2 gap-[14rpx] mt-[22rpx]">
            <view v-for="stat in starStats" :key="stat.label" class="stat-cell min-h-[82rpx] p-[14rpx] rounded-[14rpx] bg-[rgba(255,255,255,0.055)]">
              <text class="stat-label">{{ stat.label }}</text>
              <text class="stat-value">{{ stat.value }}</text>
            </view>
          </view>
        </view>

        <view class="detail-section mb-[22rpx] p-[24rpx] overflow-hidden border border-[rgba(221,166,100,0.24)] rounded-[18rpx] bg-[rgba(19,9,31,0.66)]">
          <view class="section-title-row flex items-center gap-[16rpx]">
            <view class="mini-mark">羁</view>
            <view class="section-copy">
              <text class="section-title">羁绊</text>
              <text class="section-sub">职业与特质效果</text>
            </view>
          </view>
          <view class="trait-list grid gap-[16rpx] mt-[22rpx]">
            <view v-for="trait in traitDetails" :key="trait.id" class="trait-card p-[20rpx] border border-[rgba(221,166,100,0.18)] rounded-[16rpx] bg-[rgba(255,255,255,0.05)]">
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

        <view v-if="allies.length" class="detail-section mb-[22rpx] p-[24rpx] overflow-hidden border border-[rgba(221,166,100,0.24)] rounded-[18rpx] bg-[rgba(19,9,31,0.66)]">
          <view class="section-title-row flex items-center gap-[16rpx]">
            <view class="mini-mark">协</view>
            <view class="section-copy">
              <text class="section-title">协同英雄</text>
              <text class="section-sub">共享职业或特质</text>
            </view>
          </view>
          <scroll-view scroll-x class="ally-scroll w-full mt-[20rpx] whitespace-nowrap">
            <view class="ally-row flex gap-[16rpx]">
              <view v-for="ally in allies" :key="ally.id" class="ally-card flex-none w-[112rpx] text-center">
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
        .filter((hero) => {
          const price = Number(hero.price || 0);
          return (
            compactText(hero.name) &&
            compactText(hero.showHeroTag, '1') === '1' &&
            compactText(hero.heroType, '0') === '0' &&
            price > 0 &&
            price <= 5 &&
            splitIds(hero.species).length > 0
          );
        })
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
  background: #12091d;
}

.detail-page {
  min-height: 100vh;
  color: #fff2dc;
  background:
    linear-gradient(180deg, rgba(57, 36, 102, 0.78), rgba(23, 12, 36, 0.96) 38%, #12091d 100%),
    repeating-linear-gradient(0deg, rgba(255, 255, 255, 0.035) 0, rgba(255, 255, 255, 0.035) 1rpx, transparent 1rpx, transparent 6rpx);
}

.page-scroll {
  height: 100vh;
}

.state-card {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  color: rgba(245, 230, 203, 0.76);
  font-size: 28rpx;
  font-weight: 900;
}

.state-card.error {
  color: #ffd0bf;
}

.hero-cover {
  position: relative;
  height: 560rpx;
  overflow: hidden;
}

.cover-art {
  position: absolute;
  inset: 0;
  background-position: center 18%;
  background-repeat: no-repeat;
  background-size: cover;
  transform: scale(1.06);
}

.cover-mask {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(90deg, rgba(14, 7, 24, 0.78) 0%, rgba(14, 7, 24, 0.2) 56%, rgba(14, 7, 24, 0.72) 100%),
    linear-gradient(180deg, rgba(14, 7, 24, 0.18) 0%, rgba(14, 7, 24, 0.18) 45%, #201037 100%);
}

.back-btn {
  position: absolute;
  left: 24rpx;
  top: 46rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 70rpx;
  height: 70rpx;
  padding: 0;
  border: 0;
  border-radius: 50%;
  color: #fff2dc;
  font-size: 58rpx;
  line-height: 70rpx;
  background: rgba(16, 8, 28, 0.72);
}

.back-btn::after {
  border: 0;
}

.cover-title {
  position: absolute;
  left: 28rpx;
  right: 28rpx;
  bottom: 32rpx;
}

.title-tags {
  display: flex;
  align-items: center;
}

.cost-tag {
  height: 44rpx;
  padding: 0 18rpx;
  border: 1rpx solid rgba(232, 189, 130, 0.56);
  border-radius: 12rpx;
  color: #f6d49a;
  font-size: 23rpx;
  font-weight: 900;
  line-height: 44rpx;
  background: rgba(22, 9, 28, 0.64);
}

.hero-name {
  display: block;
  margin-top: 16rpx;
  color: #fff4df;
  font-size: 54rpx;
  font-weight: 900;
}

.chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
  margin-top: 18rpx;
}

.detail-chip {
  height: 44rpx;
  padding: 0 16rpx;
  border-radius: 12rpx;
  color: #241426;
  font-size: 22rpx;
  font-weight: 900;
  line-height: 44rpx;
}

.detail-chip.trait,
.trait-levels text {
  background: linear-gradient(135deg, #ffe0a3, #c48b43);
}

.detail-chip.role {
  background: linear-gradient(135deg, #9ce6ff, #4b9bd2);
}

.content-stack {
  padding: 22rpx 24rpx 52rpx;
}

.detail-section {
  margin-bottom: 22rpx;
  padding: 24rpx;
  overflow: hidden;
  border: 1rpx solid rgba(221, 166, 100, 0.24);
  border-radius: 18rpx;
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.035)),
    rgba(19, 9, 31, 0.66);
}

.skill-section {
  border-color: rgba(245, 211, 122, 0.34);
}

.section-title-row {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.section-copy {
  min-width: 0;
}

.section-title {
  display: block;
  color: #fff0d6;
  font-size: 28rpx;
  font-weight: 900;
}

.section-sub {
  display: block;
  margin-top: 4rpx;
  overflow: hidden;
  color: rgba(239, 219, 188, 0.58);
  font-size: 21rpx;
  font-weight: 800;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.skill-icon,
.mini-mark {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  width: 70rpx;
  height: 70rpx;
  overflow: hidden;
  border: 1rpx solid rgba(255, 224, 163, 0.5);
  border-radius: 14rpx;
  color: #ffe0a3;
  font-size: 24rpx;
  font-weight: 900;
  background: rgba(255, 224, 163, 0.12);
}

.desc-text {
  display: block;
  margin-top: 16rpx;
  color: rgba(245, 230, 203, 0.76);
  font-size: 24rpx;
  line-height: 39rpx;
}

.skill-value-list {
  margin-top: 18rpx;
  border-top: 1rpx solid rgba(255, 224, 163, 0.16);
}

.skill-value-row {
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.4fr);
  gap: 16rpx;
  padding: 14rpx 0;
  border-bottom: 1rpx solid rgba(255, 224, 163, 0.12);
  color: rgba(245, 230, 203, 0.74);
  font-size: 23rpx;
  font-weight: 800;
  line-height: 34rpx;
}

.skill-value-row text:last-child {
  color: #f6d49a;
}

.stat-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12rpx;
  margin-top: 20rpx;
}

.stat-cell {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12rpx;
  min-height: 82rpx;
  padding: 14rpx 16rpx;
  border: 1rpx solid rgba(255, 255, 255, 0.06);
  border-radius: 14rpx;
  background: rgba(18, 9, 27, 0.42);
}

.stat-label,
.stat-value {
  display: block;
}

.stat-label {
  flex: 0 0 auto;
  color: rgba(235, 214, 194, 0.54);
  font-size: 22rpx;
  font-weight: 800;
}

.stat-value {
  min-width: 0;
  color: #fff2dc;
  font-size: 22rpx;
  font-weight: 900;
  line-height: 32rpx;
  text-align: right;
  word-break: break-all;
}

.trait-list {
  display: grid;
  gap: 16rpx;
  margin-top: 20rpx;
}

.trait-card {
  padding: 18rpx;
  border: 1rpx solid rgba(255, 255, 255, 0.07);
  border-radius: 16rpx;
  background: rgba(18, 9, 27, 0.42);
}

.trait-head {
  display: flex;
  align-items: center;
  gap: 14rpx;
}

.trait-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  width: 62rpx;
  height: 62rpx;
  overflow: hidden;
  border-radius: 50%;
  color: #fff2dc;
  font-size: 22rpx;
  font-weight: 900;
}

.trait-copy {
  min-width: 0;
}

.trait-name {
  display: block;
  color: #fff0d6;
  font-size: 25rpx;
  font-weight: 900;
}

.trait-count {
  display: block;
  margin-top: 4rpx;
  color: #e8c896;
  font-size: 21rpx;
  font-weight: 800;
}

.trait-desc {
  display: block;
  margin-top: 14rpx;
  color: rgba(245, 230, 203, 0.7);
  font-size: 23rpx;
  line-height: 36rpx;
}

.trait-levels {
  display: flex;
  flex-wrap: wrap;
  gap: 10rpx;
  margin-top: 14rpx;
}

.trait-levels text {
  max-width: 100%;
  padding: 8rpx 12rpx;
  border-radius: 10rpx;
  color: #241426;
  font-size: 20rpx;
  font-weight: 900;
}

.ally-scroll {
  width: 100%;
  margin-top: 20rpx;
  white-space: nowrap;
}

.ally-row {
  display: flex;
  gap: 16rpx;
}

.ally-card {
  flex: 0 0 102rpx;
  width: 102rpx;
}

.ally-avatar {
  width: 96rpx;
  height: 96rpx;
  overflow: hidden;
  border: 2rpx solid rgba(255, 224, 163, 0.34);
  border-radius: 50%;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
}

.ally-card text {
  display: block;
  margin-top: 10rpx;
  overflow: hidden;
  color: rgba(245, 230, 203, 0.76);
  font-size: 20rpx;
  font-weight: 900;
  text-align: center;
  text-overflow: ellipsis;
  white-space: nowrap;
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
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
}
</style>
