<template>
  <view class="season-page min-h-screen overflow-hidden text-[#f5e6cb] bg-[#21102a]">
    <view class="tab-shell flex items-center justify-around h-[104rpx] px-[18rpx] bg-[#21102a] border-b border-[rgba(226,176,108,0.22)]">
      <view
        v-for="tab in tabs"
        :key="tab.key"
        :class="['tab-item relative flex flex-col items-center justify-center flex-1 h-full text-[rgba(223,202,176,0.62)]', activeTab === tab.key ? 'active border border-[rgba(255,224,163,0.88)] text-[#241426] bg-[linear-gradient(135deg,#ffe0a3,#c48b43)] shadow-[0_12rpx_26rpx_rgba(196,139,67,0.22)]' : '']"
        @tap="activeTab = tab.key"
      >
        <text class="tab-icon text-[36rpx] leading-[38rpx]">{{ tab.icon }}</text>
        <text class="tab-label mt-[6rpx] text-[23rpx] font-black">{{ tab.label }}</text>
      </view>
    </view>

    <scroll-view scroll-y class="content-scroll h-[calc(100vh-104rpx)] px-[28rpx] pb-[46rpx] box-border">
      <view v-if="loading" class="state-card flex flex-col items-center justify-center min-h-[360rpx] m-[28rpx_18rpx] border border-[rgba(221,166,100,0.34)] rounded-[18rpx] text-[27rpx] font-black text-[rgba(245,230,203,0.78)] bg-[rgba(255,255,255,0.055)] flex flex-col items-center justify-center min-h-[360rpx] m-[28rpx_18rpx] border border-[rgba(221,166,100,0.34)] rounded-[18rpx] text-[27rpx] font-black text-[rgba(245,230,203,0.78)] bg-[rgba(255,255,255,0.055)]">
        <text>Loading season data...</text>
      </view>

      <view
        v-else-if="loadError"
        class="state-card error flex flex-col items-center justify-center min-h-[360rpx] m-[28rpx_18rpx] border border-[rgba(221,166,100,0.34)] rounded-[18rpx] text-[27rpx] font-black text-[rgba(245,230,203,0.78)] bg-[rgba(255,255,255,0.055)] text-[#ffd0bf]"
        @tap="loadSeasonData"
      >
        <text>{{ loadError }}</text>
        <text class="retry-text mt-[16rpx] text-[#e8c896] text-[23rpx]">Tap to retry</text>
      </view>

      <view v-else-if="activeTab === 'heroes'" class="tab-panel hero-panel pt-[22rpx] pb-[34rpx]">
        <view class="search-box flex items-center h-[82rpx] px-[24rpx] rounded-[18rpx] bg-[rgba(255,255,255,0.08)]">
          <text class="search-icon mr-[18rpx] text-[#bd9d82] text-[38rpx]">⌕</text>
          <input
            v-model="heroKeyword"
            class="search-input flex-1 h-[76rpx] text-[#fff2d8] text-[27rpx] font-extrabold"
            confirm-type="search"
            placeholder="搜索英雄"
            placeholder-class="placeholder"
          />
        </view>

        <view class="filter-row grid grid-cols-3 gap-[14rpx] mt-[20rpx]">
          <view
            v-for="filter in heroFilters"
            :key="filter.key"
            :class="[
              'filter-pill flex items-center justify-center min-w-0 h-[62rpx] rounded-[12rpx] text-[#e7d4b8] text-[23rpx] font-black bg-[rgba(255,255,255,0.06)]',
              activeHeroFilter === filter.key ? 'active border border-[rgba(255,224,163,0.88)] text-[#241426] bg-[linear-gradient(135deg,#ffe0a3,#c48b43)] shadow-[0_12rpx_26rpx_rgba(196,139,67,0.22)]' : '',
              heroFilterValue(filter.key) ? 'selected border border-[rgba(232,189,130,0.6)] text-[#ffe3a5] bg-[rgba(226,174,105,0.14)]' : '',
            ]"
            @tap="toggleHeroFilter(filter.key)"
          >
            <text class="filter-icon mr-[8rpx] text-[#c49b72]">{{ filter.icon }}</text>
            <text class="filter-label min-w-0 overflow-hidden text-ellipsis whitespace-nowrap">{{ heroFilterLabel(filter) }}</text>
            <text class="chevron ml-[8rpx] text-[#b28a67]">⌄</text>
          </view>
        </view>

        <view v-if="activeHeroFilter" class="filter-panel flex flex-wrap gap-[12rpx] mt-[16rpx] p-[16rpx] border border-[rgba(221,166,100,0.28)] rounded-[16rpx] bg-[rgba(18,9,27,0.45)]">
          <view
            v-for="option in activeHeroFilterOptions"
            :key="option.value"
            :class="[
              'filter-option flex items-center justify-center min-w-[112rpx] max-w-[220rpx] h-[54rpx] px-[18rpx] overflow-hidden border border-[rgba(231,191,132,0.18)] rounded-[10rpx] text-[rgba(235,214,194,0.74)] text-[22rpx] font-black bg-[rgba(255,255,255,0.055)] [&_text]:overflow-hidden [&_text]:text-ellipsis [&_text]:whitespace-nowrap',
              heroFilterValue(activeHeroFilter) === option.value
                ? 'active border border-[rgba(255,224,163,0.88)] text-[#241426] bg-[linear-gradient(135deg,#ffe0a3,#c48b43)] shadow-[0_12rpx_26rpx_rgba(196,139,67,0.22)]'
                : '',
            ]"
            @tap="selectHeroFilter(activeHeroFilter, option.value)"
          >
            <text>{{ option.label }}</text>
          </view>
        </view>

        <view class="hero-summary flex items-center justify-between mt-[16rpx] text-[rgba(235,214,194,0.58)] text-[22rpx] font-black">
          <text>{{ visibleHeroes.length }} / {{ heroes.length }}</text>
          <text
            v-if="hasHeroFilter"
            class="clear-filter text-[#e8c896]"
            @tap="resetHeroFilters"
            >重置筛选</text
          >
        </view>

        <view v-if="visibleHeroes.length" class="hero-grid grid grid-cols-2 gap-[26rpx_20rpx] mt-[28rpx]">
          <view
            v-for="hero in visibleHeroes"
            :key="hero.id || hero.name"
            class="hero-card relative h-[174rpx] overflow-hidden border-[4rpx] border-[rgba(127,119,143,0.9)] bg-[#25122e]"
            @tap="openHeroDetail(hero)"
          >
            <view
              :class="['hero-bg absolute inset-0 [background-position:center_24%] bg-no-repeat bg-cover', hero.bg, hero.picture ? 'remote-image' : '']"
              :style="
                hero.picture ? { backgroundImage: `url(${hero.picture})` } : {}
              "
            ></view>
            <view class="hero-shade absolute inset-0 bg-[linear-gradient(180deg,rgba(17,7,23,0.02)_0%,rgba(17,7,23,0.08)_54%,rgba(28,12,38,0.98)_55%,rgba(28,12,38,0.98)_100%),linear-gradient(90deg,rgba(17,7,23,0.7)_0%,rgba(17,7,23,0.04)_68%)]"></view>
            <view class="cost-badge absolute right-[12rpx] bottom-[10rpx] flex items-center justify-center h-[34rpx] px-[8rpx] text-white text-[22rpx] font-black">{{ hero.cost }}</view>
            <view class="hero-tags absolute left-[18rpx] right-[88rpx] top-[72rpx] grid gap-[6rpx] overflow-hidden [&_text]:block [&_text]:max-w-[150rpx] [&_text]:h-[28rpx] [&_text]:overflow-hidden [&_text]:text-[rgba(255,255,255,0.88)] [&_text]:text-[20rpx] [&_text]:font-black [&_text]:leading-[28rpx] [&_text]:text-ellipsis [&_text]:whitespace-nowrap [&_text]:[text-shadow:0_2rpx_4rpx_rgba(0,0,0,0.75)]">
              <text v-for="tag in hero.cardTags" :key="tag">{{ tag }}</text>
            </view>
            <view class="hero-meta absolute left-0 right-0 bottom-0 flex items-center justify-between h-[48rpx] pl-[12rpx] pr-[56rpx] bg-[#24142f]">
              <text class="hero-name text-[#fff2dc] text-[26rpx] font-black">{{ hero.name }}</text>
              <view class="views hidden">
                <text>◉</text>
                <text>{{ hero.views }}</text>
              </view>
            </view>
          </view>
        </view>

        <view v-else class="empty-card flex items-center justify-center min-h-[180rpx] mt-[28rpx] border border-[rgba(221,166,100,0.26)] rounded-[14rpx] text-[rgba(235,214,194,0.62)] text-[25rpx] font-black bg-[rgba(255,255,255,0.045)]">
          <text>没有匹配的英雄</text>
        </view>
      </view>

      <view v-else-if="activeTab === 'traits'" class="tab-panel trait-panel pt-[22rpx] pb-[34rpx]">
        <view class="section-head pt-[8rpx] pb-[20rpx]">
          <text class="section-title block text-[#fff0d6] text-[31rpx] font-black">羁绊效果</text>
          <text class="section-sub block mt-[8rpx] text-[rgba(235,214,194,0.56)] text-[24rpx]">按职业与特质快速查看等级收益</text>
        </view>
        <view class="trait-list grid gap-[18rpx]">
          <view
            v-for="trait in traits"
            :key="trait.id || trait.name"
            class="trait-card flex items-center gap-[20rpx] p-[22rpx] border border-[rgba(221,166,100,0.32)] rounded-[18rpx] bg-[rgba(255,255,255,0.055)]"
          >
            <view :class="['trait-emblem flex items-center justify-center shrink-0 w-[76rpx] h-[76rpx] rounded-[22rpx] text-[#1c1027] text-[30rpx] font-black', trait.tone]">
              <image
                v-if="trait.picture"
                :src="trait.picture"
                mode="aspectFit"
                class="data-icon w-full h-full"
              ></image>
              <text v-else>{{ trait.icon }}</text>
            </view>
            <view class="trait-main flex-1 min-w-0">
              <view class="trait-top flex items-center justify-between">
                <text class="trait-name text-[#fff1d5] text-[30rpx] font-black">{{ trait.name }}</text>
                <text class="trait-count text-[#d5aa72] text-[23rpx] font-black">{{ trait.count }}</text>
              </view>
              <text class="trait-desc block mt-[10rpx] text-[rgba(235,214,194,0.62)] text-[24rpx] leading-[34rpx]">{{ trait.desc }}</text>
              <view class="trait-levels flex flex-wrap gap-[10rpx] mt-[16rpx] [&_text]:p-[7rpx_12rpx] [&_text]:rounded-full [&_text]:text-[#e8c896] [&_text]:text-[20rpx] [&_text]:font-black [&_text]:bg-[rgba(226,174,105,0.12)]">
                <text v-for="level in trait.levels" :key="level">{{
                  level
                }}</text>
              </view>
            </view>
          </view>
        </view>
      </view>

      <view v-else-if="activeTab === 'items'" class="tab-panel item-panel pt-[22rpx] pb-[34rpx]">
        <view class="section-head pt-[8rpx] pb-[20rpx]">
          <text class="section-title block text-[#fff0d6] text-[31rpx] font-black">装备资料</text>
          <text class="section-sub block mt-[8rpx] text-[rgba(235,214,194,0.56)] text-[24rpx]"
            >按基础、成型、光明、神器和特殊装备分类</text
          >
        </view>

        <scroll-view scroll-x class="equip-type-scroll w-full mb-[18rpx] whitespace-nowrap">
          <view class="equip-type-row flex gap-[12rpx]">
            <view
              v-for="type in equipTypeFilters"
              :key="type.value"
              :class="[
                'equip-type-pill flex-none h-[60rpx] px-[20rpx] border border-[rgba(221,166,100,0.28)] rounded-[14rpx] text-[22rpx] font-black leading-[60rpx] text-[rgba(245,230,203,0.72)] bg-[rgba(255,255,255,0.055)]',
                activeEquipType === type.value ? 'active border border-[rgba(255,224,163,0.88)] text-[#241426] bg-[linear-gradient(135deg,#ffe0a3,#c48b43)] shadow-[0_12rpx_26rpx_rgba(196,139,67,0.22)]' : '',
              ]"
              @tap="activeEquipType = type.value"
            >
              <text>{{ type.label }}</text>
            </view>
          </view>
        </scroll-view>

        <view class="base-items flex flex-wrap gap-[12rpx] mt-[18rpx]">
          <view
            v-for="item in baseItems"
            :key="item.key"
            :class="['equip-icon relative flex items-end justify-center w-[58rpx] h-[58rpx] overflow-hidden border-[2rpx] border-[rgba(231,191,132,0.58)] rounded-[4rpx] text-[#fff5de] text-[19rpx] font-black [text-shadow:0_2rpx_4rpx_rgba(0,0,0,0.72)]', item.bg]"
          >
            <image
              v-if="item.picture"
              :src="item.picture"
              mode="aspectFit"
              class="data-icon w-full h-full"
            ></image>
            <text v-else>{{ item.label }}</text>
          </view>
        </view>

        <view class="equip-summary my-[18rpx] mb-[16rpx] text-[rgba(235,214,194,0.58)] text-[22rpx] font-black">
          <text>{{ visibleEquipItems.length }} / {{ equipItems.length }}</text>
        </view>

        <view class="equip-list grid gap-[14rpx]">
          <view
            v-for="item in visibleEquipItems"
            :key="item.id"
            class="equip-row-card grid grid-cols-[212rpx_minmax(0,1fr)] gap-[18rpx] min-h-[138rpx] p-[18rpx] border border-[rgba(221,166,100,0.24)] rounded-[16rpx] bg-[#432881]"
          >
            <view class="equip-formula flex items-center gap-[8rpx] min-w-0">
              <image
                v-if="item.componentA?.picture"
                :src="item.componentA.picture"
                mode="aspectFit"
                class="equip-formula-icon flex-none w-[46rpx] h-[46rpx] overflow-hidden border-[2rpx] border-[rgba(231,191,132,0.5)] rounded-[4rpx] bg-[rgba(18,9,27,0.38)]"
              ></image>
              <view v-else class="equip-formula-icon empty flex-none w-[46rpx] h-[46rpx] overflow-hidden border-[2rpx] border-[rgba(231,191,132,0.5)] rounded-[4rpx] bg-[rgba(18,9,27,0.38)]">
                <image
                  v-if="item.picture"
                  :src="item.picture"
                  mode="aspectFit"
                  class="data-icon w-full h-full"
                ></image>
              </view>
              <text v-if="item.hasRecipe" class="formula-symbol text-[rgba(245,230,203,0.34)] text-[24rpx] font-black">+</text>
              <image
                v-if="item.hasRecipe && item.componentB?.picture"
                :src="item.componentB.picture"
                mode="aspectFit"
                class="equip-formula-icon flex-none w-[46rpx] h-[46rpx] overflow-hidden border-[2rpx] border-[rgba(231,191,132,0.5)] rounded-[4rpx] bg-[rgba(18,9,27,0.38)]"
              ></image>
              <text v-if="item.hasRecipe" class="formula-symbol text-[rgba(245,230,203,0.34)] text-[24rpx] font-black">=</text>
              <image
                v-if="item.hasRecipe && item.picture"
                :src="item.picture"
                mode="aspectFit"
                class="equip-formula-icon result flex-none w-[46rpx] h-[46rpx] overflow-hidden border-[2rpx] border-[rgba(231,191,132,0.5)] rounded-[4rpx] bg-[rgba(18,9,27,0.38)]"
              ></image>
            </view>
            <view class="equip-copy min-w-0">
              <view class="equip-title-line flex items-center gap-[10rpx]">
                <text class="equip-name min-w-0 overflow-hidden text-[#ffe267] text-[24rpx] font-black text-ellipsis whitespace-nowrap">{{ item.name }}</text>
                <text class="equip-type-label flex-none h-[32rpx] px-[10rpx] rounded-[9rpx] text-[#fff2dc] text-[18rpx] font-black leading-[32rpx] bg-[rgba(22,9,28,0.34)]">{{ item.displayType }}</text>
              </view>
              <text v-if="item.basicDesc" class="equip-basic block mt-[8rpx] text-[#d7bdff] text-[21rpx] font-black leading-[31rpx]">{{
                item.basicDesc
              }}</text>
              <text class="equip-desc block mt-[8rpx] text-[rgba(245,230,203,0.72)] text-[21rpx] leading-[31rpx]">{{
                item.desc || item.basicDesc || "暂无装备说明"
              }}</text>
            </view>
          </view>
        </view>
      </view>

      <view v-else-if="activeTab === 'runes'" class="tab-panel rune-panel pt-[22rpx] pb-[34rpx]">
        <view class="section-head pt-[8rpx] pb-[20rpx]">
          <text class="section-title block text-[#fff0d6] text-[31rpx] font-black">强化符文</text>
          <text class="section-sub block mt-[8rpx] text-[rgba(235,214,194,0.56)] text-[24rpx]">按一级、二级、三级快速筛选</text>
        </view>
        <view class="rune-level-tabs grid grid-cols-4 gap-[12rpx] mb-[16rpx]">
          <view
            v-for="level in runeLevelFilters"
            :key="level.value"
            :class="[
              'rune-level-tab flex items-center justify-center h-[58rpx] border border-[rgba(221,166,100,0.24)] rounded-[14rpx] text-[23rpx] font-black text-[rgba(245,230,203,0.7)] bg-[rgba(255,255,255,0.055)]',
              activeRuneLevel === level.value ? 'active border border-[rgba(255,224,163,0.88)] text-[#241426] bg-[linear-gradient(135deg,#ffe0a3,#c48b43)] shadow-[0_12rpx_26rpx_rgba(196,139,67,0.22)]' : '',
            ]"
            @tap="activeRuneLevel = level.value"
          >
            <text>{{ level.label }}</text>
          </view>
        </view>
        <view class="rune-summary mb-[16rpx] text-[rgba(235,214,194,0.58)] text-[22rpx] font-black">
          <text>{{ visibleRunes.length }} / {{ runes.length }}</text>
        </view>
        <view class="rune-grid grid grid-cols-2 gap-[18rpx]">
          <view
            v-for="rune in visibleRunes"
            :key="rune.id || rune.name"
            class="rune-card min-h-[246rpx] p-[22rpx] border border-[rgba(221,166,100,0.32)] rounded-[18rpx] bg-[#684bbe]"
          >
            <view :class="['rune-mark flex items-center justify-center w-[62rpx] h-[62rpx] rounded-[18rpx] text-[#1c1027] text-[25rpx] font-black', rune.tone]">
              <image
                v-if="rune.iconUrl"
                :src="rune.iconUrl"
                mode="aspectFit"
                class="data-icon w-full h-full"
              ></image>
              <text v-else>{{ rune.icon }}</text>
            </view>
            <text class="rune-name block mt-[22rpx] text-[#fff1d5] text-[29rpx] font-black">{{ rune.name }}</text>
            <text class="rune-desc block mt-[10rpx] text-[rgba(235,214,194,0.62)] text-[23rpx] leading-[33rpx]">{{ rune.desc }}</text>
            <view class="rune-tags flex flex-wrap gap-[10rpx] mt-[16rpx] [&_text]:p-[7rpx_12rpx] [&_text]:rounded-full [&_text]:text-[#e8c896] [&_text]:text-[20rpx] [&_text]:font-black [&_text]:bg-[rgba(226,174,105,0.12)]">
              <text v-for="tag in rune.tags" :key="tag">{{ tag }}</text>
            </view>
          </view>
        </view>
      </view>

      <view v-else class="tab-panel god-panel pt-[22rpx] pb-[34rpx]">
        <scroll-view scroll-x class="god-selector-scroll w-full whitespace-nowrap">
          <view class="god-selector-row flex gap-[18rpx]">
            <view
              v-for="god in godFilters"
              :key="god.value"
              :class="[
                'god-select-card flex items-center gap-[16rpx] flex-none basis-[310rpx] min-h-[118rpx] p-[20rpx] border-[2rpx] border-transparent rounded-[24rpx] bg-[rgba(67,40,129,0.72)]',
                activeGodId === god.value ? 'active border border-[rgba(255,224,163,0.88)] text-[#241426] bg-[linear-gradient(135deg,#ffe0a3,#c48b43)] shadow-[0_12rpx_26rpx_rgba(196,139,67,0.22)]' : '',
              ]"
              @tap="activeGodId = god.value"
            >
              <image
                v-if="god.iconUrl"
                :src="god.iconUrl"
                mode="aspectFit"
                class="god-select-icon flex-none w-[86rpx] h-[74rpx]"
              ></image>
              <view class="god-select-copy min-w-0 [&_text]:block [&_text]:overflow-hidden [&_text]:text-ellipsis [&_text]:whitespace-nowrap [&_text:first-child]:text-[#fff2dc] [&_text:first-child]:text-[27rpx] [&_text:first-child]:font-black [&_text:last-child]:mt-[6rpx] [&_text:last-child]:text-[rgba(245,230,203,0.62)] [&_text:last-child]:text-[22rpx] [&_text:last-child]:font-extrabold">
                <text>{{ god.label }}</text>
                <text>{{ god.subTitle }}</text>
              </view>
            </view>
          </view>
        </scroll-view>

        <view class="god-profile-card relative min-h-[340rpx] mt-[26rpx] overflow-hidden rounded-[26rpx] bg-[#432881]">
          <image
            v-if="selectedGod.iconUrl"
            :src="selectedGod.iconUrl"
            mode="aspectFit"
            class="god-profile-art absolute right-[-30rpx] top-[-40rpx] w-[560rpx] h-[360rpx] opacity-90"
          ></image>
          <view class="god-profile-mask absolute inset-0 bg-[linear-gradient(90deg,rgba(22,9,28,0.86),rgba(22,9,28,0.34)),linear-gradient(180deg,rgba(22,9,28,0.04),rgba(22,9,28,0.82))]"></view>
          <view class="god-profile-content relative z-1 flex items-center gap-[18rpx] pt-[140rpx] px-[34rpx]">
            <image
              v-if="selectedGod.iconUrl"
              :src="selectedGod.iconUrl"
              mode="aspectFit"
              class="god-profile-icon w-[96rpx] h-[96rpx] border-[2rpx] border-[rgba(255,224,163,0.28)] rounded-[18rpx] bg-[rgba(22,9,28,0.32)]"
            ></image>
            <view>
              <text class="god-profile-name block relative z-1 text-[#fff2dc] text-[36rpx] font-black">{{ selectedGod.shortName || selectedGod.name }}</text>
              <text class="god-profile-sub block relative z-1 mt-[4rpx] text-[rgba(245,230,203,0.66)] text-[24rpx] font-extrabold">{{ selectedGod.title }}</text>
            </view>
          </view>
          <text class="god-profile-tip block relative z-1 px-[34rpx] pt-[30rpx] pb-[34rpx] text-[rgba(245,230,203,0.78)] text-[25rpx] leading-[38rpx]">查看该神明在不同阶段可能出现的恩赐效果</text>
        </view>

        <view class="god-filter-panel mt-[20rpx] p-[18rpx] border border-[rgba(221,166,100,0.26)] rounded-[18rpx] bg-[rgba(104,75,190,0.38)]">
          <view class="god-search flex items-center h-[70rpx] px-[20rpx] border border-[rgba(255,224,163,0.22)] rounded-[14rpx] bg-[rgba(22,9,28,0.34)]">
            <text class="search-icon mr-[18rpx] text-[#bd9d82] text-[38rpx]">⌕</text>
            <input
              v-model="godKeyword"
              class="god-search-input flex-1 min-w-0 text-[#fff2dc] text-[24rpx] font-extrabold"
              placeholder="搜索神明或奖励"
              placeholder-class="placeholder"
            />
          </view>
          <scroll-view scroll-x class="god-category-scroll w-full mt-[16rpx] whitespace-nowrap">
            <view class="god-category-row flex gap-[12rpx]">
              <view
                v-for="category in godCategoryFilters"
                :key="category.value"
                :class="[
                  'god-category-pill flex-none min-w-[118rpx] h-[58rpx] px-[20rpx] border border-[rgba(255,224,163,0.22)] rounded-[14rpx] text-[rgba(245,230,203,0.74)] text-[22rpx] font-black leading-[58rpx] text-center bg-[rgba(22,9,28,0.26)]',
                  activeGodCategory === category.value ? 'active border border-[rgba(255,224,163,0.88)] text-[#241426] bg-[linear-gradient(135deg,#ffe0a3,#c48b43)] shadow-[0_12rpx_26rpx_rgba(196,139,67,0.22)]' : '',
                ]"
                @tap="activeGodCategory = category.value"
              >
                <text>{{ category.label }}</text>
              </view>
            </view>
          </scroll-view>
          <text class="god-summary block mt-[14rpx] text-[rgba(235,214,194,0.62)] text-[21rpx] font-black"
            >{{ visibleGodWishes.length }} / {{ allGodWishes.length }}</text
          >
        </view>

        <view class="god-stage-list grid gap-[26rpx] mt-[26rpx]">
          <view
            v-for="stage in godStageGroups"
            :key="stage.stage"
            class="god-stage-card p-[28rpx] border border-[rgba(221,166,100,0.24)] rounded-[26rpx] bg-[rgba(67,40,129,0.84)]"
          >
            <view class="god-stage-head flex items-center justify-between">
              <text class="god-stage-badge h-[58rpx] min-w-[118rpx] px-[22rpx] rounded-full text-[#ffe267] text-[28rpx] font-black leading-[58rpx] text-center bg-[rgba(196,139,67,0.58)]">{{ stage.stage }}阶段</text>
              <text class="god-stage-count text-[rgba(245,230,203,0.62)] text-[23rpx] font-extrabold">{{ stage.wishes.length }}项恩赐</text>
            </view>
            <view class="god-stage-divider h-[1rpx] my-[28rpx] bg-[rgba(255,255,255,0.08)]"></view>
            <view class="god-wish-list grid gap-[28rpx]">
              <view
                v-for="wish in stage.wishes"
                :key="wish.id"
                class="god-wish-row pb-[28rpx] border-b border-[rgba(255,255,255,0.08)] last:pb-0 last:border-b-0"
              >
                <view class="god-wish-row-top flex items-center gap-[16rpx]">
                  <image
                    v-if="wish.icon"
                    :src="wish.icon"
                    mode="aspectFit"
                    class="god-wish-icon flex items-center justify-center flex-none w-[62rpx] h-[62rpx] overflow-hidden rounded-[18rpx] text-[#fff2dc] text-[22rpx] font-black"
                  ></image>
                  <view v-else :class="['god-wish-icon flex items-center justify-center flex-none w-[62rpx] h-[62rpx] overflow-hidden rounded-[18rpx] text-[#fff2dc] text-[22rpx] font-black', wish.tone]">{{
                    wish.iconText
                  }}</view>
                  <view class="god-card-title min-w-0">
                    <text class="god-name block text-[#fff1d5] text-[27rpx] font-black">{{ wish.name }}</text>
                    <view class="god-tags flex flex-wrap gap-[10rpx] mt-[16rpx]">
                      <text
                        v-for="tag in wish.tags"
                        :key="`${wish.id}-${tag.value}`"
                        :class="['god-tag h-[36rpx] px-[12rpx] rounded-[10rpx] text-[#fff2dc] text-[18rpx] font-black leading-[36rpx] bg-[rgba(22,9,28,0.38)]', tag.className]"
                      >
                        {{ tag.label }}
                      </text>
                    </view>
                  </view>
                </view>
                <text class="god-tip block mt-[16rpx] text-[rgba(245,230,203,0.74)] text-[22rpx] leading-[34rpx]">{{ wish.desc }}</text>
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
const tonePalette = ["bg-[#684bbe]", "bg-[#684bbe]", "bg-[#684bbe]", "bg-[linear-gradient(135deg,#be8bff,#5631b3)]"];
const heroPalette = ["bg-[radial-gradient(circle_at_66%_28%,#dcc067,transparent_20%),linear-gradient(135deg,#33205f,#7548ec_48%,#16091f)]", "bg-[radial-gradient(circle_at_70%_26%,#f0b16f,transparent_22%),linear-gradient(135deg,#122b55,#23a1e4_48%,#16091f)]", "bg-[radial-gradient(circle_at_25%_28%,#6dc7ff,transparent_24%),linear-gradient(135deg,#17235b,#435df0_52%,#16091f)]", "bg-[radial-gradient(circle_at_65%_42%,#78fff3,transparent_24%),linear-gradient(135deg,#3f2261,#31c4bc_48%,#16091f)]", "bg-[radial-gradient(circle_at_20%_26%,#f49133,transparent_23%),linear-gradient(135deg,#38162d,#a44d20_52%,#16091f)]", "bg-[radial-gradient(circle_at_60%_30%,#c66cff,transparent_24%),linear-gradient(135deg,#1b1d61,#7433cd_52%,#16091f)]"];
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

