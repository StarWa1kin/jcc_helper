<template>
  <view class="min-h-screen bg-[#f6f3fc] text-[#101828] pb-[44rpx]">
    <view class="relative overflow-hidden bg-gradient-to-br from-[#32127f] via-[#5a25c8] to-[#8a3ffc] px-[52rpx] pt-[58rpx] pb-[46rpx] text-white">
      <view class="absolute left-[-120rpx] top-[-160rpx] h-[360rpx] w-[360rpx] rounded-full bg-[#6c35ff]/35 blur-[40rpx]"></view>
      <view class="absolute right-[-80rpx] bottom-[-90rpx] h-[260rpx] w-[260rpx] rounded-full bg-[#9a5cff]/40 blur-[36rpx]"></view>

      <view class="relative flex items-center justify-between">
        <view class="flex items-center gap-[22rpx]">
          <view class="h-[96rpx] w-[96rpx] rounded-[24rpx] bg-[#ffdc5f] p-[8rpx] shadow-[0_12rpx_28rpx_rgba(26,8,80,0.25)]">
            <view class="h-full w-full flex items-center justify-center rounded-[18rpx] border-[4rpx] border-white bg-[#6931dc] text-[42rpx] font-black text-[#fff3a6]">
              铲
            </view>
          </view>
          <view>
            <text class="block text-[24rpx] font-medium text-white/78">小程序 / H5</text>
            <text class="mt-[4rpx] block text-[40rpx] font-black leading-[48rpx] tracking-[0]">金铲铲军师</text>
          </view>
        </view>
        <view class="rounded-full bg-white/12 px-[22rpx] py-[12rpx] text-[22rpx] font-semibold text-[#eadfff]">
          星神专属
        </view>
      </view>

      <text class="relative mt-[36rpx] block text-[27rpx] font-medium text-[#eee8ff]">最智能的铲铲助手，助你上分如饮水~</text>

      <view class="relative mt-[34rpx] flex h-[76rpx] items-center gap-[16rpx] rounded-[28rpx] bg-white/16 px-[28rpx] text-[#d9cff8]">
        <text class="text-[34rpx] leading-none">⌕</text>
        <text class="text-[26rpx] font-semibold">搜索阵容 / 英雄 / 羁绊 / 装备 / 符文</text>
      </view>

      <view class="relative mt-[36rpx] grid grid-cols-3 gap-[24rpx]">
        <view
          v-for="tag in summaryCards"
          :key="tag.label"
          class="rounded-[24rpx] bg-white/13 px-[22rpx] py-[22rpx] shadow-[0_10rpx_24rpx_rgba(34,12,97,0.16)]"
        >
          <text class="block text-[22rpx] font-semibold text-[#cfc0ff]">{{ tag.label }}</text>
          <view class="mt-[8rpx] flex items-center justify-between">
            <text class="text-[30rpx] font-black text-white">{{ tag.value }}</text>
            <text v-if="tag.arrow" class="text-[28rpx] text-[#d7cfff]">⌄</text>
          </view>
        </view>
      </view>
    </view>

    <view class="grid grid-cols-2 gap-[22rpx] px-[52rpx] pt-[78rpx]">
      <view
        v-for="item in featureCards"
        :key="item.title"
        class="min-h-[250rpx] rounded-[34rpx] bg-white px-[32rpx] py-[30rpx] shadow-[0_8rpx_22rpx_rgba(49,35,95,0.10)] ring-1 ring-[#e8e2f2]"
      >
        <view :class="['h-[74rpx] w-[74rpx] flex items-center justify-center rounded-[24rpx] text-[34rpx] font-black', item.iconClass]">
          {{ item.icon }}
        </view>
        <text class="mt-[34rpx] block text-[30rpx] font-black leading-[38rpx] text-[#06112d]">{{ item.title }}</text>
        <text class="mt-[14rpx] block text-[23rpx] font-medium leading-[30rpx] text-[#93a0bd]">{{ item.desc }}</text>
      </view>
    </view>

  </view>
</template>

<script>
export default {
  data() {
    return {
      summaryCards: [
        { label: '当前版本', value: '星神', arrow: true },
        { label: '主推玩法', value: '上分阵容' },
        { label: '核心能力', value: 'AI推荐' },
      ],
      featureCards: [
        { icon: '冠', iconClass: 'bg-[#f1ecff] text-[#7a35ff]', title: '阵容榜', desc: '标签 / 难度 / 强度' },
        { icon: '弈', iconClass: 'bg-[#edf2ff] text-[#5c63ff]', title: '羁绊速查', desc: '星神赛季羁绊库' },
        { icon: '装', iconClass: 'bg-[#fff3e8] text-[#ff6b1a]', title: '装备速查', desc: '合成与英雄适配' },
        { icon: '符', iconClass: 'bg-[#fff8e7] text-[#f48b00]', title: '符文速查', desc: '强化符文推荐' },
        { icon: '英', iconClass: 'bg-[#ecf8ff] text-[#0f9bd7]', title: '英雄速查', desc: '技能 / 费用 / 推荐装备' },
        { icon: '学', iconClass: 'bg-[#e8fbf1] text-[#00a870]', title: '新手学堂', desc: '规则 / D牌 / 卡利息' },
      ],
    };
  },
  onLoad() {},
  methods: {},
};
</script>
