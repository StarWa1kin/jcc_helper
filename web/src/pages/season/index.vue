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
            price > 0
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
          picture: hero.picture,
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
  min-height: 100vh;
  overflow: hidden;
  color: #f5e6cb;
  background: #21102a;
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
  background: linear-gradient(
    180deg,
    rgba(216, 149, 72, 0.18),
    rgba(216, 149, 72, 0.02)
  );
}

.tab-item.active::after {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 4rpx;
  background: linear-gradient(90deg, transparent, #e6ad58, transparent);
  content: "";
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
    radial-gradient(
      circle at 100% 4%,
      rgba(111, 65, 138, 0.24),
      transparent 30%
    ),
    linear-gradient(180deg, #21102a 0%, #35173a 100%);
}

.tab-panel {
  padding: 22rpx 18rpx 34rpx;
}

.state-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 360rpx;
  margin: 28rpx 18rpx;
  border: 1rpx solid rgba(221, 166, 100, 0.34);
  border-radius: 18rpx;
  color: rgba(245, 230, 203, 0.78);
  font-size: 27rpx;
  font-weight: 900;
  background: rgba(255, 255, 255, 0.055);
}

.state-card.error {
  color: #ffd0bf;
}

.retry-text {
  margin-top: 16rpx;
  color: #e8c896;
  font-size: 23rpx;
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

.filter-pill.active,
.filter-pill.selected {
  border: 1rpx solid rgba(232, 189, 130, 0.6);
  color: #ffe3a5;
  background: rgba(226, 174, 105, 0.14);
}

.filter-label {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.filter-icon {
  margin-right: 8rpx;
  color: #c49b72;
}

.chevron {
  margin-left: 8rpx;
  color: #b28a67;
}

.filter-panel {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
  margin-top: 16rpx;
  padding: 16rpx;
  border: 1rpx solid rgba(221, 166, 100, 0.28);
  border-radius: 16rpx;
  background: rgba(18, 9, 27, 0.45);
}

.filter-option {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 112rpx;
  max-width: 220rpx;
  height: 54rpx;
  padding: 0 18rpx;
  overflow: hidden;
  border: 1rpx solid rgba(231, 191, 132, 0.18);
  border-radius: 10rpx;
  color: rgba(235, 214, 194, 0.74);
  font-size: 22rpx;
  font-weight: 900;
  background: rgba(255, 255, 255, 0.055);
}

.filter-option text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.filter-option.active {
  border-color: rgba(232, 189, 130, 0.72);
  color: #fff2dc;
  background: rgba(226, 174, 105, 0.22);
}

.hero-summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 16rpx;
  color: rgba(235, 214, 194, 0.58);
  font-size: 22rpx;
  font-weight: 900;
}

.clear-filter {
  color: #e8c896;
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

.mini-1,
.mini-5 {
  background: #c99b39;
}
.mini-2,
.mini-6 {
  background: #286bd8;
}
.mini-3,
.mini-7 {
  background: #7932b8;
}
.mini-4,
.mini-8 {
  background: #1b994f;
}

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
.trait-top {
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

.empty-card {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 180rpx;
  margin-top: 28rpx;
  border: 1rpx solid rgba(221, 166, 100, 0.26);
  border-radius: 14rpx;
  color: rgba(235, 214, 194, 0.62);
  font-size: 25rpx;
  font-weight: 900;
  background: rgba(255, 255, 255, 0.045);
}

.hero-card {
  position: relative;
  height: 220rpx;
  overflow: hidden;
  border: 1rpx solid rgba(221, 166, 100, 0.62);
  border-radius: 14rpx;
  background: #25122e;
}

.hero-card::after {
  position: absolute;
  inset: 1rpx;
  border: 1rpx solid rgba(255, 255, 255, 0.06);
  border-radius: 12rpx;
  content: "";
  pointer-events: none;
}

.hero-bg,
.hero-shade {
  position: absolute;
  inset: 0;
}

.hero-bg.remote-image {
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
}

.hero-shade {
  background: linear-gradient(
    180deg,
    transparent 35%,
    rgba(17, 7, 23, 0.86) 100%
  );
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

.hero-tags {
  position: absolute;
  left: 62rpx;
  right: 12rpx;
  top: 14rpx;
  display: flex;
  gap: 8rpx;
  overflow: hidden;
}

.hero-tags text {
  max-width: 116rpx;
  height: 38rpx;
  padding: 0 10rpx;
  overflow: hidden;
  border: 1rpx solid rgba(232, 189, 130, 0.34);
  border-radius: 10rpx;
  color: rgba(255, 242, 220, 0.86);
  font-size: 18rpx;
  font-weight: 900;
  line-height: 38rpx;
  text-overflow: ellipsis;
  white-space: nowrap;
  background: rgba(22, 9, 28, 0.58);
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

.detail-mask {
  position: fixed;
  inset: 0;
  z-index: 50;
  display: flex;
  align-items: flex-end;
  background: rgba(9, 4, 14, 0.78);
}

.hero-detail {
  width: 100%;
  height: 92vh;
  overflow: hidden;
  border-radius: 30rpx 30rpx 0 0;
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
  height: 92vh;
}

.detail-visual {
  position: relative;
  height: 520rpx;
  overflow: hidden;
}

.detail-portrait {
  position: absolute;
  inset: 0;
  background-position: center 18%;
  background-repeat: no-repeat;
  background-size: cover;
  transform: scale(1.08);
}

.detail-cover {
  position: absolute;
  inset: 0;
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
  position: absolute;
  right: 24rpx;
  top: 24rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 68rpx;
  height: 68rpx;
  padding: 0;
  border: 0;
  border-radius: 50%;
  color: #fff2dc;
  font-size: 44rpx;
  line-height: 68rpx;
  background: rgba(16, 8, 28, 0.72);
  backdrop-filter: blur(8rpx);
}

.detail-close::after {
  border: 0;
}

.detail-title {
  position: absolute;
  left: 28rpx;
  right: 28rpx;
  bottom: 28rpx;
}

.detail-title-row {
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.detail-cost {
  display: inline-flex;
  align-items: center;
  height: 42rpx;
  padding: 0 16rpx;
  border: 1rpx solid rgba(232, 189, 130, 0.56);
  border-radius: 12rpx;
  color: #f6d49a;
  font-size: 22rpx;
  font-weight: 900;
  background: rgba(22, 9, 28, 0.64);
}

.detail-star {
  display: inline-flex;
  align-items: center;
  height: 42rpx;
  padding: 0 16rpx;
  border: 1rpx solid rgba(133, 244, 236, 0.56);
  border-radius: 12rpx;
  color: #a8fff6;
  font-size: 22rpx;
  font-weight: 900;
  background: rgba(18, 68, 72, 0.42);
}

.detail-name {
  display: block;
  margin-top: 14rpx;
  color: #fff4df;
  font-size: 52rpx;
  font-weight: 900;
}

.detail-body {
  position: relative;
  z-index: 1;
  margin-top: -8rpx;
  padding: 22rpx 24rpx 48rpx;
}

.detail-section {
  margin-bottom: 22rpx;
  padding: 24rpx;
  overflow: hidden;
  border: 1rpx solid rgba(221, 166, 100, 0.24);
  border-radius: 18rpx;
  background:
    linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.08),
      rgba(255, 255, 255, 0.035)
    ),
    rgba(19, 9, 31, 0.66);
  box-shadow: inset 0 1rpx 0 rgba(255, 255, 255, 0.08);
}

.skill-section {
  border-color: rgba(245, 211, 122, 0.34);
}

.section-line-title {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.section-title-copy {
  min-width: 0;
}

.detail-section-title {
  display: block;
  color: #fff0d6;
  font-size: 28rpx;
  font-weight: 900;
}

.detail-section-sub {
  display: block;
  margin-top: 4rpx;
  overflow: hidden;
  color: rgba(239, 219, 188, 0.58);
  font-size: 21rpx;
  font-weight: 800;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.detail-chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
  margin-top: 16rpx;
}

.detail-chip-row.compact {
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

.detail-chip.trait {
  background: linear-gradient(135deg, #ffe0a3, #c48b43);
}

.detail-chip.role {
  background: linear-gradient(135deg, #9ce6ff, #4b9bd2);
}

.detail-desc,
.detail-value {
  display: block;
  margin-top: 16rpx;
  color: rgba(245, 230, 203, 0.76);
  font-size: 24rpx;
  line-height: 39rpx;
}

.detail-value {
  color: #e8c896;
}

.skill-icon,
.mini-mark {
  flex: 0 0 auto;
  width: 70rpx;
  height: 70rpx;
  overflow: hidden;
  border: 1rpx solid rgba(255, 224, 163, 0.5);
  border-radius: 14rpx;
  background: rgba(255, 224, 163, 0.12);
}

.skill-icon.fallback,
.mini-mark {
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffe0a3;
  font-size: 24rpx;
  font-weight: 900;
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

.trait-detail-list {
  display: grid;
  gap: 16rpx;
  margin-top: 20rpx;
}

.trait-detail-card {
  padding: 18rpx;
  border: 1rpx solid rgba(255, 255, 255, 0.07);
  border-radius: 16rpx;
  background: rgba(18, 9, 27, 0.42);
}

.trait-detail-head {
  display: flex;
  align-items: center;
  gap: 14rpx;
}

.trait-detail-icon {
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

.trait-detail-copy {
  min-width: 0;
}

.trait-detail-name {
  display: block;
  color: #fff0d6;
  font-size: 25rpx;
  font-weight: 900;
}

.trait-detail-count {
  display: block;
  margin-top: 4rpx;
  color: #e8c896;
  font-size: 21rpx;
  font-weight: 800;
}

.trait-detail-desc {
  display: block;
  margin-top: 14rpx;
  color: rgba(245, 230, 203, 0.7);
  font-size: 23rpx;
  line-height: 36rpx;
}

.trait-detail-levels {
  display: flex;
  flex-wrap: wrap;
  gap: 10rpx;
  margin-top: 14rpx;
}

.trait-detail-levels text {
  max-width: 100%;
  padding: 8rpx 12rpx;
  border-radius: 10rpx;
  color: #241426;
  font-size: 20rpx;
  font-weight: 900;
  background: linear-gradient(135deg, #ffe0a3, #c48b43);
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

.data-icon {
  width: 100%;
  height: 100%;
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
  margin-top: 18rpx;
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

.equip-type-scroll {
  width: 100%;
  margin-bottom: 18rpx;
  white-space: nowrap;
}

.equip-type-row {
  display: flex;
  gap: 12rpx;
}

.equip-type-pill {
  flex: 0 0 auto;
  height: 60rpx;
  padding: 0 20rpx;
  border: 1rpx solid rgba(221, 166, 100, 0.28);
  border-radius: 14rpx;
  color: rgba(245, 230, 203, 0.72);
  font-size: 22rpx;
  font-weight: 900;
  line-height: 60rpx;
  background: rgba(255, 255, 255, 0.055);
}

.equip-type-pill.active {
  color: #241426;
  border-color: rgba(255, 224, 163, 0.88);
  background: linear-gradient(135deg, #ffe0a3, #c48b43);
}

.equip-summary {
  margin: 18rpx 0 16rpx;
  color: rgba(235, 214, 194, 0.58);
  font-size: 22rpx;
  font-weight: 900;
}

.equip-list {
  display: grid;
  gap: 14rpx;
}

.equip-row-card {
  display: grid;
  grid-template-columns: 212rpx minmax(0, 1fr);
  gap: 18rpx;
  min-height: 138rpx;
  padding: 18rpx;
  border: 1rpx solid rgba(221, 166, 100, 0.24);
  border-radius: 16rpx;
  background: #432881;
}

.equip-formula {
  display: flex;
  align-items: center;
  gap: 8rpx;
  min-width: 0;
}

.equip-formula-icon {
  flex: 0 0 auto;
  width: 46rpx;
  height: 46rpx;
  overflow: hidden;
  border: 2rpx solid rgba(231, 191, 132, 0.5);
  border-radius: 4rpx;
  background: rgba(18, 9, 27, 0.38);
}

.equip-formula-icon.empty {
  width: 58rpx;
  height: 58rpx;
}

.equip-formula-icon.result {
  width: 54rpx;
  height: 54rpx;
  border-color: rgba(255, 224, 163, 0.72);
}

.formula-symbol {
  color: rgba(245, 230, 203, 0.34);
  font-size: 24rpx;
  font-weight: 900;
}

.equip-copy {
  min-width: 0;
}

.equip-title-line {
  display: flex;
  align-items: center;
  gap: 10rpx;
}

.equip-name {
  min-width: 0;
  overflow: hidden;
  color: #ffe267;
  font-size: 24rpx;
  font-weight: 900;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.equip-type-label {
  flex: 0 0 auto;
  height: 32rpx;
  padding: 0 10rpx;
  border-radius: 9rpx;
  color: #fff2dc;
  font-size: 18rpx;
  font-weight: 900;
  line-height: 32rpx;
  background: rgba(22, 9, 28, 0.34);
}

.equip-basic,
.equip-desc {
  display: block;
  margin-top: 8rpx;
  color: rgba(245, 230, 203, 0.72);
  font-size: 21rpx;
  line-height: 31rpx;
}

.equip-basic {
  color: #d7bdff;
  font-weight: 900;
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

.rune-level-tabs {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12rpx;
  margin-bottom: 16rpx;
}

.rune-level-tab {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 58rpx;
  border: 1rpx solid rgba(221, 166, 100, 0.24);
  border-radius: 14rpx;
  color: rgba(245, 230, 203, 0.7);
  font-size: 23rpx;
  font-weight: 900;
  background: rgba(255, 255, 255, 0.055);
}

.rune-level-tab.active {
  color: #241426;
  border-color: rgba(255, 224, 163, 0.88);
  background: linear-gradient(135deg, #ffe0a3, #c48b43);
  box-shadow: 0 12rpx 26rpx rgba(196, 139, 67, 0.22);
}

.rune-summary {
  margin-bottom: 16rpx;
  color: rgba(235, 214, 194, 0.58);
  font-size: 22rpx;
  font-weight: 900;
}

.rune-card {
  min-height: 246rpx;
  padding: 22rpx;
  border: 1rpx solid rgba(221, 166, 100, 0.32);
  border-radius: 18rpx;
  background: #684bbe;
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

.god-summary {
  display: block;
}

.god-selector-scroll {
  width: 100%;
  white-space: nowrap;
}

.god-selector-row {
  display: flex;
  gap: 18rpx;
}

.god-select-card {
  display: flex;
  align-items: center;
  gap: 16rpx;
  flex: 0 0 310rpx;
  min-height: 118rpx;
  padding: 20rpx;
  border: 2rpx solid transparent;
  border-radius: 24rpx;
  background: rgba(67, 40, 129, 0.72);
}

.god-select-card.active {
  border-color: #d8a84f;
  background: rgba(104, 75, 190, 0.52);
}

.god-select-icon {
  flex: 0 0 auto;
  width: 86rpx;
  height: 74rpx;
}

.god-select-copy {
  min-width: 0;
}

.god-select-copy text {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.god-select-copy text:first-child {
  color: #fff2dc;
  font-size: 27rpx;
  font-weight: 900;
}

.god-select-copy text:last-child {
  margin-top: 6rpx;
  color: rgba(245, 230, 203, 0.62);
  font-size: 22rpx;
  font-weight: 800;
}

.god-profile-card {
  position: relative;
  min-height: 340rpx;
  margin-top: 26rpx;
  overflow: hidden;
  border-radius: 26rpx;
  background: #432881;
}

.god-profile-art {
  position: absolute;
  right: -30rpx;
  top: -40rpx;
  width: 560rpx;
  height: 360rpx;
  opacity: 0.9;
}

.god-profile-mask {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(90deg, rgba(22, 9, 28, 0.86), rgba(22, 9, 28, 0.34)),
    linear-gradient(180deg, rgba(22, 9, 28, 0.04), rgba(22, 9, 28, 0.82));
}

.god-profile-content {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 18rpx;
  padding: 140rpx 34rpx 0;
}

.god-profile-icon {
  width: 96rpx;
  height: 96rpx;
  border: 2rpx solid rgba(255, 224, 163, 0.28);
  border-radius: 18rpx;
  background: rgba(22, 9, 28, 0.32);
}

.god-profile-name,
.god-profile-sub,
.god-profile-tip {
  display: block;
  position: relative;
  z-index: 1;
}

.god-profile-name {
  color: #fff2dc;
  font-size: 36rpx;
  font-weight: 900;
}

.god-profile-sub {
  margin-top: 4rpx;
  color: rgba(245, 230, 203, 0.66);
  font-size: 24rpx;
  font-weight: 800;
}

.god-profile-tip {
  padding: 30rpx 34rpx 34rpx;
  color: rgba(245, 230, 203, 0.78);
  font-size: 25rpx;
  line-height: 38rpx;
}

.god-filter-panel {
  margin-top: 20rpx;
  padding: 18rpx;
  border: 1rpx solid rgba(221, 166, 100, 0.26);
  border-radius: 18rpx;
  background: rgba(104, 75, 190, 0.38);
}

.god-search {
  display: flex;
  align-items: center;
  height: 70rpx;
  padding: 0 20rpx;
  border: 1rpx solid rgba(255, 224, 163, 0.22);
  border-radius: 14rpx;
  background: rgba(22, 9, 28, 0.34);
}

.god-search-input {
  flex: 1;
  min-width: 0;
  color: #fff2dc;
  font-size: 24rpx;
  font-weight: 800;
}

.god-category-scroll {
  width: 100%;
  margin-top: 16rpx;
  white-space: nowrap;
}

.god-category-row {
  display: flex;
  gap: 12rpx;
}

.god-category-pill {
  flex: 0 0 auto;
  min-width: 118rpx;
  height: 58rpx;
  padding: 0 20rpx;
  border: 1rpx solid rgba(255, 224, 163, 0.22);
  border-radius: 14rpx;
  color: rgba(245, 230, 203, 0.74);
  font-size: 22rpx;
  font-weight: 900;
  line-height: 58rpx;
  text-align: center;
  background: rgba(22, 9, 28, 0.26);
}

.god-category-pill.active {
  color: #241426;
  border-color: rgba(255, 224, 163, 0.88);
  background: linear-gradient(135deg, #ffe0a3, #c48b43);
}

.god-summary {
  margin-top: 14rpx;
  color: rgba(235, 214, 194, 0.62);
  font-size: 21rpx;
  font-weight: 900;
}

.god-stage-list {
  display: grid;
  gap: 26rpx;
  margin-top: 26rpx;
}

.god-stage-card {
  padding: 28rpx;
  border: 1rpx solid rgba(221, 166, 100, 0.24);
  border-radius: 26rpx;
  background: rgba(67, 40, 129, 0.84);
}

.god-stage-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.god-stage-badge {
  height: 58rpx;
  min-width: 118rpx;
  padding: 0 22rpx;
  border-radius: 999rpx;
  color: #ffe267;
  font-size: 28rpx;
  font-weight: 900;
  line-height: 58rpx;
  text-align: center;
  background: rgba(196, 139, 67, 0.58);
}

.god-stage-count {
  color: rgba(245, 230, 203, 0.62);
  font-size: 23rpx;
  font-weight: 800;
}

.god-stage-divider {
  height: 1rpx;
  margin: 28rpx 0;
  background: rgba(255, 255, 255, 0.08);
}

.god-wish-list {
  display: grid;
  gap: 28rpx;
}

.god-wish-row {
  padding-bottom: 28rpx;
  border-bottom: 1rpx solid rgba(255, 255, 255, 0.08);
}

.god-wish-row:last-child {
  padding-bottom: 0;
  border-bottom: 0;
}

.god-wish-row-top {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.god-wish-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 62rpx;
  height: 62rpx;
  flex: 0 0 auto;
  overflow: hidden;
  border-radius: 18rpx;
  color: #fff2dc;
  font-size: 22rpx;
  font-weight: 900;
}

.god-card-title {
  min-width: 0;
}

.god-name,
.god-source,
.god-tip {
  display: block;
}

.god-name {
  color: #fff1d5;
  font-size: 27rpx;
  font-weight: 900;
}

.god-source {
  margin-top: 6rpx;
  overflow: hidden;
  color: rgba(235, 214, 194, 0.54);
  font-size: 21rpx;
  font-weight: 800;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.god-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10rpx;
  margin-top: 16rpx;
}

.god-tag {
  height: 36rpx;
  padding: 0 12rpx;
  border-radius: 10rpx;
  color: #fff2dc;
  font-size: 18rpx;
  font-weight: 900;
  line-height: 36rpx;
  background: rgba(22, 9, 28, 0.38);
}

.god-tag.economy {
  color: #92ffd1;
}

.god-tag.combat {
  color: #ffb07b;
}

.god-tag.item {
  color: #cda4ff;
}

.god-tag.utility {
  color: #9ce6ff;
}

.god-tip {
  margin-top: 16rpx;
  color: rgba(245, 230, 203, 0.74);
  font-size: 22rpx;
  line-height: 34rpx;
}

.tone-gold {
  background: #684bbe;
}
.tone-blue {
  background: linear-gradient(135deg, #7fd7ff, #1b5fb9);
  background: #684bbe;
}
.tone-violet {
  background: #684bbe;
}
.tone-rose {
  background: linear-gradient(135deg, #ff91ad, #9b2948);
  background: linear-gradient(135deg, #be8bff, #5631b3);
}

.bg-sword {
  background: linear-gradient(135deg, #1b2a66, #e1c86e 52%, #402616);
}
.bg-bow {
  background: linear-gradient(135deg, #283b1c, #c7d092 50%, #3a2614);
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
  background: linear-gradient(135deg, #153b49, #5fc3bf 48%, #1b2229);
}
.bg-cloak {
  background: linear-gradient(135deg, #fff0a8, #a67836 46%, #463322);
}
.bg-belt {
  background: linear-gradient(135deg, #372313, #a36f43 45%, #e6c29a);
}
.bg-glove {
  background: linear-gradient(135deg, #f1e06c, #b59c1e 48%, #2a240d);
}
.bg-pan {
  background: linear-gradient(135deg, #3a3a3a, #a8a29a 48%, #171717);
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