const recipePalette = ["bg-[radial-gradient(circle_at_58%_36%,#ffcf72,transparent_24%),linear-gradient(135deg,#4b1111,#f36b20_55%,#220807)]", "bg-[radial-gradient(circle_at_56%_34%,#a5f8ff,transparent_25%),linear-gradient(135deg,#0d3954,#218dd9_56%,#091626)]", "bg-[radial-gradient(circle_at_58%_36%,#bbff90,transparent_24%),linear-gradient(135deg,#123a22,#22a35a_55%,#08180f)]", "bg-[radial-gradient(circle_at_58%_36%,#e2f0ff,transparent_22%),linear-gradient(135deg,#271f5c,#5f7cff_55%,#100a24)]", "bg-[radial-gradient(circle_at_58%_36%,#d897ff,transparent_24%),linear-gradient(135deg,#35184e,#8c35b3_55%,#16091f)]", "bg-[radial-gradient(circle_at_58%_36%,#fff2a7,transparent_24%),linear-gradient(135deg,#5a3714,#d9962b_55%,#1d1207)]", "bg-[radial-gradient(circle_at_58%_36%,#d3dde6,transparent_22%),linear-gradient(135deg,#242d36,#738391_55%,#0e1115)]", "bg-[radial-gradient(circle_at_58%_36%,#ffffff,transparent_20%),linear-gradient(135deg,#363e8a,#9aa7ff_55%,#151833)]", "bg-[radial-gradient(circle_at_58%_36%,#ffafda,transparent_23%),linear-gradient(135deg,#4a1738,#d35a94_55%,#1d0a18)]", "bg-[radial-gradient(circle_at_58%_36%,#f7fff1,transparent_22%),linear-gradient(135deg,#2b4e3b,#9dcc8a_55%,#111c13)]"];

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
        1: { label: "经济类", className: "text-[#92ffd1]" },
        2: { label: "战力类", className: "text-[#ffb07b]" },
        3: { label: "道具类", className: "text-[#cda4ff]" },
        4: { label: "功能类", className: "text-[#9ce6ff]" },
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
.hero-card::after {
  position: absolute;
  inset: 0;
  border: 1rpx solid rgba(255, 255, 255, 0.1);
  content: "";
  pointer-events: none;
}
.cost-badge::before {
  width: 18rpx;
  height: 18rpx;
  margin-right: 6rpx;
  border: 4rpx solid #fff;
  border-radius: 50%;
  content: "";
}
.hero-tags text::before {
  margin-right: 8rpx;
  color: #fff;
  content: "\2725";
}
</style>
