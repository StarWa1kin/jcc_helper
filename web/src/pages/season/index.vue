<template>
  <view class="season-page">
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
      <view v-if="loading" class="state-card">
        <text>Loading season data...</text>
      </view>

      <view
        v-else-if="loadError"
        class="state-card error"
        @tap="loadSeasonData"
      >
        <text>{{ loadError }}</text>
        <text class="retry-text">Tap to retry</text>
      </view>

      <view v-else-if="activeTab === 'heroes'" class="tab-panel hero-panel">
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
          <view
            v-for="filter in heroFilters"
            :key="filter.key"
            :class="[
              'filter-pill',
              activeHeroFilter === filter.key ? 'active' : '',
              heroFilterValue(filter.key) ? 'selected' : '',
            ]"
            @tap="toggleHeroFilter(filter.key)"
          >
            <text class="filter-icon">{{ filter.icon }}</text>
            <text class="filter-label">{{ heroFilterLabel(filter) }}</text>
            <text class="chevron">⌄</text>
          </view>
        </view>

        <view v-if="activeHeroFilter" class="filter-panel">
          <view
            v-for="option in activeHeroFilterOptions"
            :key="option.value"
            :class="[
              'filter-option',
              heroFilterValue(activeHeroFilter) === option.value
                ? 'active'
                : '',
            ]"
            @tap="selectHeroFilter(activeHeroFilter, option.value)"
          >
            <text>{{ option.label }}</text>
          </view>
        </view>

        <view class="hero-summary">
          <text>{{ visibleHeroes.length }} / {{ heroes.length }}</text>
          <text
            v-if="hasHeroFilter"
            class="clear-filter"
            @tap="resetHeroFilters"
            >重置筛选</text
          >
        </view>

        <view v-if="visibleHeroes.length" class="hero-grid">
          <view
            v-for="hero in visibleHeroes"
            :key="hero.id || hero.name"
            class="hero-card"
            @tap="openHeroDetail(hero)"
          >
            <view
              :class="['hero-bg', hero.bg, hero.picture ? 'remote-image' : '']"
              :style="
                hero.picture ? { backgroundImage: `url(${hero.picture})` } : {}
              "
            ></view>
            <view class="hero-shade"></view>
            <view class="cost-badge">{{ hero.cost }}</view>
            <view class="hero-tags">
              <text v-for="tag in hero.cardTags" :key="tag">{{ tag }}</text>
            </view>
            <view class="hero-meta">
              <text class="hero-name">{{ hero.name }}</text>
              <view class="views">
                <text>◉</text>
                <text>{{ hero.views }}</text>
              </view>
            </view>
          </view>
        </view>

        <view v-else class="empty-card">
          <text>没有匹配的英雄</text>
        </view>
      </view>

      <view v-else-if="activeTab === 'traits'" class="tab-panel trait-panel">
        <view class="section-head">
          <text class="section-title">羁绊效果</text>
          <text class="section-sub">按职业与特质快速查看等级收益</text>
        </view>
        <view class="trait-list">
          <view
            v-for="trait in traits"
            :key="trait.id || trait.name"
            class="trait-card"
          >
            <view :class="['trait-emblem', trait.tone]">
              <image
                v-if="trait.picture"
                :src="trait.picture"
                mode="aspectFit"
                class="data-icon"
              ></image>
              <text v-else>{{ trait.icon }}</text>
            </view>
            <view class="trait-main">
              <view class="trait-top">
                <text class="trait-name">{{ trait.name }}</text>
                <text class="trait-count">{{ trait.count }}</text>
              </view>
              <text class="trait-desc">{{ trait.desc }}</text>
              <view class="trait-levels">
                <text v-for="level in trait.levels" :key="level">{{
                  level
                }}</text>
              </view>
            </view>
          </view>
        </view>
      </view>

      <view v-else-if="activeTab === 'items'" class="tab-panel item-panel">
        <view class="section-head">
          <text class="section-title">装备资料</text>
          <text class="section-sub"
            >按基础、成型、光明、神器和特殊装备分类</text
          >
        </view>

        <scroll-view scroll-x class="equip-type-scroll">
          <view class="equip-type-row">
            <view
              v-for="type in equipTypeFilters"
              :key="type.value"
              :class="[
                'equip-type-pill',
                activeEquipType === type.value ? 'active' : '',
              ]"
              @tap="activeEquipType = type.value"
            >
              <text>{{ type.label }}</text>
            </view>
          </view>
        </scroll-view>

        <view class="base-items">
          <view
            v-for="item in baseItems"
            :key="item.key"
            :class="['equip-icon', item.bg]"
          >
            <image
              v-if="item.picture"
              :src="item.picture"
              mode="aspectFit"
              class="data-icon"
            ></image>
            <text v-else>{{ item.label }}</text>
          </view>
        </view>

        <view class="equip-summary">
          <text>{{ visibleEquipItems.length }} / {{ equipItems.length }}</text>
        </view>

        <view class="equip-list">
          <view
            v-for="item in visibleEquipItems"
            :key="item.id"
            class="equip-row-card"
          >
            <view class="equip-formula">
              <image
                v-if="item.componentA?.picture"
                :src="item.componentA.picture"
                mode="aspectFit"
                class="equip-formula-icon"
              ></image>
              <view v-else class="equip-formula-icon empty">
                <image
                  v-if="item.picture"
                  :src="item.picture"
                  mode="aspectFit"
                  class="data-icon"
                ></image>
              </view>
              <text v-if="item.hasRecipe" class="formula-symbol">+</text>
              <image
                v-if="item.hasRecipe && item.componentB?.picture"
                :src="item.componentB.picture"
                mode="aspectFit"
                class="equip-formula-icon"
              ></image>
              <text v-if="item.hasRecipe" class="formula-symbol">=</text>
              <image
                v-if="item.hasRecipe && item.picture"
                :src="item.picture"
                mode="aspectFit"
                class="equip-formula-icon result"
              ></image>
            </view>
            <view class="equip-copy">
              <view class="equip-title-line">
                <text class="equip-name">{{ item.name }}</text>
                <text class="equip-type-label">{{ item.displayType }}</text>
              </view>
              <text v-if="item.basicDesc" class="equip-basic">{{
                item.basicDesc
              }}</text>
              <text class="equip-desc">{{
                item.desc || item.basicDesc || "暂无装备说明"
              }}</text>
            </view>
          </view>
        </view>
      </view>

      <view v-else-if="activeTab === 'runes'" class="tab-panel rune-panel">
        <view class="section-head">
          <text class="section-title">强化符文</text>
          <text class="section-sub">按一级、二级、三级快速筛选</text>
        </view>
        <view class="rune-level-tabs">
          <view
            v-for="level in runeLevelFilters"
            :key="level.value"
            :class="[
              'rune-level-tab',
              activeRuneLevel === level.value ? 'active' : '',
            ]"
            @tap="activeRuneLevel = level.value"
          >
            <text>{{ level.label }}</text>
          </view>
        </view>
        <view class="rune-summary">
          <text>{{ visibleRunes.length }} / {{ runes.length }}</text>
        </view>
        <view class="rune-grid">
          <view
            v-for="rune in visibleRunes"
            :key="rune.id || rune.name"
            class="rune-card"
          >
            <view :class="['rune-mark', rune.tone]">
              <image
                v-if="rune.iconUrl"
                :src="rune.iconUrl"
                mode="aspectFit"
                class="data-icon"
              ></image>
              <text v-else>{{ rune.icon }}</text>
            </view>
            <text class="rune-name">{{ rune.name }}</text>
            <text class="rune-desc">{{ rune.desc }}</text>
            <view class="rune-tags">
              <text v-for="tag in rune.tags" :key="tag">{{ tag }}</text>
            </view>
          </view>
        </view>
      </view>

      <view v-else class="tab-panel god-panel">
        <scroll-view scroll-x class="god-selector-scroll">
          <view class="god-selector-row">
            <view
              v-for="god in godFilters"
              :key="god.value"
              :class="[
                'god-select-card',
                activeGodId === god.value ? 'active' : '',
              ]"
              @tap="activeGodId = god.value"
            >
              <image
                v-if="god.iconUrl"
                :src="god.iconUrl"
                mode="aspectFit"
                class="god-select-icon"
              ></image>
              <view class="god-select-copy">
                <text>{{ god.label }}</text>
                <text>{{ god.subTitle }}</text>
              </view>
            </view>
          </view>
        </scroll-view>

        <view class="god-profile-card">
          <image
            v-if="selectedGod.iconUrl"
            :src="selectedGod.iconUrl"
            mode="aspectFit"
            class="god-profile-art"
          ></image>
          <view class="god-profile-mask"></view>
          <view class="god-profile-content">
            <image
              v-if="selectedGod.iconUrl"
              :src="selectedGod.iconUrl"
              mode="aspectFit"
              class="god-profile-icon"
            ></image>
            <view>
              <text class="god-profile-name">{{ selectedGod.shortName || selectedGod.name }}</text>
              <text class="god-profile-sub">{{ selectedGod.title }}</text>
            </view>
          </view>
          <text class="god-profile-tip">查看该神明在不同阶段可能出现的恩赐效果</text>
        </view>

        <view class="god-filter-panel">
          <view class="god-search">
            <text class="search-icon">⌕</text>
            <input
              v-model="godKeyword"
              class="god-search-input"
              placeholder="搜索神明或奖励"
              placeholder-class="placeholder"
            />
          </view>
          <scroll-view scroll-x class="god-category-scroll">
            <view class="god-category-row">
              <view
                v-for="category in godCategoryFilters"
                :key="category.value"
                :class="[
                  'god-category-pill',
                  activeGodCategory === category.value ? 'active' : '',
                ]"
                @tap="activeGodCategory = category.value"
              >
                <text>{{ category.label }}</text>
              </view>
            </view>
          </scroll-view>
          <text class="god-summary"
            >{{ visibleGodWishes.length }} / {{ allGodWishes.length }}</text
          >
        </view>

        <view class="god-stage-list">
          <view
            v-for="stage in godStageGroups"
            :key="stage.stage"
            class="god-stage-card"
          >
            <view class="god-stage-head">
              <text class="god-stage-badge">{{ stage.stage }}阶段</text>
              <text class="god-stage-count">{{ stage.wishes.length }}项恩赐</text>
            </view>
            <view class="god-stage-divider"></view>
            <view class="god-wish-list">
              <view
                v-for="wish in stage.wishes"
                :key="wish.id"
                class="god-wish-row"
              >
                <view class="god-wish-row-top">
                  <image
                    v-if="wish.icon"
                    :src="wish.icon"
                    mode="aspectFit"
                    class="god-wish-icon"
                  ></image>
                  <view v-else :class="['god-wish-icon', wish.tone]">{{
                    wish.iconText
                  }}</view>
                  <view class="god-card-title">
                    <text class="god-name">{{ wish.name }}</text>
                    <view class="god-tags">
                      <text
                        v-for="tag in wish.tags"
                        :key="`${wish.id}-${tag.value}`"
                        :class="['god-tag', tag.className]"
                      >
                        {{ tag.label }}
                      </text>
                    </view>
                  </view>
                </view>
                <text class="god-tip">{{ wish.desc }}</text>
              </view>
            </view>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script>
