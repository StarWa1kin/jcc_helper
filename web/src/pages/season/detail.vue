<template>
  <view class="detail-page min-h-screen text-[#fff2dc] bg-[#12091d] min-h-screen text-[#fff2dc] bg-[linear-gradient(180deg,rgba(57,36,102,0.78),rgba(23,12,36,0.96)_38%,#12091d_100%),repeating-linear-gradient(0deg,rgba(255,255,255,0.035)_0,rgba(255,255,255,0.035)_1rpx,transparent_1rpx,transparent_6rpx)]">
    <view v-if="loading" class="state-card flex items-center justify-center min-h-screen text-[28rpx] font-black text-[rgba(245,230,203,0.76)]">Loading hero data...</view>
    <view v-else-if="loadError" class="state-card error flex items-center justify-center min-h-screen text-[28rpx] font-black text-[#ffd0bf]" @tap="loadHeroDetail">{{ loadError }}</view>

    <scroll-view v-else scroll-y class="page-scroll h-screen">
      <view class="hero-cover relative h-[560rpx] overflow-hidden">
        <view
          :class="['cover-art absolute inset-0 [background-position:center_18%] bg-no-repeat bg-cover scale-106', heroArt ? 'remote-image' : heroBg]"
          :style="heroArt ? { backgroundImage: `url(${heroArt})` } : {}"
        ></view>
        <view class="cover-mask absolute inset-0 bg-[linear-gradient(90deg,rgba(14,7,24,0.78)_0%,rgba(14,7,24,0.2)_56%,rgba(14,7,24,0.72)_100%),linear-gradient(180deg,rgba(14,7,24,0.18)_0%,rgba(14,7,24,0.18)_45%,#201037_100%)]"></view>
        <button class="back-btn absolute left-[24rpx] top-[46rpx] flex items-center justify-center w-[70rpx] h-[70rpx] p-0 border-0 rounded-full text-[#fff2dc] text-[58rpx] leading-[70rpx] bg-[rgba(16,8,28,0.72)]" hover-class="button-hover" @tap="goBack">‹</button>
        <view class="cover-title absolute left-[28rpx] right-[28rpx] bottom-[32rpx]">
          <view class="title-tags flex items-center">
            <text class="cost-tag h-[44rpx] px-[18rpx] border border-[rgba(232,189,130,0.56)] rounded-[12rpx] text-[#f6d49a] text-[23rpx] font-black leading-[44rpx] bg-[rgba(22,9,28,0.64)]">{{ hero.cost }}费</text>
          </view>
          <text class="hero-name block mt-[16rpx] text-[#fff4df] text-[54rpx] font-black">{{ hero.name }}</text>
          <view class="chip-row flex flex-wrap gap-[12rpx] mt-[18rpx]">
            <text v-for="name in hero.traitNames" :key="`trait-${name}`" class="detail-chip trait h-[44rpx] px-[16rpx] rounded-[12rpx] text-[#241426] text-[22rpx] font-black leading-[44rpx] bg-[linear-gradient(135deg,#ffe0a3,#c48b43)]">{{ name }}</text>
            <text v-for="name in hero.classNames" :key="`class-${name}`" class="detail-chip role h-[44rpx] px-[16rpx] rounded-[12rpx] text-[#241426] text-[22rpx] font-black leading-[44rpx] bg-[linear-gradient(135deg,#9ce6ff,#4b9bd2)]">{{ name }}</text>
          </view>
        </view>
      </view>

      <view class="content-stack px-[24rpx] pt-[22rpx] pb-[52rpx]">
        <view class="detail-section skill-section mb-[22rpx] p-[24rpx] overflow-hidden border border-[rgba(245,211,122,0.34)] rounded-[18rpx] bg-[rgba(19,9,31,0.66)]">
          <view class="section-title-row flex items-center gap-[16rpx]">
            <image v-if="baseHero.raw.skillIcon" :src="baseHero.raw.skillIcon" mode="aspectFill" class="skill-icon flex items-center justify-center flex-none w-[70rpx] h-[70rpx] overflow-hidden border border-[rgba(255,224,163,0.5)] rounded-[14rpx] text-[#ffe0a3] text-[24rpx] font-black bg-[rgba(255,224,163,0.12)]"></image>
            <view v-else class="mini-mark flex items-center justify-center flex-none w-[70rpx] h-[70rpx] overflow-hidden border border-[rgba(255,224,163,0.5)] rounded-[14rpx] text-[#ffe0a3] text-[24rpx] font-black bg-[rgba(255,224,163,0.12)]">技</view>
            <view class="section-copy min-w-0">
              <text class="section-title block text-[#fff0d6] text-[28rpx] font-black">英雄技能</text>
              <text class="section-sub block mt-[4rpx] overflow-hidden text-[rgba(239,219,188,0.58)] text-[21rpx] font-extrabold text-ellipsis whitespace-nowrap">{{ baseHero.skillName || baseHero.raw.tftHeroId }}</text>
            </view>
          </view>
          <text class="desc-text block mt-[16rpx] text-[rgba(245,230,203,0.76)] text-[24rpx] leading-[39rpx]">{{ baseHero.raw.skillDesc || '暂无技能描述' }}</text>
          <view v-if="skillValues.length" class="skill-value-list mt-[18rpx] border-t border-[rgba(255,224,163,0.16)]">
            <view v-for="value in skillValues" :key="value.label" class="skill-value-row grid grid-cols-[minmax(0,0.9fr)_minmax(0,1.4fr)] gap-[16rpx] py-[14rpx] border-b border-[rgba(255,224,163,0.12)] text-[rgba(245,230,203,0.74)] text-[23rpx] font-extrabold leading-[34rpx] [&_text:last-child]:text-[#f6d49a]">
              <text>{{ value.label }}</text>
              <text>{{ value.value }}</text>
            </view>
          </view>
        </view>

        <view class="detail-section mb-[22rpx] p-[24rpx] overflow-hidden border border-[rgba(221,166,100,0.24)] rounded-[18rpx] bg-[rgba(19,9,31,0.66)]">
          <view class="section-title-row flex items-center gap-[16rpx]">
            <view class="mini-mark flex items-center justify-center flex-none w-[70rpx] h-[70rpx] overflow-hidden border border-[rgba(255,224,163,0.5)] rounded-[14rpx] text-[#ffe0a3] text-[24rpx] font-black bg-[rgba(255,224,163,0.12)]">属</view>
            <view class="section-copy min-w-0">
              <text class="section-title block text-[#fff0d6] text-[28rpx] font-black">属性</text>
              <text class="section-sub block mt-[4rpx] overflow-hidden text-[rgba(239,219,188,0.58)] text-[21rpx] font-extrabold text-ellipsis whitespace-nowrap">1星 / 2星 / 3星 / 4星</text>
            </view>
          </view>
          <view class="stat-grid grid grid-cols-2 gap-[14rpx] mt-[22rpx]">
            <view v-for="stat in starStats" :key="stat.label" class="stat-cell min-h-[82rpx] p-[14rpx] rounded-[14rpx] bg-[rgba(255,255,255,0.055)] flex items-start justify-between gap-[12rpx] min-h-[82rpx] p-[14rpx_16rpx] border border-[rgba(255,255,255,0.06)] rounded-[14rpx] bg-[rgba(18,9,27,0.42)]">
              <text class="stat-label block flex-none text-[rgba(235,214,194,0.54)] text-[22rpx] font-extrabold">{{ stat.label }}</text>
              <text class="stat-value block min-w-0 text-[#fff2dc] text-[22rpx] font-black leading-[32rpx] text-right break-all">{{ stat.value }}</text>
            </view>
          </view>
        </view>

        <view class="detail-section mb-[22rpx] p-[24rpx] overflow-hidden border border-[rgba(221,166,100,0.24)] rounded-[18rpx] bg-[rgba(19,9,31,0.66)]">
          <view class="section-title-row flex items-center gap-[16rpx]">
            <view class="mini-mark flex items-center justify-center flex-none w-[70rpx] h-[70rpx] overflow-hidden border border-[rgba(255,224,163,0.5)] rounded-[14rpx] text-[#ffe0a3] text-[24rpx] font-black bg-[rgba(255,224,163,0.12)]">羁</view>
            <view class="section-copy min-w-0">
              <text class="section-title block text-[#fff0d6] text-[28rpx] font-black">羁绊</text>
              <text class="section-sub block mt-[4rpx] overflow-hidden text-[rgba(239,219,188,0.58)] text-[21rpx] font-extrabold text-ellipsis whitespace-nowrap">职业与特质效果</text>
            </view>
          </view>
          <view class="trait-list grid gap-[16rpx] mt-[22rpx]">
            <view v-for="trait in traitDetails" :key="trait.id" class="trait-card p-[20rpx] border border-[rgba(221,166,100,0.18)] rounded-[16rpx] bg-[rgba(255,255,255,0.05)]">
              <view class="trait-head flex items-center gap-[14rpx]">
                <image v-if="trait.picture" :src="trait.picture" mode="aspectFit" class="trait-icon flex items-center justify-center flex-none w-[62rpx] h-[62rpx] overflow-hidden rounded-full text-[#fff2dc] text-[22rpx] font-black"></image>
                <view v-else :class="['trait-icon flex items-center justify-center flex-none w-[62rpx] h-[62rpx] overflow-hidden rounded-full text-[#fff2dc] text-[22rpx] font-black', trait.tone]">{{ trait.icon }}</view>
                <view class="trait-copy min-w-0">
                  <text class="trait-name block text-[#fff0d6] text-[25rpx] font-black">{{ trait.name }}</text>
                  <text class="trait-count block mt-[4rpx] text-[#e8c896] text-[21rpx] font-extrabold">{{ trait.count }}</text>
                </view>
              </view>
              <text class="trait-desc block mt-[14rpx] text-[rgba(245,230,203,0.7)] text-[23rpx] leading-[36rpx]">{{ trait.desc }}</text>
              <view class="trait-levels flex flex-wrap gap-[10rpx] mt-[14rpx] [&_text]:max-w-full [&_text]:p-[8rpx_12rpx] [&_text]:rounded-[10rpx] [&_text]:text-[#241426] [&_text]:text-[20rpx] [&_text]:font-black [&_text]:bg-[linear-gradient(135deg,#ffe0a3,#c48b43)]">
                <text v-for="level in trait.levels" :key="level">{{ level }}</text>
              </view>
            </view>
          </view>
        </view>

        <view v-if="allies.length" class="detail-section mb-[22rpx] p-[24rpx] overflow-hidden border border-[rgba(221,166,100,0.24)] rounded-[18rpx] bg-[rgba(19,9,31,0.66)]">
          <view class="section-title-row flex items-center gap-[16rpx]">
            <view class="mini-mark flex items-center justify-center flex-none w-[70rpx] h-[70rpx] overflow-hidden border border-[rgba(255,224,163,0.5)] rounded-[14rpx] text-[#ffe0a3] text-[24rpx] font-black bg-[rgba(255,224,163,0.12)]">协</view>
            <view class="section-copy min-w-0">
              <text class="section-title block text-[#fff0d6] text-[28rpx] font-black">协同英雄</text>
              <text class="section-sub block mt-[4rpx] overflow-hidden text-[rgba(239,219,188,0.58)] text-[21rpx] font-extrabold text-ellipsis whitespace-nowrap">共享职业或特质</text>
            </view>
          </view>
          <scroll-view scroll-x class="ally-scroll w-full mt-[20rpx] whitespace-nowrap">
            <view class="ally-row flex gap-[16rpx]">
              <view v-for="ally in allies" :key="ally.id" class="ally-card flex-none w-[112rpx] text-center flex-none w-[102rpx] text-center [&_text]:block [&_text]:mt-[10rpx] [&_text]:overflow-hidden [&_text]:text-[rgba(245,230,203,0.76)] [&_text]:text-[20rpx] [&_text]:font-black [&_text]:text-center [&_text]:text-ellipsis [&_text]:whitespace-nowrap">
                <view
                  :class="['ally-avatar w-[96rpx] h-[96rpx] overflow-hidden border-[2rpx] border-[rgba(255,224,163,0.34)] rounded-full [background-position:center] bg-no-repeat bg-cover', ally.picture ? 'remote-image' : ally.bg]"
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
const tonePalette = ["bg-[linear-gradient(135deg,#fee7a0,#c39144)]", "bg-[linear-gradient(135deg,#92e9ff,#3d7ccf)]", "bg-[linear-gradient(135deg,#d7a4ff,#7f54e8)]", "bg-[linear-gradient(135deg,#ffb1b1,#d84e6a)]"];
const heroPalette = ["bg-[radial-gradient(circle_at_66%_28%,#dcc067,transparent_20%),linear-gradient(135deg,#33205f,#7548ec_48%,#16091f)]", "bg-[radial-gradient(circle_at_70%_26%,#f0b16f,transparent_22%),linear-gradient(135deg,#122b55,#23a1e4_48%,#16091f)]", "bg-[radial-gradient(circle_at_25%_28%,#6dc7ff,transparent_24%),linear-gradient(135deg,#17235b,#435df0_52%,#16091f)]", "bg-[radial-gradient(circle_at_65%_42%,#78fff3,transparent_24%),linear-gradient(135deg,#3f2261,#31c4bc_48%,#16091f)]", "bg-[radial-gradient(circle_at_20%_26%,#f49133,transparent_23%),linear-gradient(135deg,#38162d,#a44d20_52%,#16091f)]", "bg-[radial-gradient(circle_at_60%_30%,#c66cff,transparent_24%),linear-gradient(135deg,#1b1d61,#7433cd_52%,#16091f)]"];

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
.back-btn::after {
  border: 0;
}
</style>