const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"
).replace(/\/$/, "");
const HERO_DETAIL_IMAGE_BASE =
  "https://game.gtimg.cn/images/jk/jkimg/mode17s18/1624x750/";
const tonePalette = ["tone-gold", "tone-blue", "tone-violet", "tone-rose"];
const heroPalette = [
  "hero-one",
  "hero-two",
  "hero-three",
  "hero-four",
  "hero-five",
  "hero-six",
];
const itemPalette = [
  "bg-sword",
  "bg-bow",
  "bg-rod",
  "bg-tear",
  "bg-vest",
  "bg-cloak",
  "bg-belt",
  "bg-glove",
  "bg-pan",
  "bg-spatula",
];

function requestApi(path, params = {}) {
  return new Promise((resolve, reject) => {
    uni.request({
      url: `${API_BASE_URL}${path}`,
      method: "GET",
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

function compactText(value, fallback = "") {
  if (value === undefined || value === null) return fallback;
  return String(value).replace(/\s+/g, " ").trim() || fallback;
}

function firstChar(value, fallback = "?") {
  return compactText(value, fallback).slice(0, 1) || fallback;
}

function splitLevels(value) {
  return compactText(value)
    .split(/[|#]/)
    .map((item) => compactText(item))
    .filter(Boolean)
    .slice(0, 4);
}

function splitIds(value) {
  return compactText(value)
    .split("|")
    .map((item) => compactText(item))
    .filter((item) => item && item !== "-1" && item !== "0");
}

function buildHeroArt(hero) {
  const heroPaint = compactText(hero?.heroPaint);
  return heroPaint ? `${HERO_DETAIL_IMAGE_BASE}${heroPaint}.jpg` : "";
}

const baseItems = [
  { key: "sword", label: "剑", bg: "bg-sword" },
  { key: "bow", label: "弓", bg: "bg-bow" },
  { key: "rod", label: "棒", bg: "bg-rod" },
  { key: "tear", label: "泪", bg: "bg-tear" },
  { key: "vest", label: "甲", bg: "bg-vest" },
  { key: "cloak", label: "斗", bg: "bg-cloak" },
  { key: "belt", label: "带", bg: "bg-belt" },
  { key: "glove", label: "套", bg: "bg-glove" },
  { key: "pan", label: "锅", bg: "bg-pan" },
  { key: "spatula", label: "铲", bg: "bg-spatula" },
];

const recipePalette = [
  "recipe-flame",
  "recipe-tide",
  "recipe-venom",
  "recipe-storm",
  "recipe-void",
  "recipe-gold",
  "recipe-iron",
  "recipe-star",
  "recipe-sigil",
  "recipe-spirit",
];

export default {
  data() {
    return {
      activeTab: "heroes",
      heroKeyword: "",
      activeHeroFilter: "",
      activeRuneLevel: "",
      activeGodId: "",
      activeGodCategory: "",
      godKeyword: "",
      loading: false,
      loadError: "",
      seasonMeta: null,
      heroFiltersValue: {
        cost: "",
        class: "",
        trait: "",
      },
      heroClassOptions: [],
      heroTraitOptions: [],
      traitNameMap: {},
      tabs: [
        { key: "heroes", label: "英雄", icon: "♜" },
        { key: "traits", label: "羁绊", icon: "❖" },
        { key: "items", label: "装备", icon: "♛" },
        { key: "runes", label: "强化符文", icon: "✧" },
        { key: "gods", label: "神明", icon: "✬" },
      ],
      heroFilters: [
        { key: "cost", icon: "◉", label: "全部费用" },
        { key: "class", icon: "⬟", label: "全部职业" },
        { key: "trait", icon: "⬡", label: "全部特质" },
      ],
      runeLevelFilters: [
        { value: "", label: "全部" },
        { value: "1", label: "一级" },
        { value: "2", label: "二级" },
        { value: "3", label: "三级" },
      ],
      godCategoryFilters: [
        { value: "", label: "全部" },
        { value: "1", label: "经济类" },
        { value: "2", label: "战力类" },
        { value: "3", label: "道具类" },
        { value: "4", label: "功能类" },
      ],
      activeEquipType: "基础装备",
      equipTypeFilters: [
        { value: "基础装备", label: "基础装备" },
        { value: "成型装备", label: "成型装备" },
        { value: "光明装备", label: "光明装备" },
        { value: "辅助装备", label: "辅助装备" },
        { value: "神器装备", label: "神器装备" },
        { value: "纹章", label: "纹章" },
        { value: "特殊装备", label: "特殊装备" },
      ],
      heroes: [
        { name: "崔斯特", views: "12.3万", cost: "1", bg: "hero-one" },
        { name: "伊泽瑞尔", views: "8.7万", cost: "1", bg: "hero-two" },
        { name: "泰隆", views: "10.6万", cost: "1", bg: "hero-three" },
        { name: "内瑟斯", views: "9.1万", cost: "1", bg: "hero-four" },
        { name: "暮光吸", views: "7.6万", cost: "2", bg: "hero-five" },
        { name: "吉克蓝", views: "6.2万", cost: "2", bg: "hero-six" },
      ],
      traits: [
        {
          name: "星神",
          icon: "星",
          count: "2/4/6",
          desc: "友军造成伤害时获得治疗，后期容错更高。",
          levels: ["2: 12%", "4: 25%", "6: 45%"],
          tone: "tone-gold",
        },
        {
          name: "圣盾使",
          icon: "盾",
          count: "2/4/6",
          desc: "释放技能后获得护盾，适合前排持续作战。",
          levels: ["2: 20%", "4: 35%", "6: 50%"],
          tone: "tone-blue",
        },
        {
          name: "狙神",
          icon: "狙",
          count: "2/4",
          desc: "距离越远伤害越高，适合后排主 C。",
          levels: ["2: +8%", "4: +18%"],
          tone: "tone-violet",
        },
      ],
      baseItems,
      equipRecipes: [],
      equipItems: [],
      runes: [
        {
          name: "经济扩张",
          icon: "金",
          desc: "更快成型，适合连胜或高费运营。",
          tags: ["经济", "运营"],
          tone: "tone-gold",
        },
        {
          name: "前排壁垒",
          icon: "盾",
          desc: "补足坦度，提升阵容启动时间。",
          tags: ["防御", "前排"],
          tone: "tone-blue",
        },
        {
          name: "火力倾泻",
          icon: "攻",
          desc: "提升主 C 输出峰值，适合爆发阵容。",
          tags: ["输出", "主C"],
          tone: "tone-rose",
        },
        {
          name: "职业之心",
          icon: "转",
          desc: "提前开启关键羁绊节点。",
          tags: ["转职", "羁绊"],
          tone: "tone-violet",
        },
      ],
      gods: [
        {
          name: "裁决之神",
          icon: "裁",
          tip: "适合斩杀与爆发阵容",
          tone: "tone-gold",
        },
        {
          name: "守护之神",
          icon: "守",
          tip: "适合前排厚度不足时选择",
          tone: "tone-blue",
        },
        {
          name: "秘术之神",
          icon: "秘",
          tip: "适合法系和控制链阵容",
          tone: "tone-violet",
        },
      ],
    };
  },
  computed: {
    hasHeroFilter() {
      return Boolean(
        this.heroKeyword.trim() ||
        this.heroFiltersValue.cost ||
        this.heroFiltersValue.class ||
        this.heroFiltersValue.trait,
      );
    },
    activeHeroFilterOptions() {
      if (this.activeHeroFilter === "cost") {
        return [
          { value: "", label: "全部费用" },
          ...[1, 2, 3, 4, 5].map((cost) => ({
            value: String(cost),
            label: `${cost}费`,
          })),
        ];
      }
      if (this.activeHeroFilter === "class") {
        return [{ value: "", label: "全部职业" }, ...this.heroClassOptions];
      }
      if (this.activeHeroFilter === "trait") {
        return [{ value: "", label: "全部特质" }, ...this.heroTraitOptions];
      }
      return [];
    },
    visibleRunes() {
      if (!this.activeRuneLevel) return this.runes;
      return this.runes.filter((rune) => rune.level === this.activeRuneLevel);
    },
    visibleEquipItems() {
      return this.equipItems.filter(
        (item) => item.displayType === this.activeEquipType,
      );
    },
    allGodWishes() {
      return this.gods.flatMap((god) => god.wishes || []);
    },
    godFilters() {
      return this.gods.map((god) => ({
        value: String(god.id),
        label: god.shortName || god.name,
        subTitle: god.title,
        iconUrl: god.iconUrl,
      }));
    },
    selectedGod() {
      return (
        this.gods.find((god) => String(god.id) === this.activeGodId) ||
        this.gods[0] || {
          id: "",
          name: "",
          shortName: "",
          title: "",
          iconUrl: "",
          wishes: [],
        }
      );
    },
    visibleGodWishes() {
      const keyword = this.godKeyword.trim();
      return (this.selectedGod.wishes || []).filter((wish) => {
        const matchesCategory =
          !this.activeGodCategory ||
          wish.typeIds.includes(this.activeGodCategory);
        const matchesKeyword =
          !keyword ||
          wish.name.includes(keyword) ||
          wish.godName.includes(keyword) ||
          wish.desc.includes(keyword);
        return matchesCategory && matchesKeyword;
      });
    },
    godStageGroups() {
      const groups = new Map();
      this.visibleGodWishes.forEach((wish) => {
        if (!groups.has(wish.stage)) groups.set(wish.stage, []);
        groups.get(wish.stage).push(wish);
      });
      return Array.from(groups.entries())
        .sort((a, b) => Number(a[0]) - Number(b[0]))
        .map(([stage, wishes]) => ({ stage, wishes }));
    },
    visibleHeroes() {
      const keyword = this.heroKeyword.trim();
      return this.heroes.filter((hero) => {
        const matchesKeyword =
          !keyword ||
          hero.name.includes(keyword) ||
          hero.skillName.includes(keyword) ||
          hero.classNames.some((name) => name.includes(keyword)) ||
          hero.traitNames.some((name) => name.includes(keyword));
        const matchesCost =
          !this.heroFiltersValue.cost ||
          hero.cost === this.heroFiltersValue.cost;
        const matchesClass =
          !this.heroFiltersValue.class ||
          hero.classIds.includes(this.heroFiltersValue.class);
        const matchesTrait =
          !this.heroFiltersValue.trait ||
          hero.traitIds.includes(this.heroFiltersValue.trait);
        return matchesKeyword && matchesCost && matchesClass && matchesTrait;
      });
    },
    recipes() {
      if (this.equipRecipes.length) return this.equipRecipes;
      const recipes = [];
      this.baseItems.forEach((rowItem, rowIndex) => {
        this.baseItems.forEach((colItem, colIndex) => {
          const paletteIndex =
            (rowIndex * 3 + colIndex * 5) % recipePalette.length;
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
  mounted() {
    this.loadSeasonData();
  },
  methods: {
    async loadSeasonData() {
      this.loading = true;
      this.loadError = "";
      try {
        const [heroes, traits, equips, hexes, gods] = await Promise.all([
          requestApi("/api/heroes", { show_only: true }),
          requestApi("/api/traits"),
          requestApi("/api/equips"),
          requestApi("/api/hexes"),
          requestApi("/api/gods"),
        ]);

        const mappedTraits = this.mapTraits(traits.items || []);

        this.seasonMeta =
          heroes.meta ||
          traits.meta ||
          equips.meta ||
          hexes.meta ||
          gods.meta ||
          null;
        this.traits = mappedTraits;
        this.traitNameMap = this.buildTraitNameMap(mappedTraits);
        this.heroes = this.mapHeroes(heroes.items || []);
        this.buildHeroFilterOptions(this.heroes);
        this.setEquips(equips.items || []);
        this.runes = this.mapRunes(hexes.items || []);
        this.gods = this.mapGods(gods.items || []);
        if (!this.activeGodId && this.gods.length) {
          this.activeGodId = String(this.gods[0].id);
        }
      } catch (error) {
        this.loadError = "Season API request failed";
      } finally {
        this.loading = false;
      }
    },
    toggleHeroFilter(key) {
      this.activeHeroFilter = this.activeHeroFilter === key ? "" : key;
    },
    selectHeroFilter(key, value) {
      this.heroFiltersValue[key] = value;
      this.activeHeroFilter = "";
    },
    resetHeroFilters() {
      this.heroKeyword = "";
      this.heroFiltersValue = {
        cost: "",
        class: "",
        trait: "",
      };
      this.activeHeroFilter = "";
    },
    openHeroDetail(hero) {
      uni.navigateTo({
        url: `/pages/season/detail?id=${encodeURIComponent(hero.raw?.id || hero.id || "")}`,
      });
    },
    heroFilterValue(key) {
      return this.heroFiltersValue[key] || "";
    },
    heroFilterLabel(filter) {
      const value = this.heroFilterValue(filter.key);
      if (!value) return filter.label;
      if (filter.key === "cost") return `${value}费`;
      if (filter.key === "class") {
        return (
          this.heroClassOptions.find((option) => option.value === value)
            ?.label || filter.label
        );
      }
      if (filter.key === "trait") {
        return (
          this.heroTraitOptions.find((option) => option.value === value)
            ?.label || filter.label
        );
      }
      return filter.label;
    },
    mapHeroes(items) {
      const heroGroups = new Map();
      items
        .filter((hero) => {
          const price = Number(hero.price || 0);
          return (
            compactText(hero.name) &&
            compactText(hero.showHeroTag, "1") === "1" &&
            compactText(hero.heroType, "0") === "0" &&
            price > 0 &&
            price <= 5 &&
            splitIds(hero.species).length > 0
          );
        })
        .forEach((hero) => {
          const cost = compactText(hero.price, "0");
          const classIds = splitIds(hero.class);
          const traitIds = splitIds(hero.species);
          const key = [
            compactText(hero.name),
            cost,
            traitIds.join("|"),
            classIds.join("|"),
          ].join("__");
          const star = this.getHeroStar(hero);
          if (!heroGroups.has(key)) {
            heroGroups.set(key, { classIds, traitIds, variants: [] });
          }
          heroGroups.get(key).variants.push({
            key: compactText(hero.id, `${key}-${star}`),
            label: `${star}星`,
            star,
            raw: hero,
          });
        });

      return Array.from(heroGroups.values())
        .map((group) => {
          group.variants.sort(
            (a, b) =>
              a.star - b.star || Number(a.raw.id || 0) - Number(b.raw.id || 0),
          );
          group.raw = group.variants[0].raw;
          return group;
        })
        .sort(
          (a, b) =>
            Number(a.raw.price || 0) - Number(b.raw.price || 0) ||
            compactText(a.raw.name).localeCompare(compactText(b.raw.name)),
        )
        .map(({ raw: hero, classIds, traitIds, variants }, index) => ({
          id: [
            compactText(hero.name),
            compactText(hero.price),
            traitIds.join("|"),
            classIds.join("|"),
          ].join("__"),
          name: compactText(hero.name),
          views: compactText(hero.skillName, compactText(hero.tftHeroId, "")),
          skillName: compactText(hero.skillName),
          cost: compactText(hero.price, "0"),
          classIds,
          traitIds,
          classNames: classIds.map((id) => this.traitNameMap[id] || id),
          traitNames: traitIds.map((id) => this.traitNameMap[id] || id),
          cardTags: [
            ...traitIds.map((id) => this.traitNameMap[id] || id),
            ...classIds.map((id) => this.traitNameMap[id] || id),
          ].slice(0, 3),
          variants,
          raw: hero,
          picture: buildHeroArt(hero) || hero.picture,
          bg: heroPalette[index % heroPalette.length],
        }));
    },
    getHeroStar(hero) {
      const id = compactText(hero.id);
      const fromId = Number(id.slice(0, 1));
      if (fromId >= 1 && fromId <= 4) return fromId;
      return Number(hero.star || hero.level || 1) || 1;
    },
    buildTraitNameMap(traits) {
      return traits.reduce((map, trait) => {
        map[trait.id] = trait.name;
        return map;
      }, {});
    },
    buildHeroFilterOptions(heroes) {
      const classMap = new Map();
      const traitMap = new Map();
      heroes.forEach((hero) => {
        hero.classIds.forEach((id) =>
          classMap.set(id, this.traitNameMap[id] || id),
        );
        hero.traitIds.forEach((id) =>
          traitMap.set(id, this.traitNameMap[id] || id),
        );
      });
      this.heroClassOptions = this.sortFilterOptions(classMap);
      this.heroTraitOptions = this.sortFilterOptions(traitMap);
    },
    sortFilterOptions(optionMap) {
      return Array.from(optionMap.entries())
        .map(([value, label]) => ({ value, label }))
        .sort((a, b) => a.label.localeCompare(b.label, "zh-Hans-CN"));
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
    setEquips(items) {
      const nextBaseItems = items
        .filter(
          (item) =>
            compactText(item.synthesis1, "0") === "0" &&
            compactText(item.synthesis2, "0") === "0",
        )
        .slice(0, 10)
        .map((item, index) => ({
          key: compactText(item.id, `base-${index}`),
          label: firstChar(item.name),
          name: compactText(item.name),
          picture: item.picture,
          bg: itemPalette[index % itemPalette.length],
        }));

      this.baseItems = nextBaseItems.length ? nextBaseItems : baseItems;
      this.equipRecipes = this.buildRecipes(items);
      this.equipItems = this.mapEquipItems(items);
    },
    mapEquipItems(items) {
      const itemMap = new Map(
        items.map((item) => [compactText(item.id), item]),
      );
      return items
        .map((item, index) => {
          const displayType = this.normalizeEquipType(item.type);
          const componentA = itemMap.get(compactText(item.synthesis1));
          const componentB = itemMap.get(compactText(item.synthesis2));
          const hasRecipe = Boolean(componentA && componentB);
          return {
            id: compactText(item.id, `equip-${index}`),
            name: compactText(item.name),
            picture: item.picture,
            basicDesc: compactText(item.basicDesc),
            desc: compactText(item.desc),
            rawType: compactText(item.type),
            displayType,
            componentA,
            componentB,
            hasRecipe,
            sort: Number(item.mapID || item.sort || index),
          };
        })
        .filter((item) => item.name && item.displayType)
        .sort((a, b) => a.sort - b.sort || a.name.localeCompare(b.name));
    },
    normalizeEquipType(type) {
      const value = compactText(type);
      if (value === "-1") return "特殊装备";
      if (value === "光明武器") return "光明装备";
      if (value === "转职纹章") return "纹章";
      if (value.includes("辅助")) return "辅助装备";
      return value;
    },
    buildRecipes(items) {
      const recipeMap = new Map();
      items.forEach((item, index) => {
        const s1 = compactText(item.synthesis1);
        const s2 = compactText(item.synthesis2);
        if (!s1 || !s2 || s1 === "0" || s2 === "0") return;
        recipeMap.set(`${s1}-${s2}`, { item, index });
        recipeMap.set(`${s2}-${s1}`, { item, index });
      });

      const recipes = [];
      this.baseItems.forEach((rowItem, rowIndex) => {
        this.baseItems.forEach((colItem, colIndex) => {
          const match = recipeMap.get(`${rowItem.key}-${colItem.key}`);
          const paletteIndex =
            (rowIndex * 3 + colIndex * 5) % recipePalette.length;
          recipes.push({
            key: `${rowItem.key}-${colItem.key}`,
            label: match
              ? firstChar(match.item.name)
              : `${rowItem.label}${colItem.label}`,
            name: match ? compactText(match.item.name) : "",
            picture: match?.item?.picture,
            bg: recipePalette[paletteIndex],
          });
        });
      });
      return recipes;
    },
    mapRunes(items) {
      return items.map((rune, index) => ({
        id: rune.id,
        name: compactText(rune.name),
        icon: firstChar(rune.name),
        iconUrl: rune.icon,
        desc: compactText(rune.desc),
        level: compactText(rune.level, "0"),
        tags: [compactText(rune.level, "0")]
          .filter(Boolean)
          .map((level) => `Lv.${level}`),
        tone: tonePalette[index % tonePalette.length],
      }));
    },
    mapGods(items) {
      return items.map((god, index) => {
        const tone = tonePalette[index % tonePalette.length];
        const godName = compactText(god.godName);
        return {
          id: god.godId,
          name: godName,
          shortName: godName.split(" ")[0],
          title: godName.split(" ").slice(1).join(" ") || compactText(god.godTips),
          icon: firstChar(godName),
          iconUrl: god.godIcon || god.tex,
          tip: compactText(god.godTips),
          tone,
          wishes: this.mapGodWishes(god, tone),
        };
      });
    },
    mapGodWishes(god, tone) {
      const godName = compactText(god.godName);
      return (god.stages || []).flatMap((stage) =>
        (stage.wishes || []).map((wish) => {
          const typeIds = splitIds(wish.type);
          return {
            id: `${god.godId}-${stage.num}-${wish.id}`,
            godId: String(god.godId),
            name: compactText(wish.name),
            desc: compactText(wish.desc),
            icon: wish.icon,
            iconText: firstChar(wish.name),
            godName,
            stage: compactText(stage.num),
            stageNum: Number(stage.num || 0),
            typeIds,
            tags: typeIds.map((type) => this.mapGodWishType(type)),
            tone,
          };
        }),
      );
    },
    mapGodWishType(type) {
      const typeMap = {
        1: { label: "经济类", className: "economy" },
        2: { label: "战力类", className: "combat" },
        3: { label: "道具类", className: "item" },
        4: { label: "功能类", className: "utility" },
      };
      return {
        value: type,
        ...(typeMap[type] || { label: "其他", className: "other" }),
      };
    },
  },
};
</script>

<style scoped>
.season-page {
  @apply [min-height:100vh];
  @apply [overflow:hidden];
  @apply [color:#f5e6cb];
  @apply [background:#21102a];
}

.title-bar {
  @apply [display:flex];
  @apply [align-items:center];
  @apply [justify-content:center];
  @apply [gap:14rpx];
}

.page-title {
  @apply [color:#fff1d5];
  @apply [font-size:38rpx];
  @apply [font-weight:900];
}

.title-deco {
  @apply [color:#ba8350];
  @apply [font-size:24rpx];
}

.window-actions {
  @apply [position:absolute];
  @apply [right:18rpx];
  @apply [top:calc(var(--status-bar-height)_+_22rpx)];
  @apply [display:flex];
  @apply [align-items:center];
  @apply [gap:20rpx];
  @apply [height:58rpx];
  @apply [padding:0_18rpx];
  @apply [border:1rpx_solid_rgba(233,_198,_148,_0.42)];
  @apply [border-radius:30rpx];
  @apply [color:#f1dcc0];
  @apply [font-size:27rpx];
  @apply [font-weight:900];
  @apply [background:rgba(37,_17,_49,_0.74)];
}

.divider {
  @apply [width:1rpx];
  @apply [height:34rpx];
  @apply [background:rgba(233,_198,_148,_0.35)];
}

.circle {
  @apply [width:22rpx];
  @apply [height:22rpx];
  @apply [border:6rpx_solid_#f0dcc1];
  @apply [border-radius:50%];
}

.tab-shell {
  @apply [display:grid];
  @apply [grid-template-columns:repeat(5,_1fr)];
  @apply [height:102rpx];
  @apply [border-bottom:1rpx_solid_rgba(182,_132,_84,_0.32)];
  @apply [background:linear-gradient(180deg,_#24152f,_#1c1027)];
}

.tab-item {
  @apply [position:relative];
  @apply [display:flex];
  @apply [flex-direction:column];
  @apply [align-items:center];
  @apply [justify-content:center];
  @apply [color:rgba(223,_202,_176,_0.62)];
}

.tab-item.active {
  @apply [color:#ffe3a5];
  background: linear-gradient(
    180deg,
    rgba(216, 149, 72, 0.18),
    rgba(216, 149, 72, 0.02)
  );
}

.tab-item.active::after {
  @apply [position:absolute];
  @apply [left:0];
  @apply [right:0];
  @apply [bottom:0];
  @apply [height:4rpx];
  @apply [background:linear-gradient(90deg,_transparent,_#e6ad58,_transparent)];
  @apply [content:""];
}

.tab-icon {
  @apply [font-size:36rpx];
  @apply [line-height:38rpx];
}

.tab-label {
  @apply [margin-top:6rpx];
  @apply [font-size:23rpx];
  @apply [font-weight:900];
}

.content-scroll {
  @apply [height:calc(100vh_-_260rpx_-_var(--status-bar-height))];
  background:
    radial-gradient(
      circle at 100% 4%,
      rgba(111, 65, 138, 0.24),
      transparent 30%
    ),
    linear-gradient(180deg, #21102a 0%, #35173a 100%);
}

.tab-panel {
  @apply [padding:22rpx_18rpx_34rpx];
}

.state-card {
  @apply [display:flex];
  @apply [flex-direction:column];
  @apply [align-items:center];
  @apply [justify-content:center];
  @apply [min-height:360rpx];
  @apply [margin:28rpx_18rpx];
  @apply [border:1rpx_solid_rgba(221,_166,_100,_0.34)];
  @apply [border-radius:18rpx];
  @apply [color:rgba(245,_230,_203,_0.78)];
  @apply [font-size:27rpx];
  @apply [font-weight:900];
  @apply [background:rgba(255,_255,_255,_0.055)];
}

.state-card.error {
  @apply [color:#ffd0bf];
}

.retry-text {
  @apply [margin-top:16rpx];
  @apply [color:#e8c896];
  @apply [font-size:23rpx];
}

.search-box {
  @apply [display:flex];
  @apply [align-items:center];
  @apply [height:76rpx];
  @apply [padding:0_26rpx];
  @apply [border:1rpx_solid_rgba(219,_173,_116,_0.2)];
  @apply [border-radius:38rpx];
  @apply [background:rgba(255,_255,_255,_0.06)];
}

.search-icon {
  @apply [margin-right:18rpx];
  @apply [color:#bd9d82];
  @apply [font-size:38rpx];
}

.search-input {
  @apply [flex:1];
  @apply [height:76rpx];
  @apply [color:#fff2d8];
  @apply [font-size:27rpx];
  @apply [font-weight:800];
}

.placeholder {
  @apply [color:rgba(231,_206,_181,_0.48)];
}

.filter-row {
  @apply [display:grid];
  @apply [grid-template-columns:repeat(3,_1fr)];
  @apply [gap:18rpx];
  @apply [margin-top:22rpx];
}

.filter-pill {
  @apply [display:flex];
  @apply [align-items:center];
  @apply [justify-content:center];
  @apply [min-width:0];
  @apply [height:62rpx];
  @apply [border-radius:12rpx];
  @apply [color:#e7d4b8];
  @apply [font-size:23rpx];
  @apply [font-weight:900];
  @apply [background:rgba(255,_255,_255,_0.06)];
}

.filter-pill.active,
.filter-pill.selected {
  @apply [border:1rpx_solid_rgba(232,_189,_130,_0.6)];
  @apply [color:#ffe3a5];
  @apply [background:rgba(226,_174,_105,_0.14)];
}

.filter-label {
  @apply [min-width:0];
  @apply [overflow:hidden];
  @apply [text-overflow:ellipsis];
  @apply [white-space:nowrap];
}

.filter-icon {
  @apply [margin-right:8rpx];
  @apply [color:#c49b72];
}

.chevron {
  @apply [margin-left:8rpx];
  @apply [color:#b28a67];
}

.filter-panel {
  @apply [display:flex];
  @apply [flex-wrap:wrap];
  @apply [gap:12rpx];
  @apply [margin-top:16rpx];
  @apply [padding:16rpx];
  @apply [border:1rpx_solid_rgba(221,_166,_100,_0.28)];
  @apply [border-radius:16rpx];
  @apply [background:rgba(18,_9,_27,_0.45)];
}

.filter-option {
  @apply [display:flex];
  @apply [align-items:center];
  @apply [justify-content:center];
  @apply [min-width:112rpx];
  @apply [max-width:220rpx];
  @apply [height:54rpx];
  @apply [padding:0_18rpx];
  @apply [overflow:hidden];
  @apply [border:1rpx_solid_rgba(231,_191,_132,_0.18)];
  @apply [border-radius:10rpx];
  @apply [color:rgba(235,_214,_194,_0.74)];
  @apply [font-size:22rpx];
  @apply [font-weight:900];
  @apply [background:rgba(255,_255,_255,_0.055)];
}

.filter-option text {
  @apply [overflow:hidden];
  @apply [text-overflow:ellipsis];
  @apply [white-space:nowrap];
}

.filter-option.active {
  @apply [border-color:rgba(232,_189,_130,_0.72)];
  @apply [color:#fff2dc];
  @apply [background:rgba(226,_174,_105,_0.22)];
}

.hero-summary {
  @apply [display:flex];
  @apply [align-items:center];
  @apply [justify-content:space-between];
  @apply [margin-top:16rpx];
  @apply [color:rgba(235,_214,_194,_0.58)];
  @apply [font-size:22rpx];
  @apply [font-weight:900];
}

.clear-filter {
  @apply [color:#e8c896];
}

.guide-bg {
  @apply [position:relative];
  @apply [min-height:244rpx];
  @apply [overflow:hidden];
  @apply [border-radius:14rpx];
  background:
    radial-gradient(circle at 62% 25%, #f0d77b, transparent 15%),
    radial-gradient(circle at 50% 43%, #7a3aff, transparent 36%),
    linear-gradient(135deg, #2d1537, #5c38a8 52%, #16091f);
}

.guide-badge {
  @apply [position:absolute];
  @apply [left:0];
  @apply [top:0];
  @apply [padding:10rpx_18rpx];
  @apply [border-radius:0_0_16rpx_0];
  @apply [color:#fff3dc];
  @apply [font-size:22rpx];
  @apply [font-weight:900];
  @apply [background:rgba(167,_102,_48,_0.82)];
}

.mini-items {
  @apply [position:absolute];
  @apply [left:90rpx];
  @apply [bottom:26rpx];
  @apply [display:grid];
  @apply [grid-template-columns:repeat(4,_34rpx)];
  @apply [gap:8rpx];
}

.mini-item {
  @apply [width:34rpx];
  @apply [height:34rpx];
  @apply [border:1rpx_solid_rgba(237,_197,_136,_0.68)];
  @apply [border-radius:4rpx];
}

.mini-1,
.mini-5 {
  @apply [background:#c99b39];
}
.mini-2,
.mini-6 {
  @apply [background:#286bd8];
}
.mini-3,
.mini-7 {
  @apply [background:#7932b8];
}
.mini-4,
.mini-8 {
  @apply [background:#1b994f];
}

.guide-copy {
  @apply [padding:12rpx_0];
}

.guide-title {
  @apply [display:block];
  @apply [color:#fff2dc];
  @apply [font-size:30rpx];
  @apply [font-weight:900];
  @apply [line-height:42rpx];
}

.guide-desc {
  @apply [display:block];
  @apply [margin-top:18rpx];
  @apply [color:rgba(235,_214,_194,_0.58)];
  @apply [font-size:24rpx];
  @apply [line-height:34rpx];
}

.review-row,
.hero-meta,
.views,
.trait-card,
.trait-top {
  @apply [display:flex];
  @apply [align-items:center];
}

.review-row {
  @apply [gap:14rpx];
  @apply [margin-top:24rpx];
  @apply [color:#e7d0ad];
  @apply [font-size:23rpx];
  @apply [font-weight:800];
}

.avatar {
  @apply [width:44rpx];
  @apply [height:44rpx];
  @apply [border-radius:50%];
  @apply [background:linear-gradient(135deg,_#ffe3a3,_#895421_52%,_#2b1631)];
}

.review-arrow {
  @apply [margin-left:auto];
  @apply [color:#b99569];
  @apply [font-size:42rpx];
}

.hero-grid {
  @apply [display:grid];
  @apply [grid-template-columns:repeat(2,_minmax(0,_1fr))];
  @apply [gap:26rpx_20rpx];
  @apply [margin-top:28rpx];
}

.empty-card {
  @apply [display:flex];
  @apply [align-items:center];
  @apply [justify-content:center];
  @apply [min-height:180rpx];
  @apply [margin-top:28rpx];
  @apply [border:1rpx_solid_rgba(221,_166,_100,_0.26)];
  @apply [border-radius:14rpx];
  @apply [color:rgba(235,_214,_194,_0.62)];
  @apply [font-size:25rpx];
  @apply [font-weight:900];
  @apply [background:rgba(255,_255,_255,_0.045)];
}

.hero-card {
  @apply [position:relative];
  @apply [height:174rpx];
  @apply [overflow:hidden];
  @apply [border:4rpx_solid_rgba(127,_119,_143,_0.9)];
  @apply [border-radius:0];
  @apply [background:#25122e];
}

.hero-card::after {
  @apply [position:absolute];
  @apply [inset:0];
  @apply [border:1rpx_solid_rgba(255,_255,_255,_0.1)];
  @apply [content:""];
  @apply [pointer-events:none];
}

.hero-bg,
.hero-shade {
  @apply [position:absolute];
  @apply [inset:0];
}

.hero-bg.remote-image {
  @apply [background-position:center_24%];
  @apply [background-repeat:no-repeat];
  @apply [background-size:cover];
}

.hero-shade {
  background:
    linear-gradient(180deg, rgba(17, 7, 23, 0.02) 0%, rgba(17, 7, 23, 0.08) 54%, rgba(28, 12, 38, 0.98) 55%, rgba(28, 12, 38, 0.98) 100%),
    linear-gradient(90deg, rgba(17, 7, 23, 0.7) 0%, rgba(17, 7, 23, 0.04) 68%);
}

.hero-one {
  background:
    radial-gradient(circle at 66% 28%, #dcc067, transparent 20%),
    linear-gradient(135deg, #33205f, #7548ec 48%, #16091f);
}
.hero-two {
  background:
    radial-gradient(circle at 70% 26%, #f0b16f, transparent 22%),
    linear-gradient(135deg, #122b55, #23a1e4 48%, #16091f);
}
.hero-three {
  background:
    radial-gradient(circle at 25% 28%, #6dc7ff, transparent 24%),
    linear-gradient(135deg, #17235b, #435df0 52%, #16091f);
}
.hero-four {
  background:
    radial-gradient(circle at 65% 42%, #78fff3, transparent 24%),
    linear-gradient(135deg, #3f2261, #31c4bc 48%, #16091f);
}
.hero-five {
  background:
    radial-gradient(circle at 20% 26%, #f49133, transparent 23%),
    linear-gradient(135deg, #38162d, #a44d20 52%, #16091f);
}
.hero-six {
  background:
    radial-gradient(circle at 60% 30%, #c66cff, transparent 24%),
    linear-gradient(135deg, #1b1d61, #7433cd 52%, #16091f);
}

.cost-badge {
  @apply [position:absolute];
  @apply [right:12rpx];
  @apply [bottom:10rpx];
  @apply [display:flex];
  @apply [align-items:center];
  @apply [justify-content:center];
  @apply [width:auto];
  @apply [height:34rpx];
  @apply [padding:0_8rpx];
  @apply [border:0];
  @apply [border-radius:0];
  @apply [color:#fff];
  @apply [font-size:22rpx];
  @apply [font-weight:900];
  @apply [background:transparent];
}

.cost-badge::before {
  @apply [width:18rpx];
  @apply [height:18rpx];
  @apply [margin-right:6rpx];
  @apply [border:4rpx_solid_#fff];
  @apply [border-radius:50%];
  @apply [content:""];
}

.hero-tags {
  @apply [position:absolute];
  @apply [left:18rpx];
  @apply [right:88rpx];
  @apply [top:72rpx];
  @apply [display:grid];
  @apply [gap:6rpx];
  @apply [overflow:hidden];
}

.hero-tags text {
  @apply [display:block];
  @apply [max-width:150rpx];
  @apply [height:28rpx];
  @apply [padding:0];
  @apply [overflow:hidden];
  @apply [border:0];
  @apply [border-radius:0];
  @apply [color:rgba(255,_255,_255,_0.88)];
  @apply [font-size:20rpx];
  @apply [font-weight:900];
  @apply [line-height:28rpx];
  @apply [text-overflow:ellipsis];
  @apply [white-space:nowrap];
  @apply [text-shadow:0_2rpx_4rpx_rgba(0,_0,_0,_0.75)];
  @apply [background:transparent];
}

.hero-tags text::before {
  @apply [margin-right:8rpx];
  @apply [color:#fff];
  @apply [content:"✥"];
}

.hero-meta {
  @apply [position:absolute];
  @apply [left:0];
  @apply [right:0];
  @apply [bottom:0];
  @apply [height:48rpx];
  @apply [padding:0_56rpx_0_12rpx];
  @apply [justify-content:space-between];
  @apply [background:#24142f];
}

.hero-name {
  @apply [color:#fff2dc];
  @apply [font-size:26rpx];
  @apply [font-weight:900];
}

.views {
  @apply [display:none];
}

.detail-mask {
  @apply [position:fixed];
  @apply [inset:0];
  @apply [z-index:50];
  @apply [display:flex];
  @apply [align-items:flex-end];
  @apply [background:rgba(9,_4,_14,_0.78)];
}

.hero-detail {
  @apply [width:100%];
  @apply [height:92vh];
  @apply [overflow:hidden];
  @apply [border-radius:30rpx_30rpx_0_0];
  background:
    linear-gradient(
      180deg,
      rgba(57, 36, 102, 0.88),
      rgba(23, 12, 36, 0.96) 38%,
      #14091d 100%
    ),
    repeating-linear-gradient(
      0deg,
      rgba(255, 255, 255, 0.035) 0,
      rgba(255, 255, 255, 0.035) 1rpx,
      transparent 1rpx,
      transparent 6rpx
    );
}

.detail-page-scroll {
  @apply [height:92vh];
}

.detail-visual {
  @apply [position:relative];
  @apply [height:520rpx];
  @apply [overflow:hidden];
}

.detail-portrait {
  @apply [position:absolute];
  @apply [inset:0];
  @apply [background-position:center_18%];
  @apply [background-repeat:no-repeat];
  @apply [background-size:cover];
  @apply [transform:scale(1.08)];
}

.detail-cover {
  @apply [position:absolute];
  @apply [inset:0];
  background:
    linear-gradient(
      90deg,
      rgba(14, 7, 24, 0.78) 0%,
      rgba(14, 7, 24, 0.18) 56%,
      rgba(14, 7, 24, 0.7) 100%
    ),
    linear-gradient(
      180deg,
      rgba(14, 7, 24, 0.2) 0%,
      rgba(14, 7, 24, 0.18) 45%,
      #201037 100%
    );
}

.detail-close {
  @apply [position:absolute];
  @apply [right:24rpx];
  @apply [top:24rpx];
  @apply [display:flex];
  @apply [align-items:center];
  @apply [justify-content:center];
  @apply [width:68rpx];
  @apply [height:68rpx];
  @apply [padding:0];
  @apply [border:0];
  @apply [border-radius:50%];
  @apply [color:#fff2dc];
  @apply [font-size:44rpx];
  @apply [line-height:68rpx];
  @apply [background:rgba(16,_8,_28,_0.72)];
  @apply [backdrop-filter:blur(8rpx)];
}

.detail-close::after {
  @apply [border:0];
}

.detail-title {
  @apply [position:absolute];
  @apply [left:28rpx];
  @apply [right:28rpx];
  @apply [bottom:28rpx];
}

.detail-title-row {
  @apply [display:flex];
  @apply [align-items:center];
  @apply [gap:12rpx];
}

.detail-cost {
  @apply [display:inline-flex];
  @apply [align-items:center];
  @apply [height:42rpx];
  @apply [padding:0_16rpx];
  @apply [border:1rpx_solid_rgba(232,_189,_130,_0.56)];
  @apply [border-radius:12rpx];
  @apply [color:#f6d49a];
  @apply [font-size:22rpx];
  @apply [font-weight:900];
  @apply [background:rgba(22,_9,_28,_0.64)];
}

.detail-star {
  @apply [display:inline-flex];
  @apply [align-items:center];
  @apply [height:42rpx];
  @apply [padding:0_16rpx];
  @apply [border:1rpx_solid_rgba(133,_244,_236,_0.56)];
  @apply [border-radius:12rpx];
  @apply [color:#a8fff6];
  @apply [font-size:22rpx];
  @apply [font-weight:900];
  @apply [background:rgba(18,_68,_72,_0.42)];
}

.detail-name {
  @apply [display:block];
  @apply [margin-top:14rpx];
  @apply [color:#fff4df];
  @apply [font-size:52rpx];
  @apply [font-weight:900];
}

.detail-body {
  @apply [position:relative];
  @apply [z-index:1];
  @apply [margin-top:-8rpx];
  @apply [padding:22rpx_24rpx_48rpx];
}

.detail-section {
  @apply [margin-bottom:22rpx];
  @apply [padding:24rpx];
  @apply [overflow:hidden];
  @apply [border:1rpx_solid_rgba(221,_166,_100,_0.24)];
  @apply [border-radius:18rpx];
  background:
    linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.08),
      rgba(255, 255, 255, 0.035)
    ),
    rgba(19, 9, 31, 0.66);
  @apply [box-shadow:inset_0_1rpx_0_rgba(255,_255,_255,_0.08)];
}

.skill-section {
  @apply [border-color:rgba(245,_211,_122,_0.34)];
}

.section-line-title {
  @apply [display:flex];
  @apply [align-items:center];
  @apply [gap:16rpx];
}

.section-title-copy {
  @apply [min-width:0];
}

.detail-section-title {
  @apply [display:block];
  @apply [color:#fff0d6];
  @apply [font-size:28rpx];
  @apply [font-weight:900];
}

.detail-section-sub {
  @apply [display:block];
  @apply [margin-top:4rpx];
  @apply [overflow:hidden];
  @apply [color:rgba(239,_219,_188,_0.58)];
  @apply [font-size:21rpx];
  @apply [font-weight:800];
  @apply [text-overflow:ellipsis];
  @apply [white-space:nowrap];
}

.detail-chip-row {
  @apply [display:flex];
  @apply [flex-wrap:wrap];
  @apply [gap:12rpx];
  @apply [margin-top:16rpx];
}

.detail-chip-row.compact {
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

.detail-chip.trait {
  @apply [background:linear-gradient(135deg,_#ffe0a3,_#c48b43)];
}

.detail-chip.role {
  @apply [background:linear-gradient(135deg,_#9ce6ff,_#4b9bd2)];
}

.detail-desc,
.detail-value {
  @apply [display:block];
  @apply [margin-top:16rpx];
  @apply [color:rgba(245,_230,_203,_0.76)];
  @apply [font-size:24rpx];
  @apply [line-height:39rpx];
}

.detail-value {
  @apply [color:#e8c896];
}

.skill-icon,
.mini-mark {
  @apply [flex:0_0_auto];
  @apply [width:70rpx];
  @apply [height:70rpx];
  @apply [overflow:hidden];
  @apply [border:1rpx_solid_rgba(255,_224,_163,_0.5)];
  @apply [border-radius:14rpx];
  @apply [background:rgba(255,_224,_163,_0.12)];
}

.skill-icon.fallback,
.mini-mark {
  @apply [display:flex];
  @apply [align-items:center];
  @apply [justify-content:center];
  @apply [color:#ffe0a3];
  @apply [font-size:24rpx];
  @apply [font-weight:900];
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

.trait-detail-list {
  @apply [display:grid];
  @apply [gap:16rpx];
  @apply [margin-top:20rpx];
}

.trait-detail-card {
  @apply [padding:18rpx];
  @apply [border:1rpx_solid_rgba(255,_255,_255,_0.07)];
  @apply [border-radius:16rpx];
  @apply [background:rgba(18,_9,_27,_0.42)];
}

.trait-detail-head {
  @apply [display:flex];
  @apply [align-items:center];
  @apply [gap:14rpx];
}

.trait-detail-icon {
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

.trait-detail-copy {
  @apply [min-width:0];
}

.trait-detail-name {
  @apply [display:block];
  @apply [color:#fff0d6];
  @apply [font-size:25rpx];
  @apply [font-weight:900];
}

.trait-detail-count {
  @apply [display:block];
  @apply [margin-top:4rpx];
  @apply [color:#e8c896];
  @apply [font-size:21rpx];
  @apply [font-weight:800];
}

.trait-detail-desc {
  @apply [display:block];
  @apply [margin-top:14rpx];
  @apply [color:rgba(245,_230,_203,_0.7)];
  @apply [font-size:23rpx];
  @apply [line-height:36rpx];
}

.trait-detail-levels {
  @apply [display:flex];
  @apply [flex-wrap:wrap];
  @apply [gap:10rpx];
  @apply [margin-top:14rpx];
}

.trait-detail-levels text {
  @apply [max-width:100%];
  @apply [padding:8rpx_12rpx];
  @apply [border-radius:10rpx];
  @apply [color:#241426];
  @apply [font-size:20rpx];
  @apply [font-weight:900];
  @apply [background:linear-gradient(135deg,_#ffe0a3,_#c48b43)];
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

.section-head {
  @apply [padding:8rpx_0_20rpx];
}

.section-title {
  @apply [display:block];
  @apply [color:#fff0d6];
  @apply [font-size:31rpx];
  @apply [font-weight:900];
}

.section-sub {
  @apply [display:block];
  @apply [margin-top:8rpx];
  @apply [color:rgba(235,_214,_194,_0.56)];
  @apply [font-size:24rpx];
}

.trait-list {
  @apply [display:grid];
  @apply [gap:18rpx];
}

.trait-card {
  @apply [gap:20rpx];
  @apply [padding:22rpx];
  @apply [border:1rpx_solid_rgba(221,_166,_100,_0.32)];
  @apply [border-radius:18rpx];
  @apply [background:rgba(255,_255,_255,_0.055)];
}

.trait-emblem,
.rune-mark,
.god-icon {
  @apply [display:flex];
  @apply [align-items:center];
  @apply [justify-content:center];
  @apply [flex-shrink:0];
  @apply [color:#1c1027];
  @apply [font-weight:900];
}

.data-icon {
  @apply [width:100%];
  @apply [height:100%];
}

.trait-emblem {
  @apply [width:76rpx];
  @apply [height:76rpx];
  @apply [border-radius:22rpx];
  @apply [font-size:30rpx];
}

.trait-main {
  @apply [flex:1];
}

.trait-top {
  @apply [justify-content:space-between];
}

.trait-name {
  @apply [color:#fff1d5];
  @apply [font-size:30rpx];
  @apply [font-weight:900];
}

.trait-count {
  @apply [color:#d5aa72];
  @apply [font-size:23rpx];
  @apply [font-weight:900];
}

.trait-desc {
  @apply [display:block];
  @apply [margin-top:10rpx];
  @apply [color:rgba(235,_214,_194,_0.62)];
  @apply [font-size:24rpx];
  @apply [line-height:34rpx];
}

.trait-levels,
.rune-tags {
  @apply [display:flex];
  @apply [flex-wrap:wrap];
  @apply [gap:10rpx];
  @apply [margin-top:16rpx];
}

.trait-levels text,
.rune-tags text {
  @apply [padding:7rpx_12rpx];
  @apply [border-radius:999rpx];
  @apply [color:#e8c896];
  @apply [font-size:20rpx];
  @apply [font-weight:900];
  @apply [background:rgba(226,_174,_105,_0.12)];
}

.base-items {
  @apply [display:flex];
  @apply [flex-wrap:wrap];
  @apply [gap:12rpx];
  @apply [margin-top:18rpx];
}

.equip-icon,
.axis-icon,
.recipe-icon {
  @apply [position:relative];
  @apply [display:flex];
  @apply [align-items:flex-end];
  @apply [justify-content:center];
  @apply [overflow:hidden];
  @apply [border:2rpx_solid_rgba(231,_191,_132,_0.58)];
  @apply [border-radius:4rpx];
  @apply [color:#fff5de];
  @apply [font-weight:900];
  @apply [text-shadow:0_2rpx_4rpx_rgba(0,_0,_0,_0.72)];
}

.equip-icon {
  @apply [width:58rpx];
  @apply [height:58rpx];
  @apply [font-size:19rpx];
}

.equip-type-scroll {
  @apply [width:100%];
  @apply [margin-bottom:18rpx];
  @apply [white-space:nowrap];
}

.equip-type-row {
  @apply [display:flex];
  @apply [gap:12rpx];
}

.equip-type-pill {
  @apply [flex:0_0_auto];
  @apply [height:60rpx];
  @apply [padding:0_20rpx];
  @apply [border:1rpx_solid_rgba(221,_166,_100,_0.28)];
  @apply [border-radius:14rpx];
  @apply [color:rgba(245,_230,_203,_0.72)];
  @apply [font-size:22rpx];
  @apply [font-weight:900];
  @apply [line-height:60rpx];
  @apply [background:rgba(255,_255,_255,_0.055)];
}

.equip-type-pill.active {
  @apply [color:#241426];
  @apply [border-color:rgba(255,_224,_163,_0.88)];
  @apply [background:linear-gradient(135deg,_#ffe0a3,_#c48b43)];
}

.equip-summary {
  @apply [margin:18rpx_0_16rpx];
  @apply [color:rgba(235,_214,_194,_0.58)];
  @apply [font-size:22rpx];
  @apply [font-weight:900];
}

.equip-list {
  @apply [display:grid];
  @apply [gap:14rpx];
}

.equip-row-card {
  @apply [display:grid];
  @apply [grid-template-columns:212rpx_minmax(0,_1fr)];
  @apply [gap:18rpx];
  @apply [min-height:138rpx];
  @apply [padding:18rpx];
  @apply [border:1rpx_solid_rgba(221,_166,_100,_0.24)];
  @apply [border-radius:16rpx];
  @apply [background:#432881];
}

.equip-formula {
  @apply [display:flex];
  @apply [align-items:center];
  @apply [gap:8rpx];
  @apply [min-width:0];
}

.equip-formula-icon {
  @apply [flex:0_0_auto];
  @apply [width:46rpx];
  @apply [height:46rpx];
  @apply [overflow:hidden];
  @apply [border:2rpx_solid_rgba(231,_191,_132,_0.5)];
  @apply [border-radius:4rpx];
  @apply [background:rgba(18,_9,_27,_0.38)];
}

.equip-formula-icon.empty {
  @apply [width:58rpx];
  @apply [height:58rpx];
}

.equip-formula-icon.result {
  @apply [width:54rpx];
  @apply [height:54rpx];
  @apply [border-color:rgba(255,_224,_163,_0.72)];
}

.formula-symbol {
  @apply [color:rgba(245,_230,_203,_0.34)];
  @apply [font-size:24rpx];
  @apply [font-weight:900];
}

.equip-copy {
  @apply [min-width:0];
}

.equip-title-line {
  @apply [display:flex];
  @apply [align-items:center];
  @apply [gap:10rpx];
}

.equip-name {
  @apply [min-width:0];
  @apply [overflow:hidden];
  @apply [color:#ffe267];
  @apply [font-size:24rpx];
  @apply [font-weight:900];
  @apply [text-overflow:ellipsis];
  @apply [white-space:nowrap];
}

.equip-type-label {
  @apply [flex:0_0_auto];
  @apply [height:32rpx];
  @apply [padding:0_10rpx];
  @apply [border-radius:9rpx];
  @apply [color:#fff2dc];
  @apply [font-size:18rpx];
  @apply [font-weight:900];
  @apply [line-height:32rpx];
  @apply [background:rgba(22,_9,_28,_0.34)];
}

.equip-basic,
.equip-desc {
  @apply [display:block];
  @apply [margin-top:8rpx];
  @apply [color:rgba(245,_230,_203,_0.72)];
  @apply [font-size:21rpx];
  @apply [line-height:31rpx];
}

.equip-basic {
  @apply [color:#d7bdff];
  @apply [font-weight:900];
}

.craft-title {
  @apply [margin-top:54rpx];
}

.craft-board {
  @apply [display:grid];
  @apply [grid-template-columns:48rpx_1fr];
  @apply [grid-template-rows:48rpx_auto];
  @apply [gap:6rpx];
}

.corner {
  @apply [display:flex];
  @apply [align-items:center];
  @apply [justify-content:center];
  @apply [color:rgba(217,_180,_128,_0.55)];
  @apply [font-size:36rpx];
  @apply [font-weight:900];
}

.top-axis,
.recipe-grid {
  @apply [display:grid];
  @apply [grid-template-columns:repeat(10,_1fr)];
  @apply [gap:6rpx];
}

.left-axis {
  @apply [display:grid];
  @apply [grid-template-rows:repeat(10,_1fr)];
  @apply [gap:6rpx];
}

.axis-icon,
.recipe-icon {
  @apply [width:48rpx];
  @apply [height:48rpx];
  @apply [font-size:14rpx];
}

.rune-grid {
  @apply [display:grid];
  @apply [grid-template-columns:repeat(2,_minmax(0,_1fr))];
  @apply [gap:18rpx];
}

.rune-level-tabs {
  @apply [display:grid];
  @apply [grid-template-columns:repeat(4,_minmax(0,_1fr))];
  @apply [gap:12rpx];
  @apply [margin-bottom:16rpx];
}

.rune-level-tab {
  @apply [display:flex];
  @apply [align-items:center];
  @apply [justify-content:center];
  @apply [height:58rpx];
  @apply [border:1rpx_solid_rgba(221,_166,_100,_0.24)];
  @apply [border-radius:14rpx];
  @apply [color:rgba(245,_230,_203,_0.7)];
  @apply [font-size:23rpx];
  @apply [font-weight:900];
  @apply [background:rgba(255,_255,_255,_0.055)];
}

.rune-level-tab.active {
  @apply [color:#241426];
  @apply [border-color:rgba(255,_224,_163,_0.88)];
  @apply [background:linear-gradient(135deg,_#ffe0a3,_#c48b43)];
  @apply [box-shadow:0_12rpx_26rpx_rgba(196,_139,_67,_0.22)];
}

.rune-summary {
  @apply [margin-bottom:16rpx];
  @apply [color:rgba(235,_214,_194,_0.58)];
  @apply [font-size:22rpx];
  @apply [font-weight:900];
}

.rune-card {
  @apply [min-height:246rpx];
  @apply [padding:22rpx];
  @apply [border:1rpx_solid_rgba(221,_166,_100,_0.32)];
  @apply [border-radius:18rpx];
  @apply [background:#684bbe];
}

.rune-mark {
  @apply [width:62rpx];
  @apply [height:62rpx];
  @apply [border-radius:18rpx];
  @apply [font-size:25rpx];
}

.rune-name {
  @apply [display:block];
  @apply [margin-top:22rpx];
  @apply [color:#fff1d5];
  @apply [font-size:29rpx];
  @apply [font-weight:900];
}

.rune-desc {
  @apply [display:block];
  @apply [margin-top:10rpx];
  @apply [color:rgba(235,_214,_194,_0.62)];
  @apply [font-size:23rpx];
  @apply [line-height:33rpx];
}

.god-summary {
  @apply [display:block];
}

.god-selector-scroll {
  @apply [width:100%];
  @apply [white-space:nowrap];
}

.god-selector-row {
  @apply [display:flex];
  @apply [gap:18rpx];
}

.god-select-card {
  @apply [display:flex];
  @apply [align-items:center];
  @apply [gap:16rpx];
  @apply [flex:0_0_310rpx];
  @apply [min-height:118rpx];
  @apply [padding:20rpx];
  @apply [border:2rpx_solid_transparent];
  @apply [border-radius:24rpx];
  @apply [background:rgba(67,_40,_129,_0.72)];
}

.god-select-card.active {
  @apply [border-color:#d8a84f];
  @apply [background:rgba(104,_75,_190,_0.52)];
}

.god-select-icon {
  @apply [flex:0_0_auto];
  @apply [width:86rpx];
  @apply [height:74rpx];
}

.god-select-copy {
  @apply [min-width:0];
}

.god-select-copy text {
  @apply [display:block];
  @apply [overflow:hidden];
  @apply [text-overflow:ellipsis];
  @apply [white-space:nowrap];
}

.god-select-copy text:first-child {
  @apply [color:#fff2dc];
  @apply [font-size:27rpx];
  @apply [font-weight:900];
}

.god-select-copy text:last-child {
  @apply [margin-top:6rpx];
  @apply [color:rgba(245,_230,_203,_0.62)];
  @apply [font-size:22rpx];
  @apply [font-weight:800];
}

.god-profile-card {
  @apply [position:relative];
  @apply [min-height:340rpx];
  @apply [margin-top:26rpx];
  @apply [overflow:hidden];
  @apply [border-radius:26rpx];
  @apply [background:#432881];
}

.god-profile-art {
  @apply [position:absolute];
  @apply [right:-30rpx];
  @apply [top:-40rpx];
  @apply [width:560rpx];
  @apply [height:360rpx];
  @apply [opacity:0.9];
}

.god-profile-mask {
  @apply [position:absolute];
  @apply [inset:0];
  background:
    linear-gradient(90deg, rgba(22, 9, 28, 0.86), rgba(22, 9, 28, 0.34)),
    linear-gradient(180deg, rgba(22, 9, 28, 0.04), rgba(22, 9, 28, 0.82));
}

.god-profile-content {
  @apply [position:relative];
  @apply [z-index:1];
  @apply [display:flex];
  @apply [align-items:center];
  @apply [gap:18rpx];
  @apply [padding:140rpx_34rpx_0];
}

.god-profile-icon {
  @apply [width:96rpx];
  @apply [height:96rpx];
  @apply [border:2rpx_solid_rgba(255,_224,_163,_0.28)];
  @apply [border-radius:18rpx];
  @apply [background:rgba(22,_9,_28,_0.32)];
}

.god-profile-name,
.god-profile-sub,
.god-profile-tip {
  @apply [display:block];
  @apply [position:relative];
  @apply [z-index:1];
}

.god-profile-name {
  @apply [color:#fff2dc];
  @apply [font-size:36rpx];
  @apply [font-weight:900];
}

.god-profile-sub {
  @apply [margin-top:4rpx];
  @apply [color:rgba(245,_230,_203,_0.66)];
  @apply [font-size:24rpx];
  @apply [font-weight:800];
}

.god-profile-tip {
  @apply [padding:30rpx_34rpx_34rpx];
  @apply [color:rgba(245,_230,_203,_0.78)];
  @apply [font-size:25rpx];
  @apply [line-height:38rpx];
}

.god-filter-panel {
  @apply [margin-top:20rpx];
  @apply [padding:18rpx];
  @apply [border:1rpx_solid_rgba(221,_166,_100,_0.26)];
  @apply [border-radius:18rpx];
  @apply [background:rgba(104,_75,_190,_0.38)];
}

.god-search {
  @apply [display:flex];
  @apply [align-items:center];
  @apply [height:70rpx];
  @apply [padding:0_20rpx];
  @apply [border:1rpx_solid_rgba(255,_224,_163,_0.22)];
  @apply [border-radius:14rpx];
  @apply [background:rgba(22,_9,_28,_0.34)];
}

.god-search-input {
  @apply [flex:1];
  @apply [min-width:0];
  @apply [color:#fff2dc];
  @apply [font-size:24rpx];
  @apply [font-weight:800];
}

.god-category-scroll {
  @apply [width:100%];
  @apply [margin-top:16rpx];
  @apply [white-space:nowrap];
}

.god-category-row {
  @apply [display:flex];
  @apply [gap:12rpx];
}

.god-category-pill {
  @apply [flex:0_0_auto];
  @apply [min-width:118rpx];
  @apply [height:58rpx];
  @apply [padding:0_20rpx];
  @apply [border:1rpx_solid_rgba(255,_224,_163,_0.22)];
  @apply [border-radius:14rpx];
  @apply [color:rgba(245,_230,_203,_0.74)];
  @apply [font-size:22rpx];
  @apply [font-weight:900];
  @apply [line-height:58rpx];
  @apply [text-align:center];
  @apply [background:rgba(22,_9,_28,_0.26)];
}

.god-category-pill.active {
  @apply [color:#241426];
  @apply [border-color:rgba(255,_224,_163,_0.88)];
  @apply [background:linear-gradient(135deg,_#ffe0a3,_#c48b43)];
}

.god-summary {
  @apply [margin-top:14rpx];
  @apply [color:rgba(235,_214,_194,_0.62)];
  @apply [font-size:21rpx];
  @apply [font-weight:900];
}

.god-stage-list {
  @apply [display:grid];
  @apply [gap:26rpx];
  @apply [margin-top:26rpx];
}

.god-stage-card {
  @apply [padding:28rpx];
  @apply [border:1rpx_solid_rgba(221,_166,_100,_0.24)];
  @apply [border-radius:26rpx];
  @apply [background:rgba(67,_40,_129,_0.84)];
}

.god-stage-head {
  @apply [display:flex];
  @apply [align-items:center];
  @apply [justify-content:space-between];
}

.god-stage-badge {
  @apply [height:58rpx];
  @apply [min-width:118rpx];
  @apply [padding:0_22rpx];
  @apply [border-radius:999rpx];
  @apply [color:#ffe267];
  @apply [font-size:28rpx];
  @apply [font-weight:900];
  @apply [line-height:58rpx];
  @apply [text-align:center];
  @apply [background:rgba(196,_139,_67,_0.58)];
}

.god-stage-count {
  @apply [color:rgba(245,_230,_203,_0.62)];
  @apply [font-size:23rpx];
  @apply [font-weight:800];
}

.god-stage-divider {
  @apply [height:1rpx];
  @apply [margin:28rpx_0];
  @apply [background:rgba(255,_255,_255,_0.08)];
}

.god-wish-list {
  @apply [display:grid];
  @apply [gap:28rpx];
}

.god-wish-row {
  @apply [padding-bottom:28rpx];
  @apply [border-bottom:1rpx_solid_rgba(255,_255,_255,_0.08)];
}

.god-wish-row:last-child {
  @apply [padding-bottom:0];
  @apply [border-bottom:0];
}

.god-wish-row-top {
  @apply [display:flex];
  @apply [align-items:center];
  @apply [gap:16rpx];
}

.god-wish-icon {
  @apply [display:flex];
  @apply [align-items:center];
  @apply [justify-content:center];
  @apply [width:62rpx];
  @apply [height:62rpx];
  @apply [flex:0_0_auto];
  @apply [overflow:hidden];
  @apply [border-radius:18rpx];
  @apply [color:#fff2dc];
  @apply [font-size:22rpx];
  @apply [font-weight:900];
}

.god-card-title {
  @apply [min-width:0];
}

.god-name,
.god-source,
.god-tip {
  @apply [display:block];
}

.god-name {
  @apply [color:#fff1d5];
  @apply [font-size:27rpx];
  @apply [font-weight:900];
}

.god-source {
  @apply [margin-top:6rpx];
  @apply [overflow:hidden];
  @apply [color:rgba(235,_214,_194,_0.54)];
  @apply [font-size:21rpx];
  @apply [font-weight:800];
  @apply [text-overflow:ellipsis];
  @apply [white-space:nowrap];
}

.god-tags {
  @apply [display:flex];
  @apply [flex-wrap:wrap];
  @apply [gap:10rpx];
  @apply [margin-top:16rpx];
}

.god-tag {
  @apply [height:36rpx];
  @apply [padding:0_12rpx];
  @apply [border-radius:10rpx];
  @apply [color:#fff2dc];
  @apply [font-size:18rpx];
  @apply [font-weight:900];
  @apply [line-height:36rpx];
  @apply [background:rgba(22,_9,_28,_0.38)];
}

.god-tag.economy {
  @apply [color:#92ffd1];
}

.god-tag.combat {
  @apply [color:#ffb07b];
}

.god-tag.item {
  @apply [color:#cda4ff];
}

.god-tag.utility {
  @apply [color:#9ce6ff];
}

.god-tip {
  @apply [margin-top:16rpx];
  @apply [color:rgba(245,_230,_203,_0.74)];
  @apply [font-size:22rpx];
  @apply [line-height:34rpx];
}

.tone-gold {
  @apply [background:#684bbe];
}
.tone-blue {
  @apply [background:linear-gradient(135deg,_#7fd7ff,_#1b5fb9)];
  @apply [background:#684bbe];
}
.tone-violet {
  @apply [background:#684bbe];
}
.tone-rose {
  @apply [background:linear-gradient(135deg,_#ff91ad,_#9b2948)];
  @apply [background:linear-gradient(135deg,_#be8bff,_#5631b3)];
}

.bg-sword {
  @apply [background:linear-gradient(135deg,_#1b2a66,_#e1c86e_52%,_#402616)];
}
.bg-bow {
  @apply [background:linear-gradient(135deg,_#283b1c,_#c7d092_50%,_#3a2614)];
}
.bg-rod {
  background:
    radial-gradient(circle at 62% 32%, #ff9de6, transparent 24%),
    linear-gradient(135deg, #36104e, #b932a0 55%, #1b0c27);
}
.bg-tear {
  background:
    radial-gradient(circle at 55% 36%, #55d7ff, transparent 28%),
    linear-gradient(135deg, #10225a, #164fde 58%, #070d2c);
}
.bg-vest {
  @apply [background:linear-gradient(135deg,_#153b49,_#5fc3bf_48%,_#1b2229)];
}
.bg-cloak {
  @apply [background:linear-gradient(135deg,_#fff0a8,_#a67836_46%,_#463322)];
}
.bg-belt {
  @apply [background:linear-gradient(135deg,_#372313,_#a36f43_45%,_#e6c29a)];
}
.bg-glove {
  @apply [background:linear-gradient(135deg,_#f1e06c,_#b59c1e_48%,_#2a240d)];
}
.bg-pan {
  @apply [background:linear-gradient(135deg,_#3a3a3a,_#a8a29a_48%,_#171717)];
}
.bg-spatula {
  background:
    radial-gradient(circle at 46% 44%, #fff07a, transparent 24%),
    linear-gradient(135deg, #563c16, #d6a328 58%, #3b2608);
}

.recipe-flame {
  background:
    radial-gradient(circle at 58% 36%, #ffcf72, transparent 24%),
    linear-gradient(135deg, #4b1111, #f36b20 55%, #220807);
}
.recipe-tide {
  background:
    radial-gradient(circle at 56% 34%, #a5f8ff, transparent 25%),
    linear-gradient(135deg, #0d3954, #218dd9 56%, #091626);
}
.recipe-venom {
  background:
    radial-gradient(circle at 58% 36%, #bbff90, transparent 24%),
    linear-gradient(135deg, #123a22, #22a35a 55%, #08180f);
}
.recipe-storm {
  background:
    radial-gradient(circle at 58% 36%, #e2f0ff, transparent 22%),
    linear-gradient(135deg, #271f5c, #5f7cff 55%, #100a24);
}
.recipe-void {
  background:
    radial-gradient(circle at 58% 36%, #d897ff, transparent 24%),
    linear-gradient(135deg, #35184e, #8c35b3 55%, #16091f);
}
.recipe-gold {
  background:
    radial-gradient(circle at 58% 36%, #fff2a7, transparent 24%),
    linear-gradient(135deg, #5a3714, #d9962b 55%, #1d1207);
}
.recipe-iron {
  background:
    radial-gradient(circle at 58% 36%, #d3dde6, transparent 22%),
    linear-gradient(135deg, #242d36, #738391 55%, #0e1115);
}
.recipe-star {
  background:
    radial-gradient(circle at 58% 36%, #ffffff, transparent 20%),
    linear-gradient(135deg, #363e8a, #9aa7ff 55%, #151833);
}
.recipe-sigil {
  background:
    radial-gradient(circle at 58% 36%, #ffafda, transparent 23%),
    linear-gradient(135deg, #4a1738, #d35a94 55%, #1d0a18);
}
.recipe-spirit {
  background:
    radial-gradient(circle at 58% 36%, #f7fff1, transparent 22%),
    linear-gradient(135deg, #2b4e3b, #9dcc8a 55%, #111c13);
}
</style>
